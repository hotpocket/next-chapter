### `note` — Create a Note from Template

Create a note using a template. The first argument specifies the type: `component`, `adr`, or `pattern`.

**Usage**: `note <component|adr|pattern> [name]`

#### `note component [name]`

Create at `$VAULT/projects/$PROJECT/components/{name}.md`:
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
Add `screen` and feature tags for UI components. Sections: Purpose, Gotchas

If a name argument is provided, use it as the component name. Otherwise, ask the user.

#### `note adr [title]`

Determine the next ADR number by listing existing ADRs in `$VAULT/projects/$PROJECT/architecture/ADR-*.md`.

Create at `$VAULT/projects/$PROJECT/architecture/ADR-{NNNN} {title}.md`:
```yaml
---
tags: [decision, {app-tag}]
type: adr
concerns: []
audience: [dev, claude-code]
summary: ""
status: proposed
supersedes: []
superseded-by: []
created: {YYYY-MM-DD}
---
```
Sections: Context, Decision, Alternatives Considered, Consequences

#### `note pattern [name]`

Create at `$VAULT/projects/$PROJECT/patterns/{name}.md`:
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
Sections: Pattern, When to Use, Implementation, Examples

After creating any note, add a wikilink to it from the project overview.

