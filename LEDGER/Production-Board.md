---
summary: |
  Production task dashboard. Shows all active research and production tasks.
status: active
scope: craft
fileClass: dashboard
disabled rules:
  - all
---

# Production Board

## Active Production Tasks

<!-- QueryToSerialize: TABLE WITHOUT ID file.link AS "Task", truncate(summary, 80, "...") AS "Description", status AS "Status", priority AS "Priority" FROM "LEDGER/Tasks" WHERE contains(scope, "craft") AND !contains(status, "done") AND !contains(status, "superseded") SORT priority ASC -->
<!-- SerializedQuery: TABLE WITHOUT ID file.link AS "Task", truncate(summary, 80, "...") AS "Description", status AS "Status", priority AS "Priority" FROM "LEDGER/Tasks" WHERE contains(scope, "craft") AND !contains(status, "done") AND !contains(status, "superseded") SORT priority ASC -->

*No tasks yet. Create your first task with `obsidian_create(name="LEDGER/Tasks/YYYYMMDD-HHMM-slug", template="Task")`.*

<!-- SerializedQuery END -->
