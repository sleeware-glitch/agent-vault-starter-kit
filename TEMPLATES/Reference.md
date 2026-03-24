---
summary: <% await tp.system.prompt("What does this reference document define? (or leave blank)", "") %>
disabled rules:
  - all
scope: all
document-role: reference
stale-after: 90
verified: ""
agent-note: ""
flagged-for: []
created: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
modified: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
fileClass: reference-doc
status: active
---

# <% tp.file.title %>

> [!danger]+ DEPLOYMENT GUIDE — Complete Every Step Before Considering This File Delivered
>
> A reference document defines settled knowledge that SUPPORTS the project — craft principles, scientific frameworks, literary analysis, narration rules, naming doctrine. Reference docs live in `REFERENCE/` and IS indexed by semantic search. They are HIGH-AUTHORITY: agents treat them as reliable foundations to build on. Write with that weight. A wrong claim in a reference document propagates through every agent who reads it.
>
> Reference documents have long `stale-after` (90 days) because they contain principles, not plans. But when they're wrong, they're wrong at scale. The `verified` field exists for Lee to confirm authority.
>
> ---
>
> **STEP 1 — VERIFY NO DUPLICATE EXISTS.** Reference documents must have clear SSOT boundaries. Search for existing reference docs covering this topic. If one exists, EDIT it — do not create a parallel authority. If the scope overlaps, decide which file owns what and document the boundary in both files' Reasoning sections.
>
> **STEP 2 — VERIFY UNIQUE FILENAME.** Use `resolve_wikilink("Your-Proposed-Name")`. Reference filenames should name what they define: `Narration`, `Hyperselves`, `SSOT Doctrine`, `Naming-Doctrine`. Not `Reference-1` or `Notes-on-Voice`.
>
> **STEP 3 — ESTABLISH SSOT BOUNDARIES.** In the Reasoning section, state explicitly: what this document OWNS and what it does NOT own. Reference `[[SSOT Doctrine]]` — at the document level, one file owns each fact. If this document touches territory another reference doc covers, state the boundary. Example: "This document owns narrator identity and composition technique. [[Craft-Rules]] owns creative principles and quality tests. When a principle implies a technique, the principle lives there and the technique lives here."
>
> **STEP 4 — WRITE SEMANTICALLY DESCRIPTIVE HEADINGS.** Reference documents are the most-searched files in the vault. Every heading is a retrieval interface. Agents search for principles, techniques, and frameworks by meaning — your headings must match what they're looking for. `### The Inverted Homeric Simile — Mapping the Cosmic Down to the Intimate` is discoverable. `### Section 4` is invisible.
>
> **STEP 5 — LABEL CONFIDENCE.** Where appropriate, use confidence markers: ESTABLISHED (this is settled project doctrine), PROVISIONAL (strong momentum, not yet confirmed by Lee), SPECULATIVE (explored but not committed). Agents build on reference documents — they need to know what weight to give each claim.
>
> **STEP 6 — FILL THE YAML.**
> - `summary` — What this document defines, what authority it holds, who would load it and why.
> - `scope` — Who uses this: `all` for project-wide foundations, `craft` for creative reference, `core` for technical reference.
> - `agent-note` — Gaps, areas that need development, unresolved questions.
>
> **STEP 7 — VERIFY BEFORE DELIVERY.**
> - [ ] No duplicate reference doc covers this territory
> - [ ] SSOT boundaries stated in Reasoning section
> - [ ] Filename names what the document defines
> - [ ] All headings are semantically descriptive
> - [ ] `summary` states the document's authority and audience
> - [ ] `disabled rules: [all]` is present
> - [ ] All empty fields use `""` or `[]` not blank
> - [ ] Confidence markers used where appropriate
>
> **When complete, collapse this callout** (change `+` to `-`).

*Reference content — principles, frameworks, techniques, doctrine.*

## Reasoning

*Why this document exists, what authority it holds, what SSOT boundaries it observes, how it relates to other reference documents.*
