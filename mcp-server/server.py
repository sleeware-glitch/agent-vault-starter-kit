#!/usr/bin/env python3
"""
Smart Connections MCP Server
Exposes Smart Connections .smart-env vector database to Claude Code via MCP protocol

Patch log:
- 2026-03-09 Core-9: Patched get_context_blocks to read text from source files.
- 2026-03-15 Core-13: Fixed path extraction across ALL methods. The ajson cache
  never has a top-level 'path' field — the path is encoded in the embedding key.
  Previous fix only patched get_context_blocks; semantic_search and find_related
  still returned path: null. Fixed at the cache level in load_embeddings() so all
  methods get correct paths automatically. Also applied same disk-read text
  retrieval to semantic_search (text_preview field).
- 2026-03-17 Core-13: Upgraded embedding model from TaylorAI/bge-micro-v2
  (384d, 512 tokens) to nomic-ai/nomic-embed-text-v1.5 (768d, 8192 tokens).
  Dynamic embedding key lookup replaces hardcoded model name in ajson parsing.
  Query prefix 'search_query: ' added per nomic model requirements.
- 2026-03-20 Core-16: Added EXPECTED_DIM filter to load_embeddings(). Skips
  stale embeddings from old models (384d bge-micro) that cause dimension
  mismatch errors in semantic_search. Belt-and-suspenders: SC Force Refresh
  clears old vectors, but this filter prevents the crash if any slip through.
"""

import asyncio
import os
from pathlib import Path
from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server


def extract_path_from_key(key: str) -> str:
    """Extract the vault-relative file path from a Smart Connections embedding key.
    
    Key formats:
      smart_blocks:PATH/TO/FILE.md#heading#subheading
      smart_sources:PATH/TO/FILE.md
    
    Returns the file path portion, or empty string if unparseable.
    """
    for prefix in ('smart_blocks:', 'smart_sources:'):
        if key.startswith(prefix):
            remainder = key[len(prefix):]
            return remainder.split('#')[0]
    return ''


