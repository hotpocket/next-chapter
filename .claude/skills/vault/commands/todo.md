### `todo` — Manage TODOs

View and update TODOs. TODOs are organized in per-project files under `$VAULT/todos/` (e.g., `todos/platform.md`, `todos/infrastructure.md`). `$VAULT/todos/Active TODOs.md` is a non-authoritative aggregate view.

**Usage**: `todo [action]`

#### Steps:

1. **Read current TODOs** from the per-project file at `$VAULT/todos/$PROJECT.md`. If it doesn't exist, create one (see `$VAULT/todos/platform.md` for the format).

2. **If no additional arguments**: Display the current TODOs for `$PROJECT` and ask what to update.

3. **If arguments provided**: Parse as a TODO action:
   - Plain text → Add as a new pending item in the per-project file
   - `done: <text>` → Mark matching item as completed (`- [x]`)
   - `remove: <text>` → Remove matching item

4. **Write back** the per-project file.

