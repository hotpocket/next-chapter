# Interview prep — how the plan fared on contact with reality

Prepared 2026-07-23. Companion to [`llm-docs/plan.md`](../plan.md) (the intent)
and the [decisions index](../../vault/decisions/README.md) (the record).
Interview questions are paraphrased, not quoted — the course text is private.

## The one-paragraph answer

The plan's structure survived intact: every milestone (M0 probe → M1 scaffold
→ M2 Pages live → M3 books in forced order → M4 polish) completed in sequence,
and the standing rules (recap + prompt export every session, dual hygiene
scans, /browse gates, owner-only pushes) ran all five sessions without
exception. What the plan missed was content quality as a first-class risk:
M3.5 — "owner listens to at least one full chapter per book" — was a one-line
QA gate, and it detonated. The listening pass judged the documentary books
long-winded and too fantastical, and the prescribed fix (beats-level tweaks,
prototype one chapter) was the wrong scale. The real fix was a genre change —
documentary → feature walkthrough with prompt provenance — a methodology
rewrite and two full regenerations, roughly half the post-plan effort. The
plan treated narration as a rendering problem; it was a product-definition
problem.

## Mapped to the interview themes

**What problem / what value.** Codebase-understanding time is screen-bound;
the trilogy moves it to ears (commutes, walks). Value demonstrated on the
reviewer directly: the site narrates its own three components, with ~2-minute
summary tracks for their time budget.

**Why this solution.** The pieces already existed and were battle-tested
privately (landry-ui player, repo-story pipeline); the project makes them
public, auditable, and self-describing. Decided via /vet (two-books-journey)
before building.

**How I decided what to build first.** M0.1 content probe (one chapter,
GPU smoke test) decoupled from M1 scaffold; manifest-format recon was
deliberately the first build task — the wargame flagged format mismatch as
the cheapest early kill. Order of books forced by ADR 0009: the closing book
cannot contain its own generation.

**A time I challenged the AI.** Twice, same axis. July 10 (repo-story): an
AI "understated reportage" de-fluff pass was rejected and rolled back — word
pruning didn't fix the genre. July 22: rejected the documentary framing
entirely ("long winded, and a bit too fantastical") and redirected to a
walkthrough of features and the prompts behind them; later tightened again to
repo-only story when the first rewrite still let outside history in. The
steering prompts are published verbatim and book 2 quotes the redirect.

**Most interesting bug.** The audio chunk cache is index-keyed, not
content-keyed: after rewriting narration text, a re-run reported every chunk
"cached, skipping" and silently kept the old recording. Compounded the same
night by a mid-render collision — section text was rewritten while a GPU run
was live, so one book's transcripts described text its audio never spoke.
Fix: a content hash of the narration text (`output/.text-hash`) now gates the
audio cache — text change forces a clean render, unchanged text keeps resume.
Diagnosed from file mtimes (audio chunks vs section files vs transcript
build times), which is also how the one inconsistent book was identified and
rebuilt from the exact prompt revision recovered out of git history.

**How I verified it worked.** Red→green tests before implementation
(assembler, prompt exporter, config mirror, audio-regen script — 19 checks);
/browse verification of every shipped feature in a real browser; the M3.5
listening gate (which is what caught the genre problem); transcript-vs-audio
consistency checked chunk-level after the rebuild.

**Another weekend.** The features-next list in the README, recorded as ADRs
during the build, not invented after: visitor-submitted ingestion (ADR 0004,
needs redesign since it presumed the retired S3 architecture), hosted
delivery at scale (ADR 0008's with-more-time path), wiring the feedback
endpoint (client built, deliberately inert), React player parity, audio QA
passes.

**Proudest part.** The transparency loop closing on itself: the prompts that
built the thing are published, the books narrate the features those prompts
produced and quote them, and the config that ran the sessions is mirrored
in-tree. The genre-change prompt is itself narrated by the book it reshaped.

## Honest deficits (if pressed)

- The plan had no notion of generation management; v1/v2/v3 bookkeeping and
  the cache-freshness guard were built reactively after a live failure.
- v2's narration text was deleted during cleanup — evaluated, rejected, and
  intentionally not preserved; only v1 (git history) and v3 survive.
- One leak reached a pushed prompt export (July 21, infra IDs + family names
  quoted inside agent output, past gitleaks) — caught by the private
  token-map scan, fixed by a full-history rewrite while the repo was still
  private; that scan is now a standing pre-commit rule.
