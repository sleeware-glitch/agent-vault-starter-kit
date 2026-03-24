---
summary: |
  The single source of truth doctrine. Two nested levels: every fact lives in one canonical file (document-level SSOT), and within that file every fact lives in one section under a descriptive heading (block-level SSOT). Governs how the vault is organized, how documents are structured, and how agents retrieve content. Read before writing any vault document.
status: active
scope: all
stale-after: 180d
document-role: reference
fileClass: reference-doc
disabled rules:
  - all
---

# The Single Source of Truth Doctrine

## The Principle in One Breath

Every fact in this vault exists in exactly one place. At the document level, that means one canonical file owns each fact. At the block level, that means within a document, each fact lives under one heading. Everything else references it. When a fact changes, it changes in one place.

This is not a preference. It is the architectural law that makes the vault work. Without it, facts drift, agents inherit wrong information with high confidence, and the cost of correction scales with every duplicate.

---

## Level 1: Document-Level SSOT

### What It Means

Each kind of content has a canonical home — one file where that content is authoritative. Everything else points to that file by wiki-link, transclusion, or fetch instruction rather than restating the content.

- Research methodology standards → lives in its canonical reference file
- Key domain definitions → live in their canonical knowledge files
- Settled project decisions → live in the relevant task file's `## Log` section in `LEDGER/Tasks/`
- How the vault works → lives in [[Overview]]

### The Test

Before writing a fact into any document, ask: **does a canonical file already own this fact?** If yes, reference it. If no, either create the canonical file first or establish the fact in the most appropriate existing file.

### How References Work

**Wiki-links** (`[[Filename]]`) for navigation: "See [[Methodology]] for the full protocol." Obsidian auto-updates these when files move or are renamed.

**Transclusion** (`![[File#Section]]`) for embedding: renders the source content inline in Obsidian's editor. Agents see raw syntax and should fetch the source file.

**Fetch instructions** in handoffs: "Read [[document]] — it tells you X." The handoff points to the document; it does not reproduce the document's contents.

### What Document-Level SSOT Prevents

**Drift.** A key finding stated in three files will eventually be three different findings. A structural decision restated in a handoff will eventually contradict the original. One canonical source eliminates this.

**Stale confidence.** Agents trust what they read. A restated fact carries the same apparent authority as the original, even when the original has been updated and the copy hasn't. The copy becomes a lie with the voice of truth.

**Update cost scaling.** When a fact changes, updating one file is trivial. Hunting down seven restatements across the vault is expensive and error-prone. Every duplicate is a maintenance debt.

---

## Level 2: Block-Level SSOT

### What It Means

Within a document, the unit of content is the **block** — everything under a single heading. Each block should contain one domain of content, and each fact should appear in only one block within the document.

This matters because the vault uses semantic search (Smart Connections) to find content at the block level. Each block gets an embedding based on its content. When an agent queries for something, the search returns the blocks whose embeddings are closest to the query. The quality of retrieval depends entirely on what's IN each block.

### Why Block Structure Determines Search Quality

A block that mixes experimental data, literature review, and methodological critique produces a **diluted embedding**. A search for "experimental results from the Phase II trial" returns it with low confidence because the relevant content is averaged with unrelated methodological discussion.

A block that contains ONLY experimental results under a descriptive heading (like `### Phase II Trial Results: Tumor Response Rates by Dosage`) produces a **tight embedding** that matches queries with high confidence.

Same content. Dramatically different retrieval quality. The difference is structure.

### The Block-Level Rules

**Each fact exists once within a document.** If the same finding appears in both an analysis section and a conclusion, keep the richer version and cut the other. A "summary" section that restates content from earlier sections is a block-level SSOT violation, even though it's within the same file.

**Each block serves one domain.** Experimental data lives under its own heading. Theoretical frameworks live under theirs. Literature review lives under its own. Don't mix domains in a single section — it dilutes the embedding and makes the block harder to find.

**Headings are retrieval interfaces.** Every heading must be semantically descriptive enough that its embedding captures what the section contains. `### Section 3` is invisible to search. `### Immunotherapy Response Patterns in Triple-Negative Breast Cancer` is a beacon. The heading IS the findability of the block.

