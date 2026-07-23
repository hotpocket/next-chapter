---
name: repo-story
description: Analyze repositories and produce audio walkthroughs of their features and the prompts that shaped them.
---

# /repo-story

You are executing the repo-story process. This skill surveys code repositories, inventories their features, verifies current behavior, traces each feature to the prompts that shaped it, and writes walkthrough narratives suitable for text-to-speech audio production.

Read `PLAN.md` in this skill's directory for the full process definition. The phases below are your execution guide.

**Model split — Fable plans, Opus executes.** The main session is pinned to Fable via `.claude/settings.json` (loud failure if unavailable) and does the planning: Phase 1 survey, Phase 3 inventory, Phase 5a beats, chapter ordering. Phases 2, 4, and 5b run only via the named agent types in `.claude/agents/` (`explorer`, `code-researcher`, `prompt-researcher`, `narrator`), each pinned to Opus. Never spawn generic subagents for those phases and never write sections inline. See `docs/adr/0001-fable-plans-opus-executes.md`.

## Invocation

The user will provide one or more repository paths, and for each, where its prompt provenance lives (session prompt exports, recaps, curated prompt histories). If provenance locations are not given, look for a `vault/sessions/` directory and repo-level `prompt-history.md` / `config-history.md` before asking.

## Phase 1: Survey

For each repo provided, read the README, manifest/config files (package.json, pyproject.toml, Cargo.toml, go.mod, etc.), and check the git remote to identify the author. Note which provenance sources exist and whether they contain verbatim prompts or only recaps.

Present the user with a brief catalog: project name, author, purpose, tech stack, provenance coverage. Do not wait for approval — proceed to Phase 2.

## Phase 2: Feature Inventory Exploration

Read the detailed guidance in `prompts/explore.md`.

Launch one `explorer` agent per repo, in parallel. Each agent catalogs every user-visible feature — exact commands, exact paths, exact defaults, inputs and outputs — organized by what a user meets, not by code structure.

Write dossiers to `output/dossiers/` — one markdown file per repo.

When all explorations complete, proceed to Phase 3.

## Phase 3: Feature Inventory Organization

Read all dossiers. Group the features into chapters — feature clusters a reviewer would tour in order: orientation first (what the thing is, how it's invoked), core workflow next, supporting features after. Aim for 3–5 chapters per element; do not pad.

Present the chapter plan to the user directly in the conversation — chapter name, features covered — then write it to `output/inventory.md` and proceed to Phase 4 immediately.

Do not ask for permission to continue. Present the plan and move forward. If the user wants to redirect, they will say so.

## Phase 4: Research

Read the detailed guidance in `prompts/research_code.md` and `prompts/research_prompts.md`.

For each chapter, launch parallel research:
- **`code-researcher` agent**: Re-reads source files, verifies the features' current behavior exactly, corrects Phase 2 errors
- **`prompt-researcher` agent**: Traces each feature to the prompts that shaped it — verbatim from prompt exports where they exist, recap/commit paraphrase where they don't, labeled honestly

Write research packets to `output/research/` — one markdown file per chapter per researcher.

If research contradicts the Phase 3 inventory, revise it and inform the user of the change.

## Phase 5: Walkthrough Composition

Read the detailed guidance in `prompts/narrate.md`.

**5a — Beats (main session).** For each chapter, write `output/beats/<chapter>.md`: the feature order, the must-hit details (pointing at the research packets), the prompt citations to use, and one-clause transitions.

**5b — Sections (`narrator` agents).** One `narrator` agent per chapter — parallel when independent. Never write sections inline. Each expands its beats + research into a walkthrough: present tense, feature → behavior → prompt, 700–1,200 words, no scenic openings, no lineage.

**5c — Summaries (final step of each chapter).** After a section is written, a `narrator` agent condenses it into `output/summaries/<same filename>`: a 150–250 word orientation — what this part is, its features by name, one sentence on the prompts. Same audio-prose rules (`prompts/narrate.md`). The build pipeline turns these into the player's Summary track.

Key principles:
- The only subject is this repository — its code, its features, their implementation story; external tools get name + role in one clause, never background
- Every paragraph names a feature, shows behavior, or gives the prompt behind it — otherwise cut
- Prompt attribution is labeled: verbatim, paraphrase, or inference — never blurred
- The output is audio — hearable once, no visual formatting, spell out filenames and dates
- As short as coverage allows

Write sections to `output/sections/` — one text file per chapter, named by content (e.g., `section-build-pipeline.txt`).

## Chapter Ordering

After all sections are written, confirm the chapter order — the reviewer's tour order from Phase 3: orientation, core workflow, supporting features. Write it to `output/chapters.txt` — one filename per line. Example:

```
section-what-this-is.txt
section-build-pipeline.txt
section-publishing.txt
```

## Completion

When all sections and `chapters.txt` are written, tell the user:

1. List the chapters in order with their approximate word counts
2. Tell them to run `build_audio.py` to generate the chaptered audiobook:
   ```
   python build_audio.py --voice voices/my_voice.wav --output output/book.m4b
   ```
3. Note that `build_audio.py` prints progress continuously and supports resume if interrupted
