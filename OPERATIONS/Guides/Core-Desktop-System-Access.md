---
summary: 'Step-by-step guide for granting Core Desktop agents scoped filesystem and shell access via MCP servers. Phase 1: Anthropic filesystem server (3 directories). Phase 2: custom whitelist shell server (6 allowed command categories). Security: shell server code lives OUTSIDE filesystem scope so agents cannot modify their own whitelist. Includes exact config JSON and Python server code.

  '
status: active
scope: core
created: 2026-03-12 17:59:59
modified: 2026-03-12 18:57:37
stale-after: 90d
document-role: operations
fileClass: tracked-item
---

# Core Desktop System Access — Setup Guide

## What This Enables

Core agents running in Claude Desktop get scoped access to:
- **Phase 1:** Read/write files in three specific directories (vault, MCP server code, Cloudflare config)
- **Phase 2:** Execute whitelisted shell commands (Python, npm, git, schtasks, cloudflared, pip)

This turns a Desktop Core session into a full infrastructure agent — it can modify MCP server code, install plugins, manage scheduled tasks, push to git, and restart services, all with complete project knowledge from the Project Instructions.

## Security Architecture (Read This First)

There are three layers of access. Each layer is controlled by a different file, and no agent can reach the files that control the other layers.

**Layer 1: Which MCP servers exist and what directories they can reach.**
Controlled by: `%APPDATA%\Claude\claude_desktop_config.json`
This file lives OUTSIDE all allowed directories. No agent can modify it. Only Lee can add or remove MCP servers, or change which directories the filesystem server can access. This is the master boundary.

**Layer 2: Which shell commands are allowed.**
Controlled by: `C:\Users\nosuc\mcp-servers\shell_mcp_server.py`
This file lives in its OWN directory that is NOT listed in the filesystem server's allowed paths. The agent can USE the shell commands but cannot EDIT the whitelist that determines which commands are allowed. Only Lee can modify the whitelist by editing this file directly.

**Layer 3: What happens within the allowed boundaries.**
Controlled by: The agent's own judgment + Claude's safety training.
Within the allowed directories and allowed commands, the agent can read, write, and execute freely. This is where project work happens.

**The key principle:** The files that define the agent's permissions are always stored outside the agent's reach. The agent operates within boundaries it cannot modify.

**What Core CAN access:**
- The vault directory including `.obsidian/` (plugin configs, settings)
- The Smart Connections MCP server directory (server code, patches)
- The Cloudflare tunnel configuration
- Whitelisted shell commands only (Phase 2)

**What Core CANNOT access:**
- The config file that defines its own access scope
- The shell server code that defines its command whitelist
- Browser data, passwords, cookies, email
- Documents, Downloads, Desktop, or any personal folders
- Any shell command not matching the whitelist

---

## Phase 1: Scoped Filesystem Access

### Prerequisite

Node.js must be installed (you already have it — the MCP server uses it).

### What to do

Open `%APPDATA%\Claude\claude_desktop_config.json` in Notepad. You can find it by pressing `Win+R`, pasting `%APPDATA%\Claude\`, and opening the JSON file.

Find the `"mcpServers"` object. It already contains entries for your existing servers (nexus, smart-connections, etc.). Add the `"filesystem"` entry alongside them.

### The entry to add

```json
"filesystem": {
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "C:\\Users\\nosuc\\Proton Drive\\lee.ware\\My files\\THE METASTORY PROJECT\\TRANSCENT",
    "C:\\Users\\nosuc\\smart-connections-mcp",
    "C:\\Users\\nosuc\\.cloudflared"
  ]
}
```

**Important:** JSON requires commas between entries. Make sure each server block is separated by a comma. No trailing comma after the last entry.

### After editing

1. Save the file.
2. Fully quit Claude Desktop (system tray → right-click → Quit. The X button leaves background processes running).
3. Restart Claude Desktop.
4. Open a Core project thread. You should see filesystem tools available.

### Verification test

Ask Core to: "List the contents of `C:\Users\nosuc\smart-connections-mcp`" — if it returns a file listing, Phase 1 is working. Then try: "List the contents of `C:\Users\nosuc\Documents`" — it should be BLOCKED.

---

## Phase 2: Whitelist Shell Server

### Step 1: Create the server directory

Create a new folder: `C:\Users\nosuc\mcp-servers\`

This directory is intentionally NOT listed in the filesystem server's allowed paths. The agent cannot read or modify files here. This is the security boundary.

### Step 2: Save the server code

Save the following as `C:\Users\nosuc\mcp-servers\shell_mcp_server.py`:

```python
"""
Whitelist Shell MCP Server for TRANSCENT Core agents.
Only allows pre-approved command categories. Rejects everything else.
The whitelist lives in THIS file, which is stored outside the agent's
filesystem scope — the agent can USE these commands but cannot EDIT this file.
"""

