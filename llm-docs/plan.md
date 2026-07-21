# Build plan — next-chapter V1

Sequenced build plan, synthesized from the [before-AI rough draft](2026-07-20_project-rough-draft.md),
ADRs 0001–0006, and the [two-books vet](../vault/vets/two-books-journey.md).
This is the source for the README's required "Project Plan" section.
Status: DRAFT (pending owner review, then /wargame).

**Goal.** A GitHub Pages site playing two audiobooks — landry-ui and
repo-story — that narrate this project's own sources: the reviewer listens
(or skim-reads the transcript) to the backstory of the code powering the page
they're using. Player + JSON on Pages; audio on public-read S3; generation
offline on my GPU; zero request-time backend.

## Milestones

### M0 — Gates (before any site code)
| # | Item | Done means | Effort |
|---|------|-----------|--------|
| 0.1 | One-chapter landry-ui probe: generate one journey-focused chapter with the proven repo-story prompt flow | Owner judges it consumable + journey-fit → confirms/kills two-book shape (vet claims 1, 4). Kill → re-scope to single repo-story book | GPU session, ~1–2 h |
| 0.2 | repo-story visibility decision | scrub-then-public vs private + SOURCES.md trail decided, recorded (extends ADR 0005) | decision, ~15 min |
| 0.3 | /wargame this plan | plan survives or is amended; doc saved to docs/reports/ | ~30 min |

### M1 — Site scaffold (static, stub content)
| # | Item | Done means | Effort |
|---|------|-----------|--------|
| 1.1 | Vendor landry-ui player at pinned hash + provenance note (ADR 0006) | player files in-tree, hash + source recorded | ~30 min |
| 1.2 | Pages layout: library page (two books) + player page + manifest schema | site serves locally; stub book (probe chapter audio + manifest) plays end-to-end | ~half day |
| 1.3 | Read-along transcript visible in player — the skim path (vet claim 2, design requirement) | transcript renders alongside audio, usable without pressing play | in 1.2 |
| 1.4 | /browse verification | screenshots: library → book → chapter plays, transcript scrolls | ~15 min |

### M2 — Deploy rail (public URL live)
| # | Item | Done means | Effort |
|---|------|-----------|--------|
| 2.1 | S3 bucket per ADR 0001 posture (GetObject-only prefix, no ListBucket, ACL blocks on) | policy applied, verified from unauthenticated curl | ~1 h |
| 2.2 | Deploy script: audio→S3 sync via local AWS SSO profile, fail-loud credential hygiene; **owner runs it** | stub audio served from S3, site on Pages plays it at the public URL | ~1–2 h |
| 2.3 | Pages deployment of the site itself | live demo link exists (README requirement) | ~30 min |

### M3 — Content (start early; runs in parallel with M1/M2 after 0.1)
| # | Item | Done means | Effort |
|---|------|-----------|--------|
| 3.1 | Generation run: landry-ui book (probe chapter warms this) | full book: M4A chapters + manifest + transcripts, resumable checkpoints kept | GPU hours |
| 3.2 | Generation run: repo-story book | same | GPU hours |
| 3.3 | SOURCES.md: pinned commit hashes + per-book provenance | every narrated claim traceable to a source commit/note | ~1 h |
| 3.4 | Swap stub → real books; /browse re-verify both | both books play at the live URL | ~30 min |

### M4 — Submission polish
| # | Item | Done means | Effort |
|---|------|-----------|--------|
| 4.1 | README required sections (Part 8): problem, value, plan, features, technologies, AI tools (→ config-history.md), running, live demo link | every Part-8 heading present and true | ~1 h |
| 4.2 | prompt-history.md: curated index into vault/sessions/*-prompts.md | reviewer-navigable story of the build (Part 9) | ~1–2 h |
| 4.3 | Part-11 checklist pass + final hygiene scan + commit tidy-up (owner squashes) | every checklist box verified, not assumed | ~1 h |

## Feature cut

- **Required (delivers the value):** library page, player with chapter nav,
  read-along transcript, two complete books, live public URL.
- **Stretch (only if time remains, per rough draft):** playback
  speed/position memory, per-chapter deep links, audio QA passes
  (pronunciation/cadence), V2 ingestion (ADR 0004 — deferred, stays deferred).

## Standing rules during build

- Every feature /browse-verified before called done; recap + prompt export
  every session; hygiene scan before every commit; owner runs pushes and
  deploys.
- Generation (M3) is the schedule risk — start 3.1 immediately after 0.1
  passes, never leave GPU runs for deadline week.

## Course-requirement map

Working app + HTML/CSS/JS → M1–M2 · public repo → done · Pages deployment +
live link → M2 · README sections → M4.1 · prompt history → M4.2 (raw exports
already publish per-session) · meaningful commits → ongoing · value
demonstrated → the two books themselves (M3).
