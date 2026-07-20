---
tags: [adr]
type: decision
summary: "SUPERSEDED by 0006 (2026-07-20): reuse the landry-ui player; the AI demonstration is the assembly, deploy, and hardening — not a rebuilt player"
status: superseded
created: 2026-07-20
concerns: [admissions-project, frontend]
---

# ADR 0002 — Minimal player built fresh; landry-ui player as stretch

## Context
landry-ui ships a mature 1,061-line vanilla audiobook player (PWA, transcript sync, resume). Importing it day one would demo well but read poorly against the rubric: incremental commits, one-feature-at-a-time, "code you can explain."

## Decision
MVP player is written fresh in the project repo: chapter list, `<audio>` element, current-chapter transcript — committed feature by feature. The landry-ui player is a **stretch** swap-in, cited as my own previously-extracted library (provenance documented in config-history.md).

## Consequences
The commit history shows real construction. Interview surface stays small and fully explainable. The polished player remains available without contaminating the MVP narrative.
