# Orient — TODO Digest Sub-Agent Prompts

Used by session-start orientation Step 1. CLAUDE.md (and SKILL.md Step 1) point here.

Used by Step 1. Both prompts run on **opus**: grouping, complete partition, and strict ordering are inferred each run; cheaper models interleave readiness order and miss counts-sum-to-total — and using the same model on both steps keeps errors from accumulating across the menu→drill-in handoff. When dispatching, substitute the resolved `$VAULT` path (sub-agents don't inherit it).

#### Prompt A — menu (model: opus)

> Read every authoritative TODO file in `$VAULT/todos/` in full (all of them; SKIP `Active TODOs.md` — a non-authoritative aggregate that would double-count). Large reads are expected — that's why you run in a sub-agent.
>
> **Build the partition FIRST, then derive the menu from it** — so the menu's counts can never drift from the file (a past run hand-tallied a wrong total into the menu while the file was correct):
>
> 1. Enumerate EVERY incomplete (`- [ ]`) item, assigning each to exactly one batch. GROUP BY DOMAIN inferred from item content (do not rely on any stored field; infer fresh). ~8–15 batches; large families may be one batch; add an explicit `Other / Uncategorized` batch if needed so the partition is COMPLETE (every item in exactly one batch, none dropped, none double-counted).
> 2. Write the partition to `/tmp/vault-orient/todo-batches.json` (create the dir first). **Pure JSON only — no markdown fences, no prose, no trailing commas, no comments.** Shape:
>    `{ "total": <int>, "generated": "<YYYY-MM-DD>", "sources": ["..."], "batches": [ { "id": "...", "name": "...", "readiness": "READY|PARTIALLY_BLOCKED|BLOCKED", "blocked_by": "<text|null>", "leverage": "<text|null>", "items": [ { "headline": "...", "source_file": "...", "severity": "high|med|low", "blocker": "<text|null>" } ] } ] }`
>    Include ALL items per batch (the menu shows only 2–3; the file holds the rest).
> 3. **VALIDATE before returning — do not skip.** Run `jq empty /tmp/vault-orient/todo-batches.json`; if it errors, fix and rewrite until it exits clean. Then set `"total"` to the jq-counted flat total: `jq '[.batches[].items[]] | length'`, and confirm `.total` equals it and equals `jq '[.batches[].items|length]|add'`. The file is the single source of truth.
>
> THEN produce a SCANNABLE WORK-BATCH MENU for a human choosing what to work on next, **derived from the validated file** (every count comes from the JSON, never a re-tally). Rules, exactly:
> - ONE ordered list of batches. No separate "primitives" section — annotate the batch that owns each cross-cutting primitive inline, e.g. `⚡ unblocks ~8 items (shared data-model primitive)`.
> - STRICT ORDER: READY → PARTIALLY BLOCKED → BLOCKED under headers (no interleaving); higher-leverage first within a tier.
> - PER BATCH: name · count · readiness (+ what blocks) · optional leverage tag · one-line theme · 2–3 representative headlines (prefer active bugs / high-severity), one short line each.
> - Target ~2000 tokens. End with a CALIBRATION NOTE: the jq-verified total, and confirmation that the menu's per-batch counts sum to it (they must — both come from the file).
>
> Return only the menu + calibration note.

#### Prompt B — drill-in (model: opus)

> Read `/tmp/vault-orient/todo-batches.json` (if it does not parse as JSON, say so and stop — do not guess or reconstruct it). For batch id `<ID>`, return a refined work-package: the batch's full item list with one-line context each, the shared primitive(s) to build first and what they unblock, readiness/blockers, and a suggested order of attack. Do NOT re-group or re-read source files — the partition is authoritative. Target ~2–3k tokens.
