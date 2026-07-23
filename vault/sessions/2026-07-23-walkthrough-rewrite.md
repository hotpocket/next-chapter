---
tags: [session]
type: session
concerns: [ops, infra, data]
audience: []
summary: "Rewrote the repo-story methodology from documentary to feature-walkthrough + prompt-provenance (repo-only story, verbatim/paraphrase/inference labels) and regenerated all three books' text under it (v3, ~1.4h vs v1's 4.6h). Built scripts/regen-trilogy-audio (registry-driven, content-hash freshness, 19-test suite). Narration text + transcripts now tracked in git; v1/v2 generations archived under gitignored output/. v3 selected for the public site; trilogy.json descriptions updated; vendor-scrub.rules truncation fixed; todos cleared for finalization."
created: 2026-07-23
status: completed
projects: [next-chapter]
branch: main
---

# 2026-07-23 — Walkthrough rewrite, generation management, finalize prep

Companion prompts: [[2026-07-23-walkthrough-rewrite-prompts]]

## Work

1. repo-story methodology rewritten (94aec5e): documentary → feature walkthrough + prompt provenance. narrate.md paragraph test (every paragraph names a feature, shows behavior, or gives the prompt — else cut); research_history.md → research_prompts.md (attributions labeled verbatim/paraphrase/inference, never blurred); explore.md → feature inventory; Phase 3 = chapter plan (inventory.md); history-researcher agent → prompt-researcher.
2. Second tightening (970bf89): the story is the repo's own only — no outside history; external tools get name + role in one clause.
3. All three books regenerated under the new contract (Fable planned, Opus executed per ADR 0001): 4 chapters + 4 summaries each, ~1.4h total. Prior generations archived per book: output/_v1-documentary/ (docs/ still serves this), output/_v2-first-walkthrough/ (overnight audio + landry-ui rebuild text).
4. scripts/regen-trilogy-audio + 19-check test suite (f02be6d, 29a44ff, ee421c2): registry-driven audio rebuild for all books; voice resolved from repo-story/voices/; content-hash freshness — .text-hash of chapters+sections+summaries; mismatch wipes that book's derived audio, match resumes.
5. Narration text version-controlled (f3cc835): gitignore negations track sections/, summaries/, chapters.txt, site/transcripts.json per book; audio/caches/archives stay ignored. Tracked text is v3-only (landry-ui-v2 removed from history by owner instruction, its text preserved in the gitignored v2 archive).
6. v2 evaluated via a local, gitignored, self-contained preview (llm-docs/logs/v2-preview). landry-ui's audio/transcript mismatch was diagnosed (section rewrite landed mid-GPU-run), the v2 contract recovered from git (94aec5e), the book re-narrated and re-rendered consistent.
7. Finalize prep: v3 selected for the public site; trilogy.json descriptions rewritten for the walkthrough books; vendor-scrub.rules truncation fixed (SCRUB_SED array was unclosed — BANNED loaded, sed expressions didn't); todos cleared.

## Discoveries

- build_audio.py's chunk cache is index-keyed, not content-keyed: after a text edit it silently reuses stale audio ("cached, skipping" against brand-new sections). The regen script's content-hash guard exists because of this.
- docs/ had never been rebuilt after the documentary era — all pre-2026-07-23 listening was generation 1.
- Never edit section text while a render is running: the landry-ui v2 mismatch came from a 3:24 rewrite landing inside a 2:47 GPU run — transcripts picked up new text against old audio.
- Prompt-provenance coverage varies honestly by era: next-chapter is verbatim-rich (110 exported prompts); landry-ui and repo-story's pre-export features survive only as commit paraphrase, and the books say so.

## Decisions

- Walkthrough over documentary — the reviewer's time budget wins; the steering prompt is itself quoted in book 2. Rejected: keeping the documentary format with lighter prose (the 2026-07-10 de-fluff rollback showed trimming words doesn't fix genre).
- Repo-only narrative — no outside history, dependencies in one clause. Rejected: allowing brief external context (still read as "outside history" to the owner).
- Generations live side-by-side under gitignored output/ archives; only current text is tracked in git; v2 stays a local preview, never committed.
- v3 is the public generation (owner decision, 2026-07-23).

## Next Steps

None — project is in finalization. The owner's finalize flow (not TODOs): scripts/regen-trilogy-audio → python3 scripts/build-trilogy-site → review → push.
