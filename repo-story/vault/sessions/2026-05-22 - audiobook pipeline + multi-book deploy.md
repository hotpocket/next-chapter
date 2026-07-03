---
tags: [session]
type: session
concerns: []
audience: [dev, claude-code]
summary: "Full repo-story pipeline run on mattpocock/skills; diagnosed and fixed two player bugs; promoted per-repo deploy into [family-site-deploy]'s multi-book pipeline via books.json + build_site/transcripts --config support."
created: 2026-05-22
status: completed
projects: [repo-story]
branch: main
---

# 2026-05-22 — audiobook pipeline + multi-book deploy

## Context

Question: does repo-story have enough to take a GitHub URL and produce a podcast end-to-end? Confirmed yes (no auto-clone helper but trivial to add), then ran the full pipeline on `github.com/mattpocock/skills`. Two production bugs surfaced on the deployed player; fixed both, then promoted from one-off side-merge into the durable `[family-site-deploy]/deploy.sh` multi-book pipeline. Final: two books live at [family-site]/books/.

## Work Done

1. **Wrote [[AUTORUN]]** — single-file runbook at repo root. GitHub URL → audiobook + site in 9 phases. Folder convention (`<repo-name>/repo/` + `<repo-name>/output/`), decision rules, no-SSH/no-deploy constraints. References [[PLAN]] and `prompts/` for methodology depth but is self-sufficient for execution.

2. **Full repo-story pipeline on mattpocock/skills** — 5 exploration agents (alignment, shared-language, feedback-loops, architecture, workflow-ops) → 5 themes (anti-isolation, two-modes, state-machines, durability-over-precision, self-fractal) → 8 research agents in parallel (4 code-verification + 4 history/landscape via WebSearch) → 5 narrative sections (~16,400 words) → 113.7-minute audiobook (5 chapters, 89 MB M4B initially; later split to per-chapter M4As) → static site.

3. **Diagnosed two player bugs** via gstack `browse` headless verification:
   - Transcripts not loading → slug mismatch (build_transcripts.py default `--slug book` vs my use of `mattpocock-skills`).
   - Chapter clicks "restart chapter 1" → the landry-ui player switched to a per-chapter M4A model (`chapter.filename` per chapter). My pipeline produced a single book.m4b. Repo-story's build_audio/build_site lag this architecture change.

4. **Rebuilt the site in per-chapter format** — ffmpeg-encoded 5 chapter WAVs to AAC M4As (24kHz mono 64k +faststart with title metadata), wrote chapters_manifest.json, paragraph-based transcripts.json (slug=`book`), copied current player files (including PWA assets) from `landry-ui-playground/lui-deps/player/`. Headless-verified.

5. **Diagnosed offline-download stuck on "Preparing…"** — Cache API requires a secure context. Plain HTTP on LAN IP (192.168.5.50) → `caches` is undefined → synchronous TypeError after the button shows "Preparing…", cleanup never runs. Reproduced via browse: `isSecureContext: false` on LAN, `true` on 127.0.0.1. Same applies to service worker registration and PWA install.

