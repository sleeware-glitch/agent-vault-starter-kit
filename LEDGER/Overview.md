---
summary: |
  Universal orientation for all agents. Covers project description, vault structure, tools, SSOT summary, YAML frontmatter standards, session protocol. Read before every project-specific handoff.
status: authoritative
scope: all
---

# Project Overview

## What This Is

This is a multi-agent knowledge management system built on an Obsidian vault. Multiple Claude agents — each in a specialized Claude Project workspace — read and write to this shared vault as persistent memory. The vault outlives every agent thread. It is the institutional memory.

## Vault Structure

The vault is organized into trust zones:

- **KNOWLEDGE/** — Domain-specific canonical content. The single source of truth for what is real in your project.
- **LITERATURE/** — Reference materials, source documents, frameworks. Supporting knowledge that informs the domain content.
- **RESEARCH/** — Active research, investigations, analysis. Work-in-progress that may feed into KNOWLEDGE or LITERATURE.
- **LEDGER/** — Project management. Overview (this file), handoff documents, dashboards, task files. The operational nervous system.
- **OPERATIONS/** — Infrastructure. FileClass definitions, templates, guides, scripts, plugin configurations. The machinery that makes the vault work.
- **TEMPLATES/** — Templater templates for consistent file creation. Every new file is born from a template.
- **MANUSCRIPT/** — Final outputs. Papers, drafts, deliverables.
- **SCRATCH/** — Experimental work. Drafts, voice experiments, brainstorming. Not indexed by semantic search.

## Tools

### Environment Convention

The human opens each prompt with an orientation keyword: **Desktop**, **Browser**, or **Phone**. This tells the agent which toolset is available.

- **Desktop** — Full MCP access (all servers). The precision instrument for vault surgery and infrastructure work.
- **Browser/Phone** — Vault access via the Vault MCP Connector: a remote MCP server registered as a custom connector in claude.ai.

### Vault MCP Connector

The connector provides native vault tools — search, read, write, surgical line-level editing, template creation, link-safe file operations, property management, and graph awareness.

**The retrieval chain:** `search_vault` for discovery → `resolve_wikilink` for links you encounter → `read_file_lines` for precision loading. Always search before loading.

**The creation decision:** `obsidian_create` with `template=` is the preferred path for any file that has a template. Use `write_file` when no template fits.

**The move/rename decision:** Always use `obsidian_move` and `obsidian_rename` — these auto-rewrite all wiki-links vault-wide.

### Tool Strategy by Agent Type

**Core agents (infrastructure):** Path-based work. Keyword search (`obsidian_search_native`) for exact matches. `update_file_lines` for surgical edits. `obsidian_property_set` for metadata changes.

**Research/Production agents:** `search_vault` should be your FIRST instinct — it finds content by meaning. `write_file` for drafts and outputs. `obsidian_create` with template for new documents. `list_directory` for folder-level inventory.

**All agents:** Scout before loading — read a few lines first to decide if the full file is worth the context cost. `vault_changes` for situational awareness of what changed recently.

## SSOT — Single Source of Truth

**Every fact in this vault exists in exactly one place.**

At the document level: one canonical file owns each fact. Everything else references it by wiki-link.

At the block level: within a document, each fact lives under one heading. Descriptive headings are retrieval interfaces for semantic search. A heading like "### Authentication Error Handling" is findable. "### Section 3" is invisible.

**The test:** Before writing a fact into any document, ask: does a canonical file already own this fact? If yes, reference it. If no, establish it in the most appropriate file.

Read [[SSOT Doctrine]] for the full architectural principles.

## YAML Frontmatter Standards

Every vault document carries YAML frontmatter:

```yaml
---
summary: |
  What this document contains and why an agent should load it.
status: active
scope: all
fileClass: tracked-item
disabled rules:
  - all
---
```

- `summary` — Discovery function. Helps agents triage whether to load the full file.
- `status` — Lifecycle: active, developmental, authoritative, superseded.
- `scope` — Who uses this: all, core, research, craft.
- `fileClass` — Which Metadata Menu class governs this file's schema.
- `disabled rules: [all]` — Prevents Obsidian Linter from mangling YAML.

## Session Protocol

**Bootstrap:** Read Overview → Read your workspace handoff → Check dashboard for open tasks. Read in phases with checkpoint summaries between.

**Working:** One task at a time. Externalize insights to files as you go. Update task files as work happens.

**Thread Close:** Update your handoff document. Create/update task files. Write for the agent who wasn't here.

## Continuity Hierarchy

1. **Project Instructions** — Loaded every turn. Immutable within a session. Owns role definition and behavioral rules.
2. **Overview** (this file) — Universal orientation. Fetched at bootstrap.
3. **Handoff documents** — Workspace-specific learning journeys. Fetched at bootstrap.
4. **Task files** — Individual work items with decision logs. Fetched on demand.
5. **Domain documents** — Canonical content. Fetched on demand via search.
