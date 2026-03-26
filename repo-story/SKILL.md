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

Read all dossiers. Do connection-finding first: notice resonances, contradictions, and surprises across projects without organizing them yet.

Then organize into themes. Present them to the user directly in the conversation — theme name, general principle, which repos embody it, rough origin — so the user can see what you found. Then write themes to `output/themes.md` and proceed to Phase 4 immediately.

Do not ask for permission to continue. The user does not have deep knowledge of the repos — that is why they are running this skill. Present your findings and move forward. If the user wants to redirect, they will say so.

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

## Chapter Ordering

After all sections are written, determine the chapter order. The sections should flow as a narrative arc — not alphabetically, not by repo, but by the logic of how the ideas build on each other. Consider: opening with the broadest philosophical frame, moving through process and methodology, deepening into technical substance, and closing with a unifying principle.

Write the ordered chapter list to `output/chapters.txt` — one filename per line, in the order they should appear in the audiobook. Example:

```
section-boil-the-lake.txt
section-three-layer-knowledge-search.txt
section-fail-fast.txt
```

## Completion

When all sections and `chapters.txt` are written, tell the user:

1. List the chapters in order with their approximate word counts
2. Tell them to run `build_audio.py` to generate the chaptered audiobook:
   ```
   python build_audio.py --voice voices/my_voice.wav --output output/book.m4b
   ```
3. Note that `build_audio.py` prints progress continuously and supports resume if interrupted
