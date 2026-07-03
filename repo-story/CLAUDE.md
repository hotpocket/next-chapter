# repo-story

Claude Code skill that analyzes repositories and produces documentary audio narratives.

## Build pipeline

1. Skill phases (in Claude Code): Survey → Explore → Synthesize → Research → Narrate → `output/sections/`
2. `build_audio.py` — sections → chunk WAVs → chapter WAVs → chaptered M4B
3. `build_transcripts.py` — chunk WAVs + section text → `transcripts.json`
4. `build_site.py` — M4B + player component → static site in `output/site/`
5. `deploy.sh` — sync to S3 + CloudFront

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
- `scripts/generate-manifest.sh` — generates manifest.json for brandonlandry.com
