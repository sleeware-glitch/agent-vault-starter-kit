# MCP Server Setup Guide

This directory contains the custom MCP server that gives Claude agents native vault access — search, read, write, surgical editing, property management, and graph awareness.

## Architecture

Three files work together:

- **`vault_mcp_server.py`** — The main MCP server. 19 tools exposed via FastMCP. Handles all vault operations.
- **`server.py`** — Smart Connections embedding database wrapper. Reads the `.smart-env/` embedding files and provides semantic search.
- **`desktop_sc_server.py`** — A lightweight MCP server for Desktop Claude only. Wraps the SC database for local use.

## Prerequisites

- Python 3.10+
- Obsidian with Smart Connections plugin (embeddings must be built first)
- Obsidian CLI enabled (v1.12+)

## Installation

```bash
# Create a directory for the MCP server (outside the vault)
mkdir C:\Users\YOUR_USERNAME\mcp-server
cd C:\Users\YOUR_USERNAME\mcp-server

# Copy the three .py files and requirements.txt here

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### Step 1: Edit vault_mcp_server.py

Find the `VAULT_PATH` constant near the top and change it to your vault's path:

```python
VAULT_PATH = Path(
    os.environ.get(
        "OBSIDIAN_VAULT_PATH",
        r"C:\Users\YOUR_USERNAME\PATH\TO\YOUR\VAULT",  # ← CHANGE THIS
    )
)
```

### Step 2: Change the server name (optional)

Find the `FastMCP(...)` instantiation and rename:

```python
mcp = FastMCP(
    "my_project_vault",  # ← Change from "transcent_vault" to your name
    stateless_http=True,
    host=HOST,
    port=PORT,
)
```

### Step 3: Update run_python sandbox paths (if using Desktop)

The `run_python` function has a filesystem sandbox. Update `_ALLOWED_ROOTS` to include your directories.

## Running

```bash
# Activate venv
.venv\Scripts\activate

# Start the server
python vault_mcp_server.py
```

The server starts on port 5000. You should see a startup banner showing the vault path, embedding count, and available tools.

## Connecting to Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-vault": {
      "command": "C:\\Users\\YOUR_USERNAME\\mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YOUR_USERNAME\\mcp-server\\vault_mcp_server.py"]
    }
  }
}
```

## Remote Access (Browser/Mobile)

To give browser and mobile Claude sessions vault access, you need a Cloudflare tunnel:

1. **Install cloudflared:** https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
2. **Create a tunnel:**
   ```bash
   cloudflared tunnel login
   cloudflared tunnel create my-vault-tunnel
   ```
3. **Configure the tunnel** to route to `http://localhost:5000`
4. **Run the tunnel:**
   ```bash
   cloudflared tunnel run my-vault-tunnel
   ```
5. **Register as Claude Connector:**
   - Go to claude.ai → Settings → Connectors → Add custom connector
   - Paste your tunnel URL + `/mcp`

## Auto-Start (Windows)

Create a VBS script in your Windows Startup folder to auto-start both the MCP server and tunnel on login:

```vbs
Set WshShell = CreateObject("WScript.Shell")
' Start MCP server
WshShell.Run "cmd /c cd /d C:\Users\YOUR_USERNAME\mcp-server && .venv\Scripts\python.exe vault_mcp_server.py", 0, False
' Start tunnel
WshShell.Run "cmd /c cloudflared tunnel run my-vault-tunnel", 0, False
```

Save as `start_vault_services.vbs` in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`.

## Security Warning

The MCP server has NO authentication by default. Anyone who knows your tunnel URL can read and write your vault files. This is a known security gap. Options:

1. **Don't expose the tunnel publicly** — use it only on trusted networks
2. **Add Cloudflare Access** — put an authentication layer in front of the tunnel
3. **IP allowlisting** — restrict tunnel access to specific IPs

## Tool Reference

The server exposes 19 tools (plus 1 Desktop-only):

| Tool | Purpose |
|------|---------|
| `search_vault` | Semantic search via Smart Connections embeddings |
| `read_file` | Read entire file |
| `read_file_lines` | Read specific line range |
| `list_directory` | List folder contents |
| `write_file` | Create/overwrite files |
| `update_file_lines` | Surgical line-level editing (insert/replace/delete) |
| `resolve_wikilink` | Convert [[wiki-links]] to file paths |
| `obsidian_move` | Move files with link rewriting |
| `obsidian_create` | Create files from templates |
| `obsidian_rename` | Rename files with link rewriting |
| `obsidian_property_set` | Set YAML frontmatter properties |
| `obsidian_property_read` | Read YAML frontmatter properties |
| `obsidian_orphans` | Find files with no incoming links |
| `obsidian_backlinks` | Find files that link to a given file |
| `obsidian_search_native` | Keyword search via Obsidian's index |
| `obsidian_tags` | List all tags with counts |
| `obsidian_read_computed` | Read Dataview inline computed fields |
| `vault_refresh` | Refresh Dataview Serializer dashboards |
| `vault_changes` | Git-powered change tracking |
| `run_python` | Ephemeral Python execution (Desktop only, NOT on connector) |

## Troubleshooting

**"Zero embeddings loaded"** — Smart Connections hasn't built its index yet. Open Obsidian, wait for SC to finish indexing, then restart the MCP server.

**"FATAL: Cannot import SmartConnectionsDatabase"** — `server.py` must be in the same directory as `vault_mcp_server.py`.

**CLI tools returning errors** — Obsidian must be running. The CLI communicates via IPC to the running Obsidian instance.

**"command not found: obsidian"** — The Obsidian CLI needs to be in your PATH. See Obsidian CLI setup docs.
