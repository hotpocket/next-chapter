# Build plan — next-chapter V1

Sequenced build plan. Sources: the [before-AI rough draft](2026-07-20_project-rough-draft.md),
the [decisions index](../vault/decisions/README.md) (ADRs 0003, 0005–0009),
the [two-books vet](../vault/vets/two-books-journey.md), and the build-plan
wargame (red-team record promoted into the moves below). This feeds the
README's required "Project Plan" section.
Status: owner-reviewed 2026-07-21 (supersedes the S3-era draft; wargame
amendments + owner decisions applied). Scheduling/deadlines are the owner's
concern and deliberately absent here.

**Goal.** A GitHub Pages site — served from `docs/` of this repo — playing a
trilogy of audiobooks that narrate the site's own lineage: landry-ui (the
player), repo-story (the generator, vendored at `repo-story/`), next-chapter
(the assembly). Audio + transcripts committed in-tree; no AWS, no backend;
publishing is the owner's `git push`.

## Milestones

### M0 — Content probe (independent of M1; only M3 gates on it)
| # | Item | Done means | Notes |
|---|------|-----------|-------|
| 0.1 | One landry-ui chapter via the repo-story pipeline, prompts as-is | Owner runs the regenerate-and-tweak loop and ends it when satisfied | Doubles as GPU-environment smoke; kill of journey frame → re-scope per vet |

### M1 — Site scaffold (stub content; may start immediately)
| # | Item | Done means | Notes |
|---|------|-----------|-------|
| 1.1 | Manifest-format recon: diff repo-story output JSON vs vendored player expectations | Mismatches listed or "compatible" recorded | First build task (wargame RECON) |
| 1.2 | Vendor landry-ui player into `docs/` at pinned hash + provenance note | Player files in-tree, hash + source recorded | ADR 0006 |
| 1.3 | Library page (3 books) + player page + manifests in `docs/` | Stub book (any short M4A + hand-written manifest) plays end-to-end locally | Stub ≠ probe chapter (decoupled) |
| 1.4 | Read-along transcript visible — the skim path | Transcript readable without pressing play | Vet claim 2; player already supports it |
| 1.5 | /browse verification | Screenshots: library → book → chapter plays + seeks, transcript scrolls | Audio same-origin — SW works as designed (ADR 0008) |

### M2 — Pages live
| # | Item | Done means | Notes |
|---|------|-----------|-------|
| 2.1 | Enable Pages: `main` + `/docs` (owner clicks repo settings) | Stub book plays at the public URL; /browse re-verify | Repo public flip is the owner's gate |
| 2.2 | README gains the live-demo link | Link resolves | Part-8 requirement |

### M3 — Books (order forced by ADR 0009; starts after 0.1)
| # | Item | Done means | Notes |
|---|------|-----------|-------|
| 3.1 | landry-ui book | M4As + manifest + transcripts in `docs/`, every chapter <50 MB, plays at live URL | Probe chapter warms it |
| 3.2 | repo-story book | same | Narrates the vendored replayed history |
| 3.3 | next-chapter book — **last** | same + provenance pins narrated range ("through commit X") | Cannot contain its own generation |
| 3.4 | SOURCES.md: pinned hashes + per-book provenance records | Every narrated claim traceable | repo-story cites `Replayed-From` trailers |
| 3.5 | Owner listens to ≥1 full chapter per book before ship | Recorded in recap | Wargame elephant: self-referential QA |

### M4 — Submission polish
| # | Item | Done means |
|---|------|-----------|
| 4.1 | README Part-8 sections: problem, value, plan, features, technologies, AI tools (→ config-history.md), running, live link | Every heading present and true |
| 4.2 | prompt-history.md — curated index into vault/sessions/*-prompts.md | Reviewer-navigable build story (Part 9) |
| 4.3 | Part-11 checklist pass + hygiene scans (gitleaks + private token map) + commit tidy (owner squashes/pushes) | Every box verified, not assumed |

## Feature cut

- **Required:** library page (3 books), player + chapter nav, read-along
  transcripts, complete trilogy, live Pages URL.
- **Stretch / "with more time" (V2, the course's features-next answer):**
  move off Pages to properly hosted delivery (S3/CloudFront — the pattern
  already running in production for the owner's other book sites; ADR 0008)
  and visitor-submitted ingestion (ADR 0004). Smaller stretch: playback
  position memory, per-chapter deep links, audio QA passes.

## Standing rules

- Every feature /browse-verified before called done; recap + prompt export
  every session; dual hygiene scan (gitleaks + private token map) before
  every commit; owner runs pushes; publishing = push.
- Chapter size check (<50 MB) inside generation done-means — never brick a
  push (ADR 0008).

## Course-requirement map

Working app + HTML/CSS/JS → M1 · public repo + Pages + live link → M2 ·
README sections → M4.1 · prompt history → M4.2 (raw exports publish
per-session) · value demonstrated → the trilogy (M3) · code you can explain →
the books themselves + the decisions index.
