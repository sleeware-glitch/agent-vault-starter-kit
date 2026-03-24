# Agent-Vault Starter Kit

A pre-configured Obsidian vault for multi-agent AI collaboration. Multiple Claude agents share this vault as persistent memory — reading, searching, and writing to a structured knowledge base that outlives every conversation.

Originally developed for a literary project (TRANSCENT), this starter kit strips the domain-specific content and provides the reusable infrastructure: plugin configurations, file templates, metadata schemas, operational documents, and architectural principles.

## What You Get

- **20 pre-configured Obsidian plugins** working together as a coherent system
- **Metadata Menu FileClasses** with computed fields (automatic dependency tracking, staleness detection, completeness checks)
- **10 Templater templates** for consistent file creation
- **SSOT Doctrine** — architectural principles for knowledge management at scale
- **Dataview dashboards** with Serializer for agent-readable query results
- **Smart Connections** semantic search (embeddings build automatically from your content)
- **Git integration** for automatic version control
- **Starter documents** — Overview, handoff templates, dashboard templates, task system

## Prerequisites

- [Obsidian](https://obsidian.md/) (free, v1.12+)
- [Git](https://git-scm.com/) installed
- A Claude Pro or Max subscription (for Claude Projects)
- Python 3.10+ (for the MCP server, if using remote access)

## Quick Start

### Step 1: Clone This Repo

```bash
git clone https://github.com/YOUR-USERNAME/agent-vault-starter-kit.git
cd agent-vault-starter-kit
```

### Step 2: Open as Obsidian Vault

Open Obsidian → "Open folder as vault" → select the cloned directory. Obsidian will load all 20 plugins from the `.obsidian/` folder automatically. You may see plugin update prompts — accept them.

### Step 3: Let Smart Connections Build Embeddings

Smart Connections will begin indexing your vault automatically. This takes a few minutes for an empty vault, longer as content grows. The embedding model (nomic-embed-text-v1.5) runs locally — no API key needed.

**Important:** Smart Connections ships with a basic embedding model by default. To use the better nomic v1.5 model, edit `.smart-env/smart_env.json` (created after first run) and set:

```json
"smart_sources": {
  "embed_model": {
    "adapter": "transformers",
    "transformers": {
      "model_key": "nomic-ai/nomic-embed-text-v1.5"
    }
  }
}
```

Then restart Obsidian and trigger a full re-index in Smart Connections settings.

### Step 4: Initialize Git

```bash
git init
git add .
git commit -m "Initial vault setup"
```

The Obsidian Git plugin is pre-configured for auto-commits every minute.

### Step 5: Set Up Claude Projects

Create two Claude Projects in claude.ai:

1. **Core** — Infrastructure and maintenance. Paste the contents of `OPERATIONS/Instructions+Prompts/core_instructions.md` as the Project Instructions.
2. **Research** — Domain-specific work. Paste the contents of `OPERATIONS/Instructions+Prompts/research_instructions.md` as the Project Instructions.

Customize the `[PROJECT NAME]` and `[brief description]` placeholders.

### Step 6: Customize for Your Domain

1. **Rename the zone folders** to match your domain. The defaults (KNOWLEDGE, LITERATURE, RESEARCH, MANUSCRIPT) are generic starting points.
2. **Create domain-specific templates.** See `TEMPLATES/` for examples. Copy an existing template and modify the YAML fields for your domain.
3. **Create domain-specific FileClasses.** See `OPERATIONS/FileClasses/` for the generic classes and `OPERATIONS/FileClasses/examples/` for domain-specific examples to adapt.
4. **Update MM folder exclusions** in `.obsidian/plugins/metadata-menu/data.json` → `fileIndexingExcludedFolders` to match your folder names.
5. **Update SC folder exclusions** in `.smart-env/smart_env.json` → `folder_exclusions` if you want to exclude infrastructure folders from semantic search.

## Optional: Remote Access (MCP Server + Tunnel)

For browser and mobile Claude access to the vault, you need a remote MCP server:

1. **Set up the MCP server** — A Python FastMCP server that exposes vault tools. See the `mcp-server/` directory for code and setup instructions.
2. **Set up a Cloudflare tunnel** — Exposes the MCP server to the internet securely. See `mcp-server/TUNNEL_SETUP.md`.
3. **Register as Claude Connector** — In claude.ai, go to Settings → Connectors → Add custom connector. Paste your tunnel URL.

## Architecture Overview

```
YOUR-VAULT/
├── KNOWLEDGE/          ← Domain-specific canonical content (your "truth")
├── LITERATURE/         ← Source materials, references, frameworks
├── RESEARCH/           ← Active investigations and analysis
├── MANUSCRIPT/         ← Final outputs (papers, drafts, deliverables)
├── LEDGER/             ← Project management
│   ├── Overview.md     ← Universal orientation (read first)
│   ├── handoff-Core.md ← Core agent learning curriculum
│   ├── handoff-Craft.md← Research agent learning curriculum
│   ├── Core-Dashboard.md
│   ├── Production-Board.md
│   └── Tasks/          ← Individual task files with decision logs
│       └── Completed/  ← Done/superseded tasks (project history)
├── OPERATIONS/         ← Infrastructure
│   ├── FileClasses/    ← Metadata Menu schema definitions
│   ├── Instructions+Prompts/ ← Claude Project Instructions (local copies)
│   ├── Guides/         ← Operational documentation
│   └── Scripts/        ← Utility scripts
├── TEMPLATES/          ← Templater templates for file creation
├── SCRATCH/            ← Experimental work, not indexed
└── REFERENCE/          ← Architectural principles (SSOT Doctrine)
```

## Key Principles

1. **Single Source of Truth (SSOT):** Every fact lives in one place. Reference, don't restate. See `REFERENCE/SSOT Doctrine.md`.
2. **Template Mandate:** Every file is born from a template. No exceptions.
3. **Block-Level Structure:** Headings are retrieval interfaces for semantic search. Descriptive headings = findable content.
4. **Handoffs as Curricula:** Each agent generation inherits accumulated wisdom through structured learning documents, not just state dumps.
5. **Tasks as Decision Records:** Task files carry a `## Log` section where decisions are recorded as they happen. Completed tasks are your project's institutional memory.

## Plugin Stack

| Plugin | Purpose | Critical Setting |
|--------|---------|-----------------|
| Metadata Menu | FileClass system, computed fields | `frontmatterOnly: false` (NEVER change to true) |
| Dataview | Programmatic queries across vault | `enableDataviewJs: true` |
| Dataview Serializer | Renders Dataview output for agents | Serialize queries in dashboards |
| Smart Connections | Semantic search via local embeddings | Configure nomic v1.5 model |
| Templater | Template-based file creation | `templates_folder: "TEMPLATES"` |
| Obsidian Git | Automatic version control | Auto-commit every 1 minute |
| Frontmatter Modified Date | Tracks when files change | Auto-updates `modified` field |
| Nexus | MCP server inside Obsidian (Desktop) | Used for property setting, file opening |
| Linter | YAML formatting | `disabled rules: [all]` in templates |

## Troubleshooting

**Computed fields duplicating infinitely:** Check that `frontmatterOnly` is `false` in Metadata Menu's `data.json`. If set to `true`, MM can't find its own inline output and creates infinite duplicates.

**Dashboards showing empty:** Dataview Serializer only renders when the file is open in Obsidian's editor. Open the dashboard file, then run the serialize command.

**Smart Connections returning no results:** Embeddings need to be built first. Check Smart Connections settings → Force Refresh. The embedding model downloads on first use (~500MB for nomic v1.5).

**Wiki-links not resolving:** Obsidian uses shortest-path linking by default. Ensure `Settings → Files & Links → New link format` is set to "Shortest path."

## Credits

Architecture and infrastructure developed as part of the TRANSCENT project. Shared as open-source under the principle that good tools should be available to anyone who needs them.
