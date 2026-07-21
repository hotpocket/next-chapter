# AUTORUN — GitHub URL → Audiobook + Site, Unattended

One-shot orchestrator for repo-story. Point at this file, give it a GitHub URL, run to completion.

> Source of truth for the *methodology* is [PLAN.md](PLAN.md) and the per-phase guidance in [prompts/](prompts/). This file is the *execution* contract: folder layout, command lines, decision rules. The two documents are intentionally separated — PLAN.md is the thinking, AUTORUN.md is the doing.

---

## Inputs

- A GitHub repository URL (e.g. `https://github.com/owner/name`).
- Optional: attribution level — `full`, `light`, `minimal`. Default `light`.
- Optional: existing voice reference in `voices/*.wav`. If exactly one wav exists it auto-detects; otherwise pass `--voice`.

Do **not** ask the user for a "lens" up front. The lens emerges from the material (per PLAN.md).

## Folder convention

Everything for a single run lives under one top-level folder at the repo-story root, named after the repo (e.g. `mattpocock-skills/`). This isolates each run from prior runs and from other repos.

```
<repo-folder>/
├── repo/                          git clone (gitignored)
└── output/
    ├── dossiers/                  Phase 2 — one .md per repo/subproject
    ├── themes.md                  Phase 3
    ├── research/                  Phase 4 — one .md per theme
    ├── beats/                     Phase 5a — per-theme arc notes (main session)
    ├── sections/                  Phase 5b — section-*.txt per theme
    ├── summaries/                 Phase 5c — condensed section-*.txt (Summary track)
    ├── chapters.txt               narrative-arc order of sections
    ├── audio/
    │   ├── chunks/                intermediate chunk WAVs (resume cache)
    │   └── chapter-NN-*.wav       per-chapter concat WAVs
    ├── m4a/                       per-chapter M4As + chapters_manifest.json (production format)
    ├── book.m4b                   single-file audiobook (brandonlandry.com path)
    ├── transcripts.json           time-aligned transcript
    └── site/                      deploy-ready static site
```

Why this layout: the build scripts (`build_audio.py`, `build_transcripts.py`, `build_site.py`) all default to `output/...` relative to the current directory. Running them with `cd <repo-folder>` makes every default Just Work — no path-override flags needed.

## Constraints — read these before running anything

- **No SSH commands.** The user manages ssh-agent manually. `luinst` defaults to `git@github.com:`; override with `LANDRY_UI_REPO=https://github.com/hotpocket/landry-ui.git`. If HTTPS fails because the repo is private, fall back to whatever is already in `player/` and skip PWA assets — the site will still work, just without offline support. See `memory/feedback_no_ssh.md`.
- **Don't publish without explicit ask.** Publishing is the user's `git push` of the parent next-chapter repo (Pages). Stop after the build steps.
- **Don't clobber prior runs.** Each repo gets its own folder. Never write into the repo-story root `output/`.
- **Model split — Fable plans, Opus executes.** The main session is pinned to Fable via `.claude/settings.json` (loud failure if unavailable — do not fall back silently) and does the planning phases: 1 survey, 3 themes, 5a beats, chapter ordering. Phases 2, 4, and 5b run only via the named agent types in `.claude/agents/` (`explorer`, `code-researcher`, `history-researcher`, `narrator`), each pinned to Opus. Never spawn generic subagents for those phases and never write sections inline. See [docs/adr/0001](docs/adr/0001-fable-plans-opus-executes.md).
- **Don't pause for approval mid-pipeline.** PLAN.md says Phase 3 "presented to the user for review" — AUTORUN mode overrides that to present-and-continue. The user invoked AUTORUN precisely so they could walk away. If a real problem arises (auth prompt, GPU OOM, missing file), stop and report.

## Pipeline

### Phase 0 — Acquire

