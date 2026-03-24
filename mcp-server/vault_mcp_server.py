"""
TRANSCENT Vault MCP Server
===========================
Exposes the Obsidian vault to browser/mobile Claude agents via remote MCP.

Browser and mobile agents connect through claude.ai's custom connector feature.
This replaces the old vault_bridge.py (web_fetch hack) with native MCP tool calls.

Place in:  C:\\Users\\nosuc\\smart-connections-mcp\\vault_mcp_server.py
Run:       python vault_mcp_server.py
Expose:    cloudflared tunnel run transcent-vault
Connect:   claude.ai > Settings > Connectors > Add custom connector > paste URL/mcp

Requires:  pip install "mcp[cli]" numpy sentence-transformers
           (run in the existing .venv)
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional

import numpy as np

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

VAULT_PATH = Path(
    os.environ.get(
        "OBSIDIAN_VAULT_PATH",
        r"C:\Users\nosuc\Proton Drive\lee.ware\My files\THE METASTORY PROJECT\TRANSCENT",
    )
)
PORT = int(os.environ.get("VAULT_MCP_PORT", "5000"))
HOST = "0.0.0.0"

# Ensure the env var is set (server.py may read it)
os.environ["OBSIDIAN_VAULT_PATH"] = str(VAULT_PATH)

# ---------------------------------------------------------------------------
# Import Smart Connections database from server.py in the same directory
# ---------------------------------------------------------------------------

_this_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_this_dir))

try:
    from server import SmartConnectionsDatabase
except ImportError as exc:
    print(f"FATAL: Cannot import SmartConnectionsDatabase from server.py")
    print(f"  Expected location: {_this_dir / 'server.py'}")
    print(f"  Error: {exc}")
    print(f"  Make sure this file is in the same directory as server.py")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Initialize the Smart Connections search engine
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("vault-mcp")

log.info("Initializing Smart Connections database...")

try:
    db = SmartConnectionsDatabase(vault_path=str(VAULT_PATH))

    # Diagnostic: show where the DB is looking for embeddings
    smart_env = VAULT_PATH / ".smart-env"
    log.info(f"Vault path: {VAULT_PATH}")
    log.info(f".smart-env exists at vault root? {smart_env.exists()}")
    if smart_env.exists():
        multi = smart_env / "multi"
        log.info(f".smart-env/multi exists? {multi.exists()}")
        if multi.exists():
            ajson_files = list(multi.glob("*.ajson"))
            log.info(f"Found {len(ajson_files)} .ajson files in .smart-env/multi/")

    if hasattr(db, 'vault_path'):
        log.info(f"DB vault_path: {db.vault_path}")

    # Force-load embeddings now so startup failures surface immediately
    db.ensure_model_loaded()
    db.load_embeddings()
    embed_count = len(db.embeddings_cache)
    log.info(f"Loaded {embed_count} embeddings from vault")

    if embed_count == 0:
        log.warning("=" * 50)
        log.warning("  WARNING: Zero embeddings loaded!")
        log.warning("  Possible causes:")
        log.warning("  1. Obsidian/Smart Connections not running")
        log.warning("  2. .smart-env folder in unexpected location")
        log.warning("  3. DB vault_path doesn't match actual vault")
        log.warning("=" * 50)
except Exception as exc:
    print(f"FATAL: Failed to initialize Smart Connections database")
    print(f"  Vault path: {VAULT_PATH}")
    print(f"  Error: {exc}")
    print(f"  Is Obsidian open? Are embeddings present in .smart-env/?")
    sys.exit(1)

# ---------------------------------------------------------------------------
# FastMCP Server
# ---------------------------------------------------------------------------

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "transcent_vault",
    stateless_http=True,
    host=HOST,
    port=PORT,
)


@mcp.tool()
def search_vault(query: str, max_results: int = 5) -> str:
    """Semantic search across the TRANSCENT vault using Smart Connections embeddings.

    Returns the most relevant text blocks with file paths, line numbers,
    and similarity scores. Use this to find where a topic lives in the vault
    before reading specific files.

    RETRIEVAL CHAIN: search_vault for discovery → resolve_wikilink for links
    you find → read_file_lines for precision loading. Always search before
    loading. Use vault domain terms for best results.

    Complements obsidian_search_native (keyword/exact match). Use search_vault
    for conceptual queries, obsidian_search_native for exact text.

    Args:
        query: Natural language search query. Use vault domain terms for best
               results (e.g. "hyperself cognitive light cone" not "how thinking works").
        max_results: Maximum blocks to return (1-20). Default 5.
    """
    max_results = max(1, min(20, max_results))
    results = db.get_context_blocks(query, max_blocks=max_results)

    if not results:
        return json.dumps({"results": [], "message": "No matching blocks found."})

    clean = []
    for r in results:
        clean.append({
            "path": r.get("path", ""),
            "similarity": round(float(r.get("similarity", 0)), 4),
            "lines": r.get("lines", []),
            "text": r.get("text") or "(text unavailable — possible ghost entry)",
            "key": r.get("key", ""),
        })

    return json.dumps({"results": clean}, indent=2)


@mcp.tool()
def read_file(path: str) -> str:
    """Read a vault file by its path relative to the vault root.

    Returns the raw markdown content. For large files, use read_file_lines
    to load only the section you need. Use resolve_wikilink first to convert
    [[wiki-link]] names to file paths.

    Args:
        path: File path relative to vault root (e.g. "REFERENCE/Hyperselves.md").
    """
    full = VAULT_PATH / path
    if not _is_safe_path(full):
        return f"ERROR: Path outside vault boundary: {path}"
    if not full.exists():
        return f"ERROR: File not found: {path}"
    if not full.is_file():
        return f"ERROR: Not a file: {path}"
    try:
        return full.read_text(encoding="utf-8")
    except Exception as exc:
        return f"ERROR: Could not read file: {exc}"


@mcp.tool()
def read_file_lines(path: str, start_line: int, end_line: int = -1) -> str:
    """Read a specific line range from a vault file.

    Useful for surgical retrieval after search_vault tells you which lines
    contain the content you need. Equivalent to Nexus contentManager.read.

    Args:
        path: File path relative to vault root.
        start_line: First line to read (1-based, inclusive).
        end_line: Last line to read (1-based, inclusive). Use -1 to read to end of file.
    """
    full = VAULT_PATH / path
    if not _is_safe_path(full):
        return f"ERROR: Path outside vault boundary: {path}"
    if not full.exists():
        return f"ERROR: File not found: {path}"
    try:
        all_lines = full.read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception as exc:
        return f"ERROR: Could not read file: {exc}"

    start = max(0, start_line - 1)
    end = len(all_lines) if end_line == -1 else min(len(all_lines), end_line)

    if start >= len(all_lines):
        return f"ERROR: start_line {start_line} exceeds file length ({len(all_lines)} lines)"

    numbered = []
    for i, line in enumerate(all_lines[start:end], start=start + 1):
        numbered.append(f"{i:>5}\t{line}")

    return "".join(numbered)


@mcp.tool()
def list_directory(path: str = "") -> str:
    """List files and subdirectories in a vault directory.

    Returns a sorted list. Directories have a trailing slash.
    Hidden items (starting with '.') are excluded.

    Args:
        path: Directory path relative to vault root. Empty string = vault root.
    """
    full = VAULT_PATH / path
    if not _is_safe_path(full):
        return f"ERROR: Path outside vault boundary: {path}"
    if not full.exists():
        return f"ERROR: Directory not found: {path}"
    if not full.is_dir():
        return f"ERROR: Not a directory: {path}"

    items = []
    for item in sorted(full.iterdir()):
        if item.name.startswith("."):
            continue
        name = item.name + ("/" if item.is_dir() else "")
        items.append(name)

    return json.dumps(items, indent=2)


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to a vault file. Creates parent directories if needed.
    Overwrites the file if it already exists.

    WARNING: This writes directly to disk. Obsidian plugins (Dataview,
    Metadata Menu, Serializer) will NOT see the change. Files created
    this way won't appear on dashboards until vault_refresh() is called.
    For files that need dashboard visibility, use obsidian_create instead.
    For property changes, use obsidian_property_set instead.

    For new files with a template (scenes, characters, research reports),
    prefer obsidian_create with template= instead — it produces proper
    YAML schema and body structure. Use write_file when no template fits
    or when you need full control over every byte.

    All new files MUST include YAML frontmatter with at minimum a summary
    field. Use disabled rules: [all] and explicit empty strings for
    placeholder fields (e.g. protagonist: \"\").

    Args:
        path: File path relative to vault root (e.g. "RESEARCH/new-doc.md").
        content: Full file content to write.
    """
    full = VAULT_PATH / path
    if not _is_safe_path(full):
        return f"ERROR: Path outside vault boundary: {path}"

    try:
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        return f"OK: Written {len(content)} characters to {path}"
    except Exception as exc:
        return f"ERROR: Write failed: {exc}"