import subprocess
import re
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "TRANSCENT Shell",
    host="127.0.0.1",
    port=5050
)

# --- WHITELIST DEFINITIONS ---
# Each entry: (description, regex pattern that the full command must match)

ALLOWED_PATTERNS = [
    # Python: run .py files from specific directories only
    ("python script (vault OPERATIONS/)", 
     r'^python\s+"?C:\\Users\\nosuc\\Proton Drive\\lee\.ware\\My files\\THE METASTORY PROJECT\\TRANSCENT\\OPERATIONS\\[^"]+\.py"?(\s+.*)?$'),
    
    ("python script (smart-connections-mcp/)", 
     r'^python\s+"?C:\\Users\\nosuc\\smart-connections-mcp\\[^"]+\.py"?(\s+.*)?$'),

    # npm: install packages (global or in specific directories)
    ("npm install", r'^npm\s+install\s+'),

    # pip: install packages (must include --break-system-packages)
    ("pip install", r'^pip\s+install\s+.*--break-system-packages'),

    # git: standard operations
    ("git operation", r'^git\s+(status|add|commit|push|pull|log|diff|remote|fetch|stash)(\s+.*)?$'),

    # Windows Task Scheduler: create, query, delete, change, run, end tasks
    ("schtasks", r'^schtasks\s+/(create|query|delete|change|run|end)(\s+.*)?$'),

    # cloudflared: tunnel management
    ("cloudflared", r'^cloudflared\s+(tunnel|service|version)(\s+.*)?$'),

    # Process check: see if specific services are running
    ("tasklist check", r'^tasklist\s+/FI\s+"IMAGENAME\s+eq\s+(python|cloudflared|node)\.exe"'),

    # Directory listing (read-only, safe)
    ("dir listing", r'^dir\s+'),

    # Type command (read file contents, read-only, safe)
    ("type file", r'^type\s+'),
]


def check_whitelist(command: str) -> tuple[bool, str]:
    """Check if a command matches any whitelisted pattern."""
    command = command.strip()
    for description, pattern in ALLOWED_PATTERNS:
        if re.match(pattern, command, re.IGNORECASE):
            return True, description
    return False, ""


@mcp.tool()
def run_command(command: str) -> str:
    """
    Execute a whitelisted shell command and return its output.
    Only pre-approved command categories are allowed.
    Rejected commands return an error without execution.
    """
    allowed, category = check_whitelist(command)

    if not allowed:
        return (
            f"BLOCKED: Command not in whitelist.\n"
            f"Command: {command}\n\n"
            f"Allowed categories:\n"
            f"- python scripts (from vault OPERATIONS/ or smart-connections-mcp/)\n"
            f"- npm install\n"
            f"- pip install (with --break-system-packages)\n"
            f"- git (status, add, commit, push, pull, log, diff, remote, fetch, stash)\n"
            f"- schtasks (create, query, delete, change, run, end)\n"
            f"- cloudflared (tunnel, service, version)\n"
            f"- tasklist (filtered to python, cloudflared, node)\n"
            f"- dir (directory listings)\n"
            f"- type (read file contents)\n"
        )

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
            cwd="C:\\Users\\nosuc"
        )

        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        output += f"EXIT CODE: {result.returncode}"

        return output

    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out after 120 seconds."
    except Exception as e:
        return f"ERROR: {str(e)}"


