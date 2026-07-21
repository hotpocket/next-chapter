---
tags: [adr]
type: decision
summary: "V1 ships two audiobooks — landry-ui and repo-story — so the site narrates its own sources: backstory/journey + product demo in one artifact"
status: accepted
created: 2026-07-20
concerns: [admissions-project, content, scope]
---

# ADR 0005 — V1 content: audiobooks for landry-ui and repo-story

> **EXTENDED by [[0009-three-books-trilogy|ADR 0009]]** (2026-07-21): a third book — next-chapter itself — joins the two decided here.

## Context
The project's purpose (owner, 2026-07-20): the GitHub Pages site is the
product — the interface to audiobooks *about repositories*. For admissions, the
subjects are the project's own sources: landry-ui (the player library) and
repo-story (the generation pipeline).

## Decision
V1 ships two books: **landry-ui** and **repo-story**. Dual purpose: (1) the
backstory of these projects and the journey of building them; (2) a live demo
of the final product rendering them.

## Consequences
- Self-demonstrating: the player plays a book explaining the player's own code —
  the strongest available answer to "can you explain this code."
- Two offline generation runs (GPU hours each, resumable) — schedule early.
- Sharpens the source-visibility requirement: a book about a repo the reviewer
  cannot open undercuts purpose (1). landry-ui: flip public (verify contents
  first). repo-story: scrub before any flip (voice WAV, personal vault,
  generated books) or stay private with SOURCES.md carrying pinned hashes and
  excerpts.
- V1 work-list gains the three visibility mechanisms: README spine (entry-point
  index: config-history → ADRs → recaps/prompts → provenance), SOURCES.md
  (pinned commits per source repo), per-book provenance record generated at
  build time (target repo+commit, pipeline commit, date, TTS engine, prompts).
