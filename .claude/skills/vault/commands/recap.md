### `recap` — Session Recaps

Generate, review, and search session recaps.

**Usage**: `recap [action]`

#### `recap` (no arguments)

Gather context, render a session recap to the screen, then offer to write it to the vault.

##### Step 1: Gather session context

```bash
git log --oneline -20
git diff --stat HEAD~5..HEAD 2>/dev/null || git diff --stat
git branch --show-current
```

##### Step 2: Read current TODOs

File-based via vault-digest (repo's `scripts/vault-digest` if present, else `~/bin/vault-digest`):
```bash
vault-digest todos $PROJECT      # or bare `vault-digest todos` for all files
```
Fallback: Read the per-project TODO file at `$VAULT/todos/$PROJECT.md`.

##### Step 3: Read project overview

Read `$VAULT/projects/$PROJECT/$PROJECT.md` for wikilinks and context.

##### Step 4: Render the recap

Display the session recap with these sections (omit any that are empty):
- **Work**: numbered outcome-level list — what changed, one line each
- **Discoveries**: technical findings worth remembering
- **Decisions**: design choices + rejected alternative, one line each
- **Next Steps**: forward engineering work, **triaged into two buckets** (see format below)

**Content rules:**
- **Be compact, don't be verbose.**
- **State-only.** Describe what exists in the final state and what was decided — not the path traveled. If something was added then removed within the session, it doesn't belong in the recap; only the resulting state does. Future readers want "what is", not "what we tried."
- **Next Steps: triage into "loose ends" vs "needs a dedicated session", don't just dump checkboxes.** Split the open work into two labelled groups, and for each item give a one-line plain-English description plus a rough effort estimate — not a bare checkbox title. The point is to let the reader decide *what's cleanable right now* vs *what needs its own focus*:
  - **Loose ends (cleanable now):** small, self-contained items knockable out in the same or next short session — a doc note, an ADR write-up, a single-function fix, a yes/no decision. Estimate in minutes.
  - **Needs dedicated focus:** real engineering tasks — new features, multi-file refactors, anything investigation-heavy or with regression risk. Estimate in hours and say *why* it's not quick (blast radius, edge cases, testing). These also go to the per-project TODO file; the recap just flags them.
  - A compact table (`item | what it is | quick?`) is a good shape at 4+ items. Be honest about effort — don't label something "quick" to make the list look tidy. If the session left nothing loose, say so rather than padding.
- **Next Steps are forward engineering work, not operational reminders or coordination tracking.** Open TODOs, deferred decisions, in-flight work. NOT: `git push`, "run X command", "user has untracked drafts", "remember to check Y" (operational); NOT "wait for team response on X", "watch the discussion", "follow up with Y", "flip status when teammate accepts" (coordination). Operational reminders are the user's next-5-minutes worklist; coordination is expected ongoing collaboration with coworkers. Neither belongs in a record future agents will read months later. If a coworker's eventual response will *trigger* engineering work, write the engineering work itself as the TODO — the wait-and-react is implicit.
- **Don't propagate prior recaps' patterns blindly.** Use them for shape only. Filter each line through "is this durable session knowledge?" before keeping.

##### Step 5: Offer to write

Ask: "Write this to the vault?" If the user confirms:

1. **Write session note** — direct file write (`Write` tool), no Obsidian involved.

   First draft a 2-4 sentence `summary` field — concrete, not marketing copy. This is the Level 0 representation; future sessions decide whether to read the full recap based on this string alone. List the major work + final state if testable. Pick `concerns` from the controlled vocabulary (`security`, `api`, `data`, `infra`, `ops`, etc.) — typically 2-5 for sessions that touch multiple areas.

   **Filename: match the vault's existing convention.** `ls $VAULT/sessions/` and mirror what's there (e.g. kebab-case `YYYY-MM-DD-title.md`). Only if the vault has no prior recaps, default to `YYYY-MM-DD-title.md`.

   Write `$VAULT/sessions/{filename}.md` with this frontmatter (mirror any extra fields the vault's existing recaps carry):
   ```yaml
   ---
   tags: [session]
   type: session
   concerns: [<populated>]
   audience: []
   summary: "<drafted 2-4 sentence summary>"
   created: {YYYY-MM-DD}
   status: completed
   projects: [$PROJECT]
   branch: {current-branch}
   ---
   ```

   **Required fields are non-negotiable.** Session notes without a populated `summary` defeat the Level 0 reading strategy — every future read becomes a full-file load. Don't skip the draft step; the summary is part of the recap, not optional metadata.

2. **Update TODOs**: Edit `$VAULT/todos/$PROJECT.md` (or `$VAULT/todos/platform.md` for cross-cutting items):
   - Mark completed items (`- [x]`) based on Work Done
   - **Extract every Next Steps checkbox from the recap into the appropriate TODO file.** Next steps that only live in session recaps get lost between sessions. The TODO file is the authoritative task list — if it's not there, it doesn't get tracked.
   - Remove items that are no longer relevant
   - Keep TODO files clean — open items only, no completed cruft accumulating

3. **Update Session Log**: Append a row to `$VAULT/sessions/Session Log.md` linking the new recap (`[[{filename}]]`) with a one-line summary, matching the existing table shape. **Row order is the authoritative "latest"** — orientation tooling reads the last row, so always append at the bottom.

4. **Report** what was written.

#### `recap search <query>`

Search past session recaps for a keyword or topic.

```bash
OBSIDIAN_VAULT_PATH=$VAULT vault-digest search "<query>"   # then narrow to sessions/ hits
```
Fallback: Grep for `<query>` across `$VAULT/sessions/*.md`.

Present matching recaps with date, title, and the matching context lines.

#### `recap history`

Show a chronological list of past session recaps with one-line summaries.

##### Steps:

1. **Read Session Log** at `$VAULT/sessions/Session Log.md` — this contains the date, project, branch, and summary for each session.

2. **Present as a numbered list** with date and summary for each entry.

3. **Offer to expand**: Ask the user which recap(s) they'd like to see in full. Read and display the selected recap note(s).

