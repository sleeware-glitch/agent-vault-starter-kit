---
summary: |
  Complete reference of Obsidian commands accessible to agents via obsidian eval. Organized by use case. Load this document when you need to do something the standard MCP tools don't cover. Every command is invocable with: obsidian eval code="app.commands.executeCommandById('command-id')"
scope: all
status: active
document-role: operations
fileClass: tracked-item
disabled rules:
  - all
---

# Obsidian Commands Reference for Agents

> **When to load this document:** When you need to do something the 19 standard MCP tools don't cover. **Desktop agents only** — these commands require shell access to `obsidian eval`, which is not available through the browser/mobile MCP connector. Most creative and research work never needs this — the standard tools handle reading, writing, searching, creating, moving, and property management. This document is for edge cases and power operations.
>
> **How to invoke any command (Desktop shell only):** All commands work via `obsidian eval`:
> ```
> obsidian eval code="app.commands.executeCommandById('command-id')"
> ```
> Also available as: `obsidian command execute id=command-id`

---

## Vault Maintenance

Commands Core agents use for vault health and upkeep.

| Command ID | What it does | When to use |
|---|---|---|
| `dataview-serializer:serialize-all-dataview-queries` | Serialize all Dataview queries across open files | Dashboard refresh (used internally by `vault_refresh`) |
| `dataview-serializer:serialize-current-file-dataview-queries` | Serialize queries in the currently open file only | Targeted refresh of a single dashboard |
| `dataview:dataview-drop-cache` | Clear Dataview's entire cache | When queries return stale results after major edits |
| `dataview:dataview-force-refresh-views` | Force all Dataview views to re-render | Lighter than dropping cache — try this first |
| `metadata-menu:update_all_lookups` | Recompute all MM lookup fields vault-wide | After bulk file moves or renames |
| `metadata-menu:update_file_formulas` | Recompute MM formulas on the active file | After editing a file that has computed fields |
| `metadata-menu:update_file_lookups` | Recompute MM lookups on the active file | After changing a field that other files look up |
| `metadata-menu:insert_missing_fields` | Add all fileClass fields that the file is missing | Useful after creating a file without a template |
| `obsidian-linter:lint-file` | Run Linter on the active file | After batch edits to clean up formatting |
| `obsidian-linter:lint-all-files` | Run Linter across the entire vault | Major cleanup — use sparingly, slow |
| `novel-word-count:recount-vault` | Recalculate all word counts | After bulk imports or migrations |
| `smart-connections:smart-connections-random` | Jump to a random note | Serendipitous discovery during exploration |

---

## File Operations

Structural operations on files and content — splitting, merging, extracting.

| Command ID | What it does | When to use |
|---|---|---|
| `note-composer:extract-heading` | Extract a heading and its content into a new file | Breaking a monolithic document into SSOT-compliant pieces |
| `note-composer:merge-file` | Merge another file into the current one | Consolidating duplicates |
| `note-composer:split-file` | Split a file at headings into separate files | Breaking up long documents — powerful for manuscript work |
| `file-explorer:duplicate-file` | Create a copy of the current file | Use cautiously — violates Live Document Principle unless temporary |
| `file-explorer:move-file` | Move file via Obsidian's UI dialog | Prefer `obsidian_move` MCP tool instead (link-safe, no UI) |

---

## Git Operations

Version control from within Obsidian. The Git plugin auto-commits, but manual operations are available.

| Command ID | What it does | When to use |
|---|---|---|
| `obsidian-git:commit` | Commit all changes | Before major operations as a save point |
| `obsidian-git:push` | Push to GitHub | After completing a session's work |
| `obsidian-git:pull` | Pull from GitHub | Start of session if another device may have pushed |
| `obsidian-git:list-changed-files` | Show what's changed since last commit | Quick diff awareness |
| `obsidian-git:discard-all` | Discard all uncommitted changes | Emergency rollback — destructive, use with extreme caution |
| `obsidian-git:stage-current-file` | Stage just the active file | Selective commits |
| `obsidian-git:commit-staged` | Commit only staged files | Selective commits |
| `obsidian-git:open-diff-view` | Visual diff of changes | Review before committing |

**Note:** Most git operations are better done via shell (`git log`, `git diff`, `git show`) for programmatic use. These commands are for manual/interactive git workflows.

---

## Longform Plugin (Manuscript)

Commands for the Longform writing plugin. Will become critical when MANUSCRIPT/ is set up.

| Command ID | What it does | When to use |
|---|---|---|
| `longform:longform-compile-current` | Compile the current project's draft into a single document | Manuscript compilation for review or export |
| `longform:longform-compile-selection` | Compile selected scenes only | Partial compilation (act, chapter) |
| `longform:longform-insert-single-scene` | Add a new scene to the project | Creating scenes within the Longform structure |
| `longform:longform-insert-multi-scene` | Add multiple scenes at once | Batch scene creation |
| `longform:longform-indent-scene` | Nest a scene under the one above it | Building chapter/act hierarchy |
| `longform:longform-unindent-scene` | Un-nest a scene | Restructuring |
| `longform:longform-next-scene` | Navigate to the next scene in order | Sequential scene work |
| `longform:longform-previous-scene` | Navigate to the previous scene | Sequential scene work |
| `longform:longform-show-view` | Open the Longform sidebar | Project overview |
| `longform:longform-start-new-session` | Begin a writing session with word count tracking | Session tracking for productivity |

