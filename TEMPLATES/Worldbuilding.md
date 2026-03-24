---
summary: <% await tp.system.prompt("What environment does this file render? (or leave blank)", "") %>
disabled rules:
  - all
fileClass: worldbuilding
status: in-progress
scope: craft
document-role: worldbuilding
environment-type: <% await tp.system.suggester(["city", "institution", "ecosystem", "digital", "historical-era", "natural", "domestic", "sacred"], ["city", "institution", "ecosystem", "digital", "historical-era", "natural", "domestic", "sacred"]) %>
protagonist: []
book: []
time-period: ""
research-sources: []
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
> A worldbuilding file is the RENDERING LAYER between research (facts) and scenes (moments). A scene writer loading this file should have everything they need to write a scene in this environment without loading any research report. The content here must be SENSORY, SPECIFIC, and SCENE-WRITABLE — not scholarly, not abstract, not summarized.
>
> This file lives in `CANON/Worldbuilding/` and IS indexed by semantic search. Every heading you write, every detail you render, is discoverable by every future agent. Build it like it will be searched by a hundred agents who have never seen it before — because it will be.
>
> ---
>
> **STEP 1 — VERIFY NO DUPLICATE EXISTS.** Before creating this file, search the vault: `search_vault` or `resolve_wikilink` for this environment name. A worldbuilding file may already exist for this location, era, or institution. If it does, EDIT the existing file — do not create a duplicate. If a file exists for a related but distinct environment (e.g., `Louisville.md` exists and you're creating `Louisville-West-End.md`), ensure the scope is clearly different and cross-link them.
>
> **STEP 2 — VERIFY UNIQUE FILENAME.** The filename must be unique across the entire vault. Use `resolve_wikilink("Your-Proposed-Name")` — if it returns a result, the name is taken. Worldbuilding filenames should be evocative and specific: `South-African-Coast-Birth-Fire` not `Setting-1`. `Louisville-Ohio-River-Industrial-Belt` not `City`. The filename IS the wiki-link every scene file will use.
>
> **STEP 3 — RENDER, DON'T COPY.** If you're extracting from a research report, TRANSFORM the material. A research fact ("TSMC received $6.6 billion in CHIPS Act grants") becomes a rendered environment detail ("The lobby has a Kuai Kuai snack placed beside the first server rack — a Taiwanese superstition brought from Hsinchu, practiced with half-ironic sincerity by engineers who understand quantum physics but won't tempt fate"). Every paragraph should be writable into a scene. If it reads like a Wikipedia article, it's not rendered yet.
>
> **STEP 4 — WRITE SEMANTICALLY DESCRIPTIVE HEADINGS.** Every subheading is a retrieval interface for scene writers. `### The Night Sky — No Light for Ten Thousand Miles` tells a scene writer exactly what ammunition is here. `### Visual Details` tells them nothing. Use temporal sub-headings when this environment appears in different eras: `### Jerusalem 600 BCE — The Temple Mount Under Babylonian Siege`, `### Jerusalem 2026 — The Old City at Shabbat Dusk`.
>
> **STEP 5 — FILL THE YAML.**
> - `summary` — What environment this file renders, what era(s) it covers, what makes it distinctive. Write for a scene writer deciding whether to load this file.
> - `environment-type` — One of: city, institution, ecosystem, digital, historical-era, natural, domestic, sacred.
> - `protagonist` — Every character who inhabits, visits, or is shaped by this environment. Tag generously.
> - `book` — Which book(s) this environment appears in. Use `[1]`, `[2]`, `[3]`, or `[1, 2]` etc.
> - `time-period` — Human-readable era description (e.g., "~80,000 years ago", "2026", "600 BCE - 2026").
> - `research-sources` — Wiki-links (`[[filename]]`) to every research report this content was drawn from. This is the traceability chain — a future agent can follow these back to the full scholarly apparatus.
> - `source` — Your session ID or "Migration from [[source-file]]".
> - `agent-note` — Gaps you know about, areas that need enrichment, connections you noticed.
>
> **STEP 6 — POPULATE THE SCENE-READY INVENTORY.** This section is the highest-value content in the file. Concrete, specific, grab-and-use ammunition for prose. Not descriptions — objects, sounds, images, textures, smells, phrases. A scene writer under time pressure scans this section and finds what they need in seconds. If this section is thin, the file isn't doing its job yet.
>
> **STEP 7 — WIRE BIDIRECTIONAL CONNECTIONS.** This file exists in a web. Verify:
> - Every research report listed in `research-sources` has this file listed in its `## Extracted To` section (if migrated) or is noted in its `agent-note`.
> - Search for scene files that should reference this environment in their `setting` field. If scenes exist that are set here but don't link to this file, note them in `agent-note` for a future agent to fix.
> - Search for character files whose characters inhabit this environment. Verify they're tagged in `protagonist`.
>
> **STEP 8 — VERIFY BEFORE DELIVERY.**
> - [ ] No duplicate worldbuilding file exists for this environment
> - [ ] Filename is unique and evocative (not generic)
> - [ ] Content is RENDERED (sensory, scene-writable) not raw research
> - [ ] Every subheading is semantically descriptive
> - [ ] Scene-Ready Inventory has concrete, specific ammunition
> - [ ] `summary` describes the environment for a scene writer deciding whether to load it
> - [ ] `protagonist` tags every character connected to this environment
> - [ ] `research-sources` links every research report this draws from
> - [ ] `disabled rules: [all]` is present
> - [ ] All empty fields use `""` not blank
> - [ ] Vault Nervous System callout is at the bottom
> - [ ] Bidirectional connections verified or gaps noted in `agent-note`
>
> **When complete, collapse this callout** (change `+` to `-`).

## Physical Environment

*The sensory world. What you see, hear, smell, touch. Time of day matters. Season matters. Light quality, ambient sound, temperature, the specific objects that make this place THIS place and not a generic location. Use temporal sub-headings when this environment appears in different eras.*

## Cultural Texture

*How people behave here. Speech patterns, customs, daily rhythms, social hierarchies visible in body language and dress. What's polite, what's rude, what's invisible to outsiders. The behavioral signatures of this community.*

## Hyperself Ecology

*Which collective organisms operate in this environment. How they manifest physically — buildings, rituals, symbols, behavioral patterns. What they're feeding on. What they compete with. The organism-level dynamics visible (to Story) beneath the human surface.*

## Story's Perception

*What Story notices about this place that nobody else would. What makes it significant in the trilogy's argument. What the controlling idea looks like from THIS vantage point. Not just what's HERE but what it MEANS in the context of the vital continuum.*

## Scene-Ready Inventory

*Curated list of specific sensory details a scene writer can grab. Objects, sounds, images, textures, phrases, smells. Not prose — ammunition for prose. The check-cashing place at 2 AM. The guayusa kettle's specific sound. The jade pendant. The Kuai Kuai snack beside the server rack. If this section is thin, the file isn't doing its job.*

## Sources

*Wiki-links to the research documents this file draws from. The agent goes here when they need more depth than this file provides.*

## Reasoning

*Why this worldbuilding file exists, what creative gap it fills, what scenes it gates, what research fed it.*

---

> [!info]- Vault Nervous System
> scenes-consuming::
> reading-cost::
