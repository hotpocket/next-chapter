# Vault Reference — Navigation, CLI, Token Budget

## During Work — Multi-Resolution Graph Navigation

The vault uses a progressive encoding strategy with 4 resolution levels. The agent navigates from cheap to expensive reads, stopping at the level that satisfies the current task.

### Resolution levels

```
Level 0: Frontmatter only    (~10 lines)      — tags, concerns, audience, summary
Level 1: Hub/index note       (~50 lines)      — synthesized bullets across a domain
Level 2: Vault note body      (~100-500 lines)  — full vault note content
Level 3: Source material      (external)        — raw external content, linked via source-url
```

### How to navigate levels

**When the agent encounters a wikilink during work:**

1. **Level 0 — Frontmatter scan.** Read ~10 lines. Check `audience`, `concerns`, `type`, `summary`. Decide if deeper reading is warranted for the current task. If `summary` answers the question, stop here.
2. **Level 1 — Hub note.** If the task touches a domain, read the concern hub at `$VAULT/concerns/`. The hub synthesizes knowledge across many notes into one compact index — a self-contained keyframe the agent can reason from without reading individual notes.
3. **Level 2 — Full vault note.** If the agent needs specifics about a component, pattern, or decision, read the full note body. Prefer notes where `audience` includes `claude-code`, unless the user explicitly requests otherwise.
4. **Level 3 — Source material.** Follow `source-url` to the external source content only when the agent needs the original wording (e.g., exact regulatory language, a specific upstream ticket's details). This is the lossless original — always available, rarely needed.

**Budget adaptation:** Context window is the bitrate. Small remaining budget → stay at Level 0-1. Deep task → go to Level 2-3. Budget determines depth, not a fixed rule.

### CLI Health Check (run once per session)

Before first CLI use, verify the CLI is enabled:

```bash
obsidian tags vault=$VAULT_NAME counts sort=count 2>&1 | head -3
```

If the output contains `Command line interface is not enabled`, **STOP and warn the user immediately:**

> **Obsidian CLI is disabled.** The vault skill requires the CLI for efficient queries. To enable it:
> 1. Open Obsidian
> 2. Open the vault: `$VAULT_NAME`
> 3. Go to **Settings → General → Advanced**
> 4. Toggle **"Command line interface"** ON
>
> Until this is enabled, vault queries will fall back to grep/file reads, which is significantly slower and wastes context window tokens.

Do NOT silently fall back to grep. The user must know the CLI is disabled so they can fix it.

### CLI-first lookups (MANDATORY)

**CRITICAL: You MUST use CLI commands before grep, bash, or file reads for any vault query. Never scan vault files with grep/bash/find — a single CLI call replaces dozens of file reads. Falling back to grep/bash without a prior CLI failure is a critical performance violation. Fallback chain: CLI → targeted single-file read → grep. Never skip steps.**

CLI queries are Level 0 operations — they return structured metadata without full file reads.

```bash
# Query a component's dependencies
obsidian vault=$VAULT_NAME property:read file="Component Name" name="depends-on"

# Find what depends on a component
obsidian vault=$VAULT_NAME property:read file="Component Name" name="depended-on-by"
obsidian vault=$VAULT_NAME backlinks file="Component Name"

# Find all outgoing links from a note
obsidian vault=$VAULT_NAME links file="Component Name"

# Find all notes of a type
obsidian vault=$VAULT_NAME tag verbose name="component"

# Search vault content
obsidian vault=$VAULT_NAME search format=json query="search term" matches limit=10

# Get note structure without full read
obsidian vault=$VAULT_NAME outline file="Component Name"

# Read a specific property (audience, summary, concerns, etc.)
obsidian vault=$VAULT_NAME property:read file="Component Name" name="audience"
obsidian vault=$VAULT_NAME property:read file="Component Name" name="summary"
```

Where `$VAULT_NAME` is the vault folder name (basename of `$VAULT`).

### File-read fallback (when CLI unavailable)

Fall back to file reads when the Obsidian CLI is not available:
- Need to understand a component? The project overview links to it. Read that one note.
- Need an architecture decision? The component note or project overview links to it. Follow the link.
- Need cross-project knowledge? Component/pattern notes link to domain notes. Follow the link.
- Need session history? Only read if you're stuck or the user references prior work.

### Directory listing before reading
List directory contents before reading files — know what exists without consuming tokens:
- `$VAULT/projects/{name}/**/*.md` — all notes for a project
- `$VAULT/domains/{tech}/*.md` — domain knowledge files

## Token Budget Rules

1. **CLI is mandatory**: `obsidian` CLI for property reads, backlinks, links, tags, and search. Never use grep/bash/find on vault files without a prior CLI failure. This is non-negotiable.
2. **Session start**: At most 4 Level 2 reads (TODOs + project overview + Session Log + latest recap). O(1) regardless of vault size.
3. **During work**: Navigate Level 0 → 1 → 2 → 3 progressively. Use `summary` and `audience` fields to decide depth. Stay at Level 0-1 when context budget is tight.
4. **Frontmatter first**: When scanning, read ~10 lines (Level 0) before committing to full read (Level 2)
5. **Audience filtering**: Prefer Level 2 reads on notes with `audience: [claude-code]`. Notes without this audience value are likely low signal-to-token ratio for the agent.
6. **List before read**: List directory contents before reading files
7. **Write concisely**: Bullet points, links, tags — no prose when bullets suffice

## Error Handling

- If the vault doesn't exist → suggest running `/vault init` to bootstrap it
- If the project doesn't exist in the vault → offer to run `/vault project` to scaffold it
- If a note already exists → show it instead of overwriting, offer to edit
- If no git repo is detected → use current directory name as project name
- If CLI command fails → fall back to file read for the same data

## Vault Structure Reference
```
$VAULT/
├── Home.md                           # Dashboard (read only if lost)
├── Vault Guide.md                    # Definitive reference for all conventions
├── concerns/                         # Concern hub notes — navigational indexes (9 domains)
├── projects/{name}/
│   ├── {name}.md                     # Project overview
│   ├── components/                   # Per-component notes
│   └── patterns/                     # Project-specific patterns
├── decisions/                        # ADRs and architecture decisions
├── domains/{tech}/                   # Cross-project knowledge
├── patterns/                         # Universal patterns
├── sessions/                         # Session recaps + Session Log index
├── todos/                            # Per-project TODO files + aggregate index
├── templates/                        # Note templates
└── skills/                           # Agent skill definitions
```

## CLI query examples & advanced syntax

The basic cheatsheet above uses the portable `$VAULT_NAME` form; these are concrete examples (with a placeholder vault name `my-vault`) plus the health-check, search-syntax, and Dataview-eval queries.

**Common queries:**
```bash
# Search vault content
obsidian search query="auth flow" vault=my-vault

# Backlinks to a note (what links to it)
obsidian backlinks file="EmailService" vault=my-vault

# Tags with counts
obsidian tags vault=my-vault counts sort=count

# Read a specific property from a note
obsidian property:read name=concerns file="EmailService" vault=my-vault

# Level 0 reads: check audience and summary before full read
obsidian property:read name=audience file="EmailService" vault=my-vault
obsidian property:read name=summary file="EmailService" vault=my-vault

# List incomplete tasks
obsidian tasks todo vault=my-vault

# Find orphan notes (no incoming links)
obsidian orphans vault=my-vault

# Find dead-end notes (no outgoing links)
obsidian deadends vault=my-vault

# Unresolved wiki-links
obsidian unresolved vault=my-vault
```

**Search syntax:**
- Property filters use `[property:value]` with brackets and colon: `query="[concerns:infra] [project:project-a]"`
- Exclude with `-`: `query="[concerns:infra] -[status:completed]"`
- Combine with OR: `query="(tag:#project-a OR tag:#project-b)"`
- Bare words without brackets are free-text search
- `path:folder` limits to a directory: `query="[concerns:infra] path:projects/project-a"`

**Link traversal:**
```bash
# Outgoing links from a note (what it links to)
obsidian links path="projects/project-a/project-a.md" vault=my-vault

# Backlinks to a note (what links to it)
obsidian backlinks file="AuthService" vault=my-vault
```

Note: `links` requires `path=`, not `file=`. `backlinks` works with either.

**Combining links + filters (Dataview eval):**

The CLI `search` and `links` commands can't be combined in one call. For queries that need link traversal AND property filtering, use Dataview's JS API via `obsidian eval`. Write the query to a temp file to avoid shell quoting issues:

```bash
cat > /tmp/dv_query.js << 'JSEOF'
let dv = app.plugins.plugins.dataview.api;
let p = dv.pages('outgoing([[projects/project-a/project-a]])');
let filtered = p.where(p => p.concerns && p.concerns.includes && p.concerns.includes('infra') && p.status !== 'completed');
filtered.map(p => p.file.path).array().join('\n');
JSEOF
obsidian eval code="$(cat /tmp/dv_query.js)" vault=my-vault
```

Dataview source selectors: `outgoing([[note]])` (what note links to), `[[note]]` (what links to note), `"folder"` (all notes in folder). Chain `.where()` for any property filter.

Reserve Dataview eval for multi-axis queries (links + properties + exclusions). For single-axis lookups, prefer the simpler CLI commands.

**When to use CLI vs Read tool:**
- **CLI**: metadata lookups, backlink/link traversal, tag queries, task lists, search, vault health checks (orphans, deadends, unresolved), complex filtered queries (Dataview eval)
- **Read tool**: when you need the full body content of a note (architecture details, Design sections, gen-spec rules)
