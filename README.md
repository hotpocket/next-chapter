# next-chapter — repo → audiobook

Turn a GitHub repository into a narrated audiobook: explore its history and
core concepts, write a documentary arc, render it to audio, and play it in the
browser. This repo is my Next Chapter admissions project: the GitHub Pages site
here will serve audiobooks about the two repos that power it —
[landry-ui](https://github.com/hotpocket/landry-ui) (the player) and repo-story
(the generation pipeline).

**Status:** foundation phase — architecture decided, build not yet started.

## How to read this repo (the trail)

- [`config-history.md`](config-history.md) — how I work with AI: the tools,
  hooks, and skills you'll see invoked throughout the prompt history, and a
  glossary for reading it.
- [`.claude/`](.claude/README.md) — the AI config itself, mirrored in-tree:
  hook code, global conduct rules, and the bodies of every skill invoked in
  the prompt history, with a machine-path → repo-path cross-reference.
- [`vault/decisions/`](vault/decisions/) — ADRs: every architecture decision,
  its sources, and what was verified before deciding.
- [`vault/sessions/`](vault/sessions/) — session recaps, each paired with a
  `*-prompts.md` file of the verbatim prompts from that session.
- [`docs/reports/`](docs/reports/) — kept deliverables: security wargames and
  audits (public-repo hygiene, the landry-ui public-flip audit).
- [`docs/vets/`](docs/vets/) + [`vault/vets/`](vault/vets/) — idea vets with
  verdicts and probes.

Planning docs live in [`docs/`](docs/); the project plan and README sections
required by the course will grow here as the build proceeds.

## V1 shape (decided — see ADRs 0001–0006)

Static player (landry-ui, vendored) + library page on GitHub Pages; audio in a
dedicated public-read S3 bucket; generation runs offline on my machine (Claude
Code prose + Chatterbox TTS); deploys via local AWS SSO profiles — no
credentials ever web-exposed; zero request-time backend.
