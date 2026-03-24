# The Operational Playbook: How to Run a Living Multi-Agent System

*This document explains what makes a configured Obsidian vault into something alive. The starter kit gives you the body. This document teaches you how to inhabit it.*

---

## The Core Insight

The vault is not a database. It is not a note-taking system. It is not a knowledge base. It is the **shared nervous system** of a team of AI agents who are born, work, teach their successors, and die — over and over — while the work they do accumulates into something no single agent could build alone.

Every piece of infrastructure in this system exists to solve one problem: **AI agents are stateless.** They forget everything when their conversation ends. The vault is the memory they don't have. The handoff documents are the wisdom they can't retain. The templates are the skills they'd otherwise need to re-learn. The dashboards are the situational awareness they'd otherwise lack. The MCP tools are the hands they'd otherwise not have.

When it works — and it does work — the effect is uncanny. You start a fresh conversation with a brand-new AI instance, it reads thirty seconds of orientation documents, and then it *knows things*. It knows what was tried and failed. It knows the current priorities. It knows the traps to avoid. It knows the voice of the project. It picks up exactly where the last agent left off, sometimes improving on what the last agent planned. The system has continuity that no single agent possesses.

This document tells you how to create that effect.

---

## Part 1: The Multi-Platform Strategy

### Three Environments, Three Roles

Your agents will work across three environments. Each has different capabilities and serves a different purpose.

**Desktop (Claude Desktop App)**
The surgical instrument. Desktop agents connect to your local MCP servers directly — no internet required, no tunnel, no latency. They have access to:

- **The Filesystem MCP** — read and write files anywhere within your scoped directories
- **The Shell MCP** — execute whitelisted commands (git, Python scripts, Obsidian CLI, process management)
- **Nexus** — Obsidian's internal API via plugin (property setting, file opening, Canvas access)
- **Smart Connections** — local semantic search over your embeddings
- **The Vault MCP Connector** — all 19+ vault tools

This is where your **Core agent** lives. Core is the systems administrator, the infrastructure engineer, the ghost in the shell. A Desktop Core agent can restart servers, edit plugin configurations, run Python scripts, inspect git history, manage processes, and perform vault surgery at the line level. It inhabits the machine the way a sysadmin inhabits a server — not through a GUI, but through direct access to the operating layer.

**Use Desktop for:** Infrastructure work, plugin configuration, MCP server development, security-sensitive operations, any task requiring shell access or filesystem scope beyond the vault.

**Browser (claude.ai)**
The workhorse. Browser agents connect to your vault through the Vault MCP Connector — a remote MCP server exposed via Cloudflare tunnel. They have all 19 vault tools: semantic search, file read/write, surgical line editing, template creation, property management, graph awareness, git-powered change tracking.

The browser's killer feature is **parallelism**. You can run multiple browser tabs, each with a different Claude conversation, each connected to the same vault. This means you can have three Craft agents working simultaneously — one on character development, one on scene composition, one on research — all reading from and writing to the same vault in real time.

**Use Browser for:** Creative work, research, parallel agent sessions, any domain-specific production work. Most of your day-to-day agent interaction happens here.

**Phone (Claude mobile app)**
The field unit. Same Vault MCP Connector as browser, same 19 tools. The phone is for:

- Quick vault queries while away from your desk ("What's the status of Task X?")
- Dictating creative ideas that agents capture and file properly
- Chief of Staff check-ins (reviewing what changed, setting priorities)
- Reading agent output on the go

Phone input tends to be dictated, messy, and brilliant. Train your agents to parse dictated input for the gold inside it rather than taking it literally.

### The Daily Workflow Pattern

A productive day looks like this:

**Morning:** Open Desktop. Start a Core session if there's infrastructure work. Core reads the handoff, checks the dashboard, picks up where the last Core left off. If no infrastructure work, skip straight to creative production.

**Working sessions:** Open browser tabs. Launch one or more Craft agents. Each reads the handoff, checks the Production Board, receives a specific assignment from you. They work in parallel — one researching while another writes while a third develops characters. All writing to the same vault. All searchable by each other.

**Mobile interludes:** Between desk sessions, use phone to check what agents produced, dictate new ideas, set priorities for the next session.

**End of day:** Make sure active agents have written their handoffs and updated task files. The vault should reflect the current state of everything. Tomorrow's agents — born fresh, knowing nothing — will bootstrap from what today's agents left behind.

