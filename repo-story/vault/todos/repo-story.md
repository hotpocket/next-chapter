---
tags: [todo, repo-story]
type: todo
created: 2026-05-22
---

# repo-story TODOs

## Open

- [ ] Offline-download stuck on "Preparing…" over plain-HTTP LAN. Pick: HTTPS-with-self-signed-cert serve.py, OR patch player to detect `!isSecureContext` and hide/disable the download button. — *from [[2026-05-22 - audiobook pipeline + multi-book deploy]]*
- [ ] If the library grows past 2 books on [family-site], consider lazy-loading transcripts per book (current merged transcripts.json is 15 MB).
- [ ] Move the per-repo-vault + symlink convention into the canonical skill's bundled template (so future `/vault init` runs get it for free).
- [ ] If the narration-fluff complaint returns, redesign at the Phase 5a beats level (arc/framing, not word pruning) and prototype on one chapter for user judgment (~1–2 h; changed chapters need chunk WAVs re-rendered; word-pruning pass already tried and rejected 2026-07-10). — *from [[2026-07-10 - fable-opus model split]]*

## Completed

- [x] Guard `build_audio.py::split_into_chunks` against degenerate chunks (no word characters, e.g. `"..."`) — mirrors wbt's ch-1073 voice-sample-leak fix (Chatterbox hallucinates the conditioning sample's transcript on near-zero phonetic content; see wbt `LEAK_INVESTIGATION.md`). Verified no existing repo-story section produces a degenerate chunk, so cached chunk indices are unaffected. Note: the guard shifts indices for any future section containing one — delete that section's cached chunk WAVs before regenerating. (2026-07-02)
- [x] Retire single-M4B staleness: added `build_m4a.py` (per-chapter M4As + chapters_manifest.json, verified byte-identical structure vs deployed mattpocock manifest); `build_transcripts.py` was already per-chapter-compatible; [[AUTORUN]] Phase 7/8 now route through [family-site-deploy]/books.json as the primary publish path. `build_site.py`+M4B kept as the brandonlandry.com path. (2026-07-02)
- [x] luinst SSH/HTTPS degradation — documented in AUTORUN.md constraints (HTTPS env override, fall back to cached `player/`); [family-site-deploy]/deploy.sh handles it with `--skip-lui-deps` + ls-remote SHA cache. (2026-07-02)
- [x] Commit pending changes in repo-story: AUTORUN.md, .gitignore additions, CLAUDE.md vault pointer, vault/ (committed; `.python-version` gitignored as local pyenv state). (2026-07-02)

- [x] Take a GitHub URL and produce an audiobook end-to-end via the repo-story pipeline (validated on mattpocock/skills, 2026-05-22).
- [x] Diagnose + fix chapter-click bug (per-chapter M4A model).
- [x] Diagnose + fix transcripts not loading (slug mismatch).
- [x] Deploy mattpocock-skills book alongside WBT at [family-site]/books/.
- [x] Promote one-off side-deploy into durable multi-book pipeline ([family-site-deploy]/books.json + build_site/transcripts --config).
- [x] Initialize repo-story local vault + patch canonical skill for repo-local discovery.
