---
summary: <% await tp.system.prompt("Character summary (or leave blank for now)", "") %>
disabled rules:
  - all
fileClass: character
status: in-progress
scope: craft
document-role: canon
book: <% await tp.system.suggester(["1", "2", "3", "all"], ["1", "2", "3", "all"]) %>
tier: <% await tp.system.suggester(["protagonist", "major-secondary", "recurring-minor", "scene-character", "named-background", "hyperself", "universal", "named-god"], ["protagonist", "major-secondary", "recurring-minor", "scene-character", "named-background", "hyperself", "universal", "named-god"]) %>
arc: ""
naming-source: ""
visual-anchor: ""
behavioral-signature: ""
core-need: []
hamartia: []
sympathizing-trait: []
self-awareness: ""
spouse-partner: []
parents: []
siblings: []
children: []
depends-on: []
stale-after: 90
source: ""
agent-note: ""
flagged-for: []
verified: ""
created: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
modified: <% tp.file.creation_date("YYYY-MM-DDTHH:mm:ss") %>
---

# <% tp.file.title %>

> [!danger]+ DEPLOYMENT GUIDE — Complete Every Step Before Considering This File Delivered
>
> A character file is a CANON document — the single source of truth for who this person is. Every agent who writes a scene with this character, every plotter who designs their arc, every migration agent who enriches their profile loads THIS file. It must bring the person alive. Not as data, but as a human being Story would recognize.
>
> This file lives in `CANON/Characters/` and IS indexed by semantic search. The tier determines how much depth is expected — a protagonist needs full psychological taxonomy, a scene-character needs a name and a function. Don't over-build minor characters. Don't under-build protagonists.
>
> ---
>
> **STEP 1 — VERIFY NO DUPLICATE EXISTS.** Search the vault for this character's name. Use `resolve_wikilink("Character-Name")` and `search_vault` with character name + arc + role. A file may already exist from migration, from a different session, or under a working name. If it does, EDIT — do not create a duplicate.
>
> **STEP 2 — VERIFY UNIQUE FILENAME.** Use `resolve_wikilink("Your-Proposed-Name")` — if it returns a result, the name is taken. Character filenames use the character's full name: `Caleb Stray`, `Lin Yù`, `Maria Rai`. For hyperselves and entities: `Story`, `Reach`, `Ādi`.
>
> **STEP 3 — SET THE TIER AND CALIBRATE DEPTH.** The `tier` field determines how much the vault expects from this file:
> - **protagonist** / **major-secondary**: Full depth. Every YAML field populated. All body sections developed with prose. Psychological taxonomy complete. Relational fields wired. This is a person a scene writer must know deeply.
> - **recurring-minor**: Key fields populated. Identity section complete. Brief characterization in Who They Are. Psychology fields if known, empty if not. A scene writer needs enough to write them in a room.
> - **scene-character** / **named-background**: Minimal. Name, identity basics, narrative function. A scene writer needs to know what they DO in the scene, not their inner life.
> - **hyperself** / **universal** / **named-god**: Different axis entirely. Psychology fields don't apply in human terms. Focus on: what scale, what lifecycle stage, what feeds it, how it manifests, what Story sees when she looks at it.
>
> **STEP 4 — FILL THE PSYCHOLOGY (protagonists and major-secondary only).** These fields have DEFINED VOCABULARIES. Use only these values:
> - `core-need`: Sovereignty, Connection, Truth, Safety, Meaning, Control, Recognition, Transcendence
> - `hamartia`: Overconfidence, Obsession, Pride, Naivete, Passivity, Distrust, Stubbornness, Impulsiveness
> - `sympathizing-trait`: Vulnerability, Competence, Moral Courage, Humor, Tenderness, Intensity, Sacrifice, Defiance
> - `self-awareness`: High, Medium, Low
>
> Multiple values are allowed for core-need, hamartia, and sympathizing-trait. If you're uncertain, leave the field as `[]` and explain your uncertainty in `agent-note` — an empty field with an honest note is better than a wrong value.
>
> **STEP 5 — WRITE THE BODY AS PROSE WITH INLINE FIELDS.** The body sections use hybrid prose+inline Dataview fields. The inline fields use `(field:: value)` syntax embedded naturally within prose paragraphs. Write the PERSON first — a living paragraph that Story would recognize. Then embed the structured data within it. The body should read as literature with metadata woven in, not as a form with prose crammed between fields.
>
> **STEP 6 — WIRE RELATIONAL FIELDS.** Character relationships are bidirectional:
> - If you set `spouse-partner: [[Lin Yù]]` on this file, verify that Lin Yù's file has this character in HER `spouse-partner` field.
> - Same for `parents`, `siblings`, `children`.
> - Use `resolve_wikilink` to verify the linked files exist. If they don't, note the gap in `agent-note` — don't create stub files unless the task requires it.
> - `arc` links to the protagonist arc this character belongs to (e.g., `[[B2 Family Arc]]`).
>
> **STEP 7 — FILL REMAINING YAML.**
> - `summary` — One sentence that tells a scene writer who this person IS and why they'd load this file. Not a bio — a hook. "The doctor who can't stop diagnosing the city as a sick organism" not "Male, middle-aged, former physician."
> - `book` — Which book(s) this character appears in.
> - `naming-source` — Etymology or reasoning behind the name. See [[Naming-Doctrine]].
> - `visual-anchor` — The single image that locks this character in the reader's mind.
> - `behavioral-signature` — The habitual action that identifies them without naming them.
> - `source` — Your session ID.
> - `agent-note` — Gaps, uncertainties, connections you noticed, psychology fields you weren't sure about.
>
> **STEP 8 — VERIFY BEFORE DELIVERY.**
> - [ ] No duplicate character file exists
> - [ ] Filename is the character's name (unique across vault)
> - [ ] Tier is set and depth matches tier expectations
> - [ ] Psychology fields use ONLY the defined vocabulary (or are honestly empty with agent-note)
> - [ ] Body sections are prose with inline `(field:: value)` fields, not data dumps
> - [ ] Relational fields are bidirectional (or gaps noted in agent-note)
> - [ ] `summary` is a hook, not a bio
> - [ ] `disabled rules: [all]` is present
> - [ ] All empty fields use `""` or `[]` not blank
> - [ ] Vault Nervous System callout is at the bottom
> - [ ] For protagonists: every section developed, no empty body sections
> - [ ] For scene-characters: minimal build, don't over-engineer
>
> **When complete, collapse this callout** (change `+` to `-`).

