"""
Smart Connections MCP Server for Claude Desktop.
Stdio transport version — wraps the same SC database as vault_mcp_server.py.

Fix log:
- 2026-03-15 Core-13: Fixed db.search() calls to use correct method names.
  db.search() doesn't exist on SmartConnectionsDatabase. The correct methods
  are db.get_context_blocks() (returns text) and db.semantic_search() (returns paths).
"""
import sys
import os

# Add the directory to path so we can import server.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server import SmartConnectionsDatabase
from mcp.server.fastmcp import FastMCP

VAULT_PATH = r"C:\Users\nosuc\Proton Drive\lee.ware\My files\THE METASTORY PROJECT\TRANSCENT"

db = SmartConnectionsDatabase(VAULT_PATH)
mcp = FastMCP("Smart Connections Desktop")


@mcp.tool()
def search_vault(query: str, max_results: int = 5) -> str:
    """Semantic search across the vault. Returns relevant text blocks with paths and line numbers."""
    results = db.get_context_blocks(query, max_blocks=max_results)
    if not results:
        return "No results found."
    
    output = []
    for r in results:
        block = {
            "path": r.get("path", ""),
            "similarity": round(r.get("similarity", 0), 4),
            "lines": r.get("lines", []),
            "text": r.get("text", "(text unavailable)")
        }
        output.append(block)
    
    import json
    return json.dumps({"results": output}, indent=2)


@mcp.tool()
def get_context_blocks(query: str, max_results: int = 5) -> str:
    """Get the most relevant text blocks for a query. Wide-lens semantic search."""
    return search_vault(query, max_results)


@mcp.tool()
def semantic_search(query: str, max_results: int = 10) -> str:
    """Find where content lives in the vault. Returns paths and headings without full text."""
    results = db.semantic_search(query, limit=max_results)
    if not results:
        return "No results found."
    
    output = []
    for r in results:
        block = {
            "path": r.get("path", ""),
            "similarity": round(r.get("similarity", 0), 4),
            "lines": r.get("lines", []),
            "key": r.get("key", "")
        }
        output.append(block)
    
    import json
    return json.dumps({"results": output}, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
