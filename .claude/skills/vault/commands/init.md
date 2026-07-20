### `init` — Initialize the Vault

Bootstrap a new Obsidian Agent Memory vault. Interactive: prompts for vault name, parent directory, and which root-level folders to create. Also registers the vault with Obsidian so the CLI can address it by name.

**Usage**: `init [path]`

If `path` is supplied, skip the name/parent prompts and use it as `$VAULT`. The folder-selection prompt always runs.

#### Steps:

1. **Determine vault path**:
   - If a path argument is supplied, use it. Relative paths (e.g., `./vault`) resolve against the git root if inside a repo, otherwise the current working directory. Set `$VAULT` to its absolute form and `$VAULT_NAME = basename "$VAULT"`. Skip to step 2.
   - Otherwise prompt the user (use `AskUserQuestion` if available, else plain prompts):
     - **Name** — default: `<repo-basename>-knowledge` if inside a git repo, else `AgentMemory`. The name doubles as the CLI handle (`vault=<name>`), so it must be unique across all registered vaults — check `obsidian vault list` and reject collisions.
     - **Parent directory** — default: `./vault/` if inside a git repo, else `~/Documents/`.
   - Compute `$VAULT = $PARENT/$NAME`. Compute `$VAULT_NAME = basename "$VAULT"`.

2. **Check if vault already exists**: Look for `$VAULT/Home.md`. If it exists, tell the user the vault already exists at that path and offer to open it. Stop.

3. **Pose folder selection**: Present the candidate root-level folders with one-line descriptions and let the user toggle which to create. `sessions/` and `todos/` default ON — they're the minimum useful agent-memory surface (the wbt vault, for example, uses only these two). The rest default OFF.

   Folder catalog:

   | Folder | Default | Description |
   |---|---|---|
   | `sessions/` | ON  | Session recaps + Session Log index. Written by `/vault recap`. |
   | `todos/`    | ON  | Per-project TODO files. Written by `/vault todo`. |
   | `projects/` | OFF | Per-project overview, components, patterns, architecture. Used by `/vault project` and `/vault note component`. |
   | `decisions/`| OFF | Architecture Decision Records (ADRs) — frozen ledger of design choices. Used by `/vault note adr`. |
   | `domains/`  | OFF | Cross-project knowledge per technology (Go, React, Terraform, ...). Linked from project overviews. |
   | `patterns/` | OFF | Universal, tech-agnostic patterns and conventions. |
   | `concerns/` | OFF | Hub notes — navigational indexes for cross-cutting domains (ux, api, security, ...). |
   | `templates/`| OFF | Note templates referenced by `/vault note`. |
   | `skills/`   | OFF | Agent skill definitions (e.g., the vault skill itself, if shipped in-repo). |

   Accept shortcuts: `minimal` = `sessions, todos`; `all` = every folder; comma-separated list = exact selection.

4. **Create the vault structure**:
   ```bash
   mkdir -p "$VAULT"
   for folder in $SELECTED_FOLDERS; do
     mkdir -p "$VAULT/$folder"
   done
   ```
   Write a stub `$VAULT/Home.md`:
   ```markdown
   # $VAULT_NAME

   Vault initialized on $YYYY-MM-DD.
   ```

5. **Create Obsidian config directory**:
   ```bash
   mkdir -p "$VAULT/.obsidian"
   ```
   Write the following to `$VAULT/.obsidian/app.json`:
   ```json
   {
     "alwaysUpdateLinks": true,
     "newFileLocation": "current"
   }
   ```

6. **Register the vault with Obsidian** so the CLI can resolve `vault=$VAULT_NAME`. Registration normally happens via the Obsidian GUI (Vault Switcher → Open folder as vault). The skill prefers a headless edit to `~/.config/obsidian/obsidian.json` so no GUI window pops up.

   **Pre-flight: is the GUI running?**
   ```bash
   pgrep -f '/opt/Obsidian/obsidian|/Applications/Obsidian.app/|Obsidian.exe' >/dev/null
   ```

   - **GUI running**: A direct edit to `obsidian.json` will be overwritten when the GUI exits (it persists its in-memory vault list back to the file). Print a notice with two options and stop registration:
     1. Quit Obsidian and re-run `/vault init` to use the headless path.
     2. In Obsidian: Vault Switcher → Open folder as vault → `$VAULT` (registers via the GUI itself).

   - **GUI not running**: Direct-edit `~/.config/obsidian/obsidian.json`:
     - Read the current JSON (file may not exist on a fresh install — start from `{"vaults":{},"cli":true}`).
     - Generate a vault ID: `VAULT_ID=$(openssl rand -hex 8)`.
     - Append a new entry under `.vaults`: `"$VAULT_ID": { "path": "$VAULT", "ts": <now-ms>, "open": false }`.
     - Ensure top-level `.cli` is `true` (otherwise the CLI is disabled).
     - Write back atomically: write to a temp file, then `mv` over the original.
   - Verify with:
     ```bash
     obsidian vault list 2>&1 | grep -F "$VAULT"
     ```
     If the vault doesn't appear, instruct the user to open it in the Obsidian GUI manually.

7. **Emit agent config snippet**: For Claude Code, print a snippet the user can paste into the project's `CLAUDE.md`. If the vault is under the git root, prefer the *relative* path (e.g., `./vault`) so the snippet survives the repo being moved or cloned elsewhere:
   ```markdown
   ## Obsidian Knowledge Vault
   Persistent knowledge vault at `./vault`.
   ```
   Otherwise emit the absolute path:
   ```markdown
   ## Obsidian Knowledge Vault
   Persistent knowledge vault at `$VAULT`.
   ```
   If the vault ships the skill in-repo (i.e., `$VAULT/skills/vault/SKILL.md` exists or was selected), also include:
   ```markdown
   - **Vault Skill Source**: `<repo-relative path to SKILL.md>`
   ```
   For other agents: "Add `OBSIDIAN_VAULT_PATH=$VAULT` to your environment or agent config."

   **Optional follow-up (repo-local vaults only)**: Suggest the user symlink the vault into a common parent directory so it shows up alongside other vaults in Obsidian's vault switcher and any cross-project tooling that scans a single location:
   ```bash
   mkdir -p ~/Documents/AgentMemory
   ln -s "$VAULT" ~/Documents/AgentMemory/$(basename "$(git rev-parse --show-toplevel)")
   ```
   The skill's resolution chain still finds the repo-local vault first via step 3; the symlink is purely for human/Obsidian-GUI discoverability.

8. **Auto-scaffold current project**: If `projects/` was selected and the working directory is inside a git repo, run the `project` command to scaffold the current project in the vault.

9. **Concise output**: Keep the final output to 5-8 lines: vault path, folders created, registration status (registered / GUI-open-blocked / verify-failed), CLAUDE.md snippet pointer, next steps.