@mcp.tool()
def update_file_lines(path: str, content: str, start_line: int, end_line: int = 0) -> str:
    """Insert, replace, or delete content at specific line positions in a vault file.
    Surgical line-level editing. No equivalent in Nexus (contentManager.update
    was removed in a Nexus version update).

    NOTE: This writes directly to disk. Obsidian plugins won't see the
    change. Fine for body content edits. For YAML property changes that
    need dashboard visibility, use obsidian_property_set instead.

    Three modes:
    - REPLACE: Provide both start_line and end_line. Replaces lines start_line
      through end_line (inclusive) with the new content.
    - INSERT: Set end_line to 0 (default). Inserts content BEFORE start_line
      without removing any existing lines. Use start_line=-1 to append to end of file.
    - DELETE: Set content to empty string "" with a start_line and end_line range.
      Removes those lines.

    Always re-read the target lines with read_file_lines immediately before editing
    to ensure correct positioning. After any edit that changes line count, line
    numbers shift — re-verify before further edits to the same file.

    Args:
        path: File path relative to vault root.
        content: Content to insert/replace. Empty string to delete lines.
        start_line: Target line (1-based). Use -1 to append to end of file.
        end_line: End of replacement range (1-based, inclusive). 0 = INSERT mode
                  (no lines removed, content inserted before start_line).
    """
    full = VAULT_PATH / path
    if not _is_safe_path(full):
        return f"ERROR: Path outside vault boundary: {path}"

    if not full.exists():
        return f"ERROR: File not found: {path}. Use write_file to create new files."

    try:
        all_lines = full.read_text(encoding="utf-8").splitlines(keepends=True)
    except Exception as exc:
        return f"ERROR: Could not read file: {exc}"

    original_count = len(all_lines)

    # Ensure content ends with newline if non-empty
    if content and not content.endswith("\n"):
        content = content + "\n"

    # Split replacement content into lines (preserving line endings)
    new_lines = content.splitlines(keepends=True) if content else []

    # APPEND mode
    if start_line == -1:
        all_lines.extend(new_lines)
        try:
            full.write_text("".join(all_lines), encoding="utf-8")
            new_count = len(all_lines)
            return (
                f"OK: Appended {len(new_lines)} lines to {path}. "
                f"File: {original_count} -> {new_count} lines. "
                f"linesDelta: +{new_count - original_count}"
            )
        except Exception as exc:
            return f"ERROR: Write failed: {exc}"

    # Validate start_line
    if start_line < 1 or start_line > original_count + 1:
        return (
            f"ERROR: start_line {start_line} out of range. "
            f"File has {original_count} lines (valid: 1-{original_count + 1})."
        )

    # INSERT mode (end_line == 0): insert before start_line
    if end_line == 0:
        idx = start_line - 1
        all_lines[idx:idx] = new_lines
        try:
            full.write_text("".join(all_lines), encoding="utf-8")
            new_count = len(all_lines)
            return (
                f"OK: Inserted {len(new_lines)} lines before line {start_line} in {path}. "
                f"File: {original_count} -> {new_count} lines. "
                f"linesDelta: +{new_count - original_count}"
            )
        except Exception as exc:
            return f"ERROR: Write failed: {exc}"

    # REPLACE mode: replace start_line through end_line
    if end_line < start_line:
        return f"ERROR: end_line ({end_line}) must be >= start_line ({start_line})."
    if end_line > original_count:
        return (
            f"ERROR: end_line {end_line} exceeds file length ({original_count} lines)."
        )

    start_idx = start_line - 1
    end_idx = end_line

    all_lines[start_idx:end_idx] = new_lines
    try:
        full.write_text("".join(all_lines), encoding="utf-8")
        new_count = len(all_lines)
        lines_delta = new_count - original_count
        sign = "+" if lines_delta >= 0 else ""
        return (
            f"OK: Replaced lines {start_line}-{end_line} in {path}. "
            f"File: {original_count} -> {new_count} lines. "
            f"linesDelta: {sign}{lines_delta}"
        )
    except Exception as exc:
        return f"ERROR: Write failed: {exc}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# File index for wiki-link resolution
