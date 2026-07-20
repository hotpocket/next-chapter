# <PROJECT>

<!-- One-paragraph description of what this repo is and does. Replace this. -->

## Session conduct

Session-start orientation is injected by the global `SessionStart` router
(`~/bin/claude-orient`), which runs this repo's `scripts/session-start.sh`:
latest recap pointer + open-todo count. Go deeper on demand — read the recap body
in `vault/sessions/` or open `vault/todos/<PROJECT>.md`.

**Vault access is file-first.** Use `scripts/vault-digest` for cheap reads —
grep/awk over note frontmatter, no Obsidian app/CLI/GUI, safe across parallel
sessions:
- `scripts/vault-digest summaries [subdir]` — one-line gist per note (Level 0).
- `scripts/vault-digest type <t>` / `concern <c>` — filter by frontmatter.
- `scripts/vault-digest recap` / `todos` / `backlinks <note>` / `search <q>`.
Read a full note body (Level 2) only after a summary points you to it. The
`/vault` skill (Obsidian CLI) is an optional accelerator for a single open
vault — never load-bearing.

When you discover something durable (architecture, a gotcha, a decision and its
why), write it back to the vault. **At session end**, offer `/vault recap`.

## Docs layout

- `docs/` — generated documents: working notes, plans, analyses.
- `docs/reports/` — persistent, prepared deliverables meant to be kept/shared.
- `docs/logs/` — transient/ephemeral output of repeatable processes (gitignored).

## Skills available here

- `vault` — persistent Obsidian memory (orient, look up, write back).
- `gstack` — drive a real browser to research the web and produce results.
- `code-review` — review the current diff for bugs and cleanups.
<!-- Add/remove per what this repo actually uses. -->

## Rules of conduct

- **Durable over accurate — always.** Prefer references and constructs that survive
  commits, pushes, checkouts, moves, and machine changes over ones that are merely
  correct right now. This is a general principle, not just about paths:
  - **Paths**: relative, or derived at runtime (script location, `git rev-parse`,
    an env var with a computed default) — never hardcoded absolutes. A path that
    names `/home/<user>/...` or a specific mount breaks the moment the repo moves.
  - **Resume/cache keys**: content hashes, not mtimes (mtime resets on move, rsync,
    checkout). Identity, not incidental state.
  - **Config**: one source of truth others derive from, not the same literal copied
    to N places that then drift.
  - When durable and accurate genuinely conflict, make it durable and make the
    durable thing accurate — don't settle for a brittle literal.
- Be brief: no preamble, no recap of what the user knows, no surveying paths not taken.
- Idempotent, reversible-by-default; confirm before hard-to-undo or outward-facing actions.
- Report outcomes faithfully — if a step failed or was skipped, say so.
- Never `git push` (and never force-push) — the human pushes manually. A global
  PreToolUse guard (`~/bin/deny-git-push.sh`) enforces this mechanically; this
  line is the why, not the enforcement.
<!-- Add project-specific rules below. -->
