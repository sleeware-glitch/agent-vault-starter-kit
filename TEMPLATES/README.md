# Templates Guide

Every new vault file should be born from a template. Templates ensure consistent YAML schema, proper fileClass assignment, and body structure optimized for semantic search.

## Generic Templates (Use As-Is)

- **Task.md** — Task tracking with status, priority, scope, dependency fields, log section
- **Dashboard.md** — Dataview query dashboard with Serializer markup
- **Operations.md** — Infrastructure documentation
- **Planning.md** — Planning documents with dependency tracking
- **Reference.md** — Canonical reference documents
- **Tracked-Item.md** — General-purpose tracked document

## Domain-Specific Templates (Adapt or Replace)

These were built for a literary project. Study them for the PATTERN, then create your own:

- **Character.md** — Shows how to create domain entities with tiered completeness
- **Scene.md** — Shows how to create production units with chain-linking (reading order)
- **Worldbuilding.md** — Shows how to create rich environment/setting documents
- **Research-Report.md** — Shows how to create structured research deliverables

**For a research lab, you might create:**
- `Paper.md` — Academic paper with sections, co-authors, submission status
- `Experiment.md` — Protocol, results, analysis, conclusions
- `Literature-Review.md` — Source paper notes with relevance scoring
- `Grant.md` — Proposal with aims, budget, timeline
- `Dataset.md` — Data documentation with provenance and access info

## Mission Templates (Advanced Pattern)

- **Mission-Character-Tier2.md** and **Mission-Scene-Brief.md** demonstrate "mission templates" — structured multi-phase agent instructions with quality gates. These define a complete agent workflow: bootstrap → calibrate → produce → verify → deliver. Adapt this pattern for your domain (e.g., "Mission-Literature-Sprint" or "Mission-Data-Analysis").

## Creating a New Template

1. Copy the closest existing template
2. Update the YAML frontmatter fields for your document type
3. Set `fileClass:` to match your FileClass definition
4. Always include `disabled rules: [all]` to prevent Linter from mangling YAML
5. Structure the body with descriptive headings (these become semantic search targets)
6. Add the Vault Nervous System callout at the bottom for computed fields
7. Save in TEMPLATES/ — Templater and the Obsidian CLI both look here

## Using Templates

**Via Obsidian CLI (agent path):**
```
obsidian create path="RESEARCH/my-experiment" template="Experiment"
```

**Via Obsidian UI (human path):**
Ctrl+N → name the file → Templater inserts the template automatically (if folder templates are configured)
