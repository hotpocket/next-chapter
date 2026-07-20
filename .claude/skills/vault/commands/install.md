### `install` — Symlink the Skill into the Global Directory

Symlink the repo's vault skill into `~/.claude/skills/vault/` so `/vault` is available in all projects and **tracks this clone** — edits to the skill are live immediately, and the `commands/`, `reference/`, and `orient/` files come along. (Earlier versions copied only `SKILL.md`; that left the per-command/reference subdirs behind and went stale on every edit.)

**Usage**: `install`

> **Chicken-and-egg:** you can only run `/vault install` once the skill is already discoverable. On a brand-new clone, Claude Code does not auto-discover skills under `vault/my-vault/` — run the one-time shell symlink from CLAUDE.md's "Obsidian Knowledge Vault" setup note first. `install` is for re-pointing an already-loaded skill at this clone.

#### Steps:

1. **Locate the skill source**: Parse the project config (CLAUDE.md) for the "Vault Skill Source" field (the repo-relative path to `SKILL.md`). If not found, fail with: **"Missing vault skill source path in CLAUDE.md. Add a `Vault Skill Source` field under the Obsidian Knowledge Vault section."** The skill *directory* is that file's parent.

2. **Resolve the absolute skill directory**: `SKILL_DIR="$(git rev-parse --show-toplevel)/$(dirname <relative-path>)"`. Verify it contains `SKILL.md`; if not, fail with: **"Vault skill not found at `{SKILL_DIR}`. Check the path in CLAUDE.md."**

3. **Symlink it into the global skills dir** (replacing any prior copy or stale link — the old content is recoverable from git):
   ```bash
   mkdir -p ~/.claude/skills
   rm -rf ~/.claude/skills/vault
   ln -s "$SKILL_DIR" ~/.claude/skills/vault
   ```

4. **Verify** the link resolves and the split is reachable:
   ```bash
   test -f ~/.claude/skills/vault/SKILL.md && test -f ~/.claude/skills/vault/orient/todo-digest.md \
     && echo "linked → $(readlink ~/.claude/skills/vault)" || echo "install FAILED — check the source path"
   ```

5. **Report**: "Vault skill symlinked: `~/.claude/skills/vault` → `{SKILL_DIR}`. Repo edits are live; no re-install needed."

