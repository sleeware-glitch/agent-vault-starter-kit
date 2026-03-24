---
summary: <% await tp.system.prompt("Which scope does this dashboard serve? (or leave blank)", "") %>
disabled rules:
  - all
scope: <% await tp.system.suggester(["core", "craft", "research"], ["core", "craft", "research"]) %>
document-role: dashboard
created: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
modified: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
fileClass: dashboard
---
bre
# <% tp.file.title %>

> [!danger]+ DEPLOYMENT GUIDE — Complete Every Step Before Considering This File Delivered
>
> A dashboard is an AGENT TOOL — a computed view that surfaces actionable items, blocked tasks, stale files, and vault health signals for a specific scope. Dashboards live in `LEDGER/` and use Dataview Serializer queries to render static markdown tables that agents can read directly via MCP.
>
> **⚠️ WARNING: Dashboard and INDEX files have crashed Obsidian when opened.** The root cause is unresolved — likely Dataview Serializer output size interacting with MM or Obsidian's renderer. Build dashboards conservatively. Keep queries scoped tightly. Test by opening in Obsidian AFTER saving — if Obsidian freezes, the query is too broad.
>
> ---
>
> **STEP 1 — DEFINE THE SCOPE.** What workspace does this dashboard serve? Core, Craft, or Research? The `scope` field determines which files the queries surface. A Core dashboard queries operations and infrastructure files. A Craft dashboard queries scenes, characters, and worldbuilding.
>
> **STEP 2 — WRITE TIGHT QUERIES.** Each Dataview query should filter aggressively:
> - Always filter by `scope` or `fileClass` — never query the entire vault.
> - Always exclude `status = "done"` and `status = "superseded"` unless specifically needed.
> - Keep result sets small. A query returning 100+ rows will bloat the serialized output and risk crashes.
> - Wrap queries in Dataview Serializer comment blocks so they render as static markdown.
>
> **STEP 3 — VERIFY UNIQUE FILENAME.** Dashboard names use scope prefixes: `Core-Dashboard`, `Craft-Dashboard`. Not `Dashboard` (ambiguous).
>
> **STEP 4 — FILL THE YAML.**
> - `summary` — What scope this dashboard serves and what an agent finds here.
> - `scope` — The workspace this dashboard is built for.
>
> **STEP 5 — TEST IN OBSIDIAN.** Save the file. Open it in Obsidian. If Obsidian freezes, the query is too broad — narrow the filters. Do not deliver a dashboard that crashes Obsidian.
>
> **When complete, collapse this callout** (change `+` to `-`).

> **dep-check** indicates dependency status for orientation. It does not prohibit work.

## Actionable Now

<!-- QueryToSerialize: TABLE status, dep-check, depends-on FROM "" WHERE scope = "SCOPE" AND dep-check = "all-clear" AND status != "done" AND status != "superseded" SORT file.name ASC -->
<!-- SerializedQuery: TABLE status, dep-check, depends-on FROM "" WHERE scope = "SCOPE" AND dep-check = "all-clear" AND status != "done" AND status != "superseded" SORT file.name ASC -->

| File | status | dep-check | depends-on |
| ---- | ------ | --------- | ---------- |

<!-- SerializedQuery END -->
