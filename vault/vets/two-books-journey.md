---
tags: [vet]
type: vet
summary: "landry-ui + repo-story as V1's two audiobooks, framed as journey narrative: the easiest way for the reviewer to consume the backstory and reasoning of how I got here"
status: probing
created: 2026-07-20
concerns: [admissions-project, content]
---

# Vet: two books (landry-ui, repo-story) as journey narrative

Kernel (adjusted per owner): making landry-ui and repo-story V1's two
audiobooks gives the reviewer the easiest possible way to consume the
backstory and reasoning of how I got here — the journey told in the product
itself. Dogfooding is a bonus, not the point. Frame chosen: **journey
narrative** (autobiography first, demo second).

## Tree

- [load-bearing] The pipeline can produce a *journey* narrative (my reasoning and building arc), not just a code walkthrough — feed: generate one landry-ui chapter journey-focused and judge "is this my story, consumable?"; note the prompt flow was designed for a repo's historical arc, and repo-story's vault sessions are a new, untested source type. **pending**
- [load-bearing] The reviewer actually consumes it — audio demands minutes; a skimming reviewer may never press play — feed: ship the read-along transcript visible on the page (skim path); pipeline already produces time-aligned transcripts. Converted to a design requirement. **pending**
- [load-bearing] Journey frame survives the rubric's value test — **confirmed** (owner, 2026-07-20): the "another person" is the reviewer — a listener who can't dig through the repos, brought up to speed on the code powering the very page they're using. Part 2 value holds unamended; no conflict.
- [likely] The material supports a coherent arc — repo-story: ~40 commits + vault session notes (rich); landry-ui: sparse history but its extraction-from-repo-story story lives in repo-story's history (verified this session) — feed: the one-chapter probe doubles here. **pending**
- [likely] Journey focus doesn't cost the demo purpose — same artifact serves both by construction. **confirmed** (by construction)
- [likely] Generation fits the schedule — pipeline proven end-to-end (mattpocock book exists), resumable; two runs of GPU-hours — feed: start generation early, not at deadline. **confirmed** (prior runs)
- [speculative] Private-repo access matters less under the journey frame (audio carries the story even if the subject repo stays private) — SOURCES.md still required for verification claims — feed: ADR 0005's visibility items stand regardless. **pending**

## Hostile pass

Inline stress (proportionate; the full /wargame stays reserved for build plans):

- "Navel-gazing: two self-referential books read as an ego project against a rubric asking 'valuable to another person'" — **LANDED**; promoted to load-bearing claim 3 (value-statement reconciliation). The strongest catch of this vet.
- "landry-ui book runs thin (small repo, short history)" — partially blocked: its origin story lives in repo-story's commits; the one-chapter probe is the judge.
- "Reviewer never listens" — mitigated by transcript-skim design requirement (claim 2).
- ~~"Generation collides with deadline"~~ — killed: proven resumable pipeline, scheduled early (ADR 0005).

## Probes

- [ ] probe: generate one journey-focused landry-ui chapter with the proven prompt flow and judge consumability + journey-fit → confirms/kills claims 1 and 4
- [x] probe: reconcile Part 2 value statement with the journey frame → RESOLVED 2026-07-20: reviewer IS the listener the value statement describes; claim 3 confirmed, no amendment needed
- [ ] probe: player/site design includes visible read-along transcript as the skim path → confirms claim 2

## Verdict

- 2026-07-20 (later) — **proceed.** The cheap kill-probe resolved in the owner's
  frame: reviewer = the listener; value statement unamended. Remaining probes
  (one-chapter consumability, transcript skim path) become build-time
  verifications, not gates. ADR 0005 unconditionally accepted.
- 2026-07-20 — **probe-first.** No claim is dead; three named probes gate
  proceed. Cheapest kill first: the value-statement reconciliation (an hour of
  writing) can kill the journey frame outright if no honest reconciliation
  exists; the one-chapter generation probe is the expensive one and should not
  run before the cheap one passes. Flip condition: reconciliation fails →
  reframe content selection (e.g. one journey book + one third-party book) and
  re-vet.

## Open questions

- Does the reviewer rubric weigh "valuable to another person" against the
  content of the app, or only against the app's function? (Interview may
  answer; affects how hard claim 3 binds.)
