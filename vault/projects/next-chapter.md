---
tags: [project]
type: project
summary: "Next Chapter admissions project — a Pages site (docs/) playing a trilogy of audiobooks narrating its own lineage (landry-ui → repo-story → next-chapter). All in-repo: audio in git, no AWS. repo-story vendored as scrubbed commit replay. Plan: llm-docs/plan.md; decisions: vault/decisions/README.md."
created: 2026-07-20
concerns: [admissions-project]
---

# next-chapter

Workspace for the Next Chapter admissions submission.

**The product (as of 2026-07-21):** GitHub Pages site served from `docs/`
playing a **trilogy** of audiobooks about its own lineage: landry-ui (the
player's origin) → repo-story (the generator's origin) → next-chapter (their
assembly). Audio + transcripts committed in-tree — **no AWS, no backend**
(ADR 0008 retired S3); publishing = owner's `git push`. Generation offline:
Claude Code prose + Chatterbox TTS on the local GPU, via the pipeline
vendored at `repo-story/` (scrubbed commit replay of the private original,
`Replayed-From:` trailers; next-chapter's book generates **last**, narrated
range pinned — ADR 0009).

Navigation (read in this order in a fresh session):
- [[../todos/next-chapter|TODOs]] — milestone-shaped, mirrors the plan.
- `llm-docs/plan.md` — the sequenced build plan (M0 probe → M1 scaffold →
  M2 Pages → M3 books → M4 polish), owner-reviewed 2026-07-21.
- `vault/decisions/README.md` — decisions index; 0008/0009 are the current
  architecture, banners mark superseded ones.
- `config-history.md` + README "5-minute path" — the reviewer-facing spine.

Standing constraints: dual hygiene scan before every commit (gitleaks +
private token map in gitignored `llm-docs/logs/vendor-scrub.rules` — that
file is the ONE home for private identifiers); /browse-verify features;
recap + prompt export every session; owner pushes.

- `course/` — mirror of the 65-lesson pre-course (section 9 = spec). Never publish.
- Workflow fixed: vet → wargame → build → browse-verify → vault recap.
