# Repo Story: A Process for Walking Reviewers Through a Repository

A repeatable methodology for surveying a collection of repositories, inventorying the features within them, tracing each feature to the prompts that shaped it, and producing audio walkthroughs that show a reviewer what exists and how it was steered into existence.

---

## Pipeline Shape

```
Survey → Explore → Inventory → Research → Narrate
```

This shape is the invariant. Everything else — how many files to read, how many agents to launch, how long to write — is determined by the material, decided fresh each time.

Each phase has a different mode of thinking and a different unit of work:

- **Survey**: Breadth-first, shallow. Get the lay of the land, including where each repo's prompt provenance lives. The unit is the collection.
- **Explore**: Depth-first, per-project, parallel. Catalog each project's user-visible features exactly as they exist. The unit is the repo.
- **Inventory**: Organize features into a tour. Group them into chapters a reviewer would walk in order. The unit transitions from repo to chapter.
- **Research**: Depth-first, per-chapter, parallel. Verify current behavior and trace prompt provenance. The unit is the chapter.
- **Narrate**: Walkthrough composition. Feature, behavior, and the prompt behind it, as audio prose. The unit is the chapter.

The repo is where you find things. The chapter is how you present them. Exploration is organized by repo because features live in repos. Everything from inventory onward is organized by chapter because the final output is a tour, and tours have stops.

The pipeline is not strictly one-pass. Later phases will reveal errors and gaps in earlier phases. When that happens, go back and revise. Every phase produces drafts, not finished artifacts.

---

## Before You Start

**Provenance sources.** The walkthrough quotes the prompts that shaped each feature. Establish up front, per repo, where those live: session prompt exports (verbatim), session recaps (paraphrase), curated prompt histories, git log. Coverage varies — some repos have every prompt on record, some only recaps and commit messages. Know which you have before promising quotes.

**Audience.** The listener is a reviewer with limited time. Every phase optimizes for their question: what does this do, and what prompt made it so?

---

## Phase 1: Survey

**Goal:** Understand the landscape before diving into any single project.

Identify every project in the target set. For each one, read enough to produce a short summary of what it is, who made it, and what it's built with — and locate its provenance sources. Note relationships between repos (dependencies, one generating another) — these determine a sensible tour order later.

**Output:** A catalog of projects with enough context to guide exploration, including provenance coverage per repo.

---

## Phase 2: Feature Inventory Exploration

**Goal:** Catalog each project's features as they currently exist.

For each project, dispatch independent exploration. The explorer reads until it can state, for every user-visible feature: what it's called, where it lives, how it's invoked, what goes in, what comes out, and its exact current settings.

**What to record:** Exact command lines, exact paths, exact constants and defaults, concrete input→output behavior. Vague summaries are useless downstream.

**What not to chase:** Idea lineage, the wider field, project philosophy. An unconventional choice gets one or two sentences where it explains visible behavior, then move on.

**Output:** Per-project feature-inventory dossiers — raw, detailed, internal working documents. Drafts; Phase 4 corrects them.

**Parallelism:** Independent projects can be explored simultaneously.

---

## Phase 3: Inventory Organization

**Goal:** Turn per-repo feature lists into a tour.

Read all the dossiers. Group features into chapters — clusters a reviewer would visit together: orientation (what this is, how you invoke it), core workflow, supporting features. 3–5 chapters per element is typical. A single rich feature can carry a chapter; do not pad thin material.

**Output:** A chapter plan (`inventory.md`) — chapter names, features per chapter, intended order — presented to the user in conversation, then carried forward without waiting for approval.

**Parallelism:** This phase requires cross-project judgment. It resists parallelization.

---

## Phase 4: Research

**Goal:** For each chapter, verify the features' current behavior and trace each feature to the prompts that shaped it.

Two kinds of research per chapter, run in parallel:

**Implementation verification:** Re-read the actual source files. Extract exact commands, constants, defaults, and behavior. Verify every dossier claim — the walkthrough narrates present-tense behavior, so a stale claim becomes a false demo.

**Prompt provenance:** For each feature, find the prompt(s) that caused or shaped it. Sources in order of authority: session prompt exports (verbatim), curated prompt histories, session recaps (paraphrase), git commit messages and dates, ADRs. Label every attribution as verbatim, paraphrase, or inference — never blurred. Iteration chains (initial prompt, later correction) are especially valuable: they show steering.

When research contradicts the inventory, revise the inventory. The pipeline is not a conveyor belt.

**Output:** Per-chapter research packets — verified behavior plus labeled provenance.

**Parallelism:** Chapters are independent; both researchers within a chapter run concurrently.

---

## Phase 5: Walkthrough Composition

**Goal:** Walk the listener through each chapter's features — what each is, what it does, and the prompt behind it — in prose economical enough to respect a reviewer's time.

This is a guided tour, not a documentary. Present tense; the subject is the artifact as it works today, and the only story told is this repository's own — its features and their implementation as recorded in its prompts, commits, sessions, and decisions. The past appears only as that provenance; nothing that happened outside the repo is part of the narrative, and external dependencies get name and role in one clause, no background. The paragraph test governs everything: every paragraph names a feature, shows its behavior, or gives the prompt that shaped it — anything else is cut. No scenic openings, no extended analogies, no idea lineage, no manufactured drama.

The output is audio, heard once, in sequence: light one-clause signposts at transitions, no visual-only formatting, filenames and dates spelled out to be heard correctly.

### On certainty

Do not fabricate certainty. Quote a prompt verbatim only when a prompt export contains it. When only a recap or commit message survives, say so: "the session recap records the instruction as..." When provenance is inferred from timing, present it as inference. A walkthrough that dresses paraphrase up as quotation poisons every real quote in it.

### Length

700–1,200 words per chapter, shorter when coverage allows. Never cut a feature to fit; never pad to fill. The lever is prose economy.

**Output:** One file per chapter, named by content, written to output/sections/, each followed by a 150–250 word orientation summary in output/summaries/.

**Parallelism:** Independent chapters can be written simultaneously.