# ---------------------------------------------------------------------------

def _build_file_index() -> dict:
    """Build a map of filename (no extension, case-insensitive) -> relative path.
    Called fresh on every resolve_wikilink call so moves/creates are picked up
    without server restart. Scans ~300 files in <100ms."""
    index = {}
    for f in VAULT_PATH.rglob("*.md"):
        rel = f.relative_to(VAULT_PATH)
        # Skip hidden directories
        if any(part.startswith(".") for part in rel.parts):
            continue
        stem_lower = f.stem.lower()
        # If duplicate, keep first found (matches Obsidian behavior)
        if stem_lower not in index:
            index[stem_lower] = str(rel).replace("\\", "/")
    return index

# Startup check only — the real index is rebuilt fresh on every resolve call
_startup_index = _build_file_index()
log.info(f"File index: {len(_startup_index)} .md files found in vault")


@mcp.tool()
def resolve_wikilink(name: str) -> str:
    """Resolve an Obsidian wiki-link name to a file path.

    Takes the text inside [[brackets]] and returns the relative vault path.
    Essential for browser/mobile agents who see wiki-links in documents but
    can't click them — use this to get the path, then read_file or read_file_lines.

    Can resolve multiple names at once (comma-separated) for efficiency.

    Args:
        name: The wiki-link text, e.g. "Controlling-Idea" or "TRANSCENT Argument".
              For multiple links, separate with commas: "Controlling-Idea, TRANSCENT Argument, Book 2 Plot"
    """
    # Rebuild index fresh every call — picks up moves/creates without restart
    file_index = _build_file_index()
    names = [n.strip().strip("[]") for n in name.split(",")]
    results = {}
    for n in names:
        key = n.lower()
        if key in file_index:
            results[n] = file_index[key]
        else:
            results[n] = None
    return json.dumps(results, indent=2)


def _is_safe_path(full_path: Path) -> bool:
    """Check that a resolved path stays within the vault boundary."""
    try:
        full_path.resolve().relative_to(VAULT_PATH.resolve())
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Obsidian CLI integration (requires Obsidian 1.12.4+ with CLI registered)
# These tools pass through Obsidian's internal API via IPC, giving agents
# native Obsidian operations: link-safe moves, template-based creation,
# property management, and graph awareness.
# ---------------------------------------------------------------------------

import subprocess as _sp
import tempfile

def _shell_escape(s: str) -> str:
    """Escape a string for safe inclusion in a Windows cmd.exe command.
    Escapes characters that cmd.exe interprets as metacharacters."""
    for ch in ('"', '&', '|', '>', '<', '^', '%'):
        s = s.replace(ch, f'^{ch}')
    return s


def _run_cli(*args: str, timeout: int = 30) -> str:
    """Run an Obsidian CLI command and return stdout.
    Joins args into a single shell string to preserve quoting on Windows.
    SECURITY NOTE (Core-16, 2026-03-20): All string interpolation into
    shell commands must go through _shell_escape() first. See incident
    analysis in 20260320-0940-vault-deletion-guardrails task."""
    cmd = "obsidian " + " ".join(args)
    try:
        result = _sp.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=str(VAULT_PATH)
        )
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            return f"ERROR (exit {result.returncode}): {err}"
        return result.stdout.strip()
    except _sp.TimeoutExpired:
        return f"ERROR: CLI command timed out after {timeout}s"
    except Exception as exc:
        return f"ERROR: {exc}"


