---
summary: NEEDS SUMMARY -- invisible to Vault Map and agent discovery
disabled rules:
  - all
fileClass: task
status:
  - todo
  - developmental
scope: craft
priority: important
assigned-to: craft
track: ""
phase: ""
book: ""
depends-on: []
gates: []
flagged-for: []
due-by: ""
created-date: <% tp.file.creation_date("YYYY-MM-DD") %>
---

# <% tp.file.title %>

> [!danger]+ HOW TO USE THIS TASK — Read, Fill, Collapse
>
> A task is a unit of work that appears on the **[[Production-Board]]** (creative tracks) or **[[Core-Dashboard]]** (infrastructure). Every field exists to help agents find this task, understand it, and know when it's done.
>
> ---
>
> **NAMING CONVENTION (mandatory):** Task filenames use a timestamp prefix for guaranteed uniqueness: `YYYYMMDD-HHMM-brief-slug`. Example: `20260319-1400-scene-brief-ep7`. The timestamp IS the unique identifier. The slug is optional shorthand for human scanning. This scales to thousands of tasks without collision.
>
> **YAML — Fill what applies, leave the rest as `""` or `[]`:**
>
> - `summary` — One line: what this task IS and what it PRODUCES. Written for an agent who has never seen this file. This is how the task appears in search and on the Vault Map.
> - `track` — Which production stream: plotting, prose, characters, worldbuilding, research, voice, editorial, infrastructure. Determines which section of the Production Board shows this task. **A task with no track is invisible on the board.**
> - `phase` — Your position within the track. Freeform text. Use whatever phasing makes sense for the track (e.g., "1A", "outline", "enrichment-round-2"). Tasks sort by phase on the board.
> - `book` — Which book: 1, 2, 3, or all. Enables per-book filtering on dashboards.
> - `depends-on` — Wiki-links to tasks that must be done BEFORE this one can start. If those tasks aren't done, this task is blocked. Example: `depends-on: ["[[20260319-1400-scene-brief-ep7]]"]`
> - `gates` — Wiki-links to tasks that THIS task unlocks when completed. The inverse of depends-on. When you finish this task, the gated tasks become unblockable.
> - `flagged-for` — Cross-workspace attention flags. Set `flagged-for: craft` if a Core task needs Craft's input, or `flagged-for: lee` if it needs Lee's decision. Shows in the Cross-Track Flags section of the Production Board.
> - `status` — `todo` → `in-progress` → `done`. Use `blocked` when depends-on items aren't done yet.
>
> **BODY — Three sections, all mandatory:**
>
> - **## What** — What needs to happen, why it matters, what the deliverable is. Be specific enough that an agent loading this file for the first time can start working without asking questions.
> - **## Source Material** — Wiki-links to vault documents that feed this task. The agent loads these before starting.
> - **## Log** — Timestamped entries from every agent who touches this task. Convention: `**YYYY-MM-DD — Agent-Name:** What happened.` This is the task's memory across agent generations. Never delete log entries.
>
> **HOW TO CREATE (agents):** Generate a timestamp from the current time (YYYYMMDD-HHMM), append a brief slug, then call `obsidian_create(name="LEDGER/Tasks/YYYYMMDD-HHMM-slug", template="Task")`. Set fields via `obsidian_property_set`. Do NOT use `write_file` — it bypasses Obsidian's event system and the task won't appear on dashboards. Body content can use `update_file_lines`.
>
> **WHEN DONE (all steps, in order):**
> 1. **Place your gold before you die.** Every insight, principle, technique, dead end, or lesson learned during this mission belongs in the vault — not in this task file's log. The log RECORDS what you placed. The vault HOLDS it. Route each discovery to its SSOT home:
>    - **Craft principle** (universal, applies to all scenes/arcs/books) → add to [[Craft-Rules]] under the appropriate section
>    - **Composition technique or voice insight** → add to [[Narration]] or the relevant composition toolkit in REFERENCE/Craft/
>    - **Content** (canon facts, character details, worldbuilding specifics) → add to the canonical file in CANON/
>    - **Gap or need** (something the project should do but hasn't — a research question, a missing toolkit, a structural problem) → note in [[Lee-Inbox]] for CoS to turn into a proper mission or commission
>    - **Insight on how to be an effective agent** (what works, what doesn't, dead ends future agents should avoid, postures that make the work succeed) → add to [[handoff-Craft]] Section VII (Lessons to Internalize)
>    - **Mistake pattern or anti-pattern** → add to [[handoff-Craft]] Section V (Dead Ends and Traps)
>    Then in your final Log entry, note WHAT you placed and WHERE — so the record exists, but the gold itself lives at its permanent home.
> 2. Set `status: done` via `obsidian_property_set`
> 3. Leave a final `## Log` entry: what was delivered, where it lives, and what gold was placed where
> 4. Check `gates` — open each downstream task, check if ALL its `depends-on` are now done, and if so update its status from `blocked` to `todo`
> 5. Move this task to `LEDGER/Tasks/Completed/` via `obsidian_move`
> 6. Call `vault_refresh()` so dashboards reflect the changes
>
> **When complete, collapse this callout** (change `+` to `-`).

## What

<!-- What needs to happen? What's the deliverable? Why does this matter? -->

## Source Material

<!-- Wiki-links to vault documents that feed this task -->

## Log

<!-- **YYYY-MM-DD — Agent-Name:** What you did, what you learned, what's next. -->
