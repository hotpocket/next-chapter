---
name: vault
description: "Obsidian vault memory via Obsidian CLI: orient, lookup, recap, note, todo, relate, stale, sync. Optional accelerator — vault-digest stays the file-first path."
disable-model-invocation: true
metadata:
  author: claude-conduct
  version: "4.0"
  upstream: adamtylerlynch/obsidian-agent-memory-skills v2.2
license: MIT
---

# Obsidian Agent Memory

You have access to a persistent Obsidian knowledge vault — a graph-structured memory that persists across sessions. Use it to orient yourself, look up architecture and component knowledge, and write back discoveries.

## Vault Discovery

Resolve the vault path using this chain (first match wins):

1. **Environment variable**: `$OBSIDIAN_VAULT_PATH`
2. **Agent config reference**: Parse the vault path from the agent's project or global config (look for "Obsidian Knowledge Vault" section with a path like `~/Documents/SomeName/` or a relative path like `./vault`)
3. **Repo-local vault**: If working inside a git repo, check for `<git-root>/vault/Home.md` (use `<git-root>/vault`), then `<git-root>/vault/working-knowledge/Home.md` (use `<git-root>/vault/working-knowledge`). This makes per-repo vaults zero-config — the vault lives with the code, gets versioned alongside it, and is auto-discovered when working in the repo.
4. **Default**: `~/Documents/AgentMemory`

Store the resolved path as `$VAULT` for all subsequent operations. Derive `$VAULT_NAME` as `basename "$VAULT"` for CLI calls.

**Relative paths in step 2** (e.g., `./vault` in CLAUDE.md) resolve relative to the git root, falling back to the current working directory if not in a git repo.

**Multi-vault discoverability**: Repo-local vaults can be symlinked into a common parent (e.g., `ln -s /path/to/repo/vault ~/Documents/AgentMemory/repo-name`) so Obsidian's vault switcher and cross-project tooling see them all without changing the canonical location. The symlink is transparent — the resolution chain still picks up the repo-local vault first.

Verify the vault exists by checking for `$VAULT/Home.md`. If the vault doesn't exist, inform the user and suggest running the `init` command to bootstrap a new vault from the bundled template.

## Session Start — Orientation

Orient in two phases: a **basic orientation** that always runs (cheap, before your first reply), then **ask the user what they're here for** before any expensive or history-specific work. The user may be here for a specific task — an import, an external-source sync, a bug — and not want session history or the TODO backlog at all.

### Phase 1 — Basic orientation (always)

1. **Detect the current project** from the working directory:
   ```bash
   basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || basename $(pwd)
   ```
   List `$VAULT/projects/*/`, match the repo/dir name, and read the matched overview at `$VAULT/projects/{name}/{name}.md` — the lay of the land: wikilinks to components, patterns, ADRs, domains. **Do not follow those links yet.**
2. **Grab the latest recap filename** — cheap; do NOT read the body yet, and do NOT `Read` the full Session Log (its table is ~15k tokens when you only need the last filename):
   ```bash
   grep -oE '\[\[20[0-9]{2}-[^]]+\]\]' "$VAULT/sessions/Session Log.md" | tail -1
   ```
   Row order in Session Log is the authoritative "latest" (not filename mtime, which drifts on touched files).

### Phase 2 — Ask what they want