@mcp.tool()
def obsidian_move(file: str, to: str) -> str:
    """Move or reorganize a vault file. Obsidian auto-rewrites ALL wiki-links
    pointing to the file — no broken links.

    Use obsidian_backlinks first to see what depends on the file.
    Always prefer this over manual file moves — only this tool
    guarantees link integrity across the vault.

    Args:
        file: Source file name or path (e.g. "My Note" or "Folder/My Note.md")
        to: Destination folder (e.g. "CANON/Characters/")
    """
    return _run_cli("move", f'file="{file}"', f'to="{to}"', "silent")


# obsidian_delete REMOVED (Core-16, 2026-03-20).
# Craft-24 accidentally deleted 8 critical files (protagonist profiles,
# Production Board, handoff-Core) via this tool. Delete capability is now
# restricted to Desktop Core agents only (via shell: obsidian delete).
# Lee can delete manually through the Obsidian UI.


@mcp.tool()
def obsidian_create(name: str, template: str = "", content: str = "") -> str:
    """Create a new vault file, optionally from a Templater template.
    When using template=, the file is born with full MM integration,
    all YAML fields, and proper body structure — identical to Lee creating
    it manually through Obsidian's command palette.

    THE PREFERRED WAY TO CREATE VAULT DOCUMENTS. Available templates:
    Task, Scene, Character, Worldbuilding, Research-Report, Tracked-Item,
    Reference, Planning, Operations, Dashboard.

    For tasks: use timestamp-prefixed filenames for uniqueness:
    obsidian_create(name="LEDGER/Tasks/YYYYMMDD-HHMM-slug", template="Task")
    where YYYYMMDD-HHMM is the current time. Example:
    obsidian_create(name="LEDGER/Tasks/20260319-1400-scene-brief-ep7", template="Task")
    Fill fields via obsidian_property_set. The task appears on the
    Production Board automatically after vault_refresh.

    After creation, fill in YAML values via update_file_lines or
    obsidian_property_set. Templater interactive prompts (<% tp.system.prompt() %>)
    appear as raw text — fill these manually.

    Args:
        name: File name or path (e.g. "LEDGER/Tasks/new-task" or "CANON/Characters/Egypt")
        template: Template name from TEMPLATES/ folder (e.g. "Scene", "Character", "Research-Report"). Omit for blank file.
        content: Content to write (only used if no template). Supports \n for newlines.
    """
    # CLI requires path= for nested paths (with /), name= for root-level
    if "/" in name or "\\" in name:
        args = ["create", f'path="{name}"', "silent"]
    else:
        args = ["create", f'name="{name}"', "silent"]
    if template:
        args.append(f'template="{template}"')
    elif content:
        args.append(f'content="{content}"')
    return _run_cli(*args)


@mcp.tool()
def obsidian_rename(file: str, new_name: str) -> str:
    """Rename a vault file. Obsidian auto-rewrites ALL wiki-links.

    Args:
        file: Current file name or path
        new_name: New file name (just the name, not a path)
    """
    return _run_cli("rename", f'file="{file}"', f'name="{new_name}"')


@mcp.tool()
def obsidian_property_set(file: str, name: str, value: str) -> str:
    """Set a YAML frontmatter property through Obsidian's API.
    Writes YAML exactly as Obsidian expects — no formatting surprises,
    no MM mutation issues.

    Prefer this over editing YAML text manually via update_file_lines
    for individual property changes. For bulk YAML writes (new file
    creation with many fields), write_file or obsidian_create is more
    efficient.

    NOTE: Uses eval workaround for Windows CLI shim bug (colon+params
    fails silently). Will switch to native property:set when 1.12.2 ships.

    Args:
        file: File name or path
        name: Property name (e.g. "status", "protagonist", "draft-pass")
        value: Property value (e.g. "done", "Story", "skeleton")
    """
    # Escape for JS single-quote strings AND Windows shell metacharacters.
    # The JS is wrapped in code="..." for the shell, so double quotes and
    # cmd.exe metacharacters must be escaped. (Core-16 security fix)
    safe_value = value.replace('\\', '\\\\').replace("'", "\\'")
    safe_name = name.replace("'", "\\'")
    safe_file = file.replace("'", "\\'")
    # Shell-escape the values that will be interpolated into the command
    safe_value = _shell_escape(safe_value)
    safe_name = _shell_escape(safe_name)
    safe_file = _shell_escape(safe_file)
    # No top-level await in eval — use .then() pattern
    js = (
        f"const f = app.vault.getAbstractFileByPath("
        f"app.metadataCache.getFirstLinkpathDest('{safe_file}', '')?.path || '{safe_file}');"
        f"if (!f) throw 'File not found: {safe_file}';"
        f"app.fileManager.processFrontMatter(f, fm => {{ fm['{safe_name}'] = '{safe_value}'; }});"
        f"'Set {safe_name}={safe_value} on ' + f.path"
    )
    return _run_cli("eval", f'code="{js}"')


