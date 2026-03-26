# Repo Story: A Process for Extracting Wisdom from Code Repositories

A repeatable methodology for surveying a collection of repositories, distilling the techniques and ideas within them, tracing those ideas to their origins, and producing documentary audio narratives that teach what was found.

---

## Pipeline Shape

```
Survey → Explore → Synthesize → Research → Narrate
```

This shape is the invariant. Everything else — how many files to read, how many agents to launch, how long to write — is determined by the material, decided fresh each time.

Each phase has a different mode of thinking and a different unit of work:

- **Survey**: Breadth-first, shallow. Get the lay of the land. The unit is the collection.
- **Explore**: Depth-first, per-project, parallel. Understand each project on its own terms. The unit is the repo.
- **Synthesize**: Cross-project pattern recognition. Find the ideas that transcend individual projects. The unit transitions from repo to theme.
- **Research**: Depth-first, per-theme, parallel. Verify implementations and trace origins. The unit is the theme.
- **Narrate**: Documentary composition. Walk through the substance as audio narrative. The unit is the theme.

The repo is where you find things. The theme is how you present them. Both are units of research, at different phases. Exploration is organized by repo because you have to understand a project on its own terms before you can extract anything from it. Everything from synthesis onward is organized by theme because the final output is about ideas, not about projects.

The pipeline is not strictly one-pass. Later phases will reveal errors, gaps, and reframings in earlier phases. When that happens, go back and revise. Every phase produces drafts, not finished artifacts. Understanding deepens as you move through the process, and earlier work should reflect that deepening as it occurs.

---

## Before You Start

**Attribution level.** How much sourcing does the output need? Full academic citations, light sourcing with names and dates, or just the ideas with minimal attribution? This depends on the audience and purpose.

The lens — what you're looking for — emerges from the material. You may have a sense of it before you start, or you may discover it during synthesis. Both are valid. Do not gate the process on declaring a lens up front.

---

## Phase 1: Survey

**Goal:** Understand the landscape before diving into any single project.

Identify every project in the target set. For each one, read enough to produce a short summary of what it is, who made it, and what it's built with. The right sources vary by project — a README, a manifest file, a git remote, an about page — but the goal is always the same: know what you're looking at before you commit to studying it.

Note any obvious relationships between repos — forks, shared ancestry, dependencies, competing implementations of the same idea. These relationships, when they exist, are themselves a source of insight during synthesis.

Not every project deserves equal exploration. The catalog should give you enough information to decide how deeply to explore each project in Phase 2. Make this decision explicitly rather than defaulting to uniform treatment.

**Output:** A catalog of projects with enough context to guide exploration decisions.

---

## Phase 2: Deep Exploration

**Goal:** Understand each project on its own terms.

For each project worth exploring, dispatch independent research. The research should continue until the explorer can confidently describe what the project does, how it does it, why it makes the choices it makes, and where those choices came from.

Useful questions to start with — adapt or discard based on what the project actually is:

- What does this project do and why does it exist?
- What techniques, patterns, or methodologies does it use?
- What are the key design decisions and what motivated them?
- Where do the ideas come from?
- What philosophy or worldview does it embody?

These questions work well for application-style projects with documentation and design rationale. They may be the wrong questions for a dataset, a collection of scripts, a research artifact, or a fork. Let the project's nature determine the questions.

**What to record:** Exact quotes, exact numbers, exact variable names, exact file paths. Specificity matters because later phases depend on it. Vague summaries are useless downstream. Precise details are the raw material that makes everything else possible.

**What to watch for, above all else: surprises.** The things you didn't expect to find. The decisions that contradict convention. The techniques you've never encountered. These are often the most valuable discoveries in the entire process.

When a genuine surprise appears — something that could not have been predicted from the project's README or stated purpose — go deeper immediately. Read the related files. Understand the context. Capture enough detail that the surprise can stand on its own when it reaches synthesis. Do this while the explorer is still holding the context of the project, because rebuilding that context later is expensive.

The constraint on surprise-pursuit: if the project's documentation told you to expect it, it's not a surprise — it's the explorer doing its job. A novel optimizer in a project whose README says "we use a novel optimizer" is expected. A three-tier LLM-as-judge testing framework in a project that says nothing about testing is a surprise worth pursuing on the spot.

**Output:** Per-project research dossiers — raw, detailed, internal working documents. These are drafts. Phase 4 will correct and deepen them.

**Parallelism:** Independent projects can be explored simultaneously.

---

## Phase 3: Thematic Synthesis

This phase has two distinct steps that use different modes of thinking. Do them in order.

### Step 1: Connection-Finding

**Goal:** See what's there before you organize it.

Read all the dossiers from Phase 2. Before you start categorizing or labeling, spend time noticing. Look for resonances — the same principle appearing in different projects applied to different problems. Look for contradictions — places where two projects make opposite choices for what seem like similar reasons. Look for surprises that survived from Phase 2 — the unexpected findings that don't fit neatly into any obvious category.

Do not organize yet. The goal of this step is to see connections, not to file them.

### Step 2: Theme Organization

**Goal:** Give structure to what you found.

Group the connections, resonances, and standout findings into named themes. For each theme, capture:

- The general principle, independent of any specific project
- The specific implementations — how each relevant project embodies the idea
- A rough sense of where the ideas originate

Not every theme needs to span multiple repos. A technique so rich or novel that it deserves its own treatment is a valid theme even if only one project uses it.

