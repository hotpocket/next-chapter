---
name: conduct
description: "Stamp a repo with Claude conduct: CLAUDE.md preamble, vault-digest + SessionStart hook, vault/ scaffold, .gitignore lines. Idempotent on existing repos."
disable-model-invocation: true
metadata:
  author: setup-kit
  version: "1.0"
license: MIT
---

# Claude Conduct

Stamp a repo with the reusable scaffold that tells Claude how to behave on this
project: orient from memory at session start, write discoveries back, follow a
predictable docs layout, and obey the rules of conduct. The *project-specific*
content (pipelines, prompts) is NOT part of this kit — only the reusable shell.

## Commands

### `init` (default)
Stamp the current repo (git root). Idempotent — never clobber existing content;
add only what's missing and report what already existed vs what was created.

1. **`CLAUDE.md`** — section-aware, idempotent:
   - **If absent**, copy `templates/CLAUDE.md` to the git root and replace
     `<PROJECT>` with the repo's directory name.
   - **If present**, do NOT overwrite. Scan it for each canonical section the
     template provides — `## Session conduct`, `## Docs layout`,
     `## Skills available here`, `## Rules of conduct` — matching by intent, not
     just exact heading text (a repo may already cover "rules" under another
     name). **Report** which are present vs missing. If any are missing, show the
     user the exact content that would be added and **ask to merge**. On confirm,
     intelligently merge ONLY the missing sections: preserve every existing line
     and the user's own rules, place each new section sensibly, fold rather than
     duplicate where a section partially exists (e.g. add the brevity rule to an
     existing rules list instead of starting a second one), and never add a
     section that's already covered. Re-running converges — once all sections
     exist, there is nothing to add.
2. **Vault tooling** — make orientation deterministic and vault access cheap,
   all **file-based (no Obsidian app/CLI/GUI)**:
   - Copy `templates/vault-digest` to `scripts/vault-digest` (create `scripts/`
     if needed) and `chmod +x` it. Pure grep/awk reads of the vault's frontmatter
     — Level-0 summaries, `type`/`concern` filters, recap, todos, backlinks — the
     agent's default low-token access path.
   - Copy `templates/session-start.sh` to `scripts/session-start.sh` and
     `chmod +x` it. It delegates to `vault-digest` and prints *pointers only*
     (recap + open-todo count).
   - **Do NOT stamp a project `.claude/settings.json` hook.** Orientation is
     driven by the ONE global `SessionStart` router `~/bin/claude-orient` (shipped
     by `.configs`, registered once in `~/.claude/settings.json`); it `exec`s this
     repo's `scripts/session-start.sh`. A global router avoids per-repo hook-trust
     prompts, works in repos whose `.claude/settings.json` is the global file, and
     is the same mechanism that serves un-owned repos (see `adopt`).
3. **`vault/` scaffold** — if `vault/Home.md` is absent, bootstrap a vault via the
   `/vault init` command (the canonical vault skill owns the structure). Then make
   it cross-project discoverable:
   `ln -s "$(git rev-parse --show-toplevel)/vault" ~/Documents/AgentMemory/<PROJECT>`
   (skip if the symlink already exists; `mkdir -p ~/Documents/AgentMemory` first).
4. **`.gitignore`** — ensure the lines from the "Gitignore" section below are
   present (append any missing; don't duplicate).
5. **No-push guard (global, once)** — install `templates/deny-git-push.sh` to
   `~/bin/deny-git-push.sh` (`chmod +x`) and register it as a `PreToolUse`
   matcher `Bash` hook in the **global** `~/.claude/settings.json` (skip if
   already registered — idempotent). It mechanically denies any `git push` (force
   or plain; compound and `git -C` forms included) so the agent cannot push. This
   is a **global** hook, not a per-repo project hook — consistent with the global
   `SessionStart` router (step 2) and the "no project `.claude/settings.json`
   hook" stance: one registration protects every repo, owned, adopted, or not.
   The matching rule lives in the CLAUDE.md template's Rules of conduct as the
   human-readable why.

### `adopt` — for repos you do NOT own
Give Claude memory + conduct in a repo you can't commit to, **touching nothing in
its tree**:
1. Create an **external** vault at `~/Documents/AgentMemory/<repo>` via
   `/vault init` (so `Home.md`/`sessions/`/`todos/` live outside the repo).
2. Rely on the global `SessionStart` router `~/bin/claude-orient` — it detects the
   external vault by the project's basename and orients from it — plus
   `~/bin/vault-digest` for reads
   (`OBSIDIAN_VAULT_PATH=~/Documents/AgentMemory/<repo> vault-digest …`).
3. Global conduct (`~/.claude/CLAUDE.md`) already applies — no project `CLAUDE.md`.
4. Optional: a git-ignored `.claude/settings.local.json` for local-only per-repo
   tweaks (never committed).

### `check`
Report what a fresh `init` would create or merge — change nothing. For an
existing `CLAUDE.md`, list which canonical sections are present vs missing (the
same scan `init` performs), plus whether `scripts/vault-digest`, the
`SessionStart` hook (`scripts/session-start.sh` + `.claude/settings.json`), the
`vault/` scaffold, the `.gitignore` lines, and the global no-push guard
(`~/bin/deny-git-push.sh` + its `PreToolUse` registration) exist.

## The docs/ layout (baked into the template)

- `docs/` — generated documents (working notes, plans, analyses).
- `docs/reports/` — persistent, prepared deliverables meant to be kept and shared.
- `docs/logs/` — transient/ephemeral output of repeatable processes. **Gitignored.**

## Gitignore

Commit vault notes and shared Obsidian config; ignore UI state and transient docs:

```
# Claude conduct
docs/logs/
vault/.obsidian/workspace*.json
vault/.obsidian/plugins/
vault/.obsidian/themes/
vault/.obsidian/hotkeys.json
vault/.obsidian/appearance.json
vault/.obsidian/graph.json
```

## Notes

- This skill is the canonical source; it is symlinked into `~/.claude/skills/conduct`
  by setup-kit's `08-claude-skills.sh`. Edit it here, not in the symlink target.
- The CLAUDE.md template references the `vault` and `gstack` skills by name; those
  are installed alongside this one. If a referenced skill isn't installed on a given
  machine, the pointer is harmless — Claude just won't have that capability.
