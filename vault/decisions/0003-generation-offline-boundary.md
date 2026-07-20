---
tags: [adr]
type: decision
summary: "Audio generation stays offline machine-side tooling (Claude Code prose + local CUDA Chatterbox TTS); reviewer plays, never regenerates"
status: accepted
created: 2026-07-20
concerns: [admissions-project, pipeline, reproducibility]
---

# ADR 0003 — Generation is offline, machine-side; documented as a boundary

## Context
repo-story's pipeline works today: prose via Claude Code session (the proven path is the original 2026-03-26 prompt-based skill; the 2026-07-10 multi-agent refactor has never been exercised), TTS via local Chatterbox on CUDA GPU (hours, voice-cloned), ffmpeg muxing. Rebuilding it adds no value; it also cannot run on a reviewer's machine (GPU, voice model, subscription).

## Decision
The existing pipeline generates the book(s) offline for one chosen target repo (3–5 chapters). The project repo documents the pipeline honestly as machine-side tooling — same reproducibility-boundary pattern as config-history.md. The reviewer's testable surface is the Pages site.

## Consequences
Effort goes to the new, reviewable work (frontend + AWS publish). README must state the boundary plainly so nothing looks hidden. Publishing cloned-voice audio publicly: **approved by owner, 2026-07-20** ("use my voice, that is fine").