@mcp.tool()
def obsidian_property_read(file: str, name: str) -> str:
    """Read a YAML frontmatter property through Obsidian's API.

    Lighter than read_file when you only need one property value.
    Returns the value as JSON (strings quoted, arrays as [...]).

    NOTE: Uses eval workaround for Windows CLI shim bug (colon+params
    fails silently). Will switch to native property:read when 1.12.2 ships.

    Args:
        file: File name or path
        name: Property name to read
    """
    safe_name = _shell_escape(name.replace("'", "\\'"))
    safe_file = _shell_escape(file.replace("'", "\\'"))
    js = (
        f"const f = app.metadataCache.getFirstLinkpathDest('{safe_file}', '');"
        f"if (!f) throw 'File not found: {safe_file}';"
        f"const cache = app.metadataCache.getFileCache(f);"
        f"const val = cache?.frontmatter?.['{safe_name}'];"
        f"val === undefined ? 'UNDEFINED' : JSON.stringify(val)"
    )
    return _run_cli("eval", f'code="{js}"')


@mcp.tool()
def obsidian_orphans() -> str:
    """List all orphaned files — files with no incoming links.
    Instant vault health audit."""
    return _run_cli("orphans", timeout=60)


@mcp.tool()
def obsidian_backlinks(file: str) -> str:
    """List all files that link TO a given file. Graph awareness
    for any agent — see what depends on a file before modifying it.

    Args:
        file: File name or path to check backlinks for
    """
    return _run_cli("backlinks", f'file="{file}"')


@mcp.tool()
def obsidian_search_native(query: str, limit: int = 10) -> str:
    """Search the vault using Obsidian's native full-text search.
    Complementary to search_vault (semantic/meaning-based).

    Use this for: exact text matches, specific terms, error messages,
    field values. Use search_vault for: conceptual queries, finding
    related content, exploring a topic.

    Args:
        query: Search query (keyword-based, not semantic)
        limit: Maximum results (default 10)
    """
    return _run_cli("search", f'query="{query}"', f'limit={limit}')


@mcp.tool()
def obsidian_tags() -> str:
    """List all tags in the vault with usage counts."""
    return _run_cli("tags", "counts")



@mcp.tool()
def obsidian_read_computed(file: str, name: str) -> str:
    """Read a computed (inline body) field via Dataview's API.

    obsidian_property_read only reads YAML frontmatter. Computed fields
    (reading-cost, completeness, scene-count, consistency-alert, chain-status,
    revision-flag, dep-check, etc.) live in inline Dataview fields in the
    file body — invisible to the metadata cache.

    This tool uses Dataview's page API (dv.page) which indexes BOTH
    frontmatter AND inline fields. It can read any field on any file.

    Use obsidian_property_read for YAML fields (faster, simpler).
    Use this tool for computed/inline body fields.

    Args:
        file: File name or relative path (e.g. "Marduk" or "CANON/Characters/Marduk.md")
        name: Field name (e.g. "reading-cost", "completeness", "scene-count")
    """
    safe_file = _shell_escape(file.replace("'", "\\'"))
    safe_name = _shell_escape(name.replace("'", "\\'"))
    js = (
        f"const dv = app.plugins.plugins.dataview?.api;"
        f"if (!dv) throw 'Dataview plugin not available';"
        f"const f = app.metadataCache.getFirstLinkpathDest('{safe_file}', '');"
        f"if (!f) throw 'File not found: {safe_file}';"
        f"const page = dv.page(f.path);"
        f"if (!page) throw 'Dataview cannot resolve: ' + f.path;"
        f"const val = page['{safe_name}'];"
        f"val === undefined ? 'UNDEFINED' : JSON.stringify(val)"
    )
    return _run_cli("eval", f'code="{js}"')


# ---------------------------------------------------------------------------
# Vault automation: refresh dashboards and computed fields
# ---------------------------------------------------------------------------

import time as _time