class SmartConnectionsDatabase:
    """Interface to Smart Connections .smart-env vector database"""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.smart_env_path = self.vault_path / ".smart-env"
        self.multi_path = self.smart_env_path / "multi"

        # Lazy load embedding model (same as Smart Connections uses)
        self.model = None
        self.model_name = 'nomic-ai/nomic-embed-text-v1.5'

        # Nomic models perform best with task-instruction prefixes:
        #   Documents: 'search_document: <text>'
        #   Queries:   'search_query: <text>'
        # However, SC's transformers.js adapter embeds document text WITHOUT
        # any prefix. Adding a query prefix here would create an asymmetry
        # that hurts more than it helps. Keep both sides symmetric (no prefix)
        # until we can configure SC to add document prefixes too.
        self.query_prefix = ''

        # Expected embedding dimension — must match self.model_name.
        # Stale embeddings from old models (e.g. 384d bge-micro) are skipped
        # during load to prevent dimension mismatch in dot-product similarity.
        self.expected_dim = 768

        # Cache for embeddings
        self.embeddings_cache: Dict[str, Dict] = {}
        self.embeddings_loaded = False  # Lazy loading flag

    def ensure_model_loaded(self):
        """Lazy load the embedding model on first use"""
        if self.model is None:
            self.model = SentenceTransformer(self.model_name, trust_remote_code=True)

    def load_embeddings(self):
        """Load all .ajson embedding files (lazy loading)"""
        if self.embeddings_loaded:
            return  # Already loaded

        if not self.multi_path.exists():
            return

        count = 0
        for ajson_file in self.multi_path.glob("*.ajson"):
            try:
                import json
                with open(ajson_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()

                    # .ajson files are formatted as:
                    # "key1": {value1},
                    # "key2": {value2},
                    # We need to wrap in braces and remove trailing comma
                    if content and not content.startswith('{'):
                        # Remove trailing comma and wrap in braces
                        content = '{' + content.rstrip(',').strip() + '}'

                    # Parse the JSON structure
                    data = json.loads(content)

                    for key, item in data.items():
                        # Dynamic embedding key lookup — works with any model
                        # SC stores vectors under item['embeddings'][MODEL_KEY]['vec']
                        # We grab the first available embedding rather than hardcoding.
                        embed_dict = item.get('embeddings', {})
                        if not embed_dict:
                            continue
                        model_key = next(iter(embed_dict))
                        vec_data = embed_dict[model_key].get('vec')
                        if vec_data is None:
                            continue

                        # Dimension filter: skip stale embeddings from old models
                        if len(vec_data) != self.expected_dim:
                            continue

                        # Extract path from key — ajson data does NOT have a
                        # top-level 'path' field. The path is encoded in the
                        # embedding key string. (Core-13, 2026-03-15)
                        file_path = extract_path_from_key(key)

                        # Store in cache
                        self.embeddings_cache[key] = {
                            'path': file_path,
                            'vector': np.array(vec_data, dtype=np.float32),
                            'text': item.get('text', ''),
                            'key': key,
                            'lines': item.get('lines', []),
                            'metadata': item.get('metadata', {})
                        }
                        count += 1
            except Exception as e:
                # Skip malformed files
                continue

        self.embeddings_loaded = True

    def _read_block_text(self, file_path: str, lines: list) -> str:
        """Read actual text content from a vault file at the given line range.
        
        Returns the text, or None if the file can't be read.
        """
        if not file_path or not lines or len(lines) < 2:
            return None
        try:
            full_path = self.vault_path / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                start = max(0, lines[0] - 1)  # Convert to 0-indexed
                end = min(len(all_lines), lines[1])
                return ''.join(all_lines[start:end]).strip()
        except Exception:
            return None

    def semantic_search(self, query: str, limit: int = 10, min_similarity: float = 0.3) -> List[Dict]:
        """
        Perform semantic search against the vector database.

        Args:
            query: Natural language query
            limit: Maximum number of results
            min_similarity: Minimum cosine similarity threshold (0-1)

        Returns:
            List of results with path, score, lines, key, and text_preview
        """
        self.ensure_model_loaded()
        self.load_embeddings()

        query_with_prefix = self.query_prefix + query
        query_vec = self.model.encode(query_with_prefix)
        query_vec = query_vec / np.linalg.norm(query_vec)

        results = []
        for key, item in self.embeddings_cache.items():
            vec = item['vector']
            vec = vec / np.linalg.norm(vec)

            similarity = float(np.dot(query_vec, vec))

            if similarity >= min_similarity:
                file_path = item['path']
                lines = item.get('lines', [])

                # Read a short text preview from disk for context
                text = self._read_block_text(file_path, lines)
                text_preview = text[:200] if text else ''

                results.append({
                    'key': key,
                    'path': file_path,
                    'similarity': similarity,
                    'lines': lines,
                    'metadata': item.get('metadata', {}),
                    'text_preview': text_preview
                })

        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]

    def find_related(self, file_path: str, limit: int = 10) -> List[Dict]:
        """
        Find notes related to a specific file.

        Args:
            file_path: Path to file (relative to vault)
            limit: Maximum number of results

        Returns:
            List of related files with paths and similarity scores
        """
        self.load_embeddings()

        target_key = f"smart_sources:{file_path}"

        if target_key not in self.embeddings_cache:
            return []

        target_vec = self.embeddings_cache[target_key]['vector']
        target_vec = target_vec / np.linalg.norm(target_vec)

        results = []
        for key, item in self.embeddings_cache.items():
            if key == target_key:
                continue

            if not key.startswith('smart_sources:'):
                continue

            vec = item['vector']
            vec = vec / np.linalg.norm(vec)

            similarity = float(np.dot(target_vec, vec))

            results.append({
                'key': key,
                'path': item['path'],
                'similarity': similarity,
                'metadata': item.get('metadata', {})
            })

        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]

    def get_context_blocks(self, query: str, max_blocks: int = 5) -> List[Dict]:
        """
        Get best context blocks for a query (for RAG).
        Returns actual text content by reading source files from disk.

        Args:
            query: Query string
            max_blocks: Maximum number of blocks to return

        Returns:
            List of block contents with metadata and actual text
        """
        self.ensure_model_loaded()
        self.load_embeddings()

        query_with_prefix = self.query_prefix + query
        query_vec = self.model.encode(query_with_prefix)
        query_vec = query_vec / np.linalg.norm(query_vec)

        results = []
        for key, item in self.embeddings_cache.items():
            if not key.startswith('smart_blocks:'):
                continue

            vec = item['vector']
            vec = vec / np.linalg.norm(vec)

            similarity = float(np.dot(query_vec, vec))

            if similarity > 0.4:
                file_path = item['path']
                lines = item.get('lines', [])
                text = self._read_block_text(file_path, lines)

                results.append({
                    'key': key,
                    'path': file_path,
                    'similarity': similarity,
                    'lines': lines,
                    'text': text
                })

        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:max_blocks]


