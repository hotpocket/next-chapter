---
tags: [adr]
type: decision
summary: "UI + JSON on GitHub Pages, audio on dedicated public-read S3 bucket; no request-time backend for playback"
status: accepted
created: 2026-07-20
concerns: [architecture, security, aws]
---

# ADR 0001 — Frontend on Pages, audio on S3, no playback backend

## Context
Course requires the UI on GitHub Pages (vanilla HTML/CSS/JS). repo-story analysis confirmed every listener-facing artifact (M4A chapters, manifest, transcripts, player) is pre-generated static; nothing runs at request time. Pages could technically host the audio too, but S3 keeps large binaries out of git and is the justified AWS surface.

## Decision
- GitHub Pages serves `index.html`, JS/CSS, and all JSON (manifest, transcripts) — same-origin fetches, no CORS.
- Audio (`.m4a` per chapter) lives in a **dedicated new S3 bucket**, referenced via `<audio src>` (no CORS needed). HTTPS REST endpoint, not website-hosting mode.
- **Zero Lambdas for playback.**

## Bucket security posture
- Public principal: `s3:GetObject` on the audio prefix only; **no ListBucket** (no enumeration).
- Block Public Access: ACL blocks stay ON; only policy-based public read allowed.
- Writes: my IAM identity via CLI only; no credentials in repo or scripts; I run deploys.
- Cost abuse (public GET, no rate limit): billing alarm; CloudFront+OAC only if it ever matters.
- Deploy script syncs the audio dir explicitly — voice reference WAVs and source text can never land in the bucket.

## Consequences
Playback is fully static and reviewer-testable from the Pages link. AWS usage is real but minimal and defensible. Bucket name is public by design; nothing private ever enters that bucket.
