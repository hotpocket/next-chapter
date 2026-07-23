# repo-story

Analyze code repositories and produce audio walkthroughs of their features and the prompts that shaped them.

> **Vendored into next-chapter (2026-07-21).** This folder is a scrubbed
> commit-replay of the private `hotpocket/repo-story` repo — the generation
> pipeline behind this project's audiobooks, and the subject of one of them.
> Each replayed commit carries a `Replayed-From: repo-story@<sha>` trailer and
> its original author date; excluded from the replay: an AWS deploy path, an
> un-deployed infra blueprint, and personal/machine details (redactions appear
> as `[bracketed]` placeholders). Replay tooling: `../scripts/vendor-repo-story`.
> Publishing now targets the next-chapter GitHub Pages site, not the retired
> deploy paths mentioned in older notes.

## How it works

repo-story is a Claude Code skill. The research and writing happens inside a Claude Code session. The audio production happens via a Python script that uses Chatterbox TTS.

### 1. Install the skill

Copy or symlink this repo into your project's skills directory:

```bash
mkdir -p .claude/skills
ln -s /path/to/repo-story .claude/skills/repo-story
```

### 2. Run the skill

In Claude Code, invoke:

```
/repo-story /path/to/repo1 /path/to/repo2
```

Claude will:
- Survey the repos and locate their prompt-provenance sources
- Inventory each one's features (parallel)
- Group features into a chapter plan (the reviewer's tour order)
- Research each chapter (parallel — implementation verification + prompt provenance)
- Write walkthrough narratives for each chapter

Text sections are written to `output/sections/`.

### 3. Build the audiobook

After the sections are written:

```bash
# Generate audio (requires CUDA GPU — takes hours, supports resume)
python build_audio.py --voice voices/my_voice.wav

# Generate time-aligned transcripts from chunk WAVs
python build_transcripts.py

# Fetch the player component
./luinst audiobook/vanilla player/

# Build the static site
python build_site.py

# Serve locally (supports Range requests for seeking in large M4B files)
python serve.py
```

The audio script prints progress continuously and supports resume — if interrupted, re-run and it skips already-generated chunks.

### 4. Publish

Copy the book's artifacts (per-chapter M4As, `chapters_manifest.json`,
`transcripts.json`) into the parent next-chapter repo's Pages site and
register the book in its library manifest; the owner publishes with
`git push`. (The pre-vendoring `deploy.sh` → S3/CloudFront path was retired
and excluded from the replay — see the banner above.)

## Requirements

**For the skill (Phases 1-5):** Claude Code with a Claude subscription.

**For audio generation:** Python 3.10+, CUDA GPU, [Chatterbox TTS](https://github.com/resemble-ai/chatterbox), ffmpeg, ffprobe.

## Voice reference

Place a voice reference WAV file in `voices/`. Requirements: mono, 24kHz sample rate, 5-15 seconds of clear speech. See the Chatterbox docs for details on voice cloning.

## Project structure

```
repo-story/
├── PLAN.md              # The full process methodology
├── SKILL.md             # Claude Code skill definition
├── prompts/             # Phase-specific guidance for Claude
├── build_audio.py       # Text sections → chaptered M4B audiobook
├── build_transcripts.py # Chunk WAVs + text → transcripts.json
├── build_site.py        # M4B + player → static site
├── serve.py             # Local dev server with Range support
├── luinst               # Fetch landry-ui components
├── player/              # Fetched from landry-ui (gitignored)
├── voices/              # Voice reference WAV files
└── output/              # Generated artifacts (gitignored)
```
