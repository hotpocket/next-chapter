---
tags: [project]
type: note
summary: "M0.1 probe run facts: chatterbox pyenv env, RTF 0.15 on RTX 3090 (26-min chapter in 4 min), nested .claude/agents workaround, run-folder layout under repo-story/landry-ui/."
created: 2026-07-21
concerns: [admissions-project, audio-pipeline]
---

# M0.1 probe — pipeline run facts

First landry-ui chapter generated 2026-07-21 via the vendored pipeline
(`repo-story/`), run folder `repo-story/landry-ui/` (gitignored via root
`.gitignore`: `repo-story/*/repo/`, `repo-story/*/output/`,
`repo-story/voices/*.wav`).

**Environment (the GPU smoke — passed):**
- Python: `~/.pyenv/versions/chatterbox/bin/python` (3.10.20 pyenv env; the
  only env with chatterbox installed — system python lacks it).
- GPU: RTX 3090 24GB. Chatterbox runs ~7.4GB VRAM, **RTF ≈ 0.15** — a 26-min
  chapter (107 chunks, 4,497 words) generated in 4 min. Old 2080 Ti estimate
  (0.5–1.5×) is obsolete; budget ~1/7 of audio duration.
- Voice: copied from `~/git/repo-story/voices/brandon.wav` (never commit —
  public repo).

**Harness gotcha:** the vendored `repo-story/.claude/agents/*` (explorer,
code-researcher, history-researcher, narrator) are NOT registered when the
session runs from next-chapter root. Workaround that preserved the
Fable-plans/Opus-executes split: spawn `general-purpose` agents with
`model: opus` and the agent-file body inlined in the prompt. Worked cleanly
for all 4 agent roles.

**Artifacts (chapter 1, "Performance War"):**
`output/book.m4b` (20MB), `output/m4a/chapter_0001.m4a` (13MB — under the
50MB gate) + `chapters_manifest.json`, `output/site/transcripts.json`
(107 chunks). Upstream text: `output/{dossiers,themes.md,research,beats,
sections}` — themes.md already holds all 6 themes for the full book (M3.1).

**Regenerate loop:** edit `output/sections/section-performance-war.txt` (or
delete bad chunk WAVs in `output/audio/chunks/`), re-run `build_audio.py`
(resume skips existing chunks), then `build_m4a.py` + `build_transcripts.py`.

Related: [[next-chapter]], [[2026-07-21-repo-story-vendored]]
