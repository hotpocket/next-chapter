# next-chapter — repo → audiobook

Turn a GitHub repository into a narrated audiobook: inventory its features,
trace each one to the verbatim prompts that shaped it, write an audio
walkthrough, and play it in the browser with read-along transcripts. This repo
is my Next Chapter admissions project — and its own subject: the site serves a
trilogy of audiobooks about the three components that built it —
[repo-story](repo-story/) (the generator, vendored here),
[landry-ui](https://github.com/hotpocket/landry-ui) (the player), and
next-chapter itself (their assembly). Complete: the walkthrough edition — 12 chapters,
~1.4 hours in full, or ~19 minutes total on the Summary tracks.

## Live demo & running the project

**https://hotpocket.github.io/next-chapter/** — GitHub Pages serving
[`docs/`](docs/) from this repo. Three books, chapter navigation, read-along
transcripts, and a **Full/Summary toggle**: ~2 minutes per chapter instead of
~7 if you're short on time.

Run it locally (static site; a Range-capable server is needed for seeking):

```bash
python3 repo-story/serve.py -d docs -p 8010   # open http://localhost:8010
```

**Analytics.** The published site counts page hits with
[GoatCounter](https://www.goatcounter.com/) — no cookies, no cross-site
tracking, no personal data, nothing that needs a consent banner; it records
path, referrer, and coarse browser/country. The dashboard is public, so you
can watch your own visit land:
**https://next-chapter.goatcounter.com**. The site code lives in
[`scripts/trilogy.json`](scripts/trilogy.json) and the snippet is emitted by
the site assembler, so a local build without that key ships no third-party
script at all.

## The prompts

Every working session's user prompts are published verbatim — **168 prompts across 6 sessions** — each session a recap + prompts pair:

| Session | Recap | Prompts |
|---------|-------|---------|
| 2026-07-20 — Foundation | [recap](vault/sessions/2026-07-20-foundation.md) | [46 prompts](vault/sessions/2026-07-20-foundation-prompts.md) |
| 2026-07-20 — Config mirror | [recap](vault/sessions/2026-07-20-config-mirror.md) | [4 prompts](vault/sessions/2026-07-20-config-mirror-prompts.md) |
| 2026-07-21 — repo-story vendored + in-repo pivot | [recap](vault/sessions/2026-07-21-repo-story-vendored.md) | [27 prompts](vault/sessions/2026-07-21-repo-story-vendored-prompts.md) |
| 2026-07-21 — Trilogy built | [recap](vault/sessions/2026-07-21-trilogy-built.md) | [33 prompts](vault/sessions/2026-07-21-trilogy-built-prompts.md) |
| 2026-07-23 — Walkthrough rewrite (v3) | [recap](vault/sessions/2026-07-23-walkthrough-rewrite.md) | [37 prompts](vault/sessions/2026-07-23-walkthrough-rewrite-prompts.md) |
| 2026-07-30 — Site analytics | [recap](vault/sessions/2026-07-30-site-analytics.md) | [21 prompts](vault/sessions/2026-07-30-site-analytics-prompts.md) |

[`prompt-history.md`](prompt-history.md) is the curated index (the prompts
that best show the collaboration); [`config-history.md`](config-history.md)
holds the command glossary that makes the raw exports readable.

## Skills used

- **`/browse`** ([gstack](.claude/skills/gstack/)) — drives a real browser;
  every shipped feature was verified live in it before being called done.
- **`/vault`** — persistent session memory (Obsidian-compatible); every
  session ends in a recap note, paired with its prompt export.
- **`/wargame`** — stress-tests a plan on paper before building; the build
  plan and public-repo hygiene were both wargamed ([reports](llm-docs/reports/)).
- **`/vet`** — proceed / probe / kill verdicts on ideas before they cost
  time ([vets](vault/vets/)).

The full skill bodies, hook code, and global conduct rules are mirrored
in-tree at [`.claude/`](.claude/README.md) — read the actual config, not
descriptions of it.

## Regenerating everything

1. **Repos.** Each book has a run folder `repo-story/<slug>/` holding `repo/`
   (a clone of the subject, gitignored — only landry-ui needs one) and
   `output/`. Provenance inputs: `vault/sessions/*-prompts.md`, recaps, ADRs,
   git log.
2. **Book text** (Claude Code, no GPU). The repo-story process — point a
   Claude Code session at [`repo-story/SKILL.md`](repo-story/SKILL.md) (it's
   authored as an installable skill; here it's run directly from the file):
   an explorer agent writes a feature-inventory dossier → the main
   session groups features into a chapter plan → per chapter, code-researcher
   + prompt-researcher agents verify behavior and trace prompts → narrator
   agents write `output/sections/` + `output/summaries/`, ordered by
   `chapters.txt`. Fable plans, Opus executes (its ADR 0001). The narration
   text is tracked in git.
3. **Audio** (CUDA GPU + [Chatterbox TTS](https://github.com/resemble-ai/chatterbox)).
   [`scripts/regen-trilogy-audio`](scripts/regen-trilogy-audio) runs, per
   book: `build_audio.py` (TTS) → `build_m4a.py` (per-chapter M4As +
   manifest) → `build_transcripts.py` (time-aligned transcripts) →
   `chunk_cache.py gc` (orphan sweep). Chunk WAVs are **content-addressed**
   — `chNN_<variant>_<sha12>.wav`, hashed from the chunk's text plus the voice
   and TTS params — so editing one sentence re-renders that sentence and
   everything else is a cache hit. The last narration pass re-rendered 11
   chunks out of 151; under the previous index-keyed cache it would have
   re-rendered the whole book.
4. **Site.** [`scripts/build-trilogy-site`](scripts/build-trilogy-site) reads
   [`scripts/trilogy.json`](scripts/trilogy.json), copies audio into
   `docs/audio/`, merges transcripts (content-hash cache key), copies the
   player, writes `docs/index.html` + provenance. Publishing is a `git push`
   — no script deploys (generation is offline by design, ADR 0003).

Tests: `bash repo-story/scripts/test_build_book.sh` ·
`python3 scripts/test_build_trilogy_site.py` ·
`python3 repo-story/test_build_audio.py` ·
`python3 repo-story/test_chunk_cache.py` ·
`bash scripts/test-regen-trilogy-audio.sh` ·
`bash scripts/test-export-prompts.sh` ·
`bash scripts/test-check-session-wrapup.sh` ·
`bash scripts/test-sync-claude-mirror.sh` · in landry-ui
`node test/summary.test.mjs`.

The session record has its own gate: [`scripts/check-session-wrapup`](scripts/check-session-wrapup)
re-derives every published prompt count from the export files and fails if the
Session Log, this README's table and totals, `prompt-history.md`, or the command
glossary disagree.

---

## Problem

Understanding an unfamiliar codebase means hours in front of a screen reading
files and history. That time exists in other places — commutes, drives,
walks — where a screen doesn't. This project turns a repository into a
narrated walkthrough you can listen to away from the keyboard: its features
as they exist, each traced to the prompt that shaped it.

## Value

The listener this was built for is **you, the reviewer**: someone who cannot
spend hours digging through three repositories, brought up to speed by ear on
the code powering the very page they're using — with a ~2-minute Summary
track per chapter for exactly that time budget. The mechanism generalizes:
point the pipeline at any repo ([`repo-story/`](repo-story/) is the how) and
get a book back.

## Project Plan

Plan first, build second: milestones M0–M4, the feature cut, and the
course-requirement map live in [`llm-docs/plan.md`](llm-docs/plan.md); the
plan was stress-tested before building ([build-plan
wargame](llm-docs/reports/2026-07-21_build-plan-wargame.md)) and the idea
vetted first ([vets](vault/vets/)). The decided V1 shape: everything ships
from this repo — a static library + player on GitHub Pages, per-chapter M4A
audio and transcripts committed in-tree, no AWS, no backend (ADR 0008);
generation runs offline on my machine; three books generated in forced order,
the last with a pinned narrated range because a book cannot contain its own
generation (ADR 0009).

## Features

**Complete:**

- Library of three books — chapter navigation, per-chapter progress, resume,
  playback speed, offline download (PWA service worker).
- Read-along transcripts, time-synced, with follow mode, reading mode, and
  text-size controls.
- Full/Summary toggle per chapter — condensed ~2-minute orientation with its
  own audio and synced transcript (pipeline Phase 5c).
- Prompt provenance in the narration — every feature traced to its prompt,
  labeled verbatim / paraphrase / inference; [`docs/SOURCES.md`](docs/SOURCES.md)
  pins what each book narrates.

**Next** (recorded as decisions during the build, not afterthoughts):

- Visitor-submitted ingestion — paste a GitHub URL, get a book: Lambda →
  Tailscale → home GPU → status UI
  ([ADR 0004](vault/decisions/0004-ingestion-pipeline-lambda-tailscale.md),
  deferred to V2; noted 2026-07-21 as needing redesign since it presumed the
  retired S3 architecture).
- Hosted delivery at scale — move audio off Pages to S3/CloudFront
  ([ADR 0008](vault/decisions/0008-audio-in-repo-pages-only.md)'s
  with-more-time path).
- Wire the transcription-error feedback endpoint — the player's flag UI and
  POST client are built but deliberately inert on the static site.
- React player parity — the React variant trails the vanilla player
  (no summary toggle, reading mode, or offline).
- Audio QA passes ([plan.md](llm-docs/plan.md) stretch list; that list's
  other small items — resume, deep links — shipped in V1).

## Technologies Used

- **Player**: vanilla JavaScript (no build step), CSS, service worker —
  [landry-ui](https://github.com/hotpocket/landry-ui)'s audiobook component,
  vendored at a pinned commit ([`docs/PROVENANCE.md`](docs/PROVENANCE.md)).
- **Audio pipeline**: Python + Chatterbox TTS (local CUDA GPU, cloned voice),
  ffmpeg — the vendored [`repo-story/`](repo-story/) pipeline.
- **Hosting**: GitHub Pages serving [`docs/`](docs/) — audio in-tree, no
  backend (ADR 0008). Hit counting via cookieless
  [GoatCounter](https://next-chapter.goatcounter.com) (public dashboard); the
  service worker passes cross-origin requests through so per-hit beacon URLs
  don't accumulate as quota-padded cache entries.
- **Testing**: Playwright browser tests (player), shell + Python harnesses
  (pipeline, audio regen, site assembler), red→green throughout.

## AI Tools Used

The entire build ran through Claude Code under an audited workflow:
[`config-history.md`](config-history.md) documents the environment,
[`.claude/`](.claude/README.md) mirrors the actual config, and every
session's prompts are published (see [The prompts](#the-prompts)). Narration
is written by the [`repo-story/`](repo-story/) pipeline's research + narrator
agents ("Fable plans, Opus executes") and voiced by Chatterbox TTS.

## How to read this repo (the trail)

- [`config-history.md`](config-history.md) — the AI workflow + prompt glossary.
- [Decisions index](vault/decisions/README.md) — every ADR, active vs
  superseded at a glance.
- [`vault/sessions/`](vault/sessions/) — recaps + verbatim prompt exports.
- [`llm-docs/`](llm-docs/) — plan, [reports](llm-docs/reports/) (wargames,
  audits), [vets](llm-docs/vets/).
- [`repo-story/`](repo-story/) — the generation pipeline, vendored with its
  history replayed commit-by-commit (`Replayed-From:` trailers, private
  details redacted).

## Resources

- [Session log](vault/sessions/Session%20Log.md) — one-line index of every session.
- [landry-ui](https://github.com/hotpocket/landry-ui) — the player component
  (audited and flipped public for this project).
- [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) — local TTS
  engine (generation is offline; the site only plays — ADR 0003).
- gstack — the browser-driving skill suite behind `/browse`; entry points
  mirrored at [`.claude/skills/gstack/`](.claude/skills/gstack/).
