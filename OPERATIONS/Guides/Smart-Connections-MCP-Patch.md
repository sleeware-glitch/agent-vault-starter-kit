---
scope: core
status: active
created: 2026-03-09
summary: >
  Documents patches applied to the Smart Connections MCP server infrastructure.
  Two files: server.py (database class, patched 2026-03-09) and desktop_sc_server.py
  (Desktop wrapper, patched 2026-03-15). Critical: if either file is reinstalled
  or rewritten, patches must be reapplied. Includes exact bugs, fixes, file
  locations, and verification steps.
last-verified: 2026-03-15
document-role: operations
fileClass: tracked-item
---

# Smart Connections MCP Server: The get_context_blocks Patch

## What This Documents

The Smart Connections MCP server from `github.com/dan6684/smart-connections-mcp` has a bug in its `get_context_blocks` function. The server ships with this bug. We patched `server.py` on March 9, 2026. **If the server is ever reinstalled, updated, or cloned fresh from the repo, this patch must be reapplied.**

## The Bug

The `get_context_blocks` function is supposed to return actual text content for the vault blocks most relevant to a query. In the original code, it tries to get text from the embeddings cache:

```python
'text': item.get('text', '')
```

But Smart Connections doesn't store block text in its `.ajson` embedding files. It stores vectors, line numbers, and metadata. There IS no `text` field. So every block returns `text: null` (or empty string).

Same problem with the `path` field — `item.get('path')` returns `None` because the `.ajson` data doesn't have a top-level `path` field. The path IS encoded in the embedding key itself (e.g., `smart_blocks:REFERENCE/Hyperselves.md#Hyperselves#VI. Cognitive Architecture`) but the original code doesn't extract it.

## The Fix

The patched `get_context_blocks` method:
1. **Extracts the file path from the embedding key** by stripping the `smart_blocks:` prefix and splitting on `#` (taking the first segment)
2. **Opens the actual .md file** from disk using `self.vault_path / file_path`
3. **Reads only the line range** specified in the block's `lines` field
4. **Returns the real file path** instead of null

## File Location

```
C:\Users\nosuc\smart-connections-mcp\server.py
```

## The Patched Method (Complete)

Find the `get_context_blocks` method in `server.py` (in the `SmartConnectionsDatabase` class). Replace the entire method with:

```python
    def get_context_blocks(self, query: str, max_blocks: int = 5) -> List[Dict]:
        """
        Get best context blocks for a query (for RAG).
        Returns actual text content by reading source files from disk.
        """
        self.ensure_model_loaded()
        self.load_embeddings()
        query_vec = self.model.encode(query)
        query_vec = query_vec / np.linalg.norm(query_vec)

        results = []
        for key, item in self.embeddings_cache.items():
            if not key.startswith('smart_blocks:'):
                continue
            vec = item['vector']
            vec = vec / np.linalg.norm(vec)
            similarity = float(np.dot(query_vec, vec))

            if similarity > 0.4:
                # Extract file path from key: smart_blocks:PATH/TO/FILE.md#heading#subheading
                key_without_prefix = key[len('smart_blocks:'):]
                file_path = key_without_prefix.split('#')[0]

                # Read actual text from source file using line numbers
                text = None
                lines = item.get('lines', [])
                if file_path and lines and len(lines) >= 2:
                    try:
                        full_path = self.vault_path / file_path
                        with open(full_path, 'r', encoding='utf-8') as f:
                            all_lines = f.readlines()
                            start = max(0, lines[0] - 1)  # Convert to 0-indexed
                            end = min(len(all_lines), lines[1])
                            text = ''.join(all_lines[start:end]).strip()
                    except Exception:
                        text = None

                results.append({
                    'key': key,
                    'path': file_path,
                    'similarity': similarity,
                    'lines': lines,
                    'text': text
                })

        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:max_blocks]
```

## How to Verify the Patch Is Applied

From any Desktop agent session, run:
```
get_context_blocks(query="hyperself cognitive light cone", max_blocks=1)
```

If the `text` field contains actual vault content (not `null` or empty), the patch is working. If `text` is `null`, the server needs repatching.

## How to Repatch After a Reinstall

1. Open `C:\Users\nosuc\smart-connections-mcp\server.py` in any text editor
2. Find the `get_context_blocks` method (search for `def get_context_blocks`)
3. Replace the entire method with the code above
4. Save the file
5. Fully quit Claude Desktop (kill all processes via Task Manager) and restart
6. Verify with the test query above

## Why the Original Code Doesn't Work

The dan6684 MCP server was designed for Claude Code, which typically runs on Mac/Linux with vaults in simple home directory paths. The server loads embeddings correctly (vectors, keys, metadata) but assumes text content is stored in the embeddings data. Smart Connections stores text in the source .md files, not in the `.ajson` embedding files. The fix bridges this gap by reading source files directly.

