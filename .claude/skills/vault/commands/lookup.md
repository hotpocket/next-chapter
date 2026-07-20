### `lookup` — Search the Vault

Search the vault for knowledge. Supports targeted subcommands and freetext search.

**Usage**: `lookup <subcommand|freetext>`

#### `lookup deps <name>`

Query what a component depends on.

```bash
obsidian vault=$VAULT_NAME property:read file="<name>" name="depends-on"
```
Fallback: Read the component note and parse the `depends-on` frontmatter list.

#### `lookup consumers <name>`

Query what depends on a component (reverse dependencies).

```bash
obsidian vault=$VAULT_NAME property:read file="<name>" name="depended-on-by"
obsidian vault=$VAULT_NAME backlinks file="<name>"
```
Combine results — `depended-on-by` gives explicit relationships, `backlinks` catches implicit references. Fallback: Read the component note and search for backlinks via Grep.

#### `lookup related <name>`

Query all notes connected to a given note (both directions).

```bash
obsidian vault=$VAULT_NAME links file="<name>"
obsidian vault=$VAULT_NAME backlinks file="<name>"
```
Fallback: Read the note and extract wikilinks, then Grep for `[[<name>` across the vault.

#### `lookup type <type> [project]`

Find all notes of a given type (component, adr, session, project).

```bash
obsidian vault=$VAULT_NAME tag verbose name="<type>"
```
If `[project]` is specified, filter results to notes in that project's folder:
```bash
obsidian vault=$VAULT_NAME search query="type: <type>" path="projects/<project>"
```
Fallback: Grep for `type: <type>` across `$VAULT`.

#### `lookup layer <layer> [project]`

Find all components in a specific layer.

```bash
obsidian vault=$VAULT_NAME search query="layer: <layer>" path="projects/<project>"
```
If no project specified, search across all projects:
```bash
obsidian vault=$VAULT_NAME search query="layer: <layer>" path="projects"
```
Fallback: Grep for `layer: <layer>` across `$VAULT/projects/`.

#### `lookup files <component>`

Query key files for a component.

```bash
obsidian vault=$VAULT_NAME property:read file="<component>" name="key-files"
```
Fallback: Read the component note and parse the `key-files` frontmatter list.

#### `lookup <freetext>`

General search across the vault.

```bash
obsidian vault=$VAULT_NAME search format=json query="<freetext>" matches limit=10
```
Fallback: Search file contents for the query across all `.md` files in `$VAULT`.

If the query looks like a tag (starts with `#`):
```bash
obsidian vault=$VAULT_NAME tags name="<query>"
```

If the query matches a note name:
```bash
obsidian vault=$VAULT_NAME backlinks file="<query>"
```

**Present results**: Show matching notes with their frontmatter (first ~10 lines) so the user can decide which to read in full.

