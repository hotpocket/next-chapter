---
tags: [adr]
type: decision
summary: "Audio ships in-repo, served by GitHub Pages from docs/; S3 and all AWS surface retired from V1. Supersedes 0001's S3/bucket posture and 0006's hardened-deploy framing; publishing is the owner's git push."
status: accepted
created: 2026-07-21
concerns: [architecture, deploy, scope]
---

# ADR 0008 — Audio in-repo; Pages serves everything; S3 retired

Supersedes [[0001-pages-ui-s3-audio|ADR 0001]] (S3 audio + bucket posture)
and the hardened-S3-deploy framing of [[0006-reuse-landry-ui-player|ADR 0006]]
(whose player-reuse decision stands).

## Context
Book subjects are small repos, so books are small — per-chapter M4As fit
comfortably in git (guardrails: <50 MB/chapter vs GitHub's 100 MB hard limit,
~1 GB Pages soft limit). The build-plan wargame had flagged a cross-origin
tiger: the vendored player's service worker caches audio by relative
same-origin path, which S3 hosting would break. Owner decision 2026-07-21:
audio goes in the repo.

## Decision
- Per-chapter M4As, `chapters_manifest.json`, and `transcripts.json` are
  committed in-tree under `docs/` and served by GitHub Pages (Pages source:
  `main` + `/docs`; existing working notes moved to `llm-docs/`).
- **S3/AWS is out of V1 entirely** — no bucket, no CloudFront, no deploy
  script, no AWS credentials surface. Publishing = the owner's `git push`.
- **S3 is the V2 answer, not a dead end**: with more time, V2 moves off
  GitHub Pages to a properly hosted deploy (S3/CloudFront — the pattern the
  owner already runs in production for other book sites). This is the
  course's "what would you do with more time" answer, alongside ADR 0004's
  ingestion pipeline.
- Chapter size check is part of generation done-means (never brick a push).

## Consequences
- The wargame's service-worker/seek tiger dies naturally: audio is
  same-origin, exactly what the player was built for.
- ADR 0006's "AI demonstration" reframes from hardened deploy to: the
  composition of player + generator into a self-narrating Pages site, with
  the vendored scrubbed replay of repo-story ([[0009-three-books-trilogy|see
  also ADR 0009]]) as the transparency artifact.
- [[0004-ingestion-pipeline-lambda-tailscale|ADR 0004]] (V2 ingestion) stays
  deferred; note it presumed the S3 architecture and would need redesign, not
  revival.
- Bandwidth/size are bounded by book scope; a book outgrowing git is a
  trigger to pull V2 forward, recorded in a new ADR.
