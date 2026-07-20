### `help` — Show Available Commands

Display a summary of the vault skill with natural language usage examples.

**Usage**: `help`

Print the following:

```
/vault — Persistent Obsidian-based knowledge vault (v4.1)

Install:
  /vault install                           — (re)symlink skill into ~/.claude/skills/vault/ (tracks the repo)

Common usage:
  /vault recap                             — generate a session recap
  /vault show me the platform todos        — display TODOs for a project
  /vault what's stale in infrastructure    — check staleness of infra notes
  /vault AuthStack depends on AuthService      — create a relationship (confirms first)
  /vault show relationships for AuthStack  — display all connections

Finding things:
  /vault find security components          — notes with concerns:security + type:component
  /vault find regulatory notes             — notes with audience:regulatory
  /vault find all ADRs                     — all architecture decisions
  /vault find notes about RBAC             — full-text search
  /vault find by project project-a     — scoped to a project

Filterable axes:
  type      component, project, pattern, adr, phase, plan, index, domain, ...
  concerns  ux, api, data, infra, security, device, domain, ops, comms
  audience  dev, pm, regulatory, leadership, design, claude-code
  tags      (free-form) component, screen, project-a, flutter, ...
  summary   (free-text search)
```

