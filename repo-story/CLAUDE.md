# repo-story

Claude Code skill that analyzes repositories and produces audio walkthroughs of their features and the prompts that shaped them.

## Build pipeline

1. Skill phases (in Claude Code): Survey → Explore → Inventory → Research → Narrate → `output/sections/` + condensed `output/summaries/` (Phase 5c — final step of each chapter; feeds the player's Full/Summary toggle)
2. `build_audio.py` — sections → chunk WAVs → chapter WAVs → chaptered M4B (pass `--title`/`--artist`; album is always `Repo Story`); summaries → `summary-NN-*.wav` (never in the M4B)
3. `build_m4a.py` — chapter WAVs → per-chapter M4As + `chapters_manifest.json` (**production format** for the landry-ui player); summary WAVs → `chapter_NNNN.summary.m4a` + manifest `summary` entries
4. `build_transcripts.py` — chunk WAVs + section/summary text → `transcripts.json` (per-chapter timestamps; `summary_chunks` per chapter)
5. Publish, one target:
   - **next-chapter GitHub Pages (this repo's parent)** — copy per-chapter
     M4As, `chapters_manifest.json`, and `transcripts.json` into the parent
     repo's Pages site; the user publishes with `git push`. No AWS, no deploy
     scripts (see the parent repo's plan + ADRs).

`AUTORUN.md` is the end-to-end execution contract for unattended runs.

## UI component

The player is fetched from [landry-ui](https://github.com/hotpocket/landry-ui) via `luinst`. The `player/` directory is gitignored.

```bash
./luinst audiobook/vanilla player/
```

## Feedback API


## Obsidian Knowledge Vault

Persistent knowledge vault at `./vault`. Symlinked into `~/Documents/AgentMemory/repo-story` for cross-project discoverability.

**At session start**, orient from the vault: read `vault/sessions/Session Log.md`, then the latest recap it points to, then `vault/todos/repo-story.md`. This is cross-session memory — the recap from the prior session usually has the context you need to pick up where things left off.

**At session end** or on "wrapping up" signals, offer to run `/vault recap`. Don't auto-run; ask first.

Use `/vault` commands (or natural-language vault requests like "show me the todos" / "save this as an ADR") for all vault operations — see the vault skill at `~/.claude/skills/vault/SKILL.md` for the full conventions (note formats, frontmatter rules, audience filtering, multi-resolution graph navigation).

## See also

- [TODOS.md](TODOS.md) — project TODO list
