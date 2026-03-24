# FileClass Guide

FileClasses define the YAML schema and computed fields for different document types. Metadata Menu reads these definitions and enforces them on any file that declares `fileClass: <name>` in its frontmatter.

## Generic FileClasses (Use As-Is)

- **task.md** — Task tracking with status, priority, scope, dependency tracking
- **dashboard.md** — Dataview query dashboards (auto-serialized for agent reading)
- **tracked-item.md** — General-purpose tracked document with dependency/staleness system
- **reference-doc.md** — Canonical reference documents with reading-cost

## Domain-Specific FileClasses (Adapt for Your Domain)

These were built for a literary project but demonstrate the PATTERN for domain-specific schemas:

- **character.md** — Shows: tier-aware completeness (different fields required for different tiers), cross-file consistency alerts (detects when referenced scenes are stale), relational fields (spouse, parents, siblings, children as MultiFile links)
- **scene.md** — Shows: chain-status (linked reading order), context-pack (auto-assembled loading manifest), revision-flag (detects stale character references), editorial vs structural field distinction
- **research-report.md** — Shows: consumption-status (tracks whether research has been used in production), craft-domains multi-select
- **worldbuilding.md** — Shows: protagonist multi-select, sensory/procedural/structural content categories

**To create your own domain FileClass:**

1. Copy one of the examples
2. Rename it (e.g., `experiment.md`, `paper.md`, `dataset.md`)
3. Modify the fields: keep the generic inherited fields (status, scope, depends-on, dep-check, etc.) and replace the domain-specific fields with your own
4. Update field IDs to be unique (e.g., change `CHR` prefix to `EXP`)
5. Update the completeness formula to check YOUR required fields
6. Create a matching Templater template in TEMPLATES/

## Critical Settings

**`frontmatterOnly: false`** in Metadata Menu's `data.json`. If set to `true`, computed fields duplicate infinitely. This is the #1 cause of MM problems. NEVER change it to `true`.

**`isAutoCalculationEnabled: true`** — enables reactive computed fields. Fields auto-update when source data changes.

**`fileIndexingExcludedFolders`** — folders MM should NOT index for computed fields. Exclude infrastructure folders (TEMPLATES, OPERATIONS, SCRATCH) to reduce CPU load.