The `path` field is null for the same reason — the `.ajson` data doesn't have an explicit path property. The path is encoded in the key string. The fix parses it from the key.

## Ghost Entries

When vault files are moved or renamed, old embeddings persist in `.smart-env/multi/*.ajson` with stale paths. `get_context_blocks` tries to open a file that no longer exists at the old path, catches the exception, and returns `text: null`. These ghost entries are noise, not poison — they waste result slots but don't crash anything. Fix with periodic Smart Connections Force Refresh (plugin settings) or by deleting the `.smart-env` folder and letting the plugin rebuild.

## The Desktop Wrapper Bug (2026-03-15, Core-13)

**Separate from the `server.py` patch above.** Claude Desktop doesn't load `server.py` directly — it loads `desktop_sc_server.py`, a FastMCP wrapper created during Core-10. The wrapper imported `SmartConnectionsDatabase` from `server.py` but called `db.search()` — a method that **does not exist** on the class. The actual methods are `semantic_search()`, `get_context_blocks()`, and `find_related()`.

**Symptom:** All three SC tools (`search_vault`, `get_context_blocks`, `semantic_search`) fail with `'SmartConnectionsDatabase' object has no attribute 'search'`.

**Root cause:** `desktop_sc_server.py` line 23 and line 49 both called `db.search(query, max_results=...)`. This method was never defined. Likely a typo or assumption during the Core-10 rewrite that was never tested.

**Why it wasn't caught:** This doc only documented the `server.py` database class patch. The `desktop_sc_server.py` wrapper was undocumented. The `claude_desktop_config.json` points to `desktop_sc_server.py`, not `server.py`. Nobody connected "SC is broken" to "the wrapper calls a nonexistent method" because the documented patch was on a different file.

**The fix (desktop_sc_server.py):**
- `search_vault` tool → calls `db.get_context_blocks(query, max_blocks=max_results)` (returns text blocks read from disk)
- `semantic_search` tool → calls `db.semantic_search(query, limit=max_results)` (returns paths/keys/scores)
- `get_context_blocks` tool → delegates to `search_vault` (unchanged)

## The Null Path Bug (2026-03-15, Core-13)

**Discovered during the wrapper fix.** After fixing the wrapper, `semantic_search` returned results with `path: null`. The root cause was in `server.py`'s `load_embeddings()` method — the ajson embedding data does NOT contain a top-level `path` field. The March 9 patch fixed this in `get_context_blocks` by parsing the path from the embedding key, but `semantic_search` and `find_related` were never patched. Same bug, two methods left behind.

**The fix (server.py — structural, not method-by-method):**
1. New `extract_path_from_key()` utility: parses path from both `smart_blocks:` and `smart_sources:` key formats
2. `load_embeddings()` now stores `'path': extract_path_from_key(key)` instead of `'path': item.get('path')` — fixes ALL methods at the cache level
3. New `_read_block_text()` helper: extracted disk-read logic so `semantic_search` can also return `text_preview`

**Result:** All three database methods (`semantic_search`, `get_context_blocks`, `find_related`) return correct file paths. `semantic_search` additionally returns short text previews.

**Meta-lesson — agent blindness to environmental defects:** This null-path bug existed since March 9 (six days, multiple agents). It was documented as a "known cosmetic issue" and agents learned to parse the `key` field as a workaround. Each successor inherited the workaround as normal behavior. A fresh agent (Core-13) caught it because it hadn't yet adapted to the broken output. **Lesson for future agents:** test every tool output against its spec at bootstrap, don't just confirm tools load. Partial functionality is harder to spot than total failure.

## Files Involved

- `C:\Users\nosuc\smart-connections-mcp\server.py` — the database class (PATCHED: March 9 for text retrieval, March 15 for path extraction and structural cleanup)
- `C:\Users\nosuc\smart-connections-mcp\desktop_sc_server.py` — the Desktop FastMCP wrapper (PATCHED: March 15 for correct method names)
- `%APPDATA%\Claude\claude_desktop_config.json` — points to `desktop_sc_server.py`

## How to Verify After Any Future Reinstall

Run all three tools and check outputs:

```
smart-connections:get_context_blocks(query="hyperself cognitive light cone", max_results=1)
```
✓ `text` contains vault content, `path` contains a file path

```
smart-connections:semantic_search(query="hyperself cognitive light cone", max_results=1)
```
✓ `path` contains a file path (not null), `key` contains the full embedding key

```
smart-connections:search_vault(query="hyperself cognitive light cone", max_results=1)
```
✓ Same as `get_context_blocks` (wrapper delegates to it)

If any tool errors about `'search'` attribute → `desktop_sc_server.py` needs repatching.
If `path` is null on `semantic_search` → `server.py`'s `load_embeddings()` needs the `extract_path_from_key` fix.
