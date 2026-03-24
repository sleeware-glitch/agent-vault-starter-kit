---
scope: core
status: active
created: 2026-03-11
last-verified: 2026-03-11
stale-after: 90d
summary: 'How the remote MCP connector gives browser and mobile Claude agents native vault tools (search, read, line-level edit, write). Architecture, startup, troubleshooting, and tool reference. Supersedes Vault-Bridge-Operations.md.

  '
document-role: operations
fileClass: tracked-item
---

# Vault MCP Connector: Operations Guide

## What It Is

The Vault MCP Connector is a FastMCP server that exposes the Obsidian vault as a native claude.ai connector. Browser and mobile agents get first-class vault tools — semantic search, file reading, surgical line-level editing, directory listing, and file writing — through the same mechanism that powers the Notion, Gmail, and GitHub connectors.

This replaces the old Vault Bridge (Flask HTTP server + web_fetch workaround). The bridge required pasting tunnel URLs into every conversation and parsed JSON responses from HTTP endpoints. The connector gives agents native MCP tool calls that work automatically in every session.

## Architecture

```
[claude.ai browser/mobile]
    ↓ native MCP tool calls
[Cloudflare named tunnel: vault.leeware.org/mcp]
    ↓ HTTPS → localhost:5000
[FastMCP server: vault_mcp_server.py]
    ↓ imports SmartConnectionsDatabase
[Smart Connections embeddings + vault .md files]
```

