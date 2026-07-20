### `relate` — Manage Relationships

Create and query bidirectional relationships between notes via frontmatter properties.

**Usage**: `relate <subcommand> [args]`

#### Supported relationship types

| Forward property | Inverse property |
|---|---|
| `depends-on` | `depended-on-by` |
| `extends` | `extended-by` |
| `implements` | `implemented-by` |
| `consumes` | `consumed-by` |
| `supersedes` | `superseded-by` |

The `supersedes` / `superseded-by` pair is specific to ADRs — see the ADR Supersession Protocol in the ADR template.

#### `relate <source> <target> [type]`

Create a bidirectional relationship between two notes. Default type is `depends-on`/`depended-on-by`.

##### Steps:

1. **Resolve note names**: Use `file=` parameter for note display names. If ambiguity is possible (same name, different folders), use `path=` with full vault-relative path.

2. **Read current property on source** (forward direction):
   ```bash
   obsidian vault=$VAULT_NAME property:read file="<source>" name="<forward-property>"
   ```
   Fallback: Read the source note frontmatter.

3. **Check if relationship already exists**: If `<target>` (as a wikilink) is already in the list, skip and report "already related".

4. **Append to source** (forward direction):
   Build the new list locally by appending `[[<target>]]` to the current values, then set:
   ```bash
   obsidian vault=$VAULT_NAME property:set file="<source>" name="<forward-property>" value="<full-list>" type="list"
   ```
   Fallback: Edit the source note's frontmatter directly.

5. **Read current property on target** (inverse direction):
   ```bash
   obsidian vault=$VAULT_NAME property:read file="<target>" name="<inverse-property>"
   ```

6. **Append to target** (inverse direction):
   ```bash
   obsidian vault=$VAULT_NAME property:set file="<target>" name="<inverse-property>" value="<full-list>" type="list"
   ```

7. **Report** the created relationship.

**Safety**: Always read-then-set. Never blind-append. The full list is constructed locally and set atomically.

#### `relate show <name>`

Display all relationships for a note.

##### Steps:

1. **Query all 10 relationship properties**:
   ```bash
   obsidian vault=$VAULT_NAME property:read file="<name>" name="depends-on"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="depended-on-by"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="extends"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="extended-by"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="implements"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="implemented-by"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="consumes"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="consumed-by"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="supersedes"
   obsidian vault=$VAULT_NAME property:read file="<name>" name="superseded-by"
   ```
   Fallback: Read the note frontmatter and parse all relationship properties.

2. **Query structural links**:
   ```bash
   obsidian vault=$VAULT_NAME links file="<name>"
   obsidian vault=$VAULT_NAME backlinks file="<name>"
   ```

3. **Present results** grouped by relationship type. Show explicit (property) relationships first, then structural (wikilink) relationships that aren't already covered.

#### `relate tree <name> [depth]`

Walk the dependency tree via BFS. Default depth is 2.

##### Steps:

1. **Initialize BFS**: Start with `<name>` at depth 0. Maintain a visited set and a queue.

2. **For each node in the queue**:
   ```bash
   obsidian vault=$VAULT_NAME property:read file="<current>" name="depends-on"
   ```
   Fallback: Read the note and parse `depends-on` from frontmatter.

3. **Add unvisited dependencies** to the queue at `current_depth + 1`. Stop when `depth` limit is reached.

4. **Present** the tree as an indented list showing the dependency chain.