---

## Chronos Timeline

Commands for timeline visualization.

| Command ID | What it does | When to use |
|---|---|---|
| `chronos:insert-timeline-basic` | Insert a basic timeline codeblock | Adding a timeline to a planning document |
| `chronos:insert-timeline-advanced` | Insert a full-featured timeline codeblock | Detailed timeline with swim lanes |
| `chronos:generate-timeline-folder` | Auto-generate a timeline from files in a folder | Visualizing a folder's temporal structure |

---

## Metadata and Properties

Commands for working with file metadata beyond `obsidian_property_set/read`.

| Command ID | What it does | When to use |
|---|---|---|
| `markdown:add-metadata-property` | Add a new property to the active file | Adding fields that aren't in the fileClass |
| `markdown:clear-metadata-properties` | Remove ALL properties from active file | Nuclear option — rarely appropriate |
| `markdown:add-alias` | Add an alias to the active file | Making files findable under alternative names |
| `metadata-menu:add_fileclass_to_file` | Assign a fileClass to a file that doesn't have one | Retroactively classifying untyped files |
| `metadata-menu:open_fields_modal` | Show all fields and their values for the active file | Inspecting computed and authored fields together |
| `conditional-properties:run-current-file` | Run conditional property rules on active file | Trigger auto-property logic |
| `conditional-properties:run-now` | Run conditional property rules vault-wide | Trigger all auto-property logic |

---

## Export

Commands for exporting vault content to other formats. Requires Pandoc installed on the system.

| Command ID | What it does | When to use |
|---|---|---|
| `obsidian-pandoc:pandoc-export-pdf` | Export active file to PDF | Creating shareable documents |
| `obsidian-pandoc:pandoc-export-docx` | Export active file to Word | Manuscript submission format |
| `obsidian-pandoc:pandoc-export-html` | Export active file to HTML | Web-ready version |
| `obsidian-pandoc:pandoc-export-epub` | Export active file to EPUB | E-reader format |
| `workspace:export-pdf` | Obsidian's native PDF export | Simpler than Pandoc, less control |

---

## Search and Navigation

Commands for finding content. Most agents should use `search_vault` and `obsidian_search_native` MCP tools instead, but these offer additional search modes.

| Command ID | What it does | When to use |
|---|---|---|
| `find-n-replace:open` | Open vault-wide Find and Replace | Bulk text replacement across files |
| `find-n-replace:replace-all-vault` | Execute replacement across entire vault | After opening Find and Replace with a query |
| `global-search:open` | Open the search pane | Interactive search (UI-oriented) |
| `graph:open` | Open the full vault graph | Visual exploration of link structure |
| `graph:open-local` | Open local graph for the active file | See immediate connections |
| `outgoing-links:open-for-current` | Show all outgoing links from active file | Audit a file's dependencies |
| `backlink:open-backlinks` | Show all backlinks to active file | Same as `obsidian_backlinks` but in a pane |

---

## Plugin Management (Core Only)

Commands for managing Obsidian plugins. Core agents only — creative agents should never touch plugin state.

| Command ID | What it does | When to use |
|---|---|---|
| `obsidian42-brat:checkForUpdatesAndUpdate` | Check for and install beta plugin updates | Keeping beta plugins current |
| `obsidian42-brat:restartPlugin` | Restart a specific plugin | After config changes that need a reload |
| `obsidian42-brat:enablePlugin` | Enable a disabled plugin | Plugin management |
| `obsidian42-brat:disablePlugin` | Disable a plugin | Troubleshooting conflicts |

---

## Commands NOT Useful for Agents

These exist in the command palette but are UI-interactive, editor-cursor-dependent, or otherwise unsuitable for programmatic use. Don't waste time trying them:

**Editing Toolbar** (`editing-toolbar:*`) — All ~50 commands require an active editor cursor and are formatting tools (bold, italic, headers). Agents edit text via `update_file_lines` and `write_file`, not cursor operations.

**Editor Commands** (`editor:*`) — Cursor-dependent. `editor:toggle-bold`, `editor:insert-table`, etc. require a cursor position that agents can't control meaningfully via eval.

**Workspace/Window** (`workspace:*`, `window:*`) — Tab and window management. Agents don't benefit from rearranging Obsidian's UI.

**Bookmarks** (`bookmarks:*`) — Personal navigation aids. No value for agents.

**Canvas** (`canvas:*`) — TRANSCENT doesn't use canvas files.

**Theme** (`theme:*`) — Visual preferences. Irrelevant to agents.

---

## The Generic Execution Pattern

For any command in this document:

```javascript
// Via obsidian eval (all platforms)
obsidian eval code="app.commands.executeCommandById('command-id')"

// To open a specific file first, then run a command on it:
obsidian eval code="const f = app.vault.getAbstractFileByPath('path/to/file.md'); app.workspace.getLeaf().openFile(f).then(() => { setTimeout(() => app.commands.executeCommandById('command-id'), 500) })"

// To list all available commands (discovery):
obsidian eval code="Object.keys(app.commands.commands).filter(c => c.includes('keyword')).join('\n')"
```

**Important:** Commands that operate on "the active file" require that file to be open in the active leaf. Use `app.workspace.getLeaf().openFile(file)` first, then wait (setTimeout) before executing the command.
