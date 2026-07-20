# Global Claude conduct

Applies in every repo on this machine (owned or not). Project `CLAUDE.md` files
layer repo-specific rules on top of this.

## Session conduct

Session-start orientation is injected by the global `SessionStart` hook
(`~/bin/claude-orient`): it surfaces the latest recap pointer + open-todo count
from this repo's vault, if one is adopted. No vault → nothing to orient from.

**Vault access is file-first.** Use `vault-digest` (the repo's
`scripts/vault-digest` if present, else `~/bin/vault-digest`) for cheap reads —
grep/awk over note frontmatter, no Obsidian app/CLI/GUI:
- `vault-digest summaries [subdir]` — one-line gist per note (Level 0).
- `vault-digest type <t>` / `concern <c>` / `recap` / `todos` / `backlinks <n>` / `search <q>`.
- For an un-owned repo's external vault: `OBSIDIAN_VAULT_PATH=~/Documents/AgentMemory/<repo> vault-digest …`.

Read a full note body only after a summary points you to it. The `/vault` skill
(Obsidian CLI) is an optional accelerator for a single open vault — never
load-bearing. When you discover something durable, write it back to the vault;
at session end, offer `/vault recap`.

## Durable over accurate — always

Prefer references and constructs that survive commits, pushes, checkouts, moves,
and machine changes over ones that are merely correct right now. Not just paths
(relative or runtime-derived — `GIT_HOME`/script-location, never hardcoded
absolutes); also resume/cache keys (content hashes, not mtimes) and config (one
source of truth others derive from, not copied literals that drift). When durable
and accurate conflict, make it durable *and* make the durable thing accurate.

## Tests first, code second

- Write the tests BEFORE the implementation, always. Red → green: see the test
  fail, then write the code that makes it pass.

## Rules of conduct

- Be brief (also enforced by the brevity hook): no preamble, no recap of what the
  user knows, no surveying paths not taken.
- Idempotent, reversible-by-default; confirm before hard-to-undo or
  outward-facing actions.
- **Deploys and pushes are the user's to run.** Never execute deploy scripts
  (`deploy.sh` etc.) or `git push` yourself — prepare everything, then hand the
  user the exact command to run (e.g. `! scripts/deploy.sh`) so they can watch
  it live. Same rationale as manual pushes: visibility into what's happening.
- Report outcomes faithfully — if a step failed or was skipped, say so.
- In repos you don't own: do NOT commit conduct artifacts (`CLAUDE.md`,
  `scripts/`, `vault/`) into their tree. Keep memory in the external vault at
  `~/Documents/AgentMemory/<repo>`.

## gstack browse / Playwright (this machine)

- If gstack `browse` fails to launch: NEVER run `npx playwright install` as a
  reflex — on an OS the pinned Playwright doesn't support it deletes the cached
  browsers *before* failing. First check the pin supports this OS
  (`grep '"playwright"' ~/git/gstack/package.json` vs release notes; Ubuntu
  26.04 needs ≥1.61).
- Working baseline (2026-07-16): playwright 1.61.1 + `/etc/apparmor.d/playwright-chrome`
  (userns profile; Ubuntu 24.04+ blocks Playwright-browser sandboxes without it).
  Default launch needs no env vars; `GSTACK_CHROMIUM_PATH=/usr/bin/google-chrome`
  is an emergency fallback only. Never `--no-sandbox`.
