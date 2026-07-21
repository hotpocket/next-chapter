# Wargame (stress): docs/plan.md — the V1 build plan

Target: the sequenced build plan (M0–M4). Mode: stress — executors are me +
owner across future sessions, not a blind agent. Claims grounded in reads/runs
this session (2026-07-21): plan.md, ADRs 0001/0005/0006, two-books vet,
landry-ui `audiobook/vanilla/{player.js,sw.js}`, repo-story `output/books/`,
section-9 parts 3/5/8/11.

## Unknowns matrix

**Known knowns (verified)**
- Player has transcript support already (`player.js`: `transcriptUrl`,
  per-book `transcripts.json` lookup) — plan 1.3 is wiring, not building.
- Player ships a service worker (`sw.js`) doing per-chapter audio caching
  keyed on **relative same-origin URLs** (`audio/chapter_NNNN.m4a`).
- repo-story has produced complete books before (`output/books/[redacted-name]`,
  `my-book`) — pipeline proven; resumable (prior session's survey).
- S3 posture + billing alarm are specified in ADR 0001; deploy-script
  credential rules in ADR 0006; voice-WAV exclusion in ADR 0001.
- Part-3 plan artifact exists (rough draft, verbatim); Part-8/11 requirement
  lists read this session.

**Known unknowns**
- SW + cross-origin S3 audio: does the fetch handler intercept/cache opaque
  responses, and does seeking (Range requests) survive cache-served audio?
  RECON NEEDED (M1): read `sw.js` fetch path fully; smoke-test seek with one
  stub chapter on real S3 before building the library page.
- Manifest/transcript JSON shape: does repo-story's output match what the
  vanilla player consumes today (they diverged after extraction?).
  RECON NEEDED (M1): diff `output/books/my-book` JSON vs player expectations.
- GitHub Pages source: Pages serves only root or `/docs` of a branch — this
  repo's root is docs/vault/course tooling, and `/docs` is already working
  notes. RECON NEEDED (M1 fork below): pick root-`index.html` vs
  Actions-built `gh-pages` branch.
- Submission deadline date — not recorded anywhere in the repo. BLOCKED on
  owner: schedule risk math (GPU runs) is unquantifiable without it.
- GPU/Chatterbox environment still works post-updates (last proven run
  predates this repo). Settled cheaply by 0.1 itself — probe doubles as
  environment smoke.

**Unknown knowns (true here, not yet applied)**
- ADR 0001's **billing alarm** and **voice-WAV exclusion** are decided but
  absent from plan.md's M2 done-means — the plan under-implements its own
  ADRs. (Patched below.)
- The probe chapter needs the *player-shaped* manifest to be judged "in situ";
  a bare M4A judged in a file manager under-sells journey-fit.
- `.war/` is gitignored; promotion path for this doc is docs/reports/ + plan
  amendments (existing ledger homes).

**Unknown unknowns pass**
- Frame drift: two "journey" books generated months after the events could
  contradict the vault/ADR record the reviewer can also read — self-inconsistency
  a scanner never flags. Counter: SOURCES.md pins + a provenance line per
  chapter stating generation date.

## The fight — moves that changed the route

- **M-A Probe gating (0.1).** Attack: "probe-first sequencing stalls the whole
  build if the GPU session slips; and 'owner judges consumable' has no kill
  trigger — an ambiguous chapter yields limbo." LANDED twice. Patch: (1) M1 is
  explicitly probe-independent — start any time; only M3 gates on 0.1.
  (2) Kill trigger defined: if after one regeneration with an adjusted journey
  prompt the chapter still reads as code-walkthrough (owner verdict), re-scope
  V1 to a single repo-story book; ADR 0005 gets amended, library page renders
  one book. FORK is a trigger now, not a mood.
- **M-B Same-origin assumption (1.2).** Attack: "player + SW were built for
  same-origin audio; ADR 0001 moves audio cross-origin to S3 — caching/seek
  breakage surfaces only after the site looks done." LANDED (sw.js read).
  Patch: new first task in M1 — cross-origin smoke: one stub chapter in the
  real bucket, played through the vendored player, **seek tested**, before
  layout work. FAIL of the smoke → counters in order: scope SW to shell-only
  caching (drop audio cache), else serve audio through Pages same-origin as a
  stopgap and record the tradeoff in an ADR note.
- **M-C Pages source (1.2/2.3).** Attack: "repo root can't be a website; /docs
  is taken." LANDED. Patch: fork with trigger — default route: GitHub Actions
  workflow publishing `site/` to Pages (keeps repo root clean, no root
  index.html clutter); if Actions is judged out-of-scope complexity, fall back
  to root-served `index.html` + `site/` assets. Decision lands as one line in
  an ADR-note at M1 start.
- **M-D Stub coupling (1.2).** Attack: "M1's 'done' referenced the probe
  chapter — re-couples M1 to M0." LANDED. Patch: stub = any short M4A + hand-
  written manifest; probe chapter is an optional upgrade, never a dependency.
- **M-E S3 verification (2.1).** Attack: "curl-GetObject proves the happy
  path only." Patch: verification = GetObject succeeds on audio prefix AND
  ListBucket returns 403 AND a non-audio key GET returns 403; billing alarm
  exists (ADR 0001) — all four checks in the done-means.
- **M-F Deploy hygiene (2.2).** Attack: "sync flags drift and a voice WAV or
  source text lands in the public bucket." Patch: deploy script allowlists
  audio+manifest extensions from an explicit dir (ADR 0001 wording), refuses
  env-var credentials (ADR 0006), and a post-deploy `aws s3 ls` diff is part
  of done-means. Owner runs it.
- **M-G Generation runway (3.x).** Attack: "GPU-hours × 2 near an unknown
  deadline." Partially blocked — resumable + start-early already in plan;
  residual risk unquantifiable until the deadline date is known (BLOCKED item).

## Premortem

Failed states, worked backward: (1) site "done" but audio won't seek on S3 —
same-origin assumption found too late (M-B counters this). (2) Probe verdict
ambiguous, three sessions burned polishing prompts — no kill trigger (M-A).
(3) Deadline arrives mid-generation-run (M-G + BLOCKED deadline). (4) Reviewer
opens repo, root is an index.html jumble over vault/docs/course — Pages-source
choice made lazily (M-C). (5) A voice WAV in the public bucket (M-F).

## Risk triage

- **TIGER — SW/cross-origin audio.** Prevention: M1 opens with the smoke test.
  Detection: seek test on real S3. Verification: screenshots + network log via
  /browse.
- **TIGER — probe limbo.** Prevention: one-regen kill trigger. Detection:
  owner verdict recorded in the vet. Verification: vet updated with dated
  verdict either way.
- **TIGER — unknown deadline.** Prevention: none possible in-repo. Detection:
  ask owner now. Verification: date recorded in plan.md header.
- **PAPER TIGER — transcript feature risk.** Already in the player; wiring only.
- **PAPER TIGER — pipeline capability.** Two complete prior books on disk.
- **PAPER TIGER — bucket leak.** ADR 0001 posture + M-E/M-F checks + owner-run
  deploys.
- **ELEPHANT — self-referential QA.** The same person (me) generates the
  books, builds the player page, and verifies the result; no fresh eyes until
  the reviewer. Named mitigation: /browse evidence artifacts per milestone +
  owner listening to at least one full chapter per book before ship.
- **ELEPHANT — story consistency.** Generated narrative vs committed record
  (vault, ADRs) can drift; reviewer can read both. Mitigation: SOURCES.md
  pins + provenance-per-book; narrative claims spot-checked against the
  pinned commits.

## Red-team record

- "Probe gates everything / has no kill condition" — **LANDED** → M-A patches.
- "Cross-origin audio breaks the vendored player's SW/seek" — **LANDED** (from
  sw.js read) → M-B smoke-first.
- "Pages can't serve this repo's layout" — **LANDED** → M-C fork.
- "Plan under-implements ADR 0001 (billing alarm, WAV exclusion)" — **LANDED**
  → M-E/M-F done-means.
- "Transcript feature is hidden new work" — **failed**: player.js already
  implements it.
- "Generation pipeline unproven at book scale" — **failed**: two complete
  books on disk.

## Verdict

Plan survives with amendments: M1 gains the cross-origin smoke as its first
task and the Pages-source fork; M1 decoupled from the probe; 0.1 gains a kill
trigger; M2 done-means absorb ADR 0001's alarm + exclusion checks and the
three-way curl verification; deadline date must be obtained from owner and
recorded. Abort condition for the plan as a whole: probe kill-trigger fires
AND single-book re-scope also fails journey-fit → drop the journey frame,
ship repo-story book as a straight product demo (value statement still holds).

## Outcome addendum (2026-07-21, post-wargame owner decisions)

This wargame targeted the S3-era plan and did its job: every landed attack
changed the design. Where things settled (see ADR 0008/0009 + llm-docs/plan.md):
- SW/cross-origin tiger → **dissolved**, not mitigated: owner moved audio
  in-repo (ADR 0008); the player's same-origin assumption is now simply true.
- Probe kill-trigger → replaced by the owner running the regenerate-and-judge
  loop directly.
- Pages-source fork → resolved: `main` + `/docs`; working notes renamed to
  `llm-docs/`.
- Deadline BLOCKED item → withdrawn; scheduling is the owner's concern.
- Third book added (next-chapter, generated last, range pinned — ADR 0009).
