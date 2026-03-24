---
summary: <% await tp.system.prompt("What does this plan cover? (or leave blank)", "") %>
disabled rules:
  - all
status:
  - in-progress
  - developmental
  - active
scope: craft
document-role: planning
depends-on: []
stale-after: 14
source: ""
agent-note: ""
flagged-for: []
verified: ""
created: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
modified: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
fileClass: tracked-item
---

# <% tp.file.title %>

> [!danger]+ DEPLOYMENT GUIDE — Complete Every Step Before Considering This File Delivered
>
> A planning document coordinates the story's architecture — act structures, chapter breakdowns, timeline grids, arc coordination, scene sequencing. It lives in `CANON/Planning/` and IS indexed by semantic search. Plotters, scene writers, and the mining agent all consult planning files. They must be structurally precise and clearly organized.
>
> Planning files have a short `stale-after` (14 days) because the story evolves fast. If you're editing a planning file that hasn't been touched in weeks, treat it with skepticism — verify its assumptions against current scene files and character files before building on it.
>
> ---
>
> **STEP 1 — VERIFY NO DUPLICATE EXISTS.** Search for existing planning documents covering this scope. Act files, chapter breakdowns, arc plans, timeline documents — there may already be one that should be edited rather than replaced. Use `search_vault` with the arc name, act number, or plot element.
>
> **STEP 2 — VERIFY UNIQUE FILENAME.** Use `resolve_wikilink("Your-Proposed-Name")`. Planning filenames should identify scope: `Book-2-Act-III-Chapter-Breakdown`, `Family-Arc-Ratchet-System`, `Cross-Arc-Timeline-Grid`. Not `Plan` or `Outline`.
>
> **STEP 3 — WRITE SEMANTICALLY DESCRIPTIVE HEADINGS.** Planning files are reference documents for plotters and drafters. Every section heading must identify what planning question it answers. `### The Four Ratchets — How Solidarity Becomes Institutional DNA` is useful. `### Notes` is not.
>
> **STEP 4 — CROSS-REFERENCE SCENE AND CHARACTER FILES.** Planning documents should wiki-link to every scene file, character file, and worldbuilding file they reference. When you mention a scene by name, link it: `[[Aruta-Leaves-the-Fire]]`. When you reference a character, link them: `[[Caleb Stray]]`. These links make the planning document a navigation hub for the story section it covers.
>
> **STEP 5 — FILL THE YAML.**
> - `summary` — What scope of the story this plan covers, what decisions it contains, what depends on it.
> - `depends-on` — Wiki-links to other planning documents, character files, or reference docs this plan builds on.
> - `source` — Your session ID.
> - `agent-note` — Open questions, provisional decisions, things that need Lee's input.
>
> **STEP 6 — VERIFY BEFORE DELIVERY.**
> - [ ] No duplicate planning document covers this scope
> - [ ] Filename identifies the planning scope (not generic)
> - [ ] All references to scenes, characters, and worldbuilding use wiki-links
> - [ ] `summary` identifies scope and key decisions
> - [ ] `disabled rules: [all]` is present
> - [ ] All empty fields use `""` or `[]` not blank
> - [ ] Reasoning section explains why this organizational structure was chosen
>
> **When complete, collapse this callout** (change `+` to `-`).

*Planning content — act structure, chapter breakdowns, timeline grids, arc coordination, scene sequencing.*

## Reasoning

*Structural decisions: why this organization, what alternatives were considered, what this plan supersedes or refines.*
