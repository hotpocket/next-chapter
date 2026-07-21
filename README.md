# next-chapter — repo → audiobook

Turn a GitHub repository into a narrated audiobook: explore its history and
core concepts, write a documentary arc, render it to audio, and play it in the
browser. This repo is my Next Chapter admissions project: the GitHub Pages site
here serves a trilogy of audiobooks about its own lineage —
[landry-ui](https://github.com/hotpocket/landry-ui) (the player's origin),
[repo-story](repo-story/) (the generator's origin, vendored here), and
next-chapter itself (their assembly into this site).

**Status:** built — the trilogy (16 chapters + 16 summary tracks, 4.6 hours)
is generated and assembled in [`docs/`](docs/); going live on Pages is the
last flip.

**Live demo:** https://hotpocket.github.io/next-chapter/ *(activates when
GitHub Pages is enabled — `main` + `/docs`; until then, see
[How to run](#how-to-run-it) for the local path).*

## The 5-minute path (for the reviewer)

1. This README's [V1 shape](#v1-shape-decided--see-the-decisions-index) — what ships and why.
2. [`config-history.md`](config-history.md) — the AI workflow, and the glossary for reading the prompts.
3. [Decisions index](vault/decisions/README.md) — every architecture call, active vs superseded, one line each.
4. One [session recap + its verbatim prompts](#sessions--prompts) — how a working session actually runs; [`prompt-history.md`](prompt-history.md) is the curated index.
5. Press play on the [live site](https://hotpocket.github.io/next-chapter/) — and note the **Summary** toggle if you have four minutes per chapter, not twenty.

## The problem

Understanding an unfamiliar codebase means hours in front of a screen reading
files and history. That time exists in other places — commutes, drives,
walks — where a screen doesn't. This project turns a repository into a
narrated documentary audiobook: its ideas, decisions, and history, researched
from the code and git log, written as an arc, and rendered to audio you can
listen to away from the keyboard.

## Why it's valuable to another person

The listener this was built for is **you, the reviewer**: someone who cannot
spend hours digging through three repositories, brought up to speed by ear on
the code powering the very page they're using. Every chapter also ships a
**Summary track** (~4 minutes instead of ~20) for exactly that time budget.
The same mechanism generalizes: point the pipeline at any repo
([`repo-story/`](repo-story/) is the how) and get a book back.

## Project plan

The build plan — milestones M0–M4, feature cut, standing rules, and the
course-requirement map — is [`llm-docs/plan.md`](llm-docs/plan.md). It was
stress-tested before building ([build-plan
wargame](llm-docs/reports/2026-07-21_build-plan-wargame.md)); the ideas behind
it were vetted first ([vets](vault/vets/)). Execution state lives in
[`vault/todos/next-chapter.md`](vault/todos/next-chapter.md).

## Features

- **Library of three books** with chapter navigation, per-chapter progress,
  resume, playback speed, and offline download (PWA service worker).
- **Read-along transcripts**, time-synced with follow mode, reading mode,
  and text-size controls — the skim path if you'd rather read than listen.
- **Full/Summary toggle per chapter** — a condensed ~4-minute narration of
  every chapter's load-bearing facts, generated as part of the pipeline
  (Phase 5c), with its own audio and synced transcript.
- **Provenance built in** — [`docs/SOURCES.md`](docs/SOURCES.md) pins what
  each book narrates (book 3 is pinned to commit `8295cae`: a book cannot
  contain its own generation, so it names exactly what it can see).

## Technologies used

- **Player**: vanilla JavaScript (no build step), CSS, service worker —
  [landry-ui](https://github.com/hotpocket/landry-ui)'s audiobook component,
  vendored at a pinned commit ([`docs/PROVENANCE.md`](docs/PROVENANCE.md)).
- **Audio pipeline**: Python + [Chatterbox TTS](https://github.com/resemble-ai/chatterbox)
  (local CUDA GPU, cloned voice), ffmpeg — the vendored
  [`repo-story/`](repo-story/) pipeline (per-chapter M4A + manifest +
  time-aligned transcripts).
- **Hosting**: GitHub Pages serving [`docs/`](docs/) from this repo — audio
  committed in-tree, no AWS, no backend (ADR 0008).
- **Testing**: Playwright browser tests (player), shell + Python test
  harnesses (pipeline and site assembler), red→green throughout.

## AI tools used

The entire build ran through Claude Code under an audited workflow:
[`config-history.md`](config-history.md) documents the environment (vault
memory, hooks, `/vet`, `/wargame`, `/browse`), [`.claude/`](.claude/README.md)
mirrors the actual config in-tree, and every session's verbatim prompts are
published ([index](#sessions--prompts), curated in
[`prompt-history.md`](prompt-history.md)). Narration is written by the
[`repo-story/`](repo-story/) skill (research agents + narrator agents;
"Fable plans, Opus executes" — its ADR 0001) and voiced by Chatterbox TTS.

## How to run it

Listen: the [live site](https://hotpocket.github.io/next-chapter/), or locally
(the site is static; a Range-capable server is needed for seeking):

```bash
python3 repo-story/serve.py -d docs -p 8010   # then open http://localhost:8010
```

Regenerating books requires a CUDA GPU + Chatterbox (see
[`repo-story/README.md`](repo-story/README.md)) — by design the site never
regenerates anything (ADR 0003: generation is offline; the reviewer plays).
Site assembly from generated books: `python3 scripts/build-trilogy-site`.
Tests: `bash repo-story/scripts/test_build_book.sh`,
`python3 scripts/test_build_trilogy_site.py`, and in landry-ui
`node test/summary.test.mjs`.

## How to read this repo (the trail)

- [`config-history.md`](config-history.md) — how I work with AI: the tools,
  hooks, and skills you'll see invoked throughout the prompt history, and a
  glossary for reading it.
- [`.claude/`](.claude/README.md) — the AI config itself, mirrored in-tree:
  hook code, global conduct rules, and the bodies of every skill invoked in
  the prompt history, with a machine-path → repo-path cross-reference.
- [Decisions index](vault/decisions/README.md) — ADRs: every architecture
  decision, its sources, active vs superseded at a glance.
- [`vault/sessions/`](vault/sessions/) — session recaps, each paired with a
  `*-prompts.md` file of the verbatim prompts from that session (index below).
- [`llm-docs/reports/`](llm-docs/reports/) — kept deliverables: security wargames and
  audits (public-repo hygiene, the landry-ui public-flip audit).
- [`repo-story/`](repo-story/) — the audiobook-generation pipeline, vendored
  with its history replayed commit-by-commit (`Replayed-From:` trailers;
  private details redacted — see its README's provenance note).
- [`llm-docs/vets/`](llm-docs/vets/) + [`vault/vets/`](vault/vets/) — idea vets with
  verdicts and probes.

Planning docs live in [`llm-docs/`](llm-docs/).

## Sessions & prompts

Every working session ends in a recap note paired with the verbatim prompts
that produced it (see [`config-history.md`](config-history.md) for the
command glossary that makes the prompts readable):

| Session | Recap | Prompts |
|---------|-------|---------|
| 2026-07-20 — Foundation | [recap](vault/sessions/2026-07-20-foundation.md) | [46 prompts](vault/sessions/2026-07-20-foundation-prompts.md) |
| 2026-07-20 — Config mirror | [recap](vault/sessions/2026-07-20-config-mirror.md) | [4 prompts](vault/sessions/2026-07-20-config-mirror-prompts.md) |
| 2026-07-21 — repo-story vendored + in-repo pivot | [recap](vault/sessions/2026-07-21-repo-story-vendored.md) | [27 prompts](vault/sessions/2026-07-21-repo-story-vendored-prompts.md) |
| 2026-07-21 — Trilogy built | [recap](vault/sessions/2026-07-21-trilogy-built.md) | [30 prompts](vault/sessions/2026-07-21-trilogy-built-prompts.md) |

## Resources

In-repo, for navigating:
- [Session log](vault/sessions/Session%20Log.md) — one-line index of every session.
- [Decisions index](vault/decisions/README.md) — all ADRs: active vs superseded, one line each.
- [`.claude/README.md`](.claude/README.md) — the AI config mirror and its
  machine-path → repo-path cross-reference.
- [Reports](llm-docs/reports/) — security wargames and audits;
  [vets](llm-docs/vets/) — idea verdicts.

External:
- [landry-ui](https://github.com/hotpocket/landry-ui) — the player this
  project vendors (audited and flipped public for this project).
- [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) — the local
  TTS engine used for offline audio generation (ADR 0003).
- gstack — the open-source browser-driving skill suite (`/browse`); entry
  points mirrored at [`.claude/skills/gstack/`](.claude/skills/gstack/).

## V1 shape (decided — see the [decisions index](vault/decisions/README.md))

Everything ships from this repo: a static library + player page (landry-ui,
vendored at a pinned hash) on GitHub Pages, with per-chapter M4A audio and
read-along transcripts committed in-tree and served by Pages — no AWS, no
deploy scripts, no request-time backend. Publishing is a `git push`.
Generation runs offline on my machine (Claude Code prose + Chatterbox TTS)
using the [`repo-story/`](repo-story/) pipeline, vendored into this repo as a
scrubbed replay of its original commit history — it is both the generator and
a book subject. Three books, generated in forced order (ADR 0009): landry-ui,
repo-story, then next-chapter last with its narrated range pinned — a book
cannot contain its own generation. S3/AWS fully retired (ADR 0008).