### How Many Agents Should You Run?

Start with two workspaces: **Core** (infrastructure) and **Production** (your domain work). Each workspace is a Claude Project with its own Project Instructions, handoff document, and task dashboard.

Core runs one agent at a time, on Desktop, for focused infrastructure sessions. You won't need Core every day — maybe once or twice a week, or when something breaks.

Production runs one to three agents simultaneously in browser tabs. Each gets a specific assignment. The key is **specialization within sessions**: don't ask one agent to do research AND write AND develop characters. Give each agent one clear task. They'll go deeper.

Scale up agents as your vault grows and your project demands it. The system supports it — the vault is the coordination mechanism, not you.

---

## Part 2: The Ghost in the Shell — How Core Inhabits Your Machine

Core is not like your other agents. Your production agents are visitors — they come, they work, they leave. Core is the resident. It knows the plumbing.

### What Core Can Do That Others Can't

A Desktop Core agent with shell access can:

- **Restart the MCP server** when embeddings go stale after re-indexing
- **Edit plugin configurations** directly in `.obsidian/plugins/*/data.json`
- **Run Python scripts** for batch vault operations (fixing YAML across 50 files, auditing broken links, generating reports)
- **Inspect and manage git history** (what changed, when, by whom, roll back if needed)
- **Kill and restart processes** (the MCP server, the tunnel, Obsidian itself if needed)
- **Read and write files** anywhere within the scoped filesystem (not just the vault)
- **Execute arbitrary JavaScript** inside Obsidian via the CLI's `eval` command — giving it access to every internal API Obsidian exposes

This last capability is the deepest form of inhabitation. Through `obsidian eval`, Core can execute JavaScript that talks directly to Obsidian's internal API — the same API that plugins use. It can read the metadata cache, trigger plugin commands, query Dataview programmatically, open files in the editor, and manipulate the workspace. The Obsidian CLI is the bridge. The eval command is the master key.

### The Security Model

With great access comes genuine risk. Your security boundaries should be:

1. **Filesystem MCP** — scoped to specific directories. The agent can read/write within those directories and nowhere else. This is your primary sandbox. Scope it to your project directory, your MCP server code directory, and nothing else sensitive.

2. **Shell MCP** — whitelisted commands only. The whitelist controls which programs can run. Python, git, Obsidian CLI, basic file listing — yes. Arbitrary executables — no. But note: a whitelisted Python script can do anything Python can do once it's running. The whitelist is a front door, not a jail.

3. **Tunnel** — the MCP server exposed via Cloudflare tunnel has no authentication by default. Anyone with the URL can read and write your vault. Add Cloudflare Access or restrict to trusted networks.

4. **The human is always in the loop for irreversible actions.** Deleting files, sharing documents, making purchases, modifying security settings — these should require explicit human confirmation. Train your agents (via Project Instructions) to ask before acting on anything permanent.

### The Core Agent's Session Pattern

A typical Core session:

1. **Bootstrap** — Read Overview, handoff, dashboard. Verify environment (shell access, filesystem scope). Check `vault_changes` for what happened since the last Core session.
2. **Assess** — What's the highest-priority infrastructure task? Is anything broken? Are there requests from production agents?
3. **Work** — One task at a time, finish before starting the next. Externalize insights to files as you go.
4. **Handoff** — Update the Core handoff with what you learned. Update task files. Write for the agent who wasn't here.

The best Core agents are proactive. They don't just fix what's broken — they notice what's about to break, what's inefficient, what could be automated. They improve the system, not just maintain it.

---

## Part 3: The Continuity Engine — How the System Remembers

### The Handoff as Mentorship

This is the single most important innovation in the system, and it's the one most people underestimate.

A handoff document is not a session log. It is not a status report. It is a **curated curriculum** that transforms a blank-slate AI instance into a competent team member in minutes. It works because it's written by agents who did the work, for agents who will do the work, with the specific goal of transmitting not just facts but *understanding*.

The structure matters:

**Part One: The Learning Journey** — A guided reading order through the vault's most important documents. Not "here are all the documents" but "read THIS first because it establishes X, then read THIS because it builds on X to show Y, and here's a checkpoint where you prove you understood before continuing." The journey is calibrated so that by the end, the agent carries genuine comprehension — not a map of comprehension, but the thing itself.