**Components:**
- `vault_mcp_server.py` — FastMCP server at `C:\Users\nosuc\smart-connections-mcp\`
- `server.py` — Smart Connections database (patched). See [[Smart-Connections-MCP-Patch]]
- Cloudflare named tunnel `transcent-vault` → `vault.leeware.org`
- Config at `C:\Users\nosuc\.cloudflared\config.yml`
- Smart Connections plugin must be running in Obsidian (for current embeddings)

**Key properties:**
- Authless (no OAuth) — secured by URL obscurity and tunnel ephemerality
- Streamable HTTP transport on single `/mcp` endpoint
- Stateless — no session persistence between tool calls
- Named tunnel with stable URL — set up once in claude.ai, persists across sessions

## Available Tools

### Core Vault Tools (7)

| Tool | What it does | Desktop equivalent |
|------|-------------|-------------------|
| `search_vault(query, max_results)` | Semantic search across all vault files. Returns block text, file paths, line numbers, similarity scores. | `get_context_blocks` |
| `read_file(path)` | Read entire vault file by path. Returns raw markdown. | `contentManager.read` (full file) |
| `read_file_lines(path, start_line, end_line)` | Read specific line range. 1-based, inclusive. | `contentManager.read` (with line range) |
| `update_file_lines(path, content, start_line, end_line)` | Surgical line-level editing. Insert, replace, or delete at specific line positions. | `contentManager.update` |
| `list_directory(path)` | List folder contents. Hidden items excluded. | `storageManager.list` |
| `write_file(path, content)` | Create or overwrite a vault file. Creates parent dirs. | `contentManager.write` |
| `resolve_wikilink(name)` | Resolve `[[wiki-link]]` names to file paths. Comma-separated for batch. | *(no equivalent — Desktop uses Obsidian's internal index)* |

### Obsidian CLI Tools (10)

These pass through Obsidian's internal API via the CLI (Obsidian 1.12.4+). They provide native Obsidian operations with automatic link maintenance, proper YAML formatting, and graph awareness. Available to all agents on all platforms.

| Tool | What it does | Key advantage |
|------|-------------|---------------|
| `obsidian_create(name, template, content)` | Create files, optionally from Templater templates. Use `path=` for nested paths. | Template-native creation with full YAML schema. |
| `obsidian_move(file, to)` | Move files to a different folder. | Auto-rewrites ALL wiki-links vault-wide. |
| ~~`obsidian_delete`~~ | **REMOVED (Core-16, 2026-03-20).** Craft-24 accidentally deleted 8 critical files. Delete restricted to Desktop Core agents (shell) and Lee (UI). |
| `obsidian_rename(file, new_name)` | Rename files. | Auto-rewrites ALL wiki-links vault-wide. |
| `obsidian_property_set(file, name, value)` | Set a YAML frontmatter property. | Writes through Obsidian's API — clean formatting, no MM mutation. |
| `obsidian_property_read(file, name)` | Read a YAML frontmatter property. | Reads through Obsidian's metadata cache. |
| `obsidian_search_native(query, limit)` | Full-text keyword search. | Complements semantic `search_vault` — finds exact text matches. |
| `obsidian_backlinks(file)` | List all files that link TO a given file. | Graph awareness before modifying anything. |
| `obsidian_orphans()` | List files with no incoming links. | Instant vault health audit. |
| `obsidian_tags()` | List all tags with usage counts. | Tag inventory. |
| `obsidian_read_computed(file, name)` | Read computed (inline body) fields via Dataview API. | Reads reading-cost, completeness, scene-count, etc. that `obsidian_property_read` can't see. |

**Note on `obsidian_create` with templates:** The template skeleton (YAML fields, body structure, deployment guide) is copied correctly. Templater's dynamic expressions (`<% tp.system.prompt() %>`) appear as raw text because agents can't interact with UI prompts. Agents fill in the values afterward via `update_file_lines` or `obsidian_property_set`.

**Note on `obsidian_property_set/read`:** These use an `eval` bridge to work around a Windows CLI shim bug (colon subcommands + params fail silently on Windows, confirmed Obsidian bug, fix expected in 1.12.2). The bridge routes through `obsidian eval` with JavaScript that accesses `app.fileManager.processFrontMatter` and `app.metadataCache`. Same result, different backend. When 1.12.2 ships, the implementation switches to native `property:set/read` commands — the MCP tool interface stays identical.


### Using update_file_lines

This tool provides the same surgical editing capability as Nexus `contentManager.update` on desktop. Three modes:

**REPLACE** — Provide both `start_line` and `end_line`. Replaces those lines (inclusive) with the new content. Example: replace lines 47-49 with new text.

**INSERT** — Set `end_line` to 0 (or omit it). Inserts content BEFORE `start_line` without removing any existing lines. Set `start_line=-1` to append to end of file.

**DELETE** — Set `content` to empty string `""` with a `start_line` and `end_line` range. Removes those lines.

Returns `linesDelta` showing net line change — use this to adjust positions in multi-edit sessions. Always re-read the target lines with `read_file_lines` immediately before editing to ensure correct positioning. After any edit that changes line count, line numbers shift — re-verify before further edits to the same file.

## Browser-Desktop Tool Parity

Browser and desktop agents now have equivalent vault capabilities. The seven browser tools cover the same operations as the desktop Nexus + Smart Connections stack:

- **Search:** `search_vault` ≈ `get_context_blocks`
- **Read:** `read_file` + `read_file_lines` ≈ `contentManager.read`
- **Edit:** `update_file_lines` ≈ `contentManager.update`
- **Write:** `write_file` ≈ `contentManager.write`
- **Navigate:** `list_directory` ≈ `storageManager.list`
- **Resolve:** `resolve_wikilink` *(no desktop equivalent — Desktop uses Obsidian's internal index)*

Desktop retains advantages in having Smart Connections' full three-tool search suite (`semantic_search`, `find_related`, `get_context_blocks`) and Nexus's additional file operations (move, archive). For most creative and research work, the browser toolset is fully sufficient.

## Quick Start

You need TWO PowerShell windows. Keep both open while working.

### Window 1: Start the MCP server

```powershell
cd "C:\Users\nosuc\smart-connections-mcp"
.venv\Scripts\activate
python vault_mcp_server.py
```

You should see:
You should see:
```
TRANSCENT Vault MCP Server
Vault:    C:\Users\nosuc\Proton Drive\lee.ware\My files\THE METASTORY PROJECT\TRANSCENT
Embeddings loaded: [6000+]
File index: [300+] .md files found in vault
Endpoint: http://0.0.0.0:5000/mcp
Tools:    search_vault, read_file, read_file_lines,
          list_directory, write_file, update_file_lines,
          resolve_wikilink
