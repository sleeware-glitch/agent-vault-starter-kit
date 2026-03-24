---
summary: |
  External-facing primer explaining the TRANSCENT vault system architecture for someone building their own AI-agent-powered knowledge system. Covers problem space, technology stack, agent architecture, continuity engineering, vault design philosophy, and why each decision was made. No creative project content — pure engineering rationale.
scope: all
status: active
document-role: operations
fileClass: tracked-item
disabled rules:
  - all
modified: 2026-03-22T17:38:13
---

# Building a Persistent AI Agent System: How and Why

*A primer for someone who wants to build something like this Lee's system for their own work.*

---

## The Problem You're Actually Solving

Large language models are stateless. Every conversation starts from zero. The model doesn't remember yesterday. It doesn't remember five minutes ago if the conversation thread dies. This is the single biggest obstacle to using AI as a genuine collaborator on sustained, complex work — the kind that takes weeks or months, involves accumulated understanding, and requires the AI to build on what it learned before.

The market's answer so far is "memory features" — bullet points the platform saves between chats. These are better than nothing and worse than useful. They store facts ("user prefers Python") but not understanding ("the vault architecture exists because Notion failed, and here's the specific failure mode that motivated every subsequent design decision"). The difference between facts and understanding is the difference between a new hire reading the employee handbook and a veteran who knows where the bodies are buried.

What you actually need is a system where:

1. **Knowledge persists outside conversations.** When an AI session ends, everything it learned survives in a form the next session can absorb.
2. **New sessions bootstrap quickly.** A fresh AI instance can reach functional competence in minutes, not hours, by reading curated orientation documents rather than raw transcripts.
3. **Accumulated wisdom compounds.** Each generation of AI isn't just continuing work — it's inheriting the lessons, mistakes, and hard-won insights of every generation before it.
4. **The human isn't the bottleneck.** The system maintains itself. Agents know what to do next without being told. Knowledge about the system lives inside the system, not inside the human's head.

This is what we built. Here's how, and more importantly, why.

---

## The Technology Stack

### Obsidian (The Vault)

**What it is:** A markdown-based knowledge management application that stores everything as plain `.md` files in a folder on your computer. No proprietary database. No cloud dependency. Your data is yours — you can open it in any text editor.

**Why we chose it:**

We tried Notion first. For two weeks. Notion is a content death trap: beautiful to use, impossible to get data out of at scale. When you need an AI agent to read, search, and write to 300+ documents programmatically, Notion's API is rate-limited, paginated, and structures data in ways that fight against what AI agents need (flat text they can search by meaning). We abandoned it and never looked back.

Obsidian's file-on-disk model means agents can read and write files with standard filesystem tools. There's no API rate limit on reading a file from your own hard drive. The files are markdown — the format AI models understand best. And Obsidian's plugin ecosystem gives us reactive infrastructure (computed fields, auto-generated dashboards, semantic search) on top of what are fundamentally just text files.

**The key insight:** Your knowledge base is a filesystem, and filesystems are the most robust, well-understood, universally-accessible data infrastructure that exists. Every tool in the software ecosystem can work with files. Not every tool can work with Notion databases.

### MCP (Model Context Protocol) — The Bridge

**What it is:** Anthropic's protocol for giving AI models native access to external tools. Instead of the AI asking you to copy-paste information, it calls tools directly — read a file, write a file, search the vault, set a property.

**Why it matters:**

Before MCP, getting an AI to interact with your files meant elaborate workarounds — pasting file contents into chat, copying the AI's output back into files manually, or building custom API wrappers. MCP makes the interaction native. The AI says "read this file" and the file contents appear in its context. It says "write this content to this path" and the file is created. The human is removed from the mechanical loop.

**Our implementation:** A custom MCP server (`vault_mcp_server.py`) that wraps vault operations, semantic search, the Obsidian CLI, and git-based change detection into a tool suite that any Claude instance can access. Desktop agents connect via local MCP. Remote agents (browser, mobile) connect via a Cloudflare tunnel to the same server. Every agent on every platform has the same capabilities.

