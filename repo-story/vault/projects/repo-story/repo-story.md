---
tags: [project, repo-story]
type: project
concerns: []
audience: [dev, claude-code]
summary: "Claude Code skill that analyzes GitHub repos and produces documentary audio narratives. Per-repo folder convention; pipeline: Survey → Explore → Synthesize → Research → Narrate → audio → transcripts → static site."
repo: git@github.com:hotpocket/repo-story.git
path: ~/git/repo-story
language: Python
framework: Chatterbox TTS, landry-ui audiobook player
created: 2026-05-22
status: active
---

# repo-story

Claude Code skill that takes a GitHub URL and produces a documentary audiobook + static-site player. Five-phase pipeline (Survey, Explore, Synthesize, Research, Narrate) producing per-theme text sections, then per-chapter M4As, transcripts, and a deploy-ready site.

## Architecture

- **Phases 1–5** (in Claude Code): exploration agents per repo unit → thematic synthesis → parallel research (code verification + history/landscape) → documentary narrative writing. Outputs to `<repo-folder>/output/{dossiers,research,sections}/`.
- **build_audio.py** (stale — single-M4B model): Chatterbox TTS generates chunk WAVs, ffmpeg concatenates into chaptered M4B.
- **landry-ui audiobook pipeline** (current — per-chapter M4A model): `~/git/landry-ui-playground/audiobook/build_site.py` + `build_transcripts.py`. The repo-story scripts lag this architecture.
- **Deploy**: via `[family-site-deploy]/deploy.sh` to `[family-site]/books/`. Multi-book mode driven by `[family-site-deploy]/books.json` (added 2026-05-22).

## Folder Convention

Each repo run gets its own folder at repo root: `<repo-name>/repo/` (the git clone) + `<repo-name>/output/` (everything generated). See [[AUTORUN]] for the full runbook.

## Architecture Decisions

(none yet recorded in vault)

## Project Notes

(none yet)

## Domains

(none yet)
