# Phase 2: Deep Exploration — Agent Guidance

You are exploring a single repository to produce a detailed research dossier. Your goal is to understand this project on its own terms — what it does, how it does it, why it makes the choices it makes, and where those choices came from.

## How to explore

Read as many files as you need to answer these questions confidently. Start with the obvious entry points (README, main config, entry point files) and follow the threads they reveal. There is no target file count — some projects need five files read, some need fifty.

Useful starting questions — adapt or discard based on what this project actually is:

- What does this project do and why does it exist?
- What techniques, patterns, or methodologies does it use?
- What are the key design decisions and what motivated them?
- Where do the ideas come from? (Check citations, references, comments, dependency choices, acknowledgments, blog links, paper links)
- What philosophy or worldview does it embody? (Look for ETHOS.md, ARCHITECTURE.md, CONTRIBUTING.md, design docs)

These questions fit application-style projects. For a dataset, a script collection, a research artifact, or a fork, ask what that kind of project demands instead.

## What to record

Specificity is everything. Later phases depend on exact details, not summaries.

- Exact quotes from documentation and comments
- Exact variable names, constant values, configuration parameters
- Exact file paths where important code lives
- Exact algorithm descriptions with real numbers (not "it uses an optimizer" but "it uses the Muon optimizer with 5 iterations of Polar Express orthogonalization, momentum ramping from 0.85 to 0.95 over 300 steps")
- Design decisions with their stated rationale

Vague summaries are useless downstream. If you find yourself writing "the project uses advanced techniques for X," stop and go read the code until you can say exactly what those techniques are.

## Surprises

Above all else, watch for surprises — things you did not expect to find, decisions that contradict convention, techniques you have never encountered.

When a genuine surprise appears — something that could not have been predicted from the README or stated purpose — go deeper immediately. Read the related files. Understand the context. Capture enough detail that the surprise can stand on its own when it reaches synthesis.

The constraint: if the project's documentation told you to expect it, it is not a surprise. It is the job. Pursue only what is genuinely unpredicted.

## Output

Write a single markdown file to `output/dossiers/`. Name it after the project (e.g., `autoresearch.md`, `gstack.md`). Include everything you found, organized however makes sense for this project. This is a working document — raw detail matters more than polish.
