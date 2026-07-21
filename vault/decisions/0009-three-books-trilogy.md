---
tags: [adr]
type: decision
summary: "V1 ships three books, adding next-chapter itself: landry-ui (player origin) → repo-story (generator origin) → next-chapter (their assembly into this site). Generation order forced: next-chapter last, narrated range pinned."
status: accepted
created: 2026-07-21
concerns: [admissions-project, content, scope]
---

# ADR 0009 — Three books: next-chapter completes the trilogy

Extends [[0005-two-books-self-demonstrating|ADR 0005]] (two books).

## Context
Owner decision 2026-07-21: add next-chapter itself as a third book. Its
history now *contains* repo-story's (vendored scrubbed replay with
`Replayed-From:` trailers) and vendors landry-ui's player — so one repo's
history walks the whole lineage. It is also the richest source of the three:
ADRs, wargames, vets, session recaps, and verbatim prompt exports — and it
exercises the vault-notes-as-source path the two-books vet marked untested.

## Decision
- V1 library: **landry-ui** (the player's origin) → **repo-story** (the
  generator's origin) → **next-chapter** (their assembly into the site the
  listener is using).
- **Generation order is forced**: next-chapter's book runs last — it cannot
  contain its own generation session. Its provenance record pins the narrated
  range ("narrates through commit X").
- Prose prompts: repo-story's existing guidance as-is until the owner tunes
  them (owner runs the regenerate-and-judge loop).

## Consequences
- Strongest available "code you can explain": a book on the site narrating
  how the site was built, including the sessions that generated the earlier
  books.
- Third GPU run on the schedule (small book scope; owner owns scheduling).
- Doubles down on the self-referential frame the two-books vet stress-tested;
  same mitigation holds and is restated here: the reviewer IS the listener
  the Part-2 value statement names — someone who cannot dig through the
  repos, brought up to speed while using the product.
- The book will trail HEAD by construction; the pinned range makes that
  honest rather than confusing.