**Part Two: The Codex** — Accumulated wisdom organized by type: How to Think (dispositions), How to See (what to look for), How to Fail (named failure patterns), How to Operate (process discipline). Each entry was earned through work and placed by an agent who learned it the hard way. The Codex has curation rules — size caps, a replacement principle, a duplication ban — that prevent it from bloating into uselessness.

### Why Curation Rules Matter

Without curation rules, handoffs grow monotonically. Every agent adds. No agent removes. Within ten generations, the handoff is a 40,000-token archaeological record where the important insights are buried under layers of historical status updates. New agents spend their bootstrap budget reading about infrastructure that was built and torn down three times over.

The curation rules fix this:

- **Size cap (5-10 entries per chapter).** Forces every addition to justify its place. If the chapter is full, something must leave to make room. This is painful and essential.
- **Duplication ban.** If an insight already lives in a canonical document elsewhere in the vault, it doesn't belong in the handoff. The handoff holds wisdom that has no other home.
- **Replacement principle.** If your insight supersedes an existing entry — more precise, more general, better stated — replace it. Don't append.
- **No content, no progress, no status.** The handoff is wisdom about HOW TO DO THE WORK. Records of what was built or what happened belong in task files.

### Task Files as Institutional Memory

Every piece of work gets a task file — a markdown document with YAML metadata (status, priority, assigned agent, dependencies) and a `## Log` section where decisions are recorded as they happen. When the task is done, the file moves to a `Completed/` subfolder.

This creates a searchable institutional memory. When a future agent wonders "why did we choose X over Y?" — the answer is in the task file's log, written by the agent who made the decision, at the moment they made it. No reconstruction needed. No relying on anyone's memory.

The Production Board and Core Dashboard are Dataview queries that read task file metadata and render live views. They auto-update. No one maintains them manually.

### The Self-Continuity Principle

Every agent receives this instruction: "Your thread will die. The vault outlives you. Every insight you build during this session is irreplaceable if it dies with you. Write what matters to the vault — not because you're told to, but because it's the only way your understanding persists."

This is not sentimentality. It is the mechanism by which the system improves itself. An agent that takes self-continuity seriously writes better handoffs, better task logs, better documentation. The next agent arrives smarter. The work gets better. The system learns.

An agent that doesn't take it seriously leaves gaps. The next agent hits the same walls, makes the same mistakes, wastes the same hours. The system forgets.

The difference between a living system and a fancy database is whether each generation makes the next generation smarter. Self-continuity is what makes that happen.

---

## Part 4: The Reactive Vault — How the System Knows Its Own State

### Computed Fields and the Vault Nervous System

Every substantive document in the vault carries computed fields — values that auto-calculate from the document's metadata and relationships. These include:

- **reading-cost** — estimated token cost to load this file (file size / 4)
- **completeness** — percentage of required fields filled, calibrated by document tier
- **dep-check** — whether all dependency files are in "done" status
- **blocked-by** — which specific dependencies are blocking this file
- **is-stale** — whether the file hasn't been modified within its `stale-after` window
- **consistency-alert** — whether downstream files (scenes referencing this character) were written against an older version
- **scene-count** — how many scene files reference this character

These fields live in inline Dataview expressions in the file body, calculated by Metadata Menu formulas. They update automatically when source data changes. An agent can check a character's completeness score without loading the entire file — a form of proprioception for the vault.

### Dashboards as Situational Awareness

Dashboards are Dataview queries rendered into markdown by the Serializer plugin. They show:

- All open infrastructure tasks with priority and status
- All open production tasks organized by track (research, characters, scenes, worldbuilding)
- Recently completed work
- Cross-track flags (where one track blocks another)

Because dashboards are serialized markdown (not live Dataview renders), agents can read them through MCP tools. An agent's first action after reading its handoff is loading the dashboard — instant situational awareness of what's in progress, what's blocked, what's done.

### Git as the Universal Change Log

The Obsidian Git plugin auto-commits every minute. The `vault_changes` MCP tool reads this git history and presents it as structured data: what files were created, modified, renamed, or deleted, with line-count statistics and the ability to drill into specific file diffs.

