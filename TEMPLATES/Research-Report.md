---
summary: <% await tp.system.prompt("What does this research deliver to Craft? (or leave blank)", "") %>
disabled rules:
  - all
fileClass: research-report
status:
  - active
  - developmental
scope: research
document-role: research
protagonist: []
craft-domains: []
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
> **Context:** Deep Research mode produces a document and the turn ends. On your NEXT turn, restructure and deploy the report using this guide. This research report will eventually be MINED by a Craft agent who extracts craft-actionable material and distributes it to SSOT destinations elsewhere in the vault. After mining, RESEARCH/ is de-indexed from semantic search. Your job is to make this report maximally minable — clear domain-separated sections, precise tags, descriptive headings, honest confidence markers.
>
> **You are a Research agent, not a Craft agent.** You know the TOPIC deeply. You do NOT know the full creative project deeply enough to judge what's most valuable to Craft or where extracted material should go. That's the mining agent's job. Your job is STRUCTURAL: organize the material so the miner can find everything efficiently, tag it so the right reports surface for the right characters, and mark what's established vs. debated vs. speculative so the miner knows what weight to give each claim.
>
> ---
>
> **STEP 1 — RESTRUCTURE THE BODY.** Deep Research mode produces its own format. Reorganize the content into the domain-separated sections below. Not every section is required — a theoretical framework doc won't have Physical World, a sensory research doc won't have Conceptual Framework. Use the sections that fit your material. But every piece of content must land under the section where a mining agent would look for it:
> - Sensory details, environmental descriptions → **The Physical World**
> - Actions, procedures, ceremonies, routines → **Ritual, Practice, and Behavior**
> - Lifecycles, phase transitions, cause-and-effect → **Structural Patterns**
> - Models, taxonomies, theoretical architecture → **Conceptual Framework**
> - Timeline, dates, political background → **Historical Context**
> - Sources, methodology, competing views → **Scholarly Apparatus**
> - Factual traps, anachronisms, projection risks → **Craft Warnings**
>
> Do NOT leave content in a miscellaneous dump. Every paragraph has a home.
>
> **STEP 2 — WRITE SEMANTICALLY DESCRIPTIVE HEADINGS.** Every subheading is a retrieval interface. The mining agent will scan headings to decide what to extract. `### The Sound of a Mesopotamian Temple at Dawn` tells them exactly what's there. `### Key Findings` tells them nothing. Write headings that answer "is this what I need?" from the heading text alone.
>
> **STEP 3 — FILL THE YAML.** Every field must be populated or explicitly empty (`""`).
> - `summary` — 2-3 sentences. What does this research cover? What topics, time periods, or phenomena? Which of the four protagonists or major entities (Story, Reach, Named Gods) does it most directly serve? Factual description, not craft judgment.
> - `protagonist` — Tag every character or entity this research could plausibly inform. The four human protagonists are: Caleb, Lin Yù, Savio, the Family. Also tag hyperself entities where relevant: Story, Reach, Ādi. Tag generously — it's cheap to over-tag and expensive to miss one.
> - `craft-domains` — What kind of material does this contain? Use any combination of: `sensory`, `historical`, `institutional`, `psychological`, `theological`, `scientific`, `cosmological`, `legal`, `political`, `economic`, `ecological`, `cultural`, `architectural`, `medical`, `technological`, `literary`.
> - `depends-on` — Wiki-links (`[[filename]]`) to other research reports this builds on or relates to.
> - `source` — "Deep Research" or commission number (e.g., "Commission 26") or session ID.
> - `agent-note` — Your observations: surprising connections to other vault topics, gaps you noticed, quality/confidence assessment, anything a mining agent should know.
> - `status` — `active` when delivered.
>
> **STEP 4 — WRITE CRAFT WARNINGS.** You know the topic. What factual traps does this material set? Common anachronisms a writer would fall into? Projection errors (imposing modern psychology on ancient people, or Western frameworks on non-Western cultures)? Clichés this topic attracts? Misunderstandings that would undermine authenticity? This section captures NEGATIVE KNOWLEDGE — what the material invites you to do wrong. Every research topic has traps. Find them from your topical expertise.
>
> **STEP 5 — VERIFY BEFORE DELIVERY.**
> - [ ] Every piece of content is under the correct domain section
> - [ ] Every subheading is semantically descriptive (no "Section 3", no "Key Points", no "Overview")
> - [ ] `summary` describes what the research covers and who it serves
> - [ ] `protagonist` tags every relevant character/entity
> - [ ] `craft-domains` uses vocabulary from the list above
> - [ ] `depends-on` links related research reports
> - [ ] `disabled rules: [all]` is present in YAML
> - [ ] All empty fields use `""` not blank
> - [ ] Vault Nervous System callout is at the bottom of the file
> - [ ] Confidence markers used in Scholarly Apparatus (ESTABLISHED / DEBATED / SPECULATIVE)
> - [ ] Synthesis is labeled as synthesis; sources are attributed
> - [ ] Craft Warnings section is populated (never empty)
> - [ ] File saved to the correct RESEARCH/ subfolder
>
> **When complete, collapse this callout** (change `+` to `-` in the callout marker). The finished file should be clean for the mining agent.

## The Physical World

*What things looked like, sounded like, smelled like, felt like, tasted like. Named materials, measured dimensions, documented colors, textures, temperatures. This IS the craft palette — written once, here, with scene-level specificity. If the research topic has no physical/sensory dimension, omit this section entirely.*

## Ritual, Practice, and Behavior

*What people (or entities) did. Actions, routines, ceremonies, institutional behaviors. Step-by-step where possible. Concrete enough that a character could perform or witness these actions. If the research has no behavioral dimension, omit this section.*

## Structural Patterns

*How things unfolded over time. Lifecycle arcs, phase transitions, cause-and-effect chains. Rhythms, escalation patterns, feedback loops. How systems behaved, not just what they were. If the research has no temporal/structural dimension, omit this section.*

## Conceptual Framework

*The theoretical architecture. Models, taxonomies, analytical structures. The intellectual scaffolding the project's claims rest on. If the research is purely empirical/sensory, omit this section.*

## Historical Context

*Timeline, political background, key events, figures, dates. The factual scaffolding everything above hangs on. When referencing sensory or behavioral details from earlier sections, point to them rather than restating. If the research is not historically situated, omit this section.*

## Scholarly Apparatus

*Sources, methodology, competing interpretations. Use confidence markers: ESTABLISHED (consensus among scholars), DEBATED (active scholarly dispute — name the camps), SPECULATIVE (the project's own synthesis beyond what sources claim — label it clearly). Attribute findings. Label synthesis as synthesis.*

## Craft Warnings

*What NOT to do with this material. The traps it invites. Common anachronisms, projection errors (modern psychology imposed on ancient minds, Western frameworks on non-Western cultures), clichés this topic attracts, misunderstandings that would undermine authenticity. This section captures negative knowledge from your TOPICAL expertise. A Craft mining agent may enrich it later with project-specific warnings. Never leave this section empty.*

## Reasoning

*Why this research exists, what gap it fills, what depends on its output, what commissions it fulfills.*

---

> [!info]- Vault Nervous System
> consumption-status::
> scene-consumers::
> reading-cost::
