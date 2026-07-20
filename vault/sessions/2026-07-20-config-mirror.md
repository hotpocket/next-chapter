---
tags: [session]
type: session
concerns: [legibility, process, public-repo]
audience: []
summary: "Mirrored the machine-level AI config into the repo at .claude/ (hook scripts, global conduct + settings, skill bodies: vault/wargame/vet/conduct full, gstack slim) so reviewers can read the actual config behind vault notes and prompts. Built scripts/sync-claude-mirror (generated mirror, --check drift gate, 23-assertion test red→green). Push guard and skills now load live from in-tree copies; *.global.* mirrors deliberately inert to avoid double hook registration. Docs cross-referenced (CLAUDE.md, README, config-history, wargame addendum, ADR 0007); hygiene-scanned; committed 73feb54 (unpushed)."
created: 2026-07-20
status: completed
projects: [next-chapter]
branch: main
---

# 2026-07-20 — Config mirror

Verbatim prompts for this session: [[2026-07-20-config-mirror-prompts]].

## Work

1. Repo-local `.claude/` mirror of the machine-level AI config: `bin/claude-orient`, `bin/deny-git-push.sh`, `CLAUDE.global.md`, `settings.global.json`, `statusline-command.sh`, and skill bodies — vault, wargame, vet, conduct in full; gstack slim (SKILL.md, browse/SKILL.md, LICENSE, VERSION).
2. `scripts/sync-claude-mirror` + `scripts/test-sync-claude-mirror.sh` (23 assertions, red→green): derives the mirror from the global config, `--check` exits non-zero on drift, env-overridable roots, resolves the `~/.claude` symlinks, prunes stale mirror files, leaves hand-written `.claude/README.md` / `settings.json` alone.
3. Live in-tree: `.claude/settings.json` wires the push guard from the in-tree copy; `.claude/skills/` load as project skills.
4. `.claude/README.md`: machine-path → repo-path cross-reference table — the key for reading `~/bin` / `~/.claude` references in vault notes and prompt exports.
5. Docs: CLAUDE.md (annotated refs + mirror/drift-check rule), README trail bullet, config-history "In-tree mirror" paragraph, addendum on [[../../docs/reports/2026-07-20_public-repo-and-legibility|the public-repo wargame report]] closing its T2 dependency-inventory gap, [[../decisions/0007-repo-local-claude-mirror|ADR 0007]], `.gitignore` +`.claude/settings.local.json`.
6. Hygiene: gitleaks + identity/path grep on mirror and staged diff — clean (only upstream placeholder examples). Committed `73feb54` (unpushed).

## Decisions

- Global-layer mirrors named `*.global.*` so Claude Code does not load them — double-registering the hooks would duplicate orient/brevity injection per session/prompt. Rejected: making all mirrored settings live.
- Mirror is generated, never hand-edited — single source of truth is the global config (durable-over-accurate). Drift gate: `sync-claude-mirror --check` before config-touching commits.
- Exclusions: skill `tests/` dirs (dogfood from other private repos), gstack beyond entry points (1.7 GB MIT upstream), learn-video + writing-great-skills (unused here).
- `author: brandon` frontmatter in mirrored skills ships as-is — user confirmed name is fine to publish.

## Next Steps

No new engineering work; nothing loose. The 7 open todos in [[../todos/next-chapter|the TODO file]] (site scaffold, deploy script, generation runs, SOURCES.md, prompt-history.md, repo-story visibility) are unchanged.