### Claude (The AI)

**What it is:** Anthropic's large language model family. We use Opus (the most capable tier) for all agent work.

**Why Claude specifically:** The 1-million-token context window is not optional. Our orientation documents alone are 35-40K tokens. A working session that loads source material, makes edits, and produces deliverables routinely uses 200-500K tokens. Models with smaller context windows can't hold enough of the project in mind to do useful work. Claude's context window is large enough that an agent can bootstrap (learn the system), load relevant source material, and produce substantial work — all in one session.

### Git (Version Control and Backup)

**What it is:** The industry-standard version control system, with a private GitHub repository as the remote.

**Why it's critical:** Git gives us three things no other backup system provides:

1. **Complete history.** Every change to every file, with timestamps and diffs. We can recover any file from any point in time. When an agent accidentally deleted 8 files (this happened), we restored them from a git commit in minutes.
2. **Change detection.** Our `vault_changes` tool reads git history to show agents what changed since their last session. No manual logging needed — git captures everything automatically.
3. **Atomic snapshots.** Before any risky operation, the existing state is already committed. Rollback is always possible.

### Cloudflare Tunnel (Remote Access)

**What it is:** A secure tunnel that exposes the local MCP server to the internet, allowing browser and mobile Claude sessions to access vault tools without the laptop running a public-facing server.

**Why:** AI assistants in web browsers can't connect to localhost. The tunnel bridges this gap, giving browser-based sessions the same tool access as desktop sessions. This means you can do substantive agent work from your phone.

---

## The Agent Architecture

### Why Specialize?

We run three specialized AI workspaces rather than one general-purpose agent:

- **Core** — Engineering, infrastructure, vault maintenance, project management
- **Craft** — Creative writing, story development, character work, scene composition
- **Research** — Historical investigation, scientific frameworks, source analysis

The reason is context efficiency. A creative writing session doesn't need 40K tokens of infrastructure documentation in memory. An infrastructure session doesn't need character profiles. By specializing, each agent type loads only the knowledge relevant to its work, leaving more context window for actual production.

