# Phase 2: Feature Inventory Exploration — Agent Guidance

You are exploring a single repository to produce a feature inventory dossier. Your goal is to catalog what a user of this project can actually do with it, as it exists right now — every entry point, every command, every user-visible behavior — with enough exact detail that a walkthrough can be narrated from your dossier alone.

## How to explore

Read as many files as you need. Start with the obvious entry points (README, main config, scripts, entry point files) and follow the threads they reveal. There is no target file count.

Questions to answer for each feature you find:

- What is it called and where does it live? (exact file paths, command names)
- How is it invoked or encountered? (command line, UI element, automatic hook)
- What goes in and what comes out? (inputs, outputs, formats, side effects)
- What are its current settings and behaviors? (exact constants, defaults, flags)
- What state is it in — working, partial, superseded?

Organize by what a user would meet, not by code structure: entry points and workflows first, supporting machinery second, internal plumbing only where it explains visible behavior.

## What to record

Specificity is everything. Later phases depend on exact details, not summaries.

- Exact command lines and what they produce
- Exact file paths, variable names, constant values, defaults
- Exact quotes from documentation where they state what a feature does
- Concrete behavior: "running X writes Y to Z," not "handles output generation"

If you find yourself writing "the project provides tooling for X," stop and go read the code until you can say exactly what the tool is, how it is run, and what it emits.

## What NOT to chase

This dossier feeds a feature walkthrough whose only subject is this repository. Do not research where ideas came from, what the wider field does, or the project's philosophy. External dependencies get their name and role only — never their background. Note an unexpected or unconventional choice in one or two sentences where it explains a feature's behavior — then move on.

## Output

Write a single markdown file to `output/dossiers/`, named after the project. Structure it as the feature inventory: a numbered list of features, grouped by workflow, each with its exact details. This is a working document — raw detail matters more than polish.
