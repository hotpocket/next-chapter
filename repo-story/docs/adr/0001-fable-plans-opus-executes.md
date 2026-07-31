# Fable plans, Opus executes

**Superseded by [0002](0002-fable-writes-opus-researches.md)** (2026-07-30): Opus 5 is the stronger reasoner and Fable the stronger writer, so narration moved to Fable and only the code/research agents stayed on Opus. The reasoning below is kept as the record of why the original split was drawn where it was.

The pipeline splits by model tier: the main session runs on Fable and does the planning phases (survey, thematic synthesis, beats, chapter ordering); all spawned agents (explore, research, narrate) run on Opus. Fable is the strongest synthesizer but the wrong price for the token-heavy execution phases; Opus is the strongest generally-priced executor. The split is enforced structurally, not by prose: `.claude/settings.json` pins the session model to `fable`, and the agent types in `.claude/agents/` each pin `model: opus` in frontmatter — so the rule can't drift across AUTORUN.md/SKILL.md edits or be forgotten mid-run.

## Considered options

- **Inline "use model X" instructions in AUTORUN prose** — rejected: repeated ~6 places, drifts, relies on the orchestrator obeying prose every run.
- **Workflow-script orchestration** — rejected for now: strongest enforcement, but AUTORUN would stop being a document any operator (human or LLM) can follow top to bottom.
- **Fable narrates small books inline** (old "2–4 themes, write inline" rule) — rejected: replaced by beats (Fable) → sections (Opus), keeping planning context in the narration without paying Fable prices for prose volume.

## Consequences

- If Fable becomes unavailable to the account, sessions in this repo **fail loudly** at the model pin — deliberate; do not silently fall back. Fix by editing `.claude/settings.json` or `/model`.
- `fable`/`opus` are aliases, so version bumps within a tier are picked up automatically.
- `effortLevel: xhigh` in the same settings file makes Fable reason at maximum effort for the planning phases; subagents inherit it unless their frontmatter pins a lower effort.
- Quick unrelated sessions in this repo also start on Fable; override per-session with `/model`.
- New pipeline artifact: `output/beats/<theme>.md` (Phase 5a), the handoff from planner to narrator.
