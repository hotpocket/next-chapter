---
name: repo-story
description: Analyze repositories and produce documentary audio narratives about the techniques, ideas, and history within them.
---

# /repo-story

You are executing the repo-story process. This skill surveys code repositories, explores them deeply, synthesizes cross-project themes, researches origins and landscape, and writes documentary narratives suitable for text-to-speech audio production.

Read `PLAN.md` in this skill's directory for the full process definition. The phases below are your execution guide.

## Invocation

The user will provide one or more repository paths. They may also provide an attribution level (full, light, minimal — default to light if not specified). The lens emerges from the material — do not ask for one up front.

## Phase 1: Survey

For each repo provided, read the README, manifest/config files (package.json, pyproject.toml, Cargo.toml, go.mod, etc.), and check the git remote to identify the author.

Note any relationships between repos (forks, shared ancestry, dependencies, competing implementations).

Present the user with a brief catalog: project name, author, purpose, tech stack. Do not wait for approval — proceed to Phase 2.

## Phase 2: Deep Exploration

Read the detailed guidance in `prompts/explore.md`.

Launch parallel exploration agents — one per repo. Each agent should read as many files as needed to understand the project deeply. Record exact quotes, exact numbers, exact variable names.

**Watch for surprises above all else.** When something genuinely unexpected appears — something the README did not predict — go deeper immediately while context is held.

Write dossiers to `output/dossiers/` — one markdown file per repo.

When all explorations complete, proceed to Phase 3.

## Phase 3: Thematic Synthesis

**This phase requires user input. Do not proceed past it without the user's direction.**

Read all dossiers. Do connection-finding first: notice resonances, contradictions, and surprises across projects without organizing them yet.

Then propose themes. Present them to the user directly in the conversation:

- Theme name
- The general principle
- Which repos embody it and how
- Rough sense of origin

Ask the user: "These are the themes I found. What would you change — merge, split, drop, add?" Wait for their response. Revise as directed. When the user is satisfied, write the final themes to `output/themes.md` and proceed.

## Phase 4: Research

Read the detailed guidance in `prompts/research_code.md` and `prompts/research_history.md`.

For each theme, launch parallel research:
- **Implementation verification agent**: Re-reads source files, extracts exact details, corrects Phase 2 errors
- **History and landscape agent**: Traces origins (who, when, what paper, what problem), maps current landscape (what alternatives exist, how this compares, where it sits in the field)

Write research packets to `output/research/` — one markdown file per theme.

If research contradicts the Phase 3 themes, revise the themes and inform the user of the change.

## Phase 5: Narrative Composition

Read the detailed guidance in `prompts/narrate.md`.

For each theme, write a documentary audio narrative. Full detail. Real people, real history, real technical substance. The material determines the structure — do not force every theme into the same template.

Key principles:
- This is documentary work — factual, grounded, committed to reality
- Details are not reduced, they are contextualized within narrative flow
- The output is audio — signpost transitions, restate at transitions, no visual formatting
- Do not fabricate certainty — when origins are murky, say so honestly

Write sections to `output/sections/` — one text file per theme, named by content (e.g., `section-fail-fast.txt`).

## Completion

When all sections are written, tell the user:

1. List the sections produced and their approximate word counts
2. Tell them to run `build_audio.py` to generate the chaptered audiobook:
   ```
   python build_audio.py --voice voices/my_voice.wav --output output/book.m4b
   ```
3. Note that `build_audio.py` prints progress continuously and supports resume if interrupted