You may discover during this step that your lens needs adjusting — that the data is revealing something more interesting than what you originally set out to find. If so, follow it. The most valuable findings are often the ones nobody asked for. Capture themes that don't fit your stated lens separately rather than discarding them.

**Output:** A structured set of themes — presented to the user in conversation for review and direction before proceeding.

**Parallelism:** This phase requires cross-project judgment. It resists parallelization.

---

## Phase 4: Research

**Goal:** For each theme, verify the implementation details, trace the intellectual lineage, and map the current landscape.

Each theme typically benefits from two kinds of research, which can run in parallel because they use different tools and produce complementary outputs:

**Implementation verification:** Re-read the actual source files for the theme. Extract exact code patterns, exact constants, exact algorithms. Verify claims from the Phase 2 dossiers against what the code actually does. Phase 2 is fast and broad by design — it will have gotten things wrong. This is where you correct those errors.

**History and landscape research:** This has two dimensions — depth through time and breadth across contemporaries. Both matter.

The vertical dimension is origin tracing. Who created this technique? What problem were they solving? What did it replace? What did it inspire? Find the people, the dates, the papers, the core insights in plain language. Trace the chain of influence from origin to the implementation in front of you.

The horizontal dimension is landscape mapping. How does this technique fit into the broader world right now? What else exists that solves the same problem? What are the alternatives, and how does this implementation compare to them? Is this approach best in class, a contender, a niche choice, or an outlier? Why might someone choose this over the alternatives, and why might someone choose the alternatives over this?

The listener needs both dimensions to understand where something stands. The lineage tells them how an idea got here. The landscape tells them what it means that it's here — whether it represents the consensus, the frontier, or a deliberate departure from both.

Not every theme needs both kinds of research. A theme about a project's philosophy may have no code to verify. A theme about a bespoke implementation detail may have no meaningful intellectual history. A theme about a well-established technique may need more landscape than lineage. Match the research effort to what the theme actually requires.

When research contradicts earlier findings — and it will — update your understanding. If the contradiction changes a theme's framing, scope, or connections, go back and revise Phase 3. The pipeline is not a conveyor belt where each phase's output is frozen.

**Output:** Per-theme research packets combining verified implementation details with traced lineage and mapped landscape.

**Parallelism:** Research across themes is independent and can run simultaneously. The two kinds of research within a theme can also run in parallel.

---

## Phase 5: Narrative Composition

**Goal:** Walk through the full substance of each theme — every technique, every design choice, every architectural detail — delivered as documentary audio narrative so the listener absorbs the details through the momentum of the telling.

This is documentary work. It tells what exists, who made it, how it came to be, and where it sits in the world. The commitment is to reality — real people, real history, real technical substance, real context. The medium is audio. The listener should come away understanding the specific constants, the exact algorithms, the precise design tradeoffs — not because they were listed, but because each one arrived at the right moment in a narrative that made it meaningful.

This is not a tutorial. A tutorial says "here's how to do this." This is not a summary. A summary strips away detail to save time. This is narration of the actual substance, in full detail, woven into a causal thread — a sequence of people facing problems, making choices, and producing ideas that shaped the next generation's starting point. The details are not reduced. They are contextualized. They are carried by the narrative rather than standing apart from it.

### What makes a good narrative

Let the material determine the structure. Some themes want to be told chronologically. Some want to start with the code and zoom out. Some want to be built around an extended analogy. Some want to compare two approaches side by side. The structure should serve the material, not the other way around. Patterns that have worked in practice — grounding abstractions in analogy, telling history as a causal chain rather than a list, building from large concepts to smaller components, returning to the specific implementation after establishing general context — are available as tools, not obligations.

The output is audio. The listener cannot scan back, cannot glance at a table, cannot re-read a confusing paragraph. This means:

- Signpost transitions explicitly so the listener knows where they are in the arc
- When moving from one idea to the next, briefly restate the previous idea's conclusion so a listener who drifted can re-anchor
- Avoid formatting that only works visually — tables, code blocks, bullet lists, diagrams
- Every paragraph should make sense when heard aloud, in sequence, once

### On certainty

Do not fabricate certainty. This matters enough to state fully.

During research, some origins will be clean and well-documented. Robbins and Monro published stochastic approximation in 1951. Kingma and Ba published Adam in 2014. These are facts. State them with confidence.

Other origins will be murky. An idea may have appeared first in a blog post, then in a conference talk, then in a paper — with different people credited at each stage. An idiom may have no confirmed origin. A technique may have been independently invented by multiple groups at roughly the same time. A paper may cite an earlier paper as inspiration, but the connection may be tenuous.

When the lineage is clear, present it cleanly. When it is unclear, say so. "The exact origin is debated, but the earliest published treatment appears to be..." is more trustworthy than a false clean lineage. "The idea emerged from a community of practitioners before it was formalized in a paper" is more accurate than attributing it solely to the paper's authors.

The listener trusts the narrator more, not less, when the narrator admits what they don't know. False certainty is a form of fabrication. It degrades every claim around it, because the listener cannot distinguish the well-sourced facts from the confident guesses. Honest uncertainty preserves the credibility of everything else.

This applies to causal claims as well as attribution. "A influenced B" is a strong claim. Sometimes the evidence supports it — B's paper cites A, or B's author has stated the influence publicly. Sometimes it's inference — A was published two years before B and addresses a similar problem. Present the former as fact and the latter as plausible connection, and the narrative will be stronger for the honesty.

**Output:** One file per theme, named by content, written to output/sections/.

**Parallelism:** Themes that are independent can be written simultaneously. Themes that build on each other should be written in sequence.
