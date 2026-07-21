---
tags: [project]
type: project
summary: "Next Chapter admissions project workspace — course mirror, config-history baseline, project TBD"
created: 2026-07-20
concerns: [admissions-project]
---

# next-chapter

Workspace for the Next Chapter admissions submission.

- `course/` — mirror of the 65-lesson pre-course (section 9 = project spec). Reference only; never publish.
- `config-history.md` — first deliverable layer: the legend that lets the reviewer interpret the prompt history (vault, hooks, /browse, /wargame).
- `llm-docs/vets/config-history-as-reviewer-context.md` — vet of that strategy (verdict: proceed; open probe: submission-repo layout).
- Project (chosen 2026-07-20): **repo → podcast**, drawn from ~/git/repo-story.
  **V1 (the submission):** static player of pre-generated books. Generation is
  local-only: prose via Claude Code prompts (proven 2026-03-26 prompt flow), audio
  via python Chatterbox/chatterbook scripts on the local GPU; artifacts uploaded
  to S3; vanilla UI on GitHub Pages. No OpenRouter, no Lambdas in V1. ADRs
  0001–0003 accepted; rough draft in llm-docs/2026-07-20_project-rough-draft.md.
  **V2 (deferred):** on-demand URL ingestion via Lambda + Tailscale, prose routed
  to OpenRouter — ADR 0004. OpenRouter is V2-only tooling. Content: two books, landry-ui +
  repo-story (ADR 0005 — self-demonstrating site). V1 work-list additions:
  README spine, SOURCES.md (pinned hashes), per-book provenance records.
  Decided: reuse landry-ui player — ADR 0006 supersedes 0002. The AI
  demonstration = assembly into Pages + hardened S3 deploy (local AWS SSO
  profiles, never web-exposed).
- Workflow fixed: vet → wargame → build → browse-verify → vault recap.
