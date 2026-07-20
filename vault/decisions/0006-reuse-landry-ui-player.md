---
tags: [adr]
type: decision
summary: "Reuse the landry-ui vanilla player (supersedes 0002). The tool is the audiobook generator+player; the AI demonstration is building it into a Pages product with a hardened S3 deploy"
status: accepted
created: 2026-07-20
concerns: [admissions-project, frontend, deploy, security]
---

# ADR 0006 — Reuse the landry-ui player; the demonstration is the assembly

Supersedes ADR 0002.

## Context
V1's books narrate landry-ui and repo-story themselves (ADR 0005) — the player
plays an audiobook explaining its own code, so the import is self-documenting.
A reduced rebuild would be optics-driven rework.

## Decision
- Reuse `landry-ui/audiobook/vanilla` as the player, vendored in one isolated,
  cited commit (pinned upstream hash, provenance note).
- **The tool is the audiobook generator + player** (pre-existing work, cited).
- **The AI demonstration is the build-out in this repo**: assembling the tool
  into a GitHub Pages product — library page, manifests, provenance records,
  README spine — plus a deploy script to S3 using **local AWS profiles with SSO
  tokens, never exposed via the web** (no credentials in repo, browser, or
  bucket), and the hardening of that deployment path (ADR 0001 posture, secret
  scanning, the wargamed public-repo hygiene) — all of it evidenced in this
  repo's prompt history, recaps, ADRs, and commits.

## Consequences
- Commit history shows integration and hardening, not player construction.
- Interview surface: the assembly, deploy, and security decisions — plus the
  player, already explained by its own audiobook.
- Deploy script requirement: reads identity from local AWS config/SSO cache
  only; fails loudly if env-var credentials would leak into any artifact.