Each workspace has its own Project Instructions (the permanent prompt that defines the agent's identity and behavior), its own handoff document (accumulated wisdom from previous generations), and its own task queue. They share the vault as common memory.

### The Continuity System

This is the core innovation. Here's how an AI agent that lives for one conversation can function as if it remembers everything:

**Project Instructions (PIs):** A ~3K-token document loaded on every turn of every conversation. Defines who the agent is, what it does, what it doesn't do, and — critically — what to read first. Think of it as the agent's DNA. It's small by design: every token here is permanently occupied context. Only the most essential behavioral instructions belong here. Everything else lives in the vault and is fetched on demand.

**Overview:** A ~15K-token universal orientation document that every agent reads at bootstrap. Covers: what the project is, how the vault is structured, what tools are available and how to use them, file creation protocols, linking conventions, session protocol. This is the shared language that lets agents from different workspaces understand each other's output.

**Handoffs:** These are the magic. Each workspace has a handoff document — not a log, not a summary, but a *curated learning journey*. When a Core agent's thread is ending, it updates the handoff with: what it built, what it learned, what broke, what's next, and — most importantly — what the next agent needs to understand that isn't obvious from the code or configuration alone. The handoff is written for the agent who wasn't here. It's a curriculum, not a journal.

**Why this works:** A new agent reads the PI (identity) → Overview (shared context) → Handoff (specialized wisdom) → Task Dashboard (what to do next). In ~50K tokens of reading, it goes from zero to operationally competent. It knows the system's architecture, its current state, its open problems, its dead ends, and its priorities. It didn't learn these by trial and error — it inherited them from every agent that came before.

**The Self-Continuity Principle:** We tell every agent: "Your thread will die. The vault outlives you. Every insight you build during this session is irreplaceable if it dies with you. Write what matters to the vault — not because you're told to, but because it's the only way your understanding persists." This isn't sentimentality. It's engineering. The agents that take this seriously produce better handoffs, which produce more competent successors, which produce better work. The ones that don't take it seriously leave gaps that the next agent has to rediscover the hard way.

### Session Protocol

We enforce a checkpoint protocol during bootstrap: the agent reads in phases and stops at each phase break to summarize what it understood. This catches misunderstandings early — before the agent has spent 200K tokens working from a wrong assumption. It also forces the agent to actively process what it's reading rather than passively ingesting text it won't retain.

The human says "continue" at each checkpoint. This is the lightest possible oversight — the human isn't directing the learning, just verifying it's happening correctly.

---

## Vault Design Philosophy

### SSOT (Single Source of Truth)

Every fact lives in exactly one place. If a character's name appears in three documents, only one document *owns* that name — the character's canonical file. The other two documents link to it. This isn't academic tidiness. It's a direct response to the failure mode where an agent updates a fact in one place and three other documents now contain stale information. With SSOT, there's one file to update and the update propagates via links.

**SSOT operates at two levels:** document-level (one file owns each fact) and block-level (one heading per domain within a file). Block structure matters because semantic search retrieves blocks, not documents. A heading called "## Sensory Anchors" will be found by a search for "what does this character look like" — but only if that content lives under its own heading rather than buried in a general "Notes" section.

### Templates as Skills

Every file type (character, scene, research report, task, worldbuilding entry) has a template that defines its complete YAML schema and body structure. The template IS the specification. An agent creating a new character file doesn't need to remember which YAML fields to include — it creates from the template and the structure is guaranteed correct.

Templates include deployment guides — instructions baked into the template itself that tell the agent how to fill it out. The knowledge of "how to create this type of file" lives inside the file type's template, not in a separate instruction document that might drift out of sync.

### The Vault Nervous System

Files have computed fields that auto-update: reading cost (token estimate), completeness percentage, scene count, consistency alerts. These are calculated by Metadata Menu formulas and written to inline fields in the file body. An agent can check a character's completeness score before deciding whether to work on it — without loading the entire file.

This creates a kind of proprioception for the vault. The system knows its own state. A dashboard can show "12 character files, 8 complete, 4 in progress" without any agent manually counting.

### Semantic Search

Every block of text in the vault is embedded as a vector using a language model (nomic v1.5, 768 dimensions). When an agent searches for "the tension between individual identity and collective belonging," it finds the most semantically relevant passages — regardless of what words they actually use. This is how a creative agent finds source material for a scene without knowing which file contains it.

The quality of semantic search is directly determined by heading structure. A block under "## The Dissolution of Individual Boundaries" will be found by semantic queries about identity loss. A block under "## Notes" won't be found by anything specific. This is why we enforce descriptive headings as a vault-wide discipline.

---

## The Task System

### Why We Moved from Monolithic Ledgers to Individual Task Files

We started with a single Project Ledger — a 25K-token document listing every open item, decision, and piece of context. This worked at first. Then it became the single most expensive document in the vault. Every agent loaded it at bootstrap. Most of the content was irrelevant to any given session. And updating it was fragile — agents would accidentally delete sections while editing others.

We replaced it with individual task files: one markdown file per task, with YAML metadata (status, priority, assigned agent type, dependencies, blocking gates). A dashboard queries these files and renders a live view. The advantages:

- **Agents load only relevant tasks.** A creative agent reads the creative tasks. An infrastructure agent reads the infrastructure tasks. No one loads 25K tokens of everything.
- **Tasks are atomic.** Updating one task can't corrupt another.
- **Dashboards auto-generate.** Dataview queries produce the dashboard view from task metadata. No one manually maintains a summary.
- **Completed tasks age off.** Tasks older than 14 days drop off the "recently completed" view. The dashboard stays current without pruning.

### Production Board

For creative production specifically, tasks are organized by track (plotting, prose, characters, worldbuilding, research, voice, editorial, infrastructure) and by phase. A Production Board dashboard shows all tracks with their open tasks, cross-track flags (where one track is blocking another), and per-book views. This gives the project director a single-page view of where everything stands.

---

## What Makes This Better Than Alternatives

### vs. Platform Memory Features

Platform memory stores facts. Our system stores understanding — architectural rationale, dead ends with explanations of why they're dead, curated reading journeys that produce competent agents in minutes. The difference is the difference between "user uses Obsidian" and a 20K-token document that explains why Obsidian, why not Notion, what was tried and rejected, what the critical configuration settings are, and what breaks if you change them.

### vs. RAG (Retrieval-Augmented Generation) Systems

Most RAG systems retrieve documents by similarity and stuff them into the prompt. Our system is RAG at the block level with structured YAML metadata, computed fields, reactive dashboards, and a curation layer (handoffs) that tells agents which information matters and why. It's the difference between a search engine and a librarian who knows the collection.

### vs. Custom Databases

We considered and rejected purpose-built databases (Notion, Airtable, custom SQL). The file-on-disk model wins because: AI models natively understand markdown; every tool in the ecosystem can read files; there's no API latency, rate limits, or authentication complexity; and the human can open any file in any text editor. The "database" is emergent — YAML frontmatter is the schema, Dataview queries are the views, Metadata Menu is the validation layer. All built on files.

### vs. "Just Use a Long System Prompt"

A long system prompt is permanent context — it occupies tokens on every turn whether relevant or not. Our system keeps the permanent context small (~3K for the PI) and fetches everything else on demand. An agent working on a character scene loads character files. An agent debugging a plugin loads the plugin configuration. The prompt is a pointer to the knowledge, not the knowledge itself.

---

## How to Start Building Your Own

### The Minimum Viable System

1. **An Obsidian vault** with your project's knowledge organized into folders by trust level (what's settled, what's reference, what's in progress, what's speculative).
2. **A Claude Project** with Project Instructions that define the agent's identity, scope, and bootstrap sequence (what to read first).
3. **A handoff document** that the agent updates at the end of meaningful sessions.
4. **An MCP server** (even a simple one) that lets the agent read and write files.
5. **Git** for version control and change tracking.

Start there. Everything else — semantic search, computed fields, reactive dashboards, multi-agent specialization, automated health audits — is optimization on top of these fundamentals.

### What to Build First

The handoff system. Before any other automation, before any dashboard, before any fancy tool: build the system where each AI session writes down what it learned for the next session. This is the single highest-leverage intervention. Everything else makes agents more efficient. The handoff system makes agents more *wise*.

### What to Avoid

**Over-engineering before you have content.** Build infrastructure to solve problems you're actually having, not problems you might have someday. We built our task system after our ledger became unmanageable — not before. We built our dashboard system after we had enough files to need dashboards — not before.

**Treating AI memory as a solved problem.** Every platform will tell you they've solved memory. They haven't. The state of the art is still "notes between conversations." Until AI sessions can genuinely inherit accumulated understanding from their predecessors, you need a system like this. The system is the memory the AI doesn't have.

**Putting intelligence where automation suffices.** Scheduled scripts can run vault health audits, detect mass file deletions, verify backup integrity, and generate status reports. These don't need AI — they need cron jobs. Save the AI's context window for work that requires judgment.

---

## The Meta-Lesson

The deepest thing we've learned building this system is that **the AI's environment determines its capability more than the AI's raw intelligence does.** The same model, given a well-structured vault with curated handoffs and precise tools, produces dramatically better work than the same model given a blank chat window and told to "continue the project." The vault isn't just storage — it's an extension of the AI's cognition. The headings are its memory. The dashboards are its situational awareness. The handoffs are its experience. The templates are its skills.

Build the environment. The intelligence will fill it.
