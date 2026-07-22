---
tags: [session]
type: session
concerns: [content, architecture, ux, legibility]
audience: []
summary: "Built the complete trilogy: M0.1 probe approved, then all three books generated via the vendored pipeline (16 chapters + 16 summary tracks, 4.6h, book 3 narrated through pinned 8295cae) and assembled into docs/ by new scripts/build-trilogy-site — /browse-verified, all sizes within Pages limits. Shipped the Full/Summary feature end-to-end: landry-ui player toggle (summary clock through the whole time model, 19 new browser checks) + pipeline Phase 5c summaries (manifest summary entries, summary_chunks, chapter_NNNN.summary.m4a). Research passes caught real bugs: scrub-dropped --feedback-url (site builds crashed), README deploy.sh drift, provenance pinning the wrong repo's HEAD."
created: 2026-07-21
status: completed
projects: [next-chapter]
branch: main
---

# 2026-07-21 — trilogy built

## Work

1. **M0.1 probe**: landry-ui "Performance War" chapter via the vendored
   pipeline; owner approved. GPU env verified: chatterbox pyenv env,
   RTX 3090, RTF ≈ 0.15 (26-min chapter in 4 min) — recorded in
   [[probe-pipeline-run]].
2. **Full/Summary feature, end-to-end** (owner-proposed for time-pressed
   reviewers): landry-ui player toggle after the TRANSCRIPT label — swaps
   audio, transcript, and the whole time model onto a client-computed
   summary clock; chapter-pane durations + track-bar marks mode-aware;
   persistence, chapter-nav, offline both tracks. Pipeline Phase 5c: each
   chapter's narrator also writes a ~12–18% summary; build scripts carry it
   (chunk prefix `chNN_summary_`, `chapter_NNNN.summary.m4a`, manifest
   `summary{}` entries with version-hash folding, `summary_chunks` in
   transcripts, build_book `summaries/` staging + invalidation). Tests:
   19 summary + 30 follow browser checks (landry-ui `df00047`); 41 shell
   checks + `test_build_site.py` + `test_build_m4a.py` (pipeline).
3. **All three books generated** (full skill pipeline per book: dossier →
   themes → paired code/history research → beats → Opus narration):
   landry-ui 6 chapters 1:45:51 · repo-story 5 chapters 1:30:35 ·
   next-chapter 5 chapters 1:21:29, narrated through pinned `8295cae`
   (ADR 0009). 16 chapters + 16 summaries, 4.6 h total audio.
4. **docs/ assembled** by new `scripts/build-trilogy-site` (tested):
   slug-prefixed audio dirs, merged transcripts with sha8 `?v=` busting,
   player pinned @ landry-ui `df00047` (PROVENANCE.md), SOURCES.md (M3.4),
   `.nojekyll`. `/browse`-verified: library, playback, Range seeking,
   Summary toggle, all three books, zero console errors.
5. **Bugs found by the process itself**: vendor-scrub had dropped
   `--feedback-url`'s add_argument (every site build crashed) — restored +
   regression-tested; repo-story README still documented the excluded
   `deploy.sh` — stitched; trilogy provenance pinned the enclosing repo's
   HEAD when the player dir wasn't a real checkout — now only pins genuine
   landry-ui checkouts; stray 1-char rule removed from local scrub rules.
6. **Size audit vs GitHub/Pages**: max file 13 MB (100 MB hard / 50 warn),
   docs/ 168 MB (1 GB soft), tracked repo 169 MB; bandwidth headroom ample.

## Discoveries

- Chatterbox on the RTX 3090 runs RTF ≈ 0.15 at ~7.4 GB VRAM — budget ~1/7
  of audio duration; the 2080 Ti-era 0.5–1.5× estimate is obsolete.
- Nested `.claude/agents/*` (vendored repo-story's) are not registered when
  the session runs from the parent repo root; inlining the agent brief into
  a `general-purpose` agent with `model: opus` preserves the
  Fable-plans/Opus-executes split cleanly for all four roles.
- The pipeline's research passes double as repo QA — they surfaced the
  scrub regression, the README drift, the "Audiobooks for Kara" 2-minute
  branding revert, and a provable invariant (repo-story's PLAN.md is
  byte-identical to its initial commit across all 25 commits).

## Decisions

- Summary mode is **audio + text** (own TTS track), not text-only — matches
  "have the summary read"; the two clocks don't map, so a mode switch
  restarts the chapter (encoded in player behavior).
- Summary data contract: manifest chapters gain
  `summary{filename,duration_s,size_bytes}` (version hash folds summary
  tuples so summary-only changes bust caches), transcripts gain
  `summary_chunks`, audio files are `chapter_NNNN.summary.m4a`.
- Chapter counts follow the material (6/5/5), not a uniform target;
  book 3 order: conceit → decisions → hygiene → legibility → pinned close.

## Next Steps

**Loose ends (cleanable now)**
- M2: owner pushes landry-ui (3 commits) + this repo, enables Pages
  (`main` + `/docs`), adds README live-demo link (~10 min, owner-gated).
- Owner listen-QA: ≥1 full chapter per book — the self-referential-QA
  elephant's mitigation; in progress at session end.

**Needs dedicated focus**
- M4.1 README Part-8 sections — every rubric heading present and true
  against the now-real product (~30 min; truthing, not drafting).
- M4.2 `prompt-history.md` — curated reviewer index into the four session
  prompt exports (~30 min; curation judgment).
- M4.3 Part-11 checklist pass + dual hygiene scans + commit tidy
  (dedicated session; owner squash/push decisions).

## Addendum (session continued through ship)

- Owner listen-QA passed; M4.1 (README Part-8 truthing) + M4.2
  (prompt-history.md) done; library book descriptions added (landry-ui
  e0c5ad6). Chapter-pane durations bug fixed on the summary clock
  (landry-ui df00047).
- Prompt exports regenerated CLEAN for all sessions: task-notification
  contamination predated this session (foundation 57→46, vendored 21→27);
  standing /home/<user> → ~ redaction added; both drifts regression-tested.
- Pre-public sweep (gitleaks full history, token map over files + commit
  messages, PII greps) → repo flipped PUBLIC, pushed, Pages live at
  https://hotpocket.github.io/next-chapter/ — M2 done. Favicon = Next
  Chapter program mark via registry favicon key.
- Provenance hardening: PROVENANCE.md records landry-ui:<path> @ <hash>,
  never machine paths; only real landry-ui checkouts get pinned.
- Owner verdict for next session: narration reads "a bit stilted" —
  address at the beats level (see todos).

Prompts: [[2026-07-21-trilogy-built-prompts]]