6. **Durable multi-book deploy pipeline** (in landry-ui-playground and [family-site-deploy]):
   - **[family-site-deploy]/books.json** new file. Single source of truth: slug, title, artist, manifest path, audio_prefix per book. Two entries: `book` (WBT, prefix=\"\") and `repo-story` (prefix=\"repo-story/\").
   - **landry-ui-playground/audiobook/build_site.py** added `--config` flag. Multi-book mode loops over entries, builds per-prefix audio subdirs, emits one index.html with multi-element books array. Single-book mode (no --config) preserved.
   - **landry-ui-playground/audiobook/build_transcripts.py** added `--config`. Refactored WBT-style into `build_wbt_style_chapters()`. New `load_book_transcript()` dispatches on `transcripts_path` (preload) vs `source_dir+titles_file` (regen).
   - **[family-site-deploy]/deploy.sh** detects books.json, passes --config, expands state hash to include books.json + each book's manifest dir, sync now picks up per-book manifests recursively.

7. **Deployed via real deploy.sh --skip-lui-deps** — both books live, transcripts (1000 + 5 chapters), per-book manifests, immutable audio, CloudFront invalidation completed. Deleted the redundant one-off side-deploy script.

8. **Vault setup** — initialized this local vault at `./vault`, patched the canonical skill at `~/git/[private-repo]/vault/working-knowledge/skills/vault/SKILL.md` to add step 3 (repo-local discovery: `<git-root>/vault/Home.md` auto-detected) plus relative-path support in CLAUDE.md and a symlink convention note. Synced to `~/.claude/skills/vault/`. Symlinked `~/Documents/AgentMemory/repo-story` → this vault.
   - **Scaffolded the project entry** at `vault/projects/repo-story/repo-story.md` with the architecture summary, plus stub `components/` and `architecture/` dirs ready for future component notes and ADRs.
   - **Added vault personal-state ignores** to `repo-story/.gitignore` (workspace.json, workspace-mobile.json, plugins/, themes/, hotkeys.json, appearance.json, graph.json — mirroring the hh repo's convention). Shared config + notes get committed; per-user UI state doesn't.
   - **The canonical SKILL.md picked up proper YAML frontmatter** (name, description, metadata.author, version 4.0, upstream attribution, MIT license) — likely via a linter or follow-up edit during the patch. Worth knowing because the description field is what Claude Code uses to decide when to load the skill, so any future skill changes must keep the frontmatter intact.

## Discoveries

- **The landry-ui player switched to per-chapter M4As**; repo-story's `build_audio.py`/`build_site.py`/`build_transcripts.py` still produce single-M4B output. The headless test showed single-M4B chapter-click works *inside* the file (currentTime jumps within the M4B), but the deployed player expects per-chapter audio sources. Repo-story's scripts are effectively stale relative to the actual deploy path.
- **Cache API + service worker stack only works in a secure context.** Plain HTTP on a LAN IP disables offline-download and PWA install entirely. Two paths to fix: HTTPS w/ self-signed cert, or graceful degradation in the player.
- **`landry-ui-playground/lui-deps/player/player.js` is 857 lines; `repo-story/player/player.js` is 646 lines.** The latter is stale (HTTPS fetch fell back to the local copy when SSH was off-limits). Missing PWA assets (sw.js, manifest.webmanifest, icons/).
- **`[family-site-deploy]/deploy.sh` has a finely tuned no-op fast path via state-hash.** Multi-book mode preserves it — touching books.json or any book's manifest dir triggers a deploy; nothing else does.
- **gstack `browse` is the right tool** for headless verification of the deployed player. Used it heavily this session for both bug repro and post-fix verification. Discovered `isSecureContext`-gated behavior cleanly.
- **Vault skill canonical/installed paths**: canonical lives at `~/git/[private-repo]/vault/working-knowledge/skills/vault/SKILL.md`, installed at `~/.claude/skills/vault/SKILL.md`. `/vault install` is what syncs them. Edit canonical, then install.

## Decisions

- **Per-repo folder convention** (AUTORUN.md): `<repo-name>/repo/` for clone + `<repo-name>/output/` for artifacts, run all scripts from inside the per-repo folder so default `output/...` paths just work. Documented.
- **Multi-book audio namespacing**: legacy book uses empty audio_prefix (no path collisions with existing chapter_NNNN.m4a); additions use `<book>/` prefix subdirs. Player just consumes `audioBaseUrl + chapter.filename`.
- **Transcript merge strategy**: each book ships its own pre-built transcripts.json (under its slug); deploy aggregates by slug. WBT-style on-the-fly generation remains supported for books that don't pre-build.
- **No-SSH constraint** applied throughout — HTTPS-only git clone (mattpocock/skills succeeded; landry-ui failed because private), `--skip-lui-deps` to deploy.sh.
- **Vault location**: local-to-repo (`./vault`) for stability+portability; symlink into `~/Documents/AgentMemory/` for cross-project discoverability. Skill patched so repo-local discovery is zero-config (step 3 in resolution chain).

## Next Steps

See [[repo-story]] todo file for the persistent task list. Captured at this point:

- [ ] Repo-story's `build_audio.py`/`build_site.py`/`build_transcripts.py` are stale (single-M4B model). Either point AUTORUN.md at `landry-ui-playground/audiobook/build_*.py` instead, or rewrite repo-story's scripts to produce per-chapter M4As natively.
- [ ] Decide on the offline-download bug: HTTPS-with-self-signed-cert serve.py variant, OR patch player to detect `!isSecureContext` and hide/disable the download button gracefully.
- [ ] No git commits yet in repo-story this session — AUTORUN.md, gitignore changes, and CLAUDE.md additions are uncommitted.
- [ ] If the library grows past 2 books, consider lazy-loading transcripts per book (current merged transcripts.json is 15 MB).
- [ ] Symlink convention: write up the pattern (per-repo vault + `~/Documents/AgentMemory/<repo>` symlink) somewhere durable. Maybe in the canonical skill's vault-template/Home.md, so all new vaults get the convention.

## Files Touched

- `repo-story/AUTORUN.md` (new)
- `repo-story/.gitignore` (per-repo folders ignore + vault personal-state ignores)
- `repo-story/CLAUDE.md` (added Obsidian Knowledge Vault section)
- `repo-story/vault/` (new — this vault: Home.md, sessions/, todos/, projects/repo-story/)
- `repo-story/vault/projects/repo-story/repo-story.md` (project overview)
- `repo-story/mattpocock-skills/` (new — entire pipeline output, gitignored)
- `repo-story/mattpocock-skills/build_per_chapter_site.py` (per-chapter site rebuild helper)
- `[family-repo]/[family-site-deploy]/books.json` (new)
- `[family-repo]/[family-site-deploy]/deploy.sh` (multi-book mode)
- `landry-ui-playground/audiobook/build_site.py` (multi-book)
- `landry-ui-playground/audiobook/build_transcripts.py` (multi-book)
- `hh/vault/working-knowledge/skills/vault/SKILL.md` (repo-local discovery + symlink convention + YAML frontmatter for skill metadata)
- `~/.claude/skills/vault/SKILL.md` (synced from canonical)
- `~/Documents/AgentMemory/repo-story` (symlink → repo-story/vault)