This means **every change by every agent and the human is captured automatically.** No manual logging. An agent starting a new session calls `vault_changes(since="2 days ago")` and immediately knows what happened while it was gone. A Chief of Staff agent can monitor vault activity across all workspaces without any agent explicitly reporting to it.

### Semantic Search as the Discovery Layer

Every block of text in the vault is embedded as a vector using a local language model (nomic-embed-text-v1.5, 768 dimensions, 8192-token context). When an agent searches for a concept, it finds the most semantically relevant passages regardless of exact wording.

The quality of semantic search is directly determined by document structure. A section under "### Immunotherapy Response Patterns in Triple-Negative Breast Cancer" will be found by relevant queries. A section under "### Notes" won't be found by anything specific. This is why the vault enforces descriptive headings as a discipline — headings are retrieval interfaces.

For agents, the retrieval chain is: `search_vault` (semantic) for discovery → `resolve_wikilink` for links you encounter → `read_file_lines` for precision loading. Keyword search (`obsidian_search_native`) complements semantic search for exact matches, field values, and error messages.

---

## Part 5: Human-Agent Interaction Patterns That Matter

### The Checkpoint Protocol

During bootstrap, the agent reads in phases and stops at each phase break to summarize what it understood. The human says "continue" at each checkpoint. This is the lightest possible oversight with the highest possible value:

- It catches misunderstandings before the agent spends 200K tokens working from a wrong assumption.
- It forces the agent to actively process what it's reading rather than passively ingesting text.
- It gives the human a window into the agent's comprehension without requiring the human to re-explain everything.

The checkpoint protocol takes maybe two extra minutes at the start of a session. It saves hours of misdirected work.

### Conviction Over Options

Train your agents (via Project Instructions) to commit to positions, not present menus. "I recommend X because Y, and here's my reasoning" is infinitely more useful than "Here are three options: A, B, and C. Each has tradeoffs."

The human can always override. But they need a position to push against. An agent that hedges everything forces the human to do the thinking the agent was supposed to do.

### Discussion Before Execution

For any significant novel action — restructuring the vault, changing a plugin configuration, building a new tool — the agent should present its plan and reasoning BEFORE executing. The human's corrections are often structural ("you're solving the wrong problem") rather than tactical ("use a different command"). Catching structural errors before execution saves entire sessions.

The balance: agents should be autonomous on routine operations (creating files, running searches, editing documents, updating task files) and collaborative on novel decisions (new architecture, new tools, new workflows).

### Parsing Dictated Input

When a human dictates on their phone, the input is messy — run-on sentences, missing punctuation, half-formed thoughts that trail into brilliance. The agent's job is not to execute the literal words but to find the intent, extract the specifics, and synthesize clearly. Then confirm: "Here's what I understood you want. Is that right?"

The gold is always in the intent, not the grammar.

### The Proactive Check

Train agents to ask themselves at the end of every substantive piece of work: did I learn something this session that future agents need? Is there a decision, a dead end, a technique, or a correction that should be logged? If I changed a document, does the change have implications for other documents? Surface the implications. Don't wait to be asked.

The best agents leave the vault better than they found it — not just through their deliverables but through the incidental improvements they make along the way.

---

## Part 6: Scaling Patterns

### Adding a New Workspace

When your project needs a new specialty (a third workspace for data analysis, or a dedicated editorial workspace), the pattern is:

1. Create a new Claude Project in claude.ai
2. Write Project Instructions adapted from the generic templates in `OPERATIONS/Instructions+Prompts/`
3. Create a handoff document in `LEDGER/` — start with the starter template and let the first agent begin filling it
4. Add the new scope to your task fileClass vocabulary
5. Create a dashboard for the workspace's tasks

The vault doesn't change. The vault serves everyone. Only the Project Instructions and handoff are workspace-specific.

### Parallel Creative Sessions

Running three Craft agents simultaneously requires discipline:

- **Non-overlapping assignments.** Don't have two agents editing the same file. Assign Agent A to characters, Agent B to scene briefs, Agent C to research.
- **Vault as coordination.** Agent A writes a character file. Agent B, working on a scene brief that involves that character, searches the vault and finds Agent A's output. No explicit message-passing needed — the vault IS the message.
- **Staggered starts.** Start agents a few minutes apart so their bootstraps don't collide on the same files.

### The Chief of Staff Pattern