```

### Window 2: Start the tunnel

```powershell
cloudflared tunnel run transcent-vault
```

You should see multiple "Registered tunnel connection" lines.

Both windows must stay open while you work. The connector in claude.ai is already configured — no per-session setup needed.

## Restart Protocol

### Full restart (after laptop reboot):

1. Open Obsidian (Smart Connections must be running)
2. PowerShell Window 1: start the MCP server (commands above)
3. PowerShell Window 2: start the tunnel (command above)
4. That's it — no URL pasting needed. The connector in claude.ai points to the stable `vault.leeware.org` domain.

### Server-only restart (tunnel still running):

If the MCP server crashes but the tunnel is still up:
```powershell
cd "C:\Users\nosuc\smart-connections-mcp"
.venv\Scripts\activate
python vault_mcp_server.py
```

### Tunnel-only restart (server still running):

If the tunnel drops but the server is still up:
```powershell
cloudflared tunnel run transcent-vault
```

## Troubleshooting

### Server won't start / "Cannot import SmartConnectionsDatabase"
- Is `vault_mcp_server.py` in the same directory as `server.py`?
- Is the venv activated? (`.venv\Scripts\activate`)

### Embeddings loaded: 0
- Is Obsidian open with Smart Connections plugin running?
- Check the vault path in `vault_mcp_server.py` matches the actual vault location.
- The `.smart-env/multi/` directory must contain `.ajson` files.

### Tunnel won't connect / "tunnel with name already exists"
- The tunnel is already created. Just run: `cloudflared tunnel run transcent-vault`
- Check config: `type "$env:USERPROFILE\.cloudflared\config.yml"`

### Agent can't see vault tools in claude.ai
- Is the connector added in Settings > Connectors? (should show "Transcent Vault")
- Are both the server AND tunnel running?
- Try starting a **new conversation** — connectors added mid-conversation may not appear.
- Check that tools are enabled: Settings > Connectors > Transcent Vault > all tools toggled on.
- If new tools were added to the server, you may need to refresh the claude.ai page or start a new conversation for them to appear.

### Search returns null text / ghost entries
- Smart Connections may need a Force Refresh (plugin settings in Obsidian).
- **⚠️ CRITICAL: After a Force Refresh, you MUST restart the vault MCP server.** The server loads embeddings into memory at startup. A Force Refresh rebuilds the `.ajson` files on disk, but the running server still has old embeddings in RAM. New files won't appear in search, and ghost entries from deleted/moved files will persist. Restart with: `taskkill /f /im python.exe` then relaunch `vault_mcp_server.py`. The VBS auto-start script handles this on reboot but NOT on Force Refresh.
- Ghost entries from moved files return null text — noise, not poison.
- Check that the server.py patch is applied. See [[Smart-Connections-MCP-Patch]].

### Port 5000 in use
- The old vault_bridge.py may still be running. Kill it or set `VAULT_MCP_PORT=5001` before starting.

### "Not Acceptable: Client must accept text/event-stream"
- Normal. This appears when you visit the `/mcp` endpoint in a browser. The endpoint speaks MCP protocol, not HTTP. It works correctly when claude.ai connects to it.

## Security

The Cloudflare named tunnel does NOT expose your IP address. DNS lookups for `vault.leeware.org` resolve to Cloudflare's proxy servers. Your machine makes outbound connections to Cloudflare — nothing inbound.

The endpoint is currently authless — anyone who knows the URL and speaks MCP protocol could access the vault. Practical risk is low (URL is private, protocol is machine-only, tunnel runs only during work sessions) but not zero.

**Planned improvement:** Add OAuth authentication. The MCP SDK supports it, claude.ai supports it (Client ID/Secret fields in connector settings), and it would require ~40 lines of additional code in the server. This is tracked as a follow-up task.

## Dependencies

- **Smart Connections Obsidian plugin** — must be running for fresh embeddings
- **Python venv** at `C:\Users\nosuc\smart-connections-mcp\.venv\`
- **MCP SDK** (`pip install "mcp[cli]"`) installed in the venv
- **server.py** with the `get_context_blocks` patch applied
- **cloudflared** CLI installed
- **Cloudflare account** with tunnel `transcent-vault` and DNS route for `vault.leeware.org`
- **claude.ai connector** configured at Settings > Connectors > Transcent Vault

## Code Architecture (For Future Core Agents)

The entire vault MCP server is ONE Python file: `C:\Users\nosuc\smart-connections-mcp\vault_mcp_server.py`. Desktop Core agents can read and edit it directly via Filesystem MCP — the `smart-connections-mcp` directory is in the scoped filesystem access list.

The file has six sections in order:

1. **Configuration and imports** (~lines 1-60) — vault path, port, logging, Smart Connections database import.
2. **Embedding initialization** (~lines 60-100) — loads SC embeddings into RAM at startup. This is why search goes stale after a Force Refresh — the running process still has old embeddings. Restart the server to reload.
3. **Core tool definitions** (~lines 100-380) — the original seven `@mcp.tool()` functions: `search_vault`, `read_file`, `read_file_lines`, `update_file_lines`, `list_directory`, `write_file`, `resolve_wikilink`.
4. **Wiki-link resolver and helpers** (~lines 380-440) — `_build_file_index()` scans all `.md` files via `VAULT_PATH.rglob("*.md")` and builds a filename→path map. `resolve_wikilink()` rebuilds this index fresh on every call (not cached), so file moves and creates are picked up without server restart. `_is_safe_path()` prevents path traversal.
5. **Obsidian CLI tools** (~lines 440-580) — ten `@mcp.tool()` functions that wrap Obsidian CLI commands via `_run_cli()`. The helper joins args into a single shell string (critical for Windows quoting). Property tools (`obsidian_property_set`, `obsidian_property_read`) use `obsidian eval` with JavaScript accessing `app.fileManager.processFrontMatter` and `app.metadataCache` — this is a workaround for a Windows CLI shim bug where colon subcommands + params fail silently (confirmed bug, fix expected in Obsidian 1.12.2). When 1.12.2 ships, swap the eval JS to native `property:set`/`property:read` calls.
6. **Entry point** (~lines 580-end) — runs FastMCP with `streamable-http` transport.

**Staleness rules:**
- **Embeddings** (search): cached at startup. Stale after SC Force Refresh. Fix: restart server.
- **File index** (resolve_wikilink): rebuilt every call. Never stale.
- **File content** (read/write): reads from disk every call. Never stale.
- **CLI tools**: pass through to running Obsidian instance. Never stale. But require Obsidian to be running — if Obsidian is closed, CLI tools return errors.

**Adding a new tool:** Write a new `@mcp.tool()` function anywhere in the tool definitions sections. Restart the server. Browser agents in NEW conversations will see it (existing conversations cache the tool list). Update this guide's tool tables when you add one.

**Adding a new CLI command:** Add the command name to the shell whitelist regex in `C:\Users\nosuc\mcp-servers\shell_mcp_server.py` (outside agent filesystem scope — Lee must edit). Then write the `@mcp.tool()` wrapper in `vault_mcp_server.py`. Use `_run_cli()` for standard commands or `_run_cli("eval", f'code="..."')` for colon subcommands blocked by the Windows shim bug.

**If CLI tools fail silently:** Check that Obsidian is running. Check `obsidian version` from shell. If colon subcommands return exit -1 with no output, that's the Windows shim bug — use the eval bridge pattern. If non-colon commands fail, the CLI may not be registered in PATH (Settings → General → Command line interface → Register CLI).

**If resolve_wikilink breaks:** It's the simplest tool — a directory scan and a dictionary lookup. Most likely causes: vault path changed, or a file has non-UTF-8 characters in its name. Read the function directly: `filesystem:read_text_file` on `C:\Users\nosuc\smart-connections-mcp\vault_mcp_server.py`, look for `def resolve_wikilink`.

## Superseded Systems

This connector supersedes:
- **Vault Bridge** (`vault_bridge.py`) — Flask HTTP server with web_fetch endpoints. Functional but required per-session URL pasting and JSON parsing. No write access. See [[Vault-Bridge-Operations]] for the old system (preserved for reference).
- **GitHub mirror connector** — Read-only, file-level only, no search, no write.