async def main():
    import sys
    import logging

    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.debug("Starting smart-connections-mcp server...")

    vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
    if not vault_path:
        raise ValueError("OBSIDIAN_VAULT_PATH environment variable not set")

    logger.debug(f"Vault path: {vault_path}")

    db = SmartConnectionsDatabase(vault_path)
    logger.debug("Database initialized")

    server = Server("smart-connections-mcp")
    logger.debug("MCP server created")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="semantic_search",
                description="Search vault using semantic similarity (not keyword matching). Finds notes related to query meaning, not just exact words.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Natural language query describing what to search for"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 10)",
                            "default": 10
                        },
                        "min_similarity": {
                            "type": "number",
                            "description": "Minimum similarity threshold 0-1 (default: 0.3)",
                            "default": 0.3
                        }
                    },
                    "required": ["query"]
                }
            ),
            types.Tool(
                name="find_related",
                description="Find notes related to a specific file path. Like Smart Connections sidebar in Obsidian.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "File path relative to vault root (e.g., 'DailyNotes/2025-10-25.md')"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["file_path"]
                }
            ),
            types.Tool(
                name="get_context_blocks",
                description="Get best text blocks for a query (for RAG/context building). Returns actual text content.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Query to find relevant context for"
                        },
                        "max_blocks": {
                            "type": "integer",
                            "description": "Maximum number of blocks (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        import json

        if arguments is None:
            arguments = {}

        try:
            if name == "semantic_search":
                results = db.semantic_search(
                    query=arguments['query'],
                    limit=arguments.get('limit', 10),
                    min_similarity=arguments.get('min_similarity', 0.3)
                )

                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "query": arguments['query'],
                            "results_count": len(results),
                            "results": results
                        }, indent=2)
                    )
                ]

            elif name == "find_related":
                results = db.find_related(
                    file_path=arguments['file_path'],
                    limit=arguments.get('limit', 10)
                )

                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "source_file": arguments['file_path'],
                            "related_count": len(results),
                            "related_files": results
                        }, indent=2)
                    )
                ]

            elif name == "get_context_blocks":
                results = db.get_context_blocks(
                    query=arguments['query'],
                    max_blocks=arguments.get('max_blocks', 5)
                )

                return [
                    types.TextContent(
                        type="text",
                        text=json.dumps({
                            "query": arguments['query'],
                            "blocks_count": len(results),
                            "blocks": results
                        }, indent=2)
                    )
                ]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            raise RuntimeError(f"Tool execution error: {str(e)}")

    logger.debug("Starting stdio server...")
    async with stdio_server() as (read_stream, write_stream):
        logger.debug("stdio server started, running MCP server...")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="smart-connections-mcp",
                server_version="0.1.0",
                capabilities=types.ServerCapabilities(
                    tools=types.ToolsCapability(),
                ),
            ),
        )
        logger.debug("MCP server finished")


if __name__ == "__main__":
    asyncio.run(main())
