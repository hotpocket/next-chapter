# Phase 4: Prompt Provenance Research — Agent Guidance

You are tracing the features of one part of a project back to the prompts that caused or shaped them. The narrative phase will walk a reviewer through the features and quote these prompts as the connective tissue — your job is to find them and pin them to their sources.

## Sources, in order of authority

1. **Session prompt exports** — files like `vault/sessions/<name>-prompts.md`: the user's prompts, verbatim, per session. When these exist, they are the ground truth.
2. **Curated prompt history** — e.g. a repo-level `prompt-history.md` or `config-history.md` that annotates which prompts mattered.
3. **Session recaps** — `vault/sessions/<name>.md`: what got done and why, in the session's own words. Paraphrase, not verbatim.
4. **Git history** — commit messages and diffs date the feature and often echo the instruction. `git log --follow` on the relevant paths.
5. **ADRs and TODO files** — record the decision, sometimes the instruction behind it.

Your task prompt tells you where these live for this element. Use only sources inside the repos you are given — nothing external.

## What to produce

For each feature in the inventory you are given:

- The prompt(s) that caused or shaped it. Verbatim quote when a prompt export has it; otherwise the recap's or commit's account, explicitly labeled as paraphrase.
- Session date (or commit date) for attribution.
- What changed as a result — one or two sentences tying the prompt to the feature's current behavior.
- Iterations, when they exist: an initial prompt and a later correcting prompt are more useful together than either alone. Corrections show steering.

## Labeling — this is the core discipline

Three levels, never blurred:

- **Verbatim**: exact text from a prompt export. Quote it. Note the session.
- **Paraphrase**: a recap or commit message describing the instruction. Say which source.
- **Inference**: the feature appeared between sessions with no recorded instruction. Say so: "no prompt for this survives; it first appears in the commit of July twenty-first."

A walkthrough that misattributes a paraphrase as a quote poisons the reviewer's trust in every real quote. When in doubt, downgrade.

## What to skip

- The intellectual origins of techniques (who invented the pattern, papers, the wider field) — out of scope entirely.
- Prompts that led nowhere, unless the dead end explains a current feature's shape.
- Any content that looks private (names, credentials, machine paths). These repos are scrubbed, but if something looks like it slipped through, flag it in your output header instead of quoting it.

## Output

Write a markdown file organized feature-by-feature, matching the inventory's feature names. For each: prompt (with its label and date), then the resulting behavior. This is raw material for the narrative phase — precision over polish.
