### `analyze` — Analyze Project & Hydrate Vault

Analyze the current codebase and populate the vault with interconnected, content-rich notes.

**Usage**: `analyze` (no arguments — uses current repo)

#### Phase 1: Discovery — Scan for Knowledge Sources

Scan the repo for files that contain pre-existing knowledge:

| Category | Files to scan |
|---|---|
| Agent configs | `CLAUDE.md`, `.claude/CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `AGENTS.md`, `Agents.md` |
| Documentation | `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `docs/architecture.md`, `docs/ARCHITECTURE.md` |
| Existing ADRs | `vault/my-vault/decisions/ADR-*.md`, `architecture/ADR-*.md`, `adr/*.md`, `docs/decisions/*.md` |
| Project metadata | `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `setup.py`, `Gemfile`, `pom.xml`, `build.gradle`, `*.csproj` |
| Build/CI | `Makefile`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/*.yml`, `.gitlab-ci.yml` |
| Config | `tsconfig.json`, `.eslintrc.*`, `jest.config.*`, `.goreleaser.yml` |

Read each discovered file. For large files (README, agent configs), read fully. For metadata files, extract key fields (name, version, dependencies).

Also gather:
- Repo URL from `git remote get-url origin`
- Repo root path from `git rev-parse --show-toplevel`
- Active branch from `git branch --show-current`
- Directory tree (top 2 levels of source directories, excluding hidden/vendor/node_modules)
- File extension frequency (for language detection)

#### Phase 2: Analysis — Extract & Synthesize

Using the discovered content, synthesize:

1. **Project metadata**: name, language(s), framework(s), repo URL, local path
2. **Architecture summary**: Entry points, layer organization (e.g., `internal/` → Go service layers, `src/components/` → React app), build system
3. **Component inventory**: Major functional modules — each top-level source directory or logical grouping that represents a distinct unit. For each: purpose (from README/agent config context), key files, and relationships
4. **Pattern inventory**: Coding conventions, error handling strategies, testing approaches — extracted from agent config files (CLAUDE.md sections like "Coding Guidelines", "Testing", etc.)
5. **Domain mapping**: Detected technologies → vault domain notes (e.g., Go, TypeScript, Terraform, React)
6. **Existing decisions**: ADR files found in the repo → import as vault ADR notes
7. **Dependency summary**: Key dependencies from package manifests (listed in project overview, not separate notes)

#### Phase 3: Hydration — Write Vault Notes

**Idempotency rules:**
- If project directory doesn't exist → create everything (scaffold + populate)
- If project directory exists but overview is a skeleton → **replace** overview with populated version
- If individual component/pattern/ADR notes already exist → **skip** and report (don't overwrite manual work)
- Domain notes: create if missing, **append** project link if existing

**Notes to write:**

1. **Project overview** (`$VAULT/projects/{name}/{name}.md`) — Fully populated:
   ```yaml
   ---
   tags: [project, {app-tag}]
   type: project
   concerns: []
   audience: [dev, claude-code]
   summary: ""
   repo: {git remote url}
   path: {repo root path}
   language: {detected language(s)}
   framework: {detected framework(s)}
   created: {YYYY-MM-DD}
   status: active
   ---
   ```
   Sections:
   - **Architecture**: Real description from analysis
   - **Components**: Table with wikilinks to component notes
   - **Project Patterns**: Table with wikilinks to pattern notes
   - **Architecture Decisions**: List with wikilinks to ADR notes
   - **Key Dependencies**: From package manifests
   - **Domains**: Wikilinks to domain notes

2. **Component notes** (`$VAULT/projects/{name}/components/{Component}.md`) — One per major module:
   ```yaml
   ---
   tags: [component, {app-tag}]
   type: component
   concerns: []
   audience: [dev, claude-code]
   summary: ""
   created: {YYYY-MM-DD}
   status: active
   depends-on: []
   depended-on-by: []
   ---
   ```
   Add `screen` and feature tags for UI components: `tags: [component, {app-tag}, screen, {feature-tag}]`.
   Sections: Purpose, Gotchas

3. **Pattern notes** (`$VAULT/projects/{name}/patterns/{Pattern}.md`) — From agent config conventions:
   ```yaml
   ---
   tags: [pattern, {app-tag}]
   type: pattern
   concerns: []
   audience: [dev, claude-code]
   summary: ""
   created: {YYYY-MM-DD}
   ---
   ```
   Sections: Pattern, When to Use, Implementation

4. **ADR imports** (`$VAULT/projects/{name}/architecture/ADR-{NNNN} {title}.md`) — From existing repo ADRs:
   ```yaml
   ---
   tags: [decision, {app-tag}]
   type: adr
   concerns: []
   audience: [dev, claude-code]
   summary: ""
   status: accepted
   supersedes: []
   superseded-by: []
   created: {YYYY-MM-DD}
   ---
   ```
   Preserve original content, add vault frontmatter.

5. **Domain notes** (`$VAULT/domains/{tech}/{Tech}.md`):
   - If new: create with project link
   - If existing: add this project to "Projects Using This Domain" section

6. **Index updates**:
   - `$VAULT/projects/Projects.md` — add/update row
   - `$VAULT/domains/Domains.md` — add/update rows for new domains

#### Phase 4: Report

Print a summary:
```
Analyzed: {project-name}
  Sources read: {N} knowledge files
  Created: project overview (populated)
  Created: {N} component notes
  Created: {N} pattern notes
  Imported: {N} architecture decisions
  Linked: {N} domain notes
  Skipped: {N} existing notes (preserved)
```

