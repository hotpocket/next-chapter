# repo-story

Analyze code repositories and produce documentary audio narratives about the techniques, ideas, and history within them.

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
- Survey the repos
- Explore each one deeply (parallel)
- Propose themes and ask for your review
- Research each theme (parallel — implementation verification + history/landscape)
- Write documentary narratives for each theme

Text sections are written to `output/sections/`.

### 3. Generate audio

After the sections are written, run the audio script:

```bash
python build_audio.py --voice voices/my_voice.wav
```

This generates audio via Chatterbox TTS and assembles a chaptered M4B audiobook at `output/book.m4b`.

The script prints progress continuously and supports resume — if interrupted, re-run and it skips already-generated chunks.

## Requirements

**For the skill (Phases 1-5):** Claude Code with a Claude subscription.

**For audio generation:** Python 3.10+, CUDA GPU, [Chatterbox TTS](https://github.com/resemble-ai/chatterbox), ffmpeg, ffprobe.

## Voice reference

Place a voice reference WAV file in `voices/`. Requirements: mono, 24kHz sample rate, 5-15 seconds of clear speech. See the Chatterbox docs for details on voice cloning.

## UI component

The static site player is pulled from [landry-ui](https://github.com/hotpocket/landry-ui):

```bash
# Fetch/update the player component
./luinst audiobook/vanilla player/
```

`player/` is gitignored — it's a fetched dependency. Re-run to update.

## Project structure

```
repo-story/
├── PLAN.md              # The full process methodology
├── SKILL.md             # Claude Code skill definition
├── prompts/             # Phase-specific guidance for Claude
├── build_audio.py       # Text sections → chaptered M4B audiobook
├── build_transcripts.py # Chunk WAVs + text → transcripts.json
├── build_site.py        # M4B + player → static site
├── deploy.sh            # Deploy to S3 + CloudFront
├── serve.py             # Local dev server with Range support
├── luinst               # Fetch landry-ui components
├── player/              # Fetched from landry-ui (gitignored)
├── voices/              # Voice reference WAV files
└── output/              # Generated artifacts (gitignored)
```