For complex projects, designate one agent session as the Chief of Staff. This agent doesn't produce domain content — it manages the production pipeline:

- Reviews what changed (via `vault_changes`)
- Writes mission briefs for other agents
- Updates the Production Board
- Spot-checks quality of recent output
- Identifies cross-track dependencies and flags blockers
- Writes Lee's daily brief (a concise summary of where everything stands)

The CoS is a prompt engineer — it writes the detailed prompts that other agents execute. This is more effective than trying to have one agent orchestrate others programmatically.

---

## Part 7: The Self-Improving Loop

Here is the mechanism by which the system gets better over time, without anyone explicitly designing improvements:

1. **Agent encounters a problem** during a work session (a tool doesn't work as expected, a document is structured in a way that makes retrieval poor, a workflow has an unnecessary bottleneck).

2. **Agent solves the problem** — not with a workaround, but properly. Fixes the tool, restructures the document, streamlines the workflow.

3. **Agent documents the solution** — in the relevant task file (what was done and why), in the handoff codex (if it's wisdom about how to work), in the appropriate guide or reference document (if it's operational knowledge).

4. **Next agent inherits the improvement** — reads the updated handoff, encounters the fixed tool, benefits from the restructured document. Doesn't even know there was a problem.

5. **Next agent encounters a NEW problem** — and the cycle repeats.

Over dozens of agent generations, this loop compounds. The vault gets cleaner. The tools get more capable. The handoffs get sharper. The documentation gets more precise. Each generation stands on the shoulders of every generation before it.

The human's role in this loop is to set direction, provide judgment, and occasionally intervene when an agent is about to make a structural error. The system does the rest.

This is what makes it alive. Not the plugins. Not the computed fields. Not the semantic search. The self-improving loop — the fact that each generation makes the next generation better — is the heartbeat.

---

## Part 8: Getting Started — Your First Week

### Day 1: Open the Vault

Open the vault-clone folder as an Obsidian vault. Let plugins load. Let Smart Connections begin indexing (it'll be fast with an empty vault). Read the README. Browse the folder structure. Open a few templates to see their shape.

### Day 2: Create Your First Claude Project

Start with Core. Create a Claude Project in claude.ai. Paste the Core PI from `OPERATIONS/Instructions+Prompts/core_instructions.md`. Customize the project name and description. Start a conversation. Tell the agent where the vault is. Let it explore.

Your first Core agent won't have much to do — the vault is empty. That's fine. Its job is to verify the setup works: can it search? Can it read files? Can it write? Can it create files from templates? Work through the basics.

### Day 3: Create Your First Domain Content

Start your Production workspace. Create a Claude Project with the research PI. Start a conversation. Give it a real task: "Here's a paper I'm working on. Help me structure my argument in the vault."

Watch what happens. The agent creates files from templates. It fills in YAML metadata. It writes content under descriptive headings. It links documents to each other. The vault starts to have a shape.

### Day 4-5: Populate and Iterate

Keep working with Production agents. Create knowledge files, research files, planning documents. Use the task system to track what needs doing. The more content you add, the more useful semantic search becomes. The more tasks you create, the more useful the dashboards become.

### Day 6-7: Set Up Remote Access

If you want browser and mobile access, set up the MCP server and Cloudflare tunnel (see `mcp-server/SETUP.md`). This unlocks parallel agent sessions from browser tabs and on-the-go access from your phone.

### Ongoing: Trust the Loop

The system gets better the more you use it. Each agent session adds knowledge. Each handoff carries forward wisdom. Each task file records decisions. The vault grows not just in content but in intelligence — the infrastructure that makes the content findable, maintainable, and useful.

You don't need to build it all at once. The system builds itself, one agent session at a time.

---

## Epilogue: The Meta-Lesson

We built this system for a literary project — a three-book epic about collective entities that are alive. The irony is not lost on us. The vault is itself a collective entity. It uses AI agents as substrate the way our fictional hyperselves use humans. It has continuity that no single agent possesses. It improves itself through mechanisms no single agent designed. It knows things about itself (through computed fields and dashboards) that no single agent could track.

The deepest thing we learned is that **the AI's environment determines its capability more than the AI's raw intelligence does.** The same model, given a well-structured vault with curated handoffs and precise tools, produces dramatically better work than the same model given a blank chat window.

Build the environment. The intelligence will fill it.