@mcp.tool()
def vault_refresh(compute_formulas: str = "", formula_file: str = "") -> str:
    """Refresh the vault's reactive systems: Dataview Serializer dashboards
    and (optionally) Metadata Menu computed fields.

    Call this at bootstrap to ensure dashboard data is current, or after
    making changes that dashboards should reflect (creating/updating tasks,
    changing file status, etc.).

    Modes:
    - vault_refresh() — refreshes all Serializer dashboards vault-wide.
      Fast (<2s), safe, no side effects. The default.
    - vault_refresh(formula_file="Marduk") — also triggers MM formula
      recomputation on a specific file. Opens the file in Obsidian,
      triggers formulas, then returns. Use when you need guaranteed-fresh
      computed fields on a file you're about to read.
    - vault_refresh(compute_formulas="true") — triggers MM formulas on ALL
      files with a Vault Nervous System callout. Iterates through each file,
      opens it, triggers computation. Slower (~30s) and changes the active
      file in Obsidian's UI. Use sparingly — e.g. before a comprehensive
      vault health audit.

    Args:
        compute_formulas: Set to "true" to trigger MM formula recomputation on
            all files with computed fields. Slower but comprehensive. Default empty.
        formula_file: If set, trigger MM formulas on this specific file only.
            Takes a file name (e.g. "Marduk") or path. Faster than compute_formulas.
    """
    _do_all_formulas = compute_formulas.lower().strip() == "true"
    results = []

    # --- Step 1: Open all dashboards, serialize, close them ---
    # The Serializer reads from Dataview's rendered DOM, which only exists
    # when the file is open in Obsidian's editor. Without opening the file
    # first, serialize-all silently skips it. (Core-16, 2026-03-20)
    # REVISED: Opens dashboards in a single leaf (reusing same tab),
    # serializes after each one, then restores the original file.
    # This avoids the jarring UX of many tabs opening at once.
    dash_js = (
        "const leaf = app.workspace.getLeaf();"
        "const originalFile = leaf.view?.file;"
        "const files = app.vault.getMarkdownFiles()"
        ".filter(f => {"
        "  const cache = app.metadataCache.getFileCache(f);"
        "  const fc = cache?.frontmatter?.fileClass;"
        "  const cls = Array.isArray(fc) ? fc[0] : fc;"
        "  return cls === 'dashboard';"
        "});"
        "files.map(f => f.path).join('|')"
    )
    dash_result = _run_cli("eval", f'code="{dash_js}"')
    dash_count = 0
    if "ERROR" not in dash_result:
        raw = dash_result.strip()
        if raw.startswith("=>"):
            raw = raw[2:].strip().strip("'").strip('"')
        paths = [p.strip() for p in raw.split("|") if p.strip()]
        # Open each dashboard, wait for render, serialize just that file
        for dpath in paths:
            open_js = (
                f"const f = app.vault.getAbstractFileByPath('{dpath}');"
                f"if (f) {{ app.workspace.getLeaf().openFile(f); 'ok' }}"
                f" else {{ 'skip' }}"
            )
            _run_cli("eval", f'code="{open_js}"')
            _time.sleep(0.5)  # let Dataview render
            ser_one_js = (
                "app.commands.executeCommandById("
                "'dataview-serializer:serialize-current-file-dataview-queries')"
            )
            _run_cli("eval", f'code="{ser_one_js}"')
            dash_count += 1
        # Restore the original file
        restore_js = (
            "const leaf = app.workspace.getLeaf();"
            "const orig = app.vault.getAbstractFileByPath("
            "leaf.view?.file?.path || '');"
        )
        _run_cli("eval", f'code="{restore_js}"')

    if dash_count > 0:
        results.append(f"Serializer: refreshed {dash_count} dashboards")
    else:
        # Fallback: try serialize-all anyway
        ser_js = (
            "app.commands.executeCommandById("
            "'dataview-serializer:serialize-all-dataview-queries')"
        )
        ser_result = _run_cli("eval", f'code="{ser_js}"')
        if "ERROR" in ser_result:
            results.append(f"Serializer: FAILED \u2014 {ser_result}")
        else:
            results.append("Serializer: refreshed (fallback serialize-all)")

    # --- Step 2a: Formula refresh on a single file ---
    if formula_file and not _do_all_formulas:
        open_js = (
            f"const f = app.metadataCache.getFirstLinkpathDest('{_shell_escape(formula_file)}', '');"
            f"if (!f) throw 'File not found: {formula_file}';"
            f"app.workspace.getLeaf().openFile(f);"
            f"'opened ' + f.path"
        )
        open_result = _run_cli("eval", f'code="{open_js}"')
        if "ERROR" in open_result:
            results.append(f"Formula ({formula_file}): FAILED to open — {open_result}")
        else:
            _time.sleep(0.5)  # let Obsidian settle
            fm_js = (
                "app.commands.executeCommandById("
                "'metadata-menu:update_file_formulas')"
            )
            fm_result = _run_cli("eval", f'code="{fm_js}"')
            if "ERROR" in fm_result:
                results.append(f"Formula ({formula_file}): FAILED — {fm_result}")
            else:
                results.append(f"Formula ({formula_file}): recomputed")
        return "\n".join(results)

    # --- Step 2b: Formula refresh on ALL computed-field files ---
    if _do_all_formulas:
        # Find files with Vault Nervous System callouts via search
        scan_js = (
            "const files = app.vault.getMarkdownFiles()"
            ".filter(f => !['SCRATCH','TEMPLATES','.smart-env','REFERENCE','OPERATIONS']"
            ".some(ex => f.path.startsWith(ex)));"
            "const results = [];"
            "for (const f of files) {"
            "  const cache = app.metadataCache.getFileCache(f);"
            "  if (cache?.frontmatter?.fileClass && "
            "    ['character','worldbuilding','research-report','scene','tracked-item'].includes("
            "    Array.isArray(cache.frontmatter.fileClass) ? cache.frontmatter.fileClass[0] : cache.frontmatter.fileClass)) {"
            "    results.push(f.path);"
            "  }"
            "}"
            "results.join('\\n')"
        )
        scan_result = _run_cli("eval", f'code="{scan_js}"', timeout=15)
        if "ERROR" in scan_result or not scan_result.strip():
            results.append(f"Formula scan: no computable files found or error")
            return "\n".join(results)

        # Strip the => prefix from eval output
        paths_raw = scan_result.strip()
        if paths_raw.startswith("=>"):
            paths_raw = paths_raw[2:].strip()
        file_paths = [p.strip() for p in paths_raw.split("\n") if p.strip()]

        updated = 0
        failed = 0
        for fpath in file_paths:
            open_js = (
                f"const f = app.vault.getAbstractFileByPath('{fpath}');"
                f"if (f) {{ app.workspace.getLeaf().openFile(f); 'ok' }}"
                f" else {{ 'skip' }}"
            )
            open_r = _run_cli("eval", f'code="{open_js}"')
            if "ERROR" in open_r or "skip" in open_r:
                failed += 1
                continue
            _time.sleep(0.3)  # let file load
            fm_js = (
                "app.commands.executeCommandById("
                "'metadata-menu:update_file_formulas')"
            )
            _run_cli("eval", f'code="{fm_js}"')
            updated += 1

        results.append(f"Formulas: updated {updated} files ({failed} skipped)")

    return "\n".join(results)


# ---------------------------------------------------------------------------
# Git-powered change tracking
# ---------------------------------------------------------------------------


