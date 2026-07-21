# next-chapter — repo → audiobook

Turn a GitHub repository into a narrated audiobook: explore its history and
core concepts, write a documentary arc, render it to audio, and play it in the
browser. This repo is my Next Chapter admissions project: the GitHub Pages site
here serves a trilogy of audiobooks about its own lineage —
[landry-ui](https://github.com/hotpocket/landry-ui) (the player's origin),
[repo-story](repo-story/) (the generator's origin, vendored here), and
next-chapter itself (their assembly into this site).

**Status:** foundation phase — architecture decided, build not yet started.

## The 5-minute path (for the reviewer)

1. This README's [V1 shape](#v1-shape-decided--see-the-decisions-index) — what ships and why.
2. [`config-history.md`](config-history.md) — the AI workflow, and the glossary for reading the prompts.
3. [Decisions index](vault/decisions/README.md) — every architecture call, active vs superseded, one line each.
4. One [session recap + its verbatim prompts](#sessions--prompts) — how a working session actually runs.
5. Press play on the live site (link lands here at M2).

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

Planning docs live in [`llm-docs/`](llm-docs/); the project plan and README sections
required by the course will grow here as the build proceeds.

## Sessions & prompts

Every working session ends in a recap note paired with the verbatim prompts
that produced it (see [`config-history.md`](config-history.md) for the
command glossary that makes the prompts readable):

| Session | Recap | Prompts |
|---------|-------|---------|
| 2026-07-20 — Foundation | [recap](vault/sessions/2026-07-20-foundation.md) | [57 prompts](vault/sessions/2026-07-20-foundation-prompts.md) |
| 2026-07-20 — Config mirror | [recap](vault/sessions/2026-07-20-config-mirror.md) | [4 prompts](vault/sessions/2026-07-20-config-mirror-prompts.md) |

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
