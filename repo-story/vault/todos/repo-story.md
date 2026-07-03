---
tags: [todo, repo-story]
type: todo
created: 2026-05-22
---

# repo-story TODOs

## Open

- [ ] Repo-story's `build_audio.py`/`build_site.py`/`build_transcripts.py` are stale (single-M4B). Either retire them in favor of `landry-ui-playground/audiobook/build_*.py` (and update [[AUTORUN]] to point there), or rewrite to produce per-chapter M4As natively. — *from [[2026-05-22 - audiobook pipeline + multi-book deploy]]*
- [ ] Offline-download stuck on "Preparing…" over plain-HTTP LAN. Pick: HTTPS-with-self-signed-cert serve.py, OR patch player to detect `!isSecureContext` and hide/disable the download button. — *from [[2026-05-22 - audiobook pipeline + multi-book deploy]]*
- [ ] Commit pending changes in repo-story: AUTORUN.md, .gitignore additions, CLAUDE.md vault pointer, vault/ itself (decide what to commit vs gitignore).
- [ ] If the library grows past 2 books on [family-site], consider lazy-loading transcripts per book (current merged transcripts.json is 15 MB).
- [ ] Move the per-repo-vault + symlink convention into the canonical skill's bundled template (so future `/vault init` runs get it for free).
- [ ] `landry-ui` repo requires SSH access for `luinst` — HTTPS clone fails (private). Document or make luinst HTTPS-aware so it degrades gracefully.

## Completed

- [x] Take a GitHub URL and produce an audiobook end-to-end via the repo-story pipeline (validated on mattpocock/skills, 2026-05-22).
- [x] Diagnose + fix chapter-click bug (per-chapter M4A model).
- [x] Diagnose + fix transcripts not loading (slug mismatch).
- [x] Deploy mattpocock-skills book alongside WBT at [family-site]/books/.
- [x] Promote one-off side-deploy into durable multi-book pipeline ([family-site-deploy]/books.json + build_site/transcripts --config).
- [x] Initialize repo-story local vault + patch canonical skill for repo-local discovery.