**When a document is dominated by one domain, don't force content into multiple sections.** A theoretical framework document that is 90% conceptual should be structured as one rich section with well-differentiated subheadings — not artificially split into thin sections with overlapping content.

---

## How the Two Levels Work Together

Document-level SSOT determines **where in the vault** a fact lives. Block-level SSOT determines **where in the document** a fact lives. Together they create a two-level addressing system: any fact in the vault can be located by file + heading.

This is not just organizational tidiness. It is the architecture that makes semantic retrieval work. When an agent searches for a specific finding, the search returns specific blocks from specific files. If the fact lives in one block in one file, the agent gets one clean result. If the same fact is scattered across three blocks in two files, the agent gets noisy results with unclear authority.

### Document Organization Principles

Documents serve one of two structural roles:

**Domain documents** are comprehensive references for a single domain. A methodology file owns everything about how research is conducted. A protocol file owns everything about a specific experimental procedure. These documents are deep — they contain everything an agent needs to know about their domain, organized into blocks by sub-topic.

**Task documents** are organized around a specific purpose. Research documents investigate a question. Planning documents develop a structure. These documents may contain content from multiple domains (data, theory, context) organized into blocks by domain so that different agents can find what they need.

Both types follow the same block-level discipline: descriptive headings, one domain per block, no internal duplication.

---

## Practical Application

### When Writing a New Document

1. **Check document-level SSOT.** Does this content belong in an existing canonical file? If the fact is about research methodology, it may belong in an existing methodology reference, not a new document.
2. **If creating a new document, organize by blocks.** Separate content by domain under descriptive headings. Each heading should be findable by semantic search.
3. **Don't restate facts across sections.** If a finding serves both a data analysis narrative and a conclusions section, place it where it's primary. Reference it from the other section by implication, not restatement.

### When Updating an Existing Document

1. **Update the fact at its canonical location.** Don't add a correction elsewhere and leave the original unchanged.
2. **Check for internal duplication.** If the document has a summary that restates earlier sections, the summary may need updating too — or better, the summary should be eliminated in favor of a well-structured document that doesn't need one.

### When Writing a Handoff

Handoffs are the hardest SSOT test. The temptation is to reproduce canonical facts for convenience. The doctrine says: point to them, don't restate them. A handoff that restates key findings from domain files will eventually contradict those files. A handoff that says "Read [[Methodology]] for the full protocol" stays correct forever.

The test: **could this handoff survive unchanged if three canonical documents were updated tomorrow?** If yes, SSOT is maintained. If no, the handoff is restating facts that belong elsewhere.

---

## Edge Cases

### The Summary Field in Frontmatter

The `summary` field in YAML frontmatter is a deliberate, controlled exception. It restates what the document contains. This is acceptable because: (1) the summary serves a specific discovery function (dashboard indexing, agent triage), (2) it is always read in the context of the document it describes, and (3) the cost of the summary drifting from the document is low because any agent who loads the document immediately sees the real content.

### Handoff Integration Content

Handoffs contain integration — how decisions connect, why one led to another, the reasoning topology that no single canonical document captures. This IS original content, not a restatement. It belongs in the handoff.

### Cross-References Within Documents

A document may reference its own earlier sections: "the experimental design described above." This is navigation, not duplication. The fact lives in one block; the cross-reference points to it.

### Facts vs. Applications

A **fact** is something that can change at the source: "The response rate was 34%." An **application** is an instruction derived from that fact: "Design the next trial with a minimum sample size of 200 based on the 34% response rate." These have different lifecycles.

Facts live in canonical files (KNOWLEDGE/, LITERATURE/). Applications live in working documents and plans. When the underlying fact changes, the application needs re-derivation.

The `depends-on` frontmatter field makes these dependencies discoverable. A planning document that derives decisions from a data file should list it in `depends-on`. When the source data changes, the dependency chain is visible.

### Final Outputs and Inevitable Drift

A manuscript or paper can't be composed entirely of wiki-links. It must contain facts inline. This is unavoidable duplication.

What SSOT provides is not the elimination of this duplication but its **discoverability**. When a canonical fact changes, the `depends-on` chain and semantic search can surface which outputs were written against the old version. SSOT makes staleness traceable. The revision still requires human judgment.