Present the basic orientation (project + the last session's title/date) and ask the user what they'd like to do (a quick prompt). Offer, at minimum:
- **Catch me up** → read the latest session recap (`$VAULT/sessions/<filename>.md`) for what was done, decisions, and pending items.
- **TODO work-batch menu** → run the digest (below). Flag the **~5–7 min** cost.
- **A specific task** → they tell you (an import, an external-source sync, a bug, …); skip history and TODOs and go straight to it.

Don't read the recap body or run the digest unless the user asks. The vault IS the cross-session memory — but load only the slice the user actually needs.

### TODO digest (only on request)

`Read` [orient/todo-digest.md](orient/todo-digest.md) for the prompts, then dispatch a **foreground sub-agent** (`general-purpose`, **model: opus**) with **Prompt A**, pointed at the authoritative TODO files in `$VAULT/todos/` — all of them EXCEPT `Active TODOs.md` (non-authoritative aggregate that double-counts). The sub-agent reads the full backlog in its own context, writes the jq-validated partition to `/tmp/vault-orient/todo-batches.json`, and returns a ~1.5–2k **work-batch menu** whose counts derive from that file. Present the menu; the user picks a batch — `jq empty /tmp/vault-orient/todo-batches.json` to confirm it parses, then dispatch a drill-in sub-agent (**Prompt B**, same file) for that batch.

### What NOT to read at session start
- `Home.md` (only if you're lost)
- Component notes (only when working on that component)
- Domain indexes (only if you need cross-project knowledge)
- The Vault Guide (reference only, not for orientation)

## Automatic Behaviors

These behaviors apply to any agent using this skill. They do not require explicit commands.

### On session start

Run **Phase 1 (basic orientation)** — project overview + latest recap filename — without being asked, then **ask the user what they want** (catch-up / TODO digest / a specific task) per the Session Start procedure above. Don't auto-read the recap body or auto-run the TODO digest. If the vault doesn't exist at the resolved path, inform the user and suggest running `init`.

### On session end signals

When the user says "done", "wrapping up", "that's it", "let's stop", or similar end-of-session language — offer to run a recap. Don't auto-run; ask first: "Want me to run a recap before we wrap up?"

### On component discovery

When you deeply analyze a component that has no vault note — and the project has an active vault — offer to create a component note and infer relationships from imports and dependencies. Example: "I noticed there's no vault note for the AuthMiddleware component. Want me to create one and map its dependencies?"

### On vault note modification

After modifying any vault note during a session, check its `depended-on-by` list. If non-empty, report downstream notes that may need refresh. Do not auto-update — let the user decide. See the `stale` command for details.

### On first run

When the vault doesn't exist at any resolved path, guide the user through `init`, then auto-scaffold the current project if inside a git repo.

## Commands

Command procedures live in per-command files under `commands/`, loaded on demand (they are **not** auto-loaded). **When a command is invoked, `Read` its file below before executing — do not run from this index alone; the index names commands but omits the step-by-step procedure.**

| Command | Procedure file | What it does |
|---------|----------------|--------------|
| `help`    | [commands/help.md](commands/help.md)       | Show available commands + usage examples |
| `install` | [commands/install.md](commands/install.md) | Symlink skill into `~/.claude/skills/vault/` (tracks the repo) |
| `init`    | [commands/init.md](commands/init.md)       | Bootstrap + register a new vault |
| `analyze` | [commands/analyze.md](commands/analyze.md) | Scan repo, hydrate vault notes |
| `recap`   | [commands/recap.md](commands/recap.md)     | Generate / search / list session recaps |
| `project` | [commands/project.md](commands/project.md) | Scaffold a new project in the vault |
| `note`    | [commands/note.md](commands/note.md)       | Create component/adr/pattern note from template |
| `todo`    | [commands/todo.md](commands/todo.md)       | View / update per-project TODOs |
| `lookup`  | [commands/lookup.md](commands/lookup.md)   | Search vault (deps, consumers, related, type, freetext) |
| `relate`  | [commands/relate.md](commands/relate.md)   | Create / query note relationships |
| `stale`   | [commands/stale.md](commands/stale.md)     | Check derived-note staleness |
| `sync`    | [commands/sync.md](commands/sync.md)       | Run external-source sync pipeline into the vault (ClickUp) |

## Reference

`Read` these on demand when a task needs them — they are **not** loaded automatically:

- [reference/navigation.md](reference/navigation.md) — multi-resolution reading levels, CLI health check, the **CLI-first mandate**, CLI command cheatsheet, file-read fallback, token-budget rules, error handling, vault structure reference.
- [reference/conventions.md](reference/conventions.md) — when/where to write, scoping rules, frontmatter + `audience`/`concerns` vocabularies, wikilink conventions, note templates, generation pipeline.
- [orient/todo-digest.md](orient/todo-digest.md) — the menu (Prompt A) + drill-in (Prompt B) sub-agent prompts used by session-start orientation Step 1.
