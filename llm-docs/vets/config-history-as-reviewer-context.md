---
tags: [vet]
type: vet
summary: "config-history.md shipped alongside the prompt history lets the reviewer interpret the tool invocations they'll see there, turning cryptic prompts into legible evidence of skilled AI collaboration"
status: probing
created: 2026-07-19
concerns: [admissions-project, submission-repo, prompt-history]
---

# Vet: config-history.md as reviewer context for the prompt history

## Tree

- [load-bearing] The submitted prompt history will actually contain /wargame, /browse, and vault invocations — feed: the build itself; if the project gets built without the workflow, the doc stages a play that never happens. **pending**
- [load-bearing] Without context, those invocations read as cryptic to a reviewer (they're custom skills, not standard prompts) — feed: Part 9 asks for prompts showing planning/debugging/verification; a bare `/wargame` line shows none of that unless explained. **confirmed** (by inspection of Part 9 requirements vs. what a skill invocation looks like)
- [load-bearing] The doc's claims are true and interview-defensible — feed: every date/count in it was pulled from git history this session; interview questions ("how did AI help you") are answerable from it. **confirmed**
- [likely] The reviewer actually opens config-history.md — feed: link it from the README's required "AI Tools Used" section so the required artifact routes them to it; interview is the backstop. **pending**
- [likely] Sophistication helps rather than hurts with a beginner-program reviewer — feed: Section 9's own framing ("can *you* effectively work with AI") rewards exactly this; residual risk is "too polished to be the applicant's own" — mitigated by interview defensibility. **pending**
- [speculative] This repo (with `course/` mirror) is the right home for the submission — feed: decide repo layout before publishing. Publishing the mirrored course content in a public submission repo redistributes their paywalled material to the very reviewers who wrote it. **pending — decision required**

## Hostile pass

Inline stress pass (proportionate to a strategy doc; full /wargame reserved for the project plan itself):

- ~~"The doc substitutes for the required artifacts"~~ — killed: README/prompt-history/commits are still built as required; doc is additive.
- "Reviewer never opens it" — survives as risk → probe: README link from a required section.
- "Reads as ringer/AI-ghostwritten" — survives as risk → mitigation: factual tone, git-dated claims, interview fluency; the doc explicitly says the AI does the work and I own the controls.
- "Public repo leaks course content" — survives, promoted to load-bearing decision → probe: separate public submission repo (or strip `course/` before publishing).

## Probes

- [x] probe: submission-repo layout → RESOLVED: this repo, public, course/ gitignored (long-standing; trilogy shipped from it 2026-07-21)
- [ ] probe: add a one-line pointer to config-history.md under the README "AI Tools Used" section when the README is written → confirms "reviewer opens it"
- [x] probe: prompt log shows the tools → CONFIRMED 2026-07-21: exports carry /vet, /wargame, /vault, /clear across four sessions; glossary drift-check enforced pre-publish

## Verdict

- 2026-07-19 — **proceed.** The two claims that could kill the idea (invocations are cryptic without context; doc is defensible) are confirmed. Remaining risks are cheap, named, and probed. Flip condition: if the submission-repo probe forces publishing from this repo *with* `course/` included, stop and restructure before anything goes public.

## Open questions

- Will the submission be built in this repo or a fresh public one?
