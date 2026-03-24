---
summary: <% await tp.system.prompt("What does this operations document cover? (or leave blank)", "") %>
disabled rules:
  - all
status: active
scope: core
document-role: operations
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
> An operations document lives in `OPERATIONS/` and serves Core agents — guides, configurations, workflows, migration protocols, technical documentation. Operations docs go stale FAST (`stale-after: 14` days). If the information in this file stops being accurate, future agents are actively misled. Write with the assumption that someone will read this under time pressure and trust it completely.
>
> ---
>
> **STEP 1 — VERIFY NO DUPLICATE EXISTS.** OPERATIONS/ accumulates documents across sessions. Search for existing docs covering this topic. A superseded version may exist that should be marked `status: superseded` and archived rather than coexisting with your new file.
>
> **STEP 2 — VERIFY UNIQUE FILENAME.** Use `resolve_wikilink("Your-Proposed-Name")`. Operations filenames should describe the operation: `Migration-Guide`, `Vault-MCP-Connector`, `Smart-Connections-MCP-Patch`. Not `Notes` or `Setup`.
>
> **STEP 3 — DOCUMENT THE WHY, NOT JUST THE WHAT.** The Reasoning section is mandatory. Future Core agents will inherit this file and need to understand not just what to do, but why this approach was chosen, what alternatives were rejected, and what would need to change for this document to become obsolete. Without reasoning, operations docs become cargo cult instructions — agents follow them without understanding them and can't adapt when circumstances change.
>
> **STEP 4 — MARK SUPERSEDED PREDECESSORS.** If this document replaces an older operations doc, update the old doc's YAML: `status: superseded`, `superseded-by: [[This-File]]`. Then move the old file to ARCHIVE/. Do not leave two active docs covering the same operation.
>
> **STEP 5 — FILL THE YAML.**
> - `summary` — What operation this covers, when a Core agent would need to load it.
> - `source` — Your session ID.
> - `agent-note` — Known limitations, things likely to change, what to watch for.
>
> **STEP 6 — VERIFY BEFORE DELIVERY.**
> - [ ] No duplicate or superseded operations doc covers this territory
> - [ ] Filename describes the operation
> - [ ] Reasoning section explains WHY, not just WHAT
> - [ ] Any superseded predecessors are marked and archived
> - [ ] `summary` tells a Core agent when to load this file
> - [ ] `disabled rules: [all]` is present
> - [ ] All empty fields use `""` or `[]` not blank
>
> **When complete, collapse this callout** (change `+` to `-`).

*Operations content — guides, configurations, workflows, technical documentation.*

## Reasoning

*Why this document exists, what problem it solves, what it supersedes, what alternatives were considered and rejected. Future agents need the WHY to maintain and adapt this document as circumstances change.*