```bash
REPO_URL=<github url>
REPO_FOLDER=$(basename "$REPO_URL" .git)        # or owner-name if you prefer disambiguation
git clone --depth 1 "$REPO_URL" "$REPO_FOLDER/repo"
mkdir -p "$REPO_FOLDER/output"/{dossiers,research,beats,sections,audio/chunks,site}
```

Append the repo folder to `.gitignore` so the clone, audio, and site never enter version control.

### Phase 1 — Survey

Read README, manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.), `git log --oneline -20`, and any top-level docs. Identify:
- author (from git remote, package metadata, or README)
- purpose (one sentence)
- tech stack
- internal structure: is this one project, or a collection? (A monorepo of skills/plugins is a *collection* — treat each subdir as its own unit.)
- noteworthy files that promise depth (ETHOS.md, ARCHITECTURE.md, CONTRIBUTING.md, design docs, novel-looking source files)

Present the catalog to the user in one short paragraph in chat — then proceed to Phase 2 without waiting.

### Phase 2 — Deep exploration

Read [prompts/explore.md](prompts/explore.md).

**Parallel agents — one per unit.** For a single-project repo, one agent. For a collection (skills monorepo, plugin set, sibling libraries), one agent per meaningful unit. Each agent writes a dossier to `<repo-folder>/output/dossiers/<unit>.md`.

Agent type: `explorer` (`.claude/agents/explorer.md` — carries the methodology pointer and the Opus pin). Task prompt per unit:
> Project location: `<repo-folder>/repo/<subpath>`. Write the dossier to `<repo-folder>/output/dossiers/<unit>.md`.

Wait for all agents to finish before Phase 3.

### Phase 3 — Synthesize themes

Read all dossiers. **Step 1: connection-finding** — notice resonances, contradictions, surprises, without categorizing. **Step 2: organize** — group into named themes. Each theme captures:
- the general principle, project-independent
- specific implementations (which units, with exact references)
- rough origin sense

Write to `<repo-folder>/output/themes.md`. Present the themes briefly in chat (one line each) and continue immediately to Phase 4.

If the unit count is small (1–2) and the material is thin, allow theme count to be small (1–3). Do not pad.

### Phase 4 — Research per theme

Read [prompts/research_code.md](prompts/research_code.md) and [prompts/research_history.md](prompts/research_history.md).

**Parallel agents — two per theme** (implementation verification + history/landscape), running concurrently. Each writes a markdown file to `<repo-folder>/output/research/`.

Agent type `code-researcher`, task prompt per theme:
> Theme: `<theme>` (one-line summary from themes.md). Source location: `<repo-folder>/repo/`. Write to `<repo-folder>/output/research/<theme>-code.md`.

Agent type `history-researcher`, task prompt per theme:
> Theme: `<theme>` (one-line summary from themes.md). Write to `<repo-folder>/output/research/<theme>-history.md`.

If research contradicts the Phase 3 themes, revise `themes.md` before Phase 5 and mention the change in chat.

### Phase 5 — Narrate

**5a — Beats (main session).** For each theme, write `<repo-folder>/output/beats/<theme>.md`: the narrative arc, the must-hit facts (pointing at the research packets to pull from), and the transitions into and out of neighboring themes. This is planning work — it stays in the main session.

**5b — Sections (narrator agents).** One `narrator` agent per theme — parallel when themes are independent, sequential when they build on each other. Never write sections inline, regardless of theme count. Task prompt per theme:
> Theme: `<theme>`. Beats: `<repo-folder>/output/beats/<theme>.md`. Research: `<repo-folder>/output/research/<theme>-*.md`. Write `<repo-folder>/output/sections/section-<slug>.txt`.

