# Prompt history — a curated index

Every working session in this repo published its complete, verbatim user
prompts alongside its recap (Part 9's raw material). This file is the
reviewer's map into those exports: what each session did, and which prompts
show the workflow's teeth. The prompts read terse — fragments, corrections,
no pleasantries — because a hook enforces brevity; the decoder ring is
[`config-history.md`](config-history.md)'s command glossary.

**Reading one session end-to-end beats sampling all six.** If you read only
one, read [Trilogy built](#4--2026-07-21--trilogy-built-33-prompts) — the
session where the product went from one probe chapter to the shipped site.

*(Housekeeping note: the exports were regenerated 2026-07-21 after a
transcript-format drift was caught by the export tool's plausibility check —
background-task notifications had inflated earlier counts. The counts below
are the clean ones; the fix is regression-tested.)*

---

## 1 — 2026-07-20 · Foundation ([46 prompts](vault/sessions/2026-07-20-foundation-prompts.md))

Course mirrored, project idea formed and stress-tested, architecture decided
(ADRs 0001–0006), public-repo security wargamed.

- **#6–8** — orientation: Section 9's requirements, then the framing insight
  the whole project grew from ("there is already a large history of me
  working with ai").
- **#9, #30–32** — `/vet` invocations: ideas judged proceed / probe-first /
  kill before any planning; "what is probe 1?" shows the probe discipline in
  action.
- **#19** — "wargame our strategy for securing this as a public repo" — the
  session that produced the hygiene rules (and caught a real email in a test
  fixture).
- **#36–37** — the landry-ui public-flip audit ordered before this repo
  could serve its player.

## 2 — 2026-07-20 · Config mirror ([4 prompts](vault/sessions/2026-07-20-config-mirror-prompts.md))

Four prompts, one decision carried out: the machine-level AI config mirrored
in-tree at [`.claude/`](.claude/README.md) (ADR 0007) so process claims are
auditable, with drift-checking and a live-vs-mirror distinction.

## 3 — 2026-07-21 · repo-story vendored + in-repo pivot ([27 prompts](vault/sessions/2026-07-21-repo-story-vendored-prompts.md))

The architecture's hinge day: audio moved in-repo (ADR 0008, S3 → V2), the
trilogy decided (ADR 0009), and the generator vendored with its history.

- **#10** — the build-plan `/wargame` whose landed attack (the service
  worker's same-origin assumption) triggered the in-repo pivot: the tiger
  was dissolved, not mitigated.
- **#18** — "this is still private and we can force push to rewrite the
  remote history" — the leak remediation decision: a token-map scan had
  caught what gitleaks structurally cannot (non-regex identifiers), fixed by
  a two-pass full-history rewrite before going public.

## 4 — 2026-07-21 · Trilogy built ([33 prompts](vault/sessions/2026-07-21-trilogy-built-prompts.md))

Probe → feature → all three books → assembled site.

- **#4** — "do M0.1 (the probe)" — one prompt launches the full pipeline
  run that became book 1, chapter 1.
- **#11–13** — the Full/Summary feature is born from a product judgment
  ("I fear the reviewer won't spend the time"), with the summary reviewed
  as text before any code or audio was made.
- **#16, #23** — design corrections in the small: button placement moved;
  the chapter-pane durations caught showing the wrong clock — both fixed
  test-first upstream in the player.
- **#24** — "are all of our file sizes and total size fit for what github
  pages requires?" — the ship-readiness check (they fit, with `.nojekyll`
  added).
- **#25** — `/vault recap` — the session-end procedure whose export
  plausibility check caught the transcript-format drift described above.

---

## 5 — 2026-07-23 · Walkthrough rewrite ([37 prompts](vault/sessions/2026-07-23-walkthrough-rewrite-prompts.md))

The session where the product's genre changed on a single prompt.

- **#1** — the redirect: the documentary books are "long winded, and a bit too
  fantastical" for a reviewer's time — the ask becomes "a walkthrough of the
  features and the prompts that influenced the features." The entire
  generation methodology was rewritten from this prompt, and book 2 quotes it.
- **#8** — "here I want ONLY the story of my code" — the second tightening:
  no outside history at all; external tools get one clause.
- **#10** — the stale-cache catch: the owner notices regenerated books sound
  unchanged, pastes the "cached, skipping" evidence, and the audio pipeline
  gains content-hash freshness in response.
- **#14** — "i want the transcripts... committed to version control so that I
  can track progress" — narration text becomes a tracked, diffable artifact.
- **#26–33** — the finalize arc: README rebuilt reviewer-first, then checked
  against the course's own Part-8 spec and the improvement notes recorded as
  ADRs mid-build; history squashed thematic; a plan-vs-reality retrospective
  saved as interview prep.

---

## 6 — 2026-07-30 · Site analytics ([21 prompts](vault/sessions/2026-07-30-site-analytics-prompts.md))

Hit counting added to the published site — then three corrections that each
turned into a mechanism, ending with a rewrite of how the audio pipeline
caches its work.

- **#1** — the whole feature from one loose question: "is there a way to
  install google analytics here or something like that so I know who hits
  this page and when?" — answered with GoatCounter instead, because a
  developer audience adblocks GA.
- **#7** — "what is the latent bug on landry-ui?" — the question that forced
  a re-read and overturned my own diagnosis: I had claimed the service worker
  would 503 the analytics beacon; the `cache.put` is fire-and-forget, so it
  can't. The real defect (unbounded quota-padded opaque cache entries) is
  slower and still worth the fix.
- **#10** — "you removed the check from my global config. put it back. i
  never asked you to do that." — a scoped instruction ("add X to Y") read as
  the broader change it seemed to imply. Restored, and the boundary written
  down.
- **#13** — "you missed the curated index prompt-history.md ... add them as
  checks to the wrap up process so they don't get missed again." This section
  exists because of it, and so does
  [`scripts/check-session-wrapup`](scripts/check-session-wrapup): the fix for a
  missed step is a gate, not a longer checklist.
- **#16** — "we should have chunk audio and be able to update the
  narration/text/transcripts easily so we only regenerate a small subset" —
  the design question that overturned a "not worth fixing" verdict I had just
  written into the recap. The pipeline already chunked; the chunks were keyed
  by position, so one edited word forced a full re-render. Content-addressing
  them cut the same fix down to the handful of chunks that actually changed.
- **#18** — "there are not supposed to be any lose ends" — the standard that
  drove #16. A recap that documents a known-stale artifact instead of fixing
  it is a recap that ships debt.
- **#20** — "did you run the prose through the fabel5 check for fluid story
  telling?" — a process audit in one line. The narration fix had been
  hand-patched into the section file, but ADR 0001 says sections are written
  only by the `narrator` agent. It read as patched: a spoken five-item list,
  no session-date attribution, an uncomposed transition. Re-narrated properly,
  which the new chunk cache made cheap enough to be worth doing.

---

**Totals:** 168 prompts across 6 sessions. The unabridged exports live in
[`vault/sessions/`](vault/sessions/); each links its session recap, and the
[decisions index](vault/decisions/README.md) holds the ADRs those prompts
produced.
