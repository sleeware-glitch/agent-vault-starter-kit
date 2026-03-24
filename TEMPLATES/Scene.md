---
summary: <% await tp.system.prompt("Scene summary (or leave blank for now)", "") %>
disabled rules:
  - all
fileClass: scene
status:
  - unwritten
  - developmental
  - active
scope: craft
document-role: scene
book: <% await tp.system.suggester(["1", "2", "3"], ["1", "2", "3"]) %>
scene-type: <% await tp.system.suggester(["episode", "stasimon", "prologue", "epilogue", "interlude", "chorus", "overture", "passage", "address"], ["episode", "stasimon", "prologue", "epilogue", "interlude", "chorus", "overture", "passage", "address"]) %>
protagonist: ""
act: ""
chapter: ""
scene-order: ""
location: ""
setting: []
story-date-start: ""
story-date-end: ""
arc-color: ""
draft-pass: unwritten
synopsis: ""
characters-present: []
research-consumed: []
depends-on: []
foreshadows: []
pays-off: []
preceding-scene: ""
following-scene: ""
hyperself-organism: ""
interiority-mode: ""
mood: []
tension: ""
pace: ""
atmosphere: []
stale-after: 30
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
> A scene file is a MANUSCRIPT document — it will contain the actual prose of the trilogy. It lives in `MANUSCRIPT/` from birth and carries both planning (Scene Brief) and prose (## Draft). This file is the atomic unit of storytelling: one scene, one file, one truth. It also anchors the narrative chain — its `preceding-scene` and `following-scene` fields connect it to the scenes before and after, building the book's spine.
>
> A scene file with an empty Scene Brief is a placeholder. A scene file with a filled Scene Brief is a writing assignment. A scene file with a ## Draft is a first pass. The `draft-pass` field tracks where it is in that lifecycle: `unwritten` → `skeleton` → `voice` → `hyperself` → `polish` → `complete`.
>
> ---
>
> **STEP 1 — VERIFY NO DUPLICATE EXISTS.** Search for this scene by name, by narrative moment, and by position (act/chapter/order). Scene files may exist from a plotting session under a different name. Use `search_vault` with the scene's key dramatic moment. If a file exists for this narrative beat, EDIT — do not create a duplicate.
>
> **STEP 2 — VERIFY UNIQUE FILENAME.** Use `resolve_wikilink("Your-Proposed-Name")`. Scene filenames should identify the dramatic moment: `Aruta-Leaves-the-Fire`, `Caleb-First-Stream`, `Lin-Yu-Watches-the-Address`. Not `Scene-4` or `Chapter-2-Scene-1`. The filename is what appears in chapter outlines, timeline views, and every agent's search results.
>
> **STEP 3 — WIRE THE SETTING.** The `setting` field links to worldbuilding files. This is the single most important connection for a scene writer — it's where they get their sensory palette.
> - Search for worldbuilding files covering this scene's location and era. Use `search_vault` with location terms or `resolve_wikilink` if you know the filename.
> - If a worldbuilding file exists, add it to `setting: [[Worldbuilding-Filename]]`.
> - If NO worldbuilding file exists for this environment, note the gap in `agent-note` with `flagged-for: [craft]`. A worldbuilding file should be created before this scene is drafted.
> - Multiple settings are valid (a scene can move between locations): `setting: [[[Louisville-West-End]], [[Louisville-Ohio-River]]]`.
>
> **STEP 4 — WIRE THE CHARACTERS.** The `characters-present` field links to character files.
> - List every character who appears, speaks, or is directly referenced in this scene.
> - Use `resolve_wikilink` to verify each character file exists.
> - If a character file doesn't exist yet, note the gap in `agent-note`. For scene-characters and named-background characters who appear only here, creation can happen at drafting time.
> - `protagonist` is the scene's POV character or primary focus (single value, not a list).
>
> **STEP 5 — WIRE THE CHAIN.** Scenes exist in a sequence:
> - `preceding-scene` — Wiki-link to the scene that comes before this one in the reading order.
> - `following-scene` — Wiki-link to the scene that comes after.
> - `foreshadows` — Wiki-links to scenes this scene plants seeds for.
> - `pays-off` — Wiki-links to earlier scenes whose setups are paid off here.
> - If you set `preceding-scene: [[Scene-A]]`, verify that Scene-A has `following-scene: [[This-Scene]]`. Bidirectional.
> - These fields can be filled at plotting time and refined as the book develops. Empty chain fields on a new scene are acceptable — but a scene that enters the drafting phase without chain fields is unmoored.
>
> **STEP 6 — FILL THE SCENE BRIEF.** The Scene Brief is the writing assignment. Every field matters:
> - **Human layer** — what happens at the surface level. What a camera would record.
> - **Hyperself layer** — what the organisms are doing beneath/around the human action. What Story sees that the characters don't.
> - **Reader layer** — what this scene advances in the reader's understanding. What shifts in their perception.
> - **What changes** — THE MOST IMPORTANT FIELD. If the state at the end equals the state at the start, the scene doesn't belong. Something must be different — a relationship, a belief, a power balance, a piece of knowledge. Name it.
> - **Voice / register** — what this scene sounds like. Which Story mode. Reference [[Narration]] if needed.
> - **Sensory palette** — the dominant sensory channel. Draw from the worldbuilding file's Scene-Ready Inventory.
> - `(reader-carries-in:: )` — what the reader knows/feels entering this scene from the previous one.
> - `(scene-launches:: )` — what dramatic questions this scene opens that subsequent scenes must answer.
>
> **STEP 7 — FILL REMAINING YAML.**
> - `summary` — One sentence: what happens and why it matters. For chapter outlines and timeline views.
> - `synopsis` — Slightly longer than summary. The dramatic arc in a sentence or two.
> - `act`, `chapter`, `scene-order` — Structural position. May be provisional during plotting.
> - `story-date-start`, `story-date-end` — When this scene occurs in story-world time. Enables Chronos timeline visualization. Scenes can span minutes or millennia.
> - `research-consumed` — Wiki-links to research reports whose material informed this scene's planning. Different from worldbuilding `setting` — this tracks intellectual sources, not sensory environments.
> - `hyperself-organism` — For stasima: which organism's interiority we enter.
> - `interiority-mode` — For stasima: the technique used (see [[Writing_Hyperself_Interiority_v4]]).
> - `mood`, `tension`, `pace`, `atmosphere` — Tonal metadata. Fill what you can; refine at drafting.
> - `source` — Your session ID.
> - `agent-note` — Open questions, gaps, things a drafting agent needs to know.
>
> **STEP 8 — VERIFY BEFORE DELIVERY.**
> - [ ] No duplicate scene file exists for this narrative moment
> - [ ] Filename identifies the dramatic moment (not a generic label)
> - [ ] `setting` links to worldbuilding file(s) or gap noted in agent-note
> - [ ] `characters-present` links to character files or gaps noted
> - [ ] `protagonist` identifies the POV/focus character
> - [ ] `preceding-scene` and `following-scene` set (or noted as unplaced)
> - [ ] Chain fields are bidirectional (or gaps noted)
> - [ ] Scene Brief has all three layers filled (human, hyperself, reader)
> - [ ] "What changes" is populated — if you can't fill this, question whether the scene belongs
> - [ ] `story-date-start` is populated (enables timeline)
> - [ ] `synopsis` captures the scene in one line
> - [ ] `disabled rules: [all]` is present
> - [ ] All empty fields use `""` or `[]` not blank
> - [ ] Vault Nervous System callout is at the bottom
> - [ ] `draft-pass` is set to `unwritten` (will advance through drafting lifecycle)
>
> **When complete, collapse this callout** (change `+` to `-`).

## Scene Brief

**Human layer — what happens:**

**Hyperself layer — what the organisms are doing:**

**Reader layer — what this scene advances:**

**What changes (state at end ≠ state at start):**

**Voice / register:**

**Sensory palette:**

(reader-carries-in:: )
(scene-launches:: )

## Draft

*Scene text goes here. The draft-pass field tracks lifecycle: unwritten → skeleton → voice → hyperself → polish → complete. Each pass refines a different dimension. See [[Homer-Writing-System]] for the multi-pass composition method.*

## Reasoning

*Why this scene exists in this position, what it accomplishes structurally, what research feeds it, craft decisions about voice and perspective.*

---

> [!info]- Vault Nervous System
> dep-check::
> blocked-by::
> is-stale::
> context-pack::
> completeness::
> chain-status::
> revision-flag::
> dep-stale::
> reading-cost::
