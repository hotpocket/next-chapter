### `sync` — Run External Source Sync Pipeline

Sync external data sources into the vault. Currently supports ClickUp (docs, channels, tasks). Future modules: Figma, Google Docs, Zoom transcripts, Discord.

**Usage**: `sync [source] [options]`

#### `sync clickup`

Run the full ClickUp → vault sync pipeline. The pipeline lives at `vault/sync/clickup/run_sync.py` relative to the monorepo root.

**IMPORTANT: Two-phase execution.** The fetch stages (1-5) are long-running (10-30+ minutes due to API rate limiting) and don't need Claude Code. The classify/apply stages (6-8) are fast and benefit from AI classification. The skill splits execution across these two phases.

##### Phase 1: Fetch (user runs in their terminal)

1. **Locate the pipeline**: Resolve paths relative to the vault:
   ```bash
   REPO_ROOT="$(cd "$VAULT/../.." && pwd)"
   WRAPPER="$REPO_ROOT/scripts/sync-clickup.sh"
   ```
   If the wrapper doesn't exist, fail with: **"sync wrapper not found at `{path}`. Expected at `scripts/sync-clickup.sh` in the monorepo root."**

2. **Check prerequisites**:
   - A ClickUp OAuth token must be available (OAuth-only) — the wrapper auto-loads it from `${XDG_CONFIG_HOME:-~/.config}/clickup/oauth_token` (or `CLICKUP_OAUTH_TOKEN` / `CLICKUP_OAUTH_TOKEN_FILE` env vars)
   - Python 3 with `requests` package must be available

3. **Instruct the user** to run stages 1-5 in a separate terminal:

   Print the following:
   ```
   The fetch stages take 10-30+ minutes (ClickUp API rate limiting).
   Run this in a separate terminal and come back when it's done:

   {REPO_ROOT}/scripts/sync-clickup.sh --from 1 --to 5

   You'll see progress banners for each stage:
     Stage 1: Enumerate docs
     Stage 2: Fetch docs (slowest — 75+ doc groups)
     Stage 3: Fetch chat channels
     Stage 4: Fetch tasks from all lists
     Stage 5: Validate coverage

   Run telemetry lands at docs/logs/clickup/<timestamp>/.

   When you see "Stage 5 complete", come back here and say
   "sync done". I'll run AI classification and apply to the vault.
   ```

4. **Wait for user confirmation.** The user will say "sync done" (or similar). Do not proceed until confirmed.

##### Phase 2: Classify + Apply (agent runs inside Claude Code)

Once the user confirms fetch stages are done:

5. **Run stages 6-8** inside Claude Code (AI classification needs `CLAUDECODE=1`):
   ```bash
   CLAUDECODE=1 "$REPO_ROOT/scripts/sync-clickup.sh" --from 6
   ```

6. **Handle stage 6 classification**: The pipeline prints `CLAUDE_CLASSIFY` markers. For each marker, read the referenced file(s), generate summary/concerns/audience/skip decisions, and write `_classification.json` for each data type.

7. **Stages 7-8 run automatically**: Prepare vault notes in staging, diff against current vault, apply. Derivative notes (skipped, workspace graph, team roster) are regenerated.

8. **Report** final summary: counts per data type, new/modified/removed notes, team roster size.

##### Shortcut: Skip fetch (re-classify existing data)

If fetch data already exists from a previous run, skip straight to classification:
```
/vault sync clickup --from 6
```
This runs stages 6-8 inside Claude Code using the cached fetch output. No separate terminal needed.

##### Options:

| Flag | What it does |
|------|-------------|
| `--from N` | Resume from stage N (e.g., `--from 7` to re-prepare and apply) |
| `--only N` | Run only stage N |
| `--dry-run` | Show what would happen without API calls or vault changes |
| `--review` | Regenerate review markdown from existing classification JSON |
| `--url URL` | Sync a single ClickUp doc end-to-end (bypasses full pipeline) |

##### Examples:

```
/vault sync clickup                    — full pipeline
/vault sync clickup --from 7           — re-prepare and apply (skip fetch)
/vault sync clickup --only 4           — fetch tasks only
/vault sync clickup --dry-run          — preview without changes
/vault sync clickup --url "https://app.clickup.com/..."  — single doc
```

#### `sync status`

Show the last sync timestamp and counts for each data type.

##### Steps:

1. Read manifests from `vault/sync/clickup/output/{docs,channels,tasks}/_manifest.json`
2. For each manifest found, report: data type, item count, last sync timestamp
3. Report the team roster cache age from `vault/sync/clickup/output/_team_roster.json`

#### `sync` (no arguments)

List available sync sources and their status:
```
Available sync sources:
  clickup    ✓ configured (last sync: 2026-03-14, 808 docs + 55 tasks + 4 channels)
  figma      ✗ not configured (module not yet built)
  gdocs      ✗ not configured (module not yet built)
  zoom       ✗ not configured (module not yet built)
  discord    ✗ not configured (module not yet built)
```

