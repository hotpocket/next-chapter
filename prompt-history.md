# Prompt history — a curated index

Every working session in this repo published its complete, verbatim user
prompts alongside its recap (Part 9's raw material). This file is the
reviewer's map into those exports: what each session did, and which prompts
show the workflow's teeth. The prompts read terse — fragments, corrections,
no pleasantries — because a hook enforces brevity; the decoder ring is
[`config-history.md`](config-history.md)'s command glossary.

**Reading one session end-to-end beats sampling all four.** If you read only
one, read [Trilogy built](#4--2026-07-21--trilogy-built-26-prompts) — the
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

## 4 — 2026-07-21 · Trilogy built ([26 prompts](vault/sessions/2026-07-21-trilogy-built-prompts.md))

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

**Totals:** 103 prompts across 4 sessions. The unabridged exports live in
[`vault/sessions/`](vault/sessions/); each links its session recap, and the
[decisions index](vault/decisions/README.md) holds the ADRs those prompts
produced.