## Identity

(name:: ) (family-name:: ) (identity:: ) (species:: Human) (gender:: ) (ethnicity:: ) (birth-death:: )

## Who They Are

*A paragraph that brings this person to life. What Story sees when she looks at them. What makes them the protagonist of their own journey — because every character IS the protagonist of their own journey, regardless of tier. Embed (core-desire:: ) and (personality:: ) naturally within the prose.*

## What They Look Like

*Not a checklist. The paragraph Story would write — the detail that makes this person unmistakable in a crowd. Embed (appearance:: ), (hair-color:: ), (eye-color:: ), (voice:: ) within the description.*

## What They Carry

*The wound. The want. The lie they believe. The truth they can't face. This is the engine of their arc. Embed (believed-lies:: ), (strengths:: ), (weaknesses:: ) within the narrative.*

## Relationships

*Not just WHO but what the relationship FEELS like. The YAML relational fields carry the structural links. This section carries the human texture — what it's like to be in a room with this person and the people they love or fear or resent.*

## Narrative Function

(politics:: )
(skills:: )

*Archetypal frequency. What role this character serves in the story's architecture. How they enter scenes and what they bring with them. For hyperself-tier characters: what scale they operate at, what lifecycle stage, how they manifest.*

## Story Presence

<!-- QueryToSerialize: TABLE scene-type, story-date-start, act, chapter FROM "" WHERE fileClass = "scene" AND contains(characters-present, this.file.link) SORT story-date-start ASC -->
<!-- SerializedQuery: TABLE scene-type, story-date-start, act, chapter FROM "" WHERE fileClass = "scene" AND contains(characters-present, this.file.link) SORT story-date-start ASC -->

*Auto-populates as scene files list this character in `characters-present`.*

<!-- SerializedQuery END -->

## Reasoning

*Why this character exists, what function they serve, key decisions about their design, what research feeds them. See [[Naming-Doctrine]] for name etymology conventions.*

---

> [!info]- Vault Nervous System
> scene-count::
> completeness::
> consistency-alert::
> reading-cost::