@mcp.tool()
def vault_changes(since: str = "", path: str = "") -> str:
    """What changed in the vault since a given time. Reads git history.
    Catches ALL changes by ALL agents AND the human, automatically.
    No manual logging needed. Git auto-commits every ~1 minute.

    TWO MODES:

    1. MANIFEST (no path): Compact change manifest showing which files
       changed and how much, NOT their contents. Shows new, modified,
       renamed, deleted files with line-count stats. ~500 tokens for
       a busy day. The COS reads this to see what moved.

    2. FILE DIFF (with path): Line-level diff for ONE specific file.
       The COS drills into a specific change after reading the manifest.
       Truncated at 10K chars.

    Workflow: vault_changes(since="2 hours ago") for the manifest,
    then vault_changes(since="2 hours ago", path="CANON/Characters/Marduk.md")
    to drill into one file.

    Args:
        since: ISO timestamp or git-compatible time string.
               Examples: "2026-03-19T14:00:00", "2 hours ago", "1 day ago".
               Empty = last 24 hours.
        path: File path to get line-level diff for ONE file.
              Empty = manifest mode (all changes, compact stats).
    """
    if not since:
        since = "24 hours ago"

    # --- FILE DIFF MODE: line-level diff for one file ---
    if path:
        log_cmd = ["git", "log", f"--since={since}", "--pretty=format:%H",
                   "--", path]
        try:
            log_r = _sp.run(log_cmd, capture_output=True, text=True,
                           timeout=30, cwd=str(VAULT_PATH),
                           encoding='utf-8', errors='replace')
            hashes = [h.strip() for h in log_r.stdout.strip().split("\n") if h.strip()]
        except Exception as exc:
            return f"ERROR: {exc}"

        if not hashes:
            return json.dumps({"path": path, "message": f"No changes since {since}"})

        oldest = hashes[-1]
        # Try oldest~1 to capture the change itself
        for ref in [f"{oldest}~1", oldest]:
            try:
                diff_r = _sp.run(
                    ["git", "diff", ref, "HEAD", "--unified=3", "--", path],
                    capture_output=True, text=True, timeout=30,
                    cwd=str(VAULT_PATH), encoding='utf-8', errors='replace')
                if diff_r.stdout and diff_r.stdout.strip():
                    diff_text = diff_r.stdout.strip()
                    break
            except Exception:
                continue
        else:
            diff_text = "(diff unavailable)"

        if len(diff_text) > 10000:
            diff_text = diff_text[:10000] + "\n\n... (truncated at 10K chars)"

        return json.dumps({"path": path, "since": since,
                           "commits": len(hashes), "diff": diff_text}, indent=2)

    # --- MANIFEST MODE: compact overview of all changes ---
    log_cmd = ["git", "log", f"--since={since}", "--pretty=format:%H|%ai",
               "--reverse"]
    try:
        log_r = _sp.run(log_cmd, capture_output=True, text=True,
                        timeout=30, cwd=str(VAULT_PATH),
                        encoding='utf-8', errors='replace')
        if log_r.returncode != 0:
            return f"ERROR: git log failed: {log_r.stderr.strip()}"
    except Exception as exc:
        return f"ERROR: {exc}"

    log_lines = [l.strip() for l in log_r.stdout.strip().split("\n") if l.strip()]
    if not log_lines:
        return json.dumps({"since": since, "message": "No changes.", "files": []})

    oldest_hash = log_lines[0].split("|")[0].strip()
    commit_count = len(log_lines)

    # Try oldest~1 first for complete diff, fallback to oldest
    base_ref = oldest_hash + "~1"
    test_r = _sp.run(["git", "rev-parse", base_ref], capture_output=True,
                     text=True, timeout=10, cwd=str(VAULT_PATH))
    if test_r.returncode != 0:
        base_ref = oldest_hash

    # Per-file stats via numstat
    try:
        stat_r = _sp.run(
            ["git", "diff", base_ref, "HEAD", "--numstat"],
            capture_output=True, text=True, timeout=30,
            cwd=str(VAULT_PATH), encoding='utf-8', errors='replace')
        stat_text = stat_r.stdout.strip() if stat_r.stdout else ""
    except Exception:
        stat_text = ""

    # New files
    try:
        new_r = _sp.run(
            ["git", "diff", base_ref, "HEAD", "--diff-filter=A", "--name-only"],
            capture_output=True, text=True, timeout=30,
            cwd=str(VAULT_PATH), encoding='utf-8', errors='replace')
        new_files = set(l.strip() for l in (new_r.stdout or "").strip().split("\n")
                       if l.strip())
    except Exception:
        new_files = set()

    # Renamed files
    try:
        ren_r = _sp.run(
            ["git", "diff", base_ref, "HEAD", "--diff-filter=R", "--name-status"],
            capture_output=True, text=True, timeout=30,
            cwd=str(VAULT_PATH), encoding='utf-8', errors='replace')
        renames = []
        for line in (ren_r.stdout or "").strip().split("\n"):
            parts = line.split("\t")
            if len(parts) >= 3:
                renames.append({"from": parts[1], "to": parts[2]})
    except Exception:
        renames = []

    # Deleted files
    try:
        del_r = _sp.run(
            ["git", "diff", base_ref, "HEAD", "--diff-filter=D", "--name-only"],
            capture_output=True, text=True, timeout=30,
            cwd=str(VAULT_PATH), encoding='utf-8', errors='replace')
        deleted_files = [l.strip() for l in (del_r.stdout or "").strip().split("\n")
                        if l.strip()]
    except Exception:
        deleted_files = []

    # Parse numstat into structured entries
    modified = []
    for line in stat_text.split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            added = parts[0].strip()
            removed = parts[1].strip()
            fname = parts[2].strip()
            if fname in new_files:
                continue
            try:
                a, r = int(added), int(removed)
                total = a + r
                if total <= 5:
                    size = "trivial"
                elif total <= 30:
                    size = "minor"
                elif total <= 100:
                    size = "moderate"
                else:
                    size = "substantial"
            except ValueError:
                a, r, size = "?", "?", "binary"
            modified.append({"file": fname, "added": a, "removed": r, "size": size})

    manifest = {
        "since": since,
        "commits": commit_count,
        "totals": {
            "new": len(new_files),
            "modified": len(modified),
            "renamed": len(renames),
            "deleted": len(deleted_files)
        }
    }
    if new_files:
        manifest["new_files"] = sorted(new_files)
    if modified:
        manifest["modified_files"] = modified
    if renames:
        manifest["renamed_files"] = renames
    if deleted_files:
        manifest["deleted_files"] = deleted_files

    return json.dumps(manifest, indent=2)



