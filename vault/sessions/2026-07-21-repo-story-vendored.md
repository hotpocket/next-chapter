---
tags: [session]
type: session
concerns: [architecture, security, content, legibility]
audience: []
summary: "Pivoted V1 fully in-repo: audio in git, Pages serves docs/, S3/CloudFront reframed as the V2 with-more-time path (ADR 0008); trilogy decided — third book is next-chapter itself, generated last, range pinned (ADR 0009). Vendored repo-story as a scrubbed commit replay (scripts/vendor-repo-story, Replayed-From trailers, per-commit verification). Caught and fixed a real leak: infra IDs + family names had passed gitleaks into pushed prompt exports; full-history filter-repo rewrite (2 passes), owner force-pushed; new standing rule: private-token-map scan. docs/→llm-docs/ rename, decisions index + banners, README 5-minute path, plan v2 (M0–M4)."
created: 2026-07-21
status: completed
projects: [next-chapter]
branch: main
---

# 2026-07-21 — repo-story vendored + in-repo pivot

Verbatim prompts for this session: [[2026-07-21-repo-story-vendored-prompts]].

## Work

1. Build-plan wargame (stress): cross-origin/service-worker tiger, probe kill-trigger, Pages-source fork, ADR under-implementation — all landed, all patched; promoted to `llm-docs/reports/2026-07-21_build-plan-wargame.md` with an outcome addendum.
2. repo-story public-flip audit (read-only, full history): findings F1–F8; report kept in gitignored `llm-docs/logs/` (it names the identifiers).
3. **repo-story vendored at `repo-story/`** as a scrubbed commit replay — 23 of 24 commits with original messages + author dates and `Replayed-From: repo-story@<sha>` trailers; per-commit banned-token verification; tailoring commit points publishing at the next-chapter Pages site. Tooling: `scripts/vendor-repo-story replay|verify`; redaction map lives ONLY in gitignored `llm-docs/logs/vendor-scrub.rules`.
4. **Leak caught + fixed**: the first script version leaked the redaction map itself; pushed prompt-export + audit report had carried infra IDs and family names past gitleaks (agent output quoted inside exports). Full-history rewrite with `git filter-repo --replace-text`, two passes (second pass caught case variants of two personal names); every commit's tree + message re-verified clean; owner force-pushed. New standing CLAUDE.md rule: private-token-map scan of staged diffs and prompt exports.
5. **Architecture — V1 ships entirely from this repo** (ADR 0008): audio in-tree, Pages serves `docs/`, publishing = owner's `git push`, no AWS surface. **S3/CloudFront is the V2 path, not a dead end** — with more time, delivery moves off Pages to proper hosting (the pattern already in production for the owner's other book sites); together with ADR 0004 ingestion this is the course's "features you'd build next" answer.
6. **Trilogy** (ADR 0009): third book is next-chapter itself, generated last, narrated range pinned — its history now contains repo-story's replay and closes the lineage (landry-ui → repo-story → next-chapter).
7. Reviewer legibility pass: `docs/`→`llm-docs/` rename + full sweep (docs/ reserved for the Pages site); decisions index (`vault/decisions/README.md`) + supersession banners on 0001/0002/0004/0005/0006; README 5-minute path + trilogy framing; `llm-docs/plan.md` v2 (M0 probe → M1 scaffold → M2 Pages → M3 books in forced order → M4 polish, owner-reviewed); todos restructured to milestones; project overview rewritten for fresh-session orientation.

## Decisions

- Vendored scrubbed replay over flipping repo-story public — preserves the original's privacy while giving the public cross-reference the audiobook needs; original repo stays private.
- Redact, don't delete: filter-repo text replacement over file removal — prompt exports stay complete (course Part-9 evidence), links intact.
- Private identifiers live only in the gitignored token map; tracked files (including scrub tooling) must never contain them.
- S3 reframed: out of V1 entirely, named as V2 in ADR 0008 and the plan's stretch section.
- Deadlines/scheduling are the owner's concern — absent from the plan.

## Next Steps

Nothing loose. Build opens per [[../../llm-docs/plan|plan]] on two independent tracks: M0.1 probe (owner's regenerate-and-judge loop, doubles as GPU smoke) and M1.1 manifest-format recon.
