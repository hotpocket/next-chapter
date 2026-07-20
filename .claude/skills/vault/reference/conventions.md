# Vault Reference — Writing Conventions & Generation

## Writing to the Vault

Write concisely. Notes are for your future context, not human documentation. Prefer:
- Bullet points over prose
- Wikilinks over repeated explanations (link to it, don't re-state it)
- Frontmatter tags for discoverability over verbose descriptions

### When to write
- **New component discovered**: Create a component note when you deeply understand a part of the codebase
- **Architecture decision made**: Record ADRs when significant design choices are made
- **Pattern identified**: Document recurring patterns that future sessions should follow
- **Domain knowledge learned**: Write to domain notes when you discover cross-project knowledge

### Scoping rules
| Knowledge type | Location | Example |
|---|---|---|
| One project only | `projects/{name}/` | How this API handles auth |
| Shared across projects | `domains/{tech}/` | How Go interfaces work |
| Universal, tech-agnostic | `patterns/` | SOLID principles |
| Session summaries | `sessions/` | What was done and discovered |
| TODOs | `todos/{project}.md` | Per-project files |

### Frontmatter conventions
Always include in new notes:
```yaml
---
tags: [type-tag, {app-tag}, ...]
type: <component|adr|session|project>
concerns: []
audience: []
summary: ""
created: YYYY-MM-DD
---
```

**`audience`** classifies who finds the note useful. YAML list from this controlled vocabulary:

| Value | Who | What they need |
|-------|-----|---------------|
| `dev` | Software engineers | Architecture, components, patterns, API schemas, ADRs |
| `pm` | Project managers | Requirements, project plans, status, ticket traceability |
| `regulatory` | Regulatory/compliance | Compliance docs, risk management, compliance maps |
| `leadership` | CEO, founders, advisors | Strategic docs, ROI, pitch materials |
| `design` | UX/UI designers, art team | Design wikis, Figma references, art bible |
| `claude-code` | Claude Code agent | Notes worth spending context tokens on during on-demand reads |

Most notes have 2-3 audience values. The `audience` field is the vault's perceptual model — it encodes what each consumer perceives as valuable. When the agent must decide whether to read a note, `audience: [claude-code]` says "this contains signal for you."

**`summary`** is a 1-2 sentence gist of the note's content. This is the Level 0 representation — enough for the agent to decide whether a deeper read is warranted without consuming the full note body. Write summaries in plain language, not marketing copy.

**`source-url`** (optional, for imported notes only): A clickable URL back to the original source (e.g. an external doc or ticketing system). Include when the note was imported from an external system.

**Tags** are flat (no nesting). Use the note's type as the first tag, then the app/project tag, then feature-specific tags. Example: `tags: [component, project-a, screen, dashboard]`.

**Concerns** classify which knowledge domains a note addresses. Use these 9 controlled values:

| Concern    | What it means                                              |
| ---------- | ---------------------------------------------------------- |
| `ux`       | Screens, flows, interactions, design system, gamification  |
| `api`      | Service interfaces, GraphQL schema, resolvers              |
| `data`     | Entity models, DynamoDB schemas, field definitions         |
| `infra`    | CDK stacks, deployment, AWS resources                      |
| `security` | Auth, RBAC, audit, encryption, compliance                  |
| `device`   | Hardware, firmware, sensors, calibration                   |
| `domain`   | Domain model, outcome metrics, compliance metrics          |
| `ops`      | Monitoring, system health, testing, email operations       |
| `comms`    | Messaging, notifications, announcements, invitation emails |

Most notes have 1-3 concerns. Excluded types (`home`, `index`, `session`, `todo`, `gen-spec`) get `concerns: []`. Each concern has a **hub note** at `$VAULT/concerns/` — a navigational index that links to all vault notes tagged with that concern. Hub notes are high-connectivity nodes in the graph that serve as entry points for browsing a knowledge domain.

For full tag and concern conventions, see `$VAULT/Vault Guide.md`.

### Wikilink conventions
- Use simple wikilinks: `[[Note Name]]` — Obsidian resolves by note name across the vault
- Only use paths when names collide: `[[projects/project-a/components/api-service|api-service]]`
- Wikilinks only inside `$VAULT/`. Published snapshots at the repo root use standard markdown links for GitHub compatibility.

### Note templates

**Component Note:**
```yaml
---
tags: [component, {app-tag}, screen, {feature-tag}]
type: component
concerns: []
audience: [dev, claude-code]
summary: ""
created: {date}
status: active
figma-coverage: none | partial | full
depends-on: []
depended-on-by: []
---
```
Non-screen components omit `screen`, feature tags, and `figma-coverage`: `tags: [component, {app-tag}, bloc, auth]`.

Sections for screen/UI components:
- **Purpose** — what this screen/feature does
- **Architecture** — BLoC, services, data flow
- **Design** — Key Elements, Interaction Model, States, Data Displayed, Figma Reference (only for notes with `figma-coverage`)
- **Related Notes** — wikilinks to dependencies, patterns, domains

Sections for service/infrastructure components:
- **Purpose** — what this service does
- **Architecture** — stack structure, tables, resolvers
- **GraphQL Schema** — inline schema with auth directives
- **Related Notes** — wikilinks

**Architecture Decision:**
```yaml
---
tags: [decision, {app-tag}]
type: adr
concerns: []
audience: [dev, claude-code]
summary: ""
status: proposed | accepted | superseded
supersedes: []         # wikilinks to ADRs this one replaces (set when replacing a prior decision)
superseded-by: []      # wikilink to the ADR that replaces this one (set when status: superseded)
created: {date}
---
```

**ADR supersession:** ADRs are ledger entries — bodies are frozen once accepted. When an accepted ADR no longer reflects current architecture, write a new ADR, set `supersedes: [[ADR-XXXX]]` on it, flip the old ADR's status to `superseded`, set `superseded-by: [[ADR-YYYY]]`, and prepend a `> **Superseded (YYYY-MM-DD):**` callout to the old ADR. The body stays intact. See ADR-0018 for a reference implementation.
Sections: Context, Decision, Alternatives Considered, Consequences

**Session Note:**
```yaml
---
tags: [session]
type: session
concerns: []
audience: []
summary: ""
created: {date}
status: completed
projects: []
branch: {branch-name}
---
```
`projects` is a flat list of project names (e.g., `[platform, infrastructure]`).
Sections: Context, Work Done, Discoveries, Decisions, Next Steps

## Generation Pipeline

Published documents are generated from vault notes and reflect vault completeness. If something is missing from the output, fix the vault note — not the output.

| Document | Vault Source | Gen-Spec | Output |
|----------|-------------|----------|--------|
| Master Plan | `$VAULT/projects/platform/master-plan.md` | `$VAULT/projects/platform/master-plan-gen-spec.md` | `YYYY-MM-DD_master-plan.md` |
| Data Model | `$VAULT/projects/platform/data-model.md` | `$VAULT/projects/platform/data-model-gen-spec.md` | `YYYY-MM-DD_data_model.md` |
| UI Mindmap | `$VAULT/projects/platform/ui-mindmap.md` | `$VAULT/projects/platform/ui-mindmap-gen-spec.md` | `YYYY-MM-DD_mindmap.html` |

**Generation modes:**
- **Incremental (default)**: Use previous snapshot as baseline, apply only vault-driven changes, run continuity check
- **Full Regeneration**: Only when explicitly requested — no prior baseline

**Continuity check** (required for incremental): Diff against previous version. Every change must trace to a vault commit. No section should shrink >10% without justification.

**Prior version confirmation**: Before generating, present a ranked list of available prior versions and ask the user to confirm. One question per document — never combine into a compound question.

See the gen-spec notes for full rules.