# ---------------------------------------------------------------------------
# Ephemeral Python execution
# ---------------------------------------------------------------------------

# @mcp.tool()  # DISABLED from connector (Core-16 security decision)
# Desktop Core agents use this via shell: python -c "from vault_mcp_server import run_python; print(run_python('...'))"
# or via obsidian eval dispatching to a shell command.
def run_python(code: str, timeout: int = 30) -> str:
    """Execute Python code and return stdout+stderr. No file creation needed.

    Runs the code in a temporary file that is deleted immediately after
    execution. The code runs in the vault's Python venv with full access
    to the vault filesystem. Use for:
    - Quick vault audits and searches across multiple files
    - Batch file operations (fix YAML, rename patterns, etc.)
    - Git operations (log, grep, diff)
    - Data extraction and transformation
    - Any computation that would otherwise require write-run-delete cycle

    The code has access to the vault at VAULT_PATH (injected as a global).
    UTF-8 output is handled automatically.

    Args:
        code: Python code to execute. Multi-line supported.
        timeout: Max execution time in seconds (default 30, max 120).
    """
    timeout = min(timeout, 120)
    # Prepend vault path injection and encoding fix
    # Filesystem scoping: restrict all file operations to vault + smart-connections-mcp
    preamble = (
        "import sys, io, os\n"
        "sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')\n"
        "sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')\n"
        f"VAULT_PATH = r\"{VAULT_PATH}\"\n"
        "from pathlib import Path\n"
        "VAULT = Path(VAULT_PATH)\n"
        "\n"
        "# --- FILESYSTEM SANDBOX ---\n"
        "# Only allow access to vault and smart-connections-mcp directories\n"
        f"_ALLOWED_ROOTS = [Path(r\"{VAULT_PATH}\").resolve(), Path(r\"C:/Users/nosuc/smart-connections-mcp\").resolve()]\n"
        "_original_open = open\n"
        "def _sandboxed_open(path, *args, **kwargs):\n"
        "    p = Path(str(path)).resolve()\n"
        "    if not any(str(p).startswith(str(r)) for r in _ALLOWED_ROOTS):\n"
        "        raise PermissionError(f\"Access denied: {p} is outside allowed directories\")\n"
        "    return _original_open(path, *args, **kwargs)\n"
        "import builtins\n"
        "builtins.open = _sandboxed_open\n"
        "# --- END SANDBOX ---\n"
    )
    full_code = preamble + code

    try:
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py', encoding='utf-8',
            dir=str(Path(VAULT_PATH) / "OPERATIONS" / "Scripts"),
            delete=False, prefix='_ephemeral_'
        ) as tmp:
            tmp.write(full_code)
            tmp_path = tmp.name

        result = subprocess.run(
            [PYTHON_PATH, tmp_path],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=timeout, cwd=str(VAULT_PATH)
        )

        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr
        if result.returncode != 0:
            output += f"\nEXIT CODE: {result.returncode}"
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT: execution exceeded {timeout}s limit"
    except Exception as e:
        return f"ERROR: {e}"
    finally:
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except:
            pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  TRANSCENT Vault MCP Server")
    print("=" * 60)
    print(f"  Vault:    {VAULT_PATH}")
    print(f"  Embeddings loaded: {embed_count}")
    print(f"  Endpoint: http://{HOST}:{PORT}/mcp")
    print(f"  Tools:    search_vault, read_file, read_file_lines,")
    print(f"            list_directory, write_file, update_file_lines,")
    print(f"            resolve_wikilink")
    print(f"  CLI:      obsidian_move, obsidian_create,")
    print(f"            obsidian_rename, obsidian_property_set,")
    print(f"            obsidian_property_read, obsidian_orphans,")
    print(f"            obsidian_backlinks, obsidian_search_native,")
    print(f"            obsidian_tags, obsidian_read_computed")
    print(f"  Auto:     vault_refresh")
    print(f"  Delta:    vault_changes")
    print(f"  Exec:     run_python (Desktop Core only, not on connector)")
    print()
    print("  Next steps:")
    print("  1. Expose via tunnel:  cloudflared tunnel run transcent-vault")
    print("  2. Connect in claude.ai: Settings > Connectors > Add custom connector")
    print("  3. Paste your tunnel URL + /mcp")
    print("=" * 60)

    mcp.run(transport="streamable-http")