---
summary: <% await tp.system.prompt("Summary") %>
disabled rules:
  - all
status:
  - todo
  - active
scope: <% await tp.system.suggester(["core", "craft", "research", "all"], ["core", "craft", "research", "all"]) %>
document-role: <% await tp.system.suggester(["canon", "reference", "research", "planning", "operations", "scene", "worldbuilding", "dashboard"], ["canon", "reference", "research", "planning", "operations", "scene", "worldbuilding", "dashboard"]) %>
stale-after: 30
source: ""
agent-note: ""
flagged-for: []
verified: ""
created: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
modified: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
fileClass: tracked-item
---

# <% tp.file.title %>

> [!danger]+ DEPLOYMENT GUIDE
>
> Tracked-Item is the GENERAL-PURPOSE template for documents that don't fit a specialized fileClass (scene, character, worldbuilding, research-report, reference-doc, dashboard). Use it for migration guides, workflow documents, session logs, proposals, analysis docs, and any operational or planning artifact that needs to be discoverable and tracked.
>
> **Before using this template, ask: does a more specific template fit?** A character → use Character template. A research report → use Research-Report. A worldbuilding environment → use Worldbuilding. A scene → use Scene. A reference doc → use Reference. Tracked-Item is the fallback, not the default.
>
> ---
>
> **STEP 1 — VERIFY NO DUPLICATE EXISTS.** Search the vault. Use `resolve_wikilink` and `search_vault`.
>
> **STEP 2 — VERIFY UNIQUE FILENAME.** Use `resolve_wikilink("Your-Proposed-Name")`. Descriptive names: `Migration-Guide`, `Phase-0-Debrief`, `Infrastructure-Priority-Roadmap`. Not `Document-1` or `Notes`.
>
> **STEP 3 — SET `document-role` CORRECTLY.** This field tells agents what kind of document this is and where it belongs. Match it to the folder: operations docs → `operations`, planning docs → `planning`, etc.
>
> **STEP 4 — FILL THE YAML.**
> - `summary` — What this document is, when an agent would load it.
> - `scope` — Who uses this: core, craft, research, or all.
> - `source` — Your session ID.
> - `agent-note` — Context, gaps, what to watch for.
>
> **STEP 5 — VERIFY BEFORE DELIVERY.**
> - [ ] No duplicate exists
> - [ ] A more specific template wasn't more appropriate
> - [ ] Filename is descriptive and unique
> - [ ] `summary` tells an agent when to load this file
> - [ ] `document-role` matches the folder/purpose
> - [ ] `disabled rules: [all]` is present
> - [ ] All empty fields use `""` or `[]` not blank
>
> **When complete, collapse this callout** (change `+` to `-`).

*Document content.*

## Reasoning

*Why this document exists, what problem it solves, what depends on it.*
