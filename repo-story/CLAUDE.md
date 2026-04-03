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


## See also

- [TODOS.md](TODOS.md) — project TODO list
- `scripts/generate-manifest.sh` — generates manifest.json for brandonlandry.com
