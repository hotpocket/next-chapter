### `project` — Scaffold New Project

Scaffold a new project in the vault. Uses the first argument as the project name, or defaults to `$PROJECT`.

**Usage**: `project [name]`

#### Steps:

1. **Determine project name**: Use the argument if provided, otherwise use `$PROJECT`.

2. **Check if project exists**: Look for `$VAULT/projects/{name}/{name}.md`. If it exists, tell the user and offer to open it instead.

3. **Create directory structure**:
   - `$VAULT/projects/{name}/`
   - `$VAULT/projects/{name}/architecture/`
   - `$VAULT/projects/{name}/components/`
   - `$VAULT/projects/{name}/patterns/`

4. **Create project overview** at `$VAULT/projects/{name}/{name}.md`:
   ```yaml
   ---
   tags: [project, {app-tag}]
   type: project
   concerns: []
   audience: [dev, claude-code]
   summary: ""
   repo: {git remote url if available}
   path: {working directory}
   language: {detected from files}
   framework:
   created: {YYYY-MM-DD}
   status: active
   ---
   ```
   Sections: Architecture, Components, Project Patterns, Architecture Decisions, Domains

   Auto-detect and fill:
   - Language from file extensions in the repo
   - Repo URL from `git remote get-url origin`
   - Link to relevant domains that exist in `$VAULT/domains/`

5. **Update Projects.md**: Add a row to the project table in `$VAULT/projects/Projects.md`.

6. **Report** the scaffolded structure.