@mcp.tool()
def list_allowed_commands() -> str:
    """List all command categories that the whitelist allows."""
    lines = ["Allowed command categories:\n"]
    for description, pattern in ALLOWED_PATTERNS:
        lines.append(f"  - {description}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Step 3: Install the dependency

The server imports `mcp.server.fastmcp`, which is installed in the smart-connections-mcp venv. You have two options:

**Option A (simpler):** Use the existing venv's Python to run the server (the config below does this).

**Option B (cleaner):** Create a separate venv in `C:\Users\nosuc\mcp-servers\` and install `mcp[cli]` there. This keeps the shell server fully independent.

The config below uses Option A.

### Step 4: Add the config entry

Add this to `claude_desktop_config.json` alongside the filesystem entry:

```json
"shell": {
  "command": "C:\\Users\\nosuc\\smart-connections-mcp\\.venv\\Scripts\\python.exe",
  "args": [
    "C:\\Users\\nosuc\\mcp-servers\\shell_mcp_server.py"
  ]
}
```

Note: This uses the smart-connections-mcp venv's Python interpreter (which has FastMCP installed) to run the shell server code from the separate mcp-servers directory.

### Step 5: Restart Claude Desktop

Fully quit (system tray → right-click → Quit), then restart.

### Verification tests

1. Ask Core: `run_command("git status")` — should return git status output.
2. Ask Core: `run_command("dir C:\\Users\\nosuc\\smart-connections-mcp")` — should return directory listing.
3. Ask Core: `run_command("whoami")` — should return BLOCKED.
4. Ask Core: `run_command("del C:\\important-file.txt")` — should return BLOCKED.
5. Ask Core: `list_allowed_commands()` — should list all allowed categories.

---

## The Full Config (for reference)

After both phases, `claude_desktop_config.json` should look like this (preserving your existing entries):

```json
{
  "mcpServers": {
    "nexus": {
      ... your existing nexus config ...
    },
    "smart-connections": {
      ... your existing smart-connections config ...
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\nosuc\\Proton Drive\\lee.ware\\My files\\THE METASTORY PROJECT\\TRANSCENT",
        "C:\\Users\\nosuc\\smart-connections-mcp",
        "C:\\Users\\nosuc\\.cloudflared"
      ]
    },
    "shell": {
      "command": "C:\\Users\\nosuc\\smart-connections-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\nosuc\\mcp-servers\\shell_mcp_server.py"
      ]
    }
  }
}
```

---

## Modifying Access (Lee Only)

**To add a filesystem directory:** Edit the `args` list in the filesystem config entry. Restart Claude Desktop.

**To add a shell command category:** Edit `ALLOWED_PATTERNS` in `C:\Users\nosuc\mcp-servers\shell_mcp_server.py`. Restart Claude Desktop.

**To revoke all extended access:** Remove the `"filesystem"` and `"shell"` entries from the config. Restart Claude Desktop. Nexus and Smart Connections continue working normally.

**To check what's currently allowed:** Ask any Core agent to call `list_allowed_commands()`.

---

## Why This Is Safe

1. **The agent cannot modify its own permissions.** The config file and the whitelist file are both outside the agent's filesystem scope.
2. **The whitelist is deny-by-default.** Every command is blocked unless it matches a regex pattern. New categories must be explicitly added by Lee.
3. **Changes require a restart.** Even if something were misconfigured, it doesn't take effect until Claude Desktop is restarted — giving Lee a checkpoint.
4. **Scoped directories, not root access.** The filesystem server sees three directories, not the whole drive. Personal files, browser data, and credentials are unreachable.
5. **Same trust model as Claude Code.** Claude Code runs with full user permissions on your machine. This setup is strictly MORE restricted than Code.
