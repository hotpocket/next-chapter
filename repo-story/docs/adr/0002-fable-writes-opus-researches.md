# Fable writes, Opus researches

Supersedes [0001](0001-fable-plans-opus-executes.md).

The split is by **kind of work**, not by planning-versus-execution tier: prose runs on Fable, code and research run on Opus.

- **Fable**: the main session (survey, inventory, Phase 5a beats, chapter ordering) and the `narrator` agent (Phase 5b sections + 5c summaries).
- **Opus**: `explorer`, `code-researcher`, `prompt-researcher` — reading source, verifying behavior exactly, tracing prompts through transcripts.

0001 split on cost and tier: Fable planned because it was the strongest synthesizer, Opus executed everything spawned because prose volume at Fable prices was not worth it. The model generation moved on. Opus 5 is the stronger model for logic and code; Fable remains the stronger writer of English. Narration is the one phase whose output is judged purely as prose — it is read aloud, once, by a listener who cannot re-read a clumsy sentence — so it belongs on the writing model, and the research phases that verify what the code actually does belong on the reasoning model.

Enforcement is unchanged and still structural: `.claude/settings.json` pins the session model, and each agent type pins `model:` in its own frontmatter, so the rule cannot drift across AUTORUN.md/SKILL.md edits.

## Considered options

- **Leave 0001 in place** — rejected: it now assigns narration to the weaker writer. The rule was correct for the model generation it was written in and stopped being correct without anything in the repo changing.
- **Move everything to Opus** — rejected: it optimizes the phases that were already fine and gives up the prose quality that the entire artifact is judged on.
- **Opus drafts, Fable polishes** — rejected: two passes over the same section, and the polish pass would rewrite most of it anyway. Cheaper and cleaner to write it once on the writing model.

## Consequences

- Sections and summaries change voice. Existing books were narrated under 0001; re-narrating a chapter now produces Fable prose next to Opus prose in the same book. The content-addressed chunk cache makes a full re-narration affordable per chapter, but mixed voice within one book is the transition cost.
- Both tiers must be available to the account; either being unreachable fails loudly at the pin, as under 0001. Do not silently fall back.
- `fable`/`opus` are aliases, so version bumps within a tier are picked up automatically — which is exactly why this ADR was needed: the aliases followed the model generation, and the *assignment* of tier to task did not.
- The lesson generalizes past this repo: a model-to-task mapping is a dated decision, not a permanent one. Re-check it when the generation turns over.
