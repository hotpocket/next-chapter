### `stale` — Check Dependency Staleness

Check whether derived notes (hubs, generated docs, compacted summaries) are stale relative to their upstream sources. Uses existing `depends-on` frontmatter edges and git history — no new metadata fields needed.

**Usage**: `stale [note]`

#### `stale` (no arguments)

Report all stale derived notes in the vault.

##### Steps:

1. **Find all notes with `depends-on`**: Search for notes that have non-empty `depends-on` frontmatter lists.
   ```bash
   obsidian vault=$VAULT_NAME search query="depends-on:" matches limit=100
   ```
   Fallback: Grep for `depends-on:` across `$VAULT/**/*.md` and filter to notes with non-empty lists.

2. **For each derived note**, run the single-note staleness check (see below).

3. **Present results** as a table:
   ```
   Stale notes:
   | Derived Note | Stale Because | Source Changed | How Long Ago |
   |---|---|---|---|
   | Hub: Security | [[AuthService]] changed | abc1234 | 3 days ago |
   | master-plan | [[phase-5a]] changed | def5678 | 1 day ago |
   ```

4. **Offer to refresh**: "Want me to update any of these?" Do NOT auto-regenerate.

#### `stale <note>`

Check one note's dependencies for staleness.

##### Steps:

1. **Read the note's `depends-on` list**:
   ```bash
   obsidian vault=$VAULT_NAME property:read file="<note>" name="depends-on"
   ```
   Fallback: Read the note frontmatter and parse `depends-on`.

2. **Get the derived note's last modification commit**:
   ```bash
   git log -1 --format="%H %ai" -- "$VAULT/<note-path>"
   ```

3. **Check what changed since then**:
   ```bash
   git diff --name-only <that-sha>..HEAD
   ```

4. **Intersect** changed files with the `depends-on` list. Resolve wikilink names to file paths (search `$VAULT` for matching `.md` files).

5. **Report**:
   - If stale: "**<note>** is stale. Source(s) changed since last update: <list with commit refs and dates>"
   - If fresh: "**<note>** is up to date. All dependencies unchanged since <date>."

#### Forward propagation (automatic behavior)

After modifying any vault note during a session, check its `depended-on-by` list:
```bash
obsidian vault=$VAULT_NAME property:read file="<modified-note>" name="depended-on-by"
```
If non-empty, report: "Source **<note>** changed. These derived notes may need refresh: <list>". Do not auto-update — let the user decide.

