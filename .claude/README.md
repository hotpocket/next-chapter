# .claude/ — the AI config this repo is built under, in-tree

This repo is developed with Claude Code, and its vault notes, prompt exports,
and `config-history.md` refer to machine-level config (`~/.claude`, `~/bin`).
So a reviewer isn't asked to trust descriptions of files they can't see, that
config is **mirrored here, inside the repo**. When a path like
`~/bin/claude-orient` appears in a session note, this is where to read it:

| Path in notes/prompts            | In this repo                      | Role here |
|----------------------------------|-----------------------------------|-----------|
| `~/bin/claude-orient`            | `.claude/bin/claude-orient`       | mirror — global SessionStart router; delegates to `scripts/session-start.sh` in this repo |
| `~/bin/deny-git-push.sh`         | `.claude/bin/deny-git-push.sh`    | **live** — wired as a project hook in `settings.json` below (also registered globally) |
| `~/.claude/CLAUDE.md`            | `.claude/CLAUDE.global.md`        | mirror — global conduct; the loaded project rules are `/CLAUDE.md` at repo root |
| `~/.claude/settings.json`        | `.claude/settings.global.json`    | mirror — global hooks (orient, brevity injector, push guard), model, statusline |
| `~/.claude/statusline-command.sh`| `.claude/statusline-command.sh`   | mirror — cosmetic statusline |
| `~/.claude/skills/<name>`        | `.claude/skills/<name>`           | **live** — loaded as project skills; bodies of `/vault`, `/wargame`, `/vet`, `/conduct`, `/gstack`, `/browse` |
| `~/bin/vault-digest`             | `scripts/vault-digest`            | **live** — already committed; byte-identical to the global copy |

## What is live vs. mirror

- **Live**: `.claude/settings.json` (project hooks Claude Code actually loads
  here) and `.claude/skills/` (project skills). The push guard runs from the
  in-tree copy, so the conduct rule "the agent never pushes" is enforced by
  code a reviewer can read — and travels with a clone.
- **Mirror**: `*.global.*` files and `bin/claude-orient` document the global
  layer verbatim. They are deliberately **not** loaded from here — the global
  hooks already run, and registering them twice would duplicate their output
  (orientation injected twice per session, brevity rule twice per prompt).

## How the mirror stays honest

`scripts/sync-claude-mirror` regenerates everything above from the global
sources; `scripts/sync-claude-mirror --check` exits non-zero on any drift and
runs before commits that touch config. Mirrored files are never hand-edited —
one source of truth (the global config, itself versioned in a dotfiles repo
since 2016; see `config-history.md`), this mirror derived from it. Tests:
`scripts/test-sync-claude-mirror.sh`.

## Deliberate omissions

- **Skill `tests/` dirs** — dogfood records from other, private projects.
- **gstack** is a 1.7 GB open-source upstream (MIT, see its `LICENSE`); only
  its entry points are mirrored: `SKILL.md` (router), `browse/SKILL.md` (the
  `/browse` browser driver used throughout this project), `LICENSE`, `VERSION`.
- **learn-video**, **writing-great-skills** — installed globally, mentioned in
  `config-history.md`, but not used in this repo; not mirrored.
- `settings.local.json` — machine-local, gitignored.