**5c — Summaries (final step of each chapter).** After each section, one `narrator` agent condenses it to `<repo-folder>/output/summaries/<same filename>` — every load-bearing fact, no scenic build-up, ~12–18% of the section length. Same audio-prose rules. The build scripts pick these up automatically (summary audio + manifest + transcript → the player's Full/Summary toggle).

After all sections are written, decide chapter order in the main session — narrative arc, not alphabetical, not by-repo. Write to `<repo-folder>/output/chapters.txt`, one filename per line.

### Phase 6 — Audio

```bash
cd <repo-folder>
python ../build_audio.py --voice ../voices/<your-voice>.wav --title "<Episode Title>" --artist "<Author>"
```

Defaults are correct (sections-dir `output/sections`, chunks-dir `output/audio/chunks`, output `output/book.m4b`). `--title` is the episode title (what brandonlandry.com displays via manifest.json); album is always `Repo Story`.

This step requires CUDA. RTX 2080 Ti runs roughly 0.5–1.5× real-time for Chatterbox TurboTTS, so a 60-minute book ≈ 30–90 minutes wall-clock. **Run in background** (`run_in_background: true`) and continue with phases 7–8 only after completion notification.

Resume is automatic — re-running skips chunks whose WAV files exist. If a chunk seems wrong, delete its file and re-run.

### Phase 7 — Per-chapter M4As + transcripts (production format)

The landry-ui player consumes **per-chapter M4As**, not the M4B. This is the format deployed at [family-site]/books via [family-site-deploy].

```bash
cd <repo-folder>
python ../build_m4a.py --title "<Book Title>" --artist "<Author>"
python ../build_transcripts.py --slug <repo-folder>
```

`build_m4a.py` encodes `output/audio/chapter-*.wav` → `output/m4a/chapter_NNNN.m4a` + `chapters_manifest.json` (resume-safe). `build_transcripts.py` writes `output/site/transcripts.json` from chunk WAVs — per-chapter-relative timestamps, already the shape [family-site-deploy] expects. Both run in seconds-to-minutes, no GPU.

### Phase 8 — Publish

**Single path — the parent next-chapter repo's GitHub Pages site:** copy the
book's artifacts (per-chapter M4As, `chapters_manifest.json`,
`transcripts.json`) into the parent repo's Pages site directory and register
the book in its library manifest (see the parent repo's plan for exact paths —
they are defined there, not here). No AWS, no deploy scripts.

Preview over HTTP (file:// won't support Range requests) — `python ../serve.py`
from the repo folder.

### Phase 9 — Done

Report to the user:
- Path to the M4B and `output/m4a/` (chapter count, total duration)
- The library-manifest entry added (or proposed)
- Reminder that publishing is theirs to run: `git push` of the parent repo

---

## Decision rules

| Situation | What to do |
|---|---|
| Repo URL is for a collection (monorepo of skills/plugins) | One exploration unit per meaningful subdir. Themes can span subdirs. |
| Repo is tiny (one file, a script collection) | Single dossier, possibly a single theme. Don't pad. |
| `voices/` has multiple wavs | Stop and ask which voice — `build_audio.py` exits with that error anyway. |
| Output M4B already exists | `build_audio.py` prompts; in automated mode, write to a new path (`--output <repo-folder>/output/book-v2.m4b`) or delete the old one if the user said overwrite. |
| Pipeline interrupted mid-audio | Re-run the same command — resume is built in. |
| `luinst` HTTPS fetch fails | Continue with whatever's in `player/`; note the missing PWA assets in chat. |
| Research contradicts a theme | Revise themes.md, note the change, continue. |
| User-defined `CLAUDE.md` adds rules | Honor those — they override AUTORUN. |

## Why this file exists

PLAN.md is the methodology. SKILL.md is the Claude Code skill manifest. The phase prompts in `prompts/` are agent briefs. Without AUTORUN, an operator (human or LLM) has to read all of those, infer the folder layout, decide where to put per-repo artifacts, and remember to override `--audio-dir` and `--output` flags. AUTORUN collapses that into one document and one folder convention.

Future sessions: read AUTORUN.md, follow it top to bottom, deviate only when the material actually demands it.
