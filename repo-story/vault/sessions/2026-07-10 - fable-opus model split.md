---
tags: [session]
type: session
concerns: [ops, architecture]
audience: []
summary: "Restructured the pipeline into 'Fable plans, Opus executes': .claude/settings.json pins the session to fable at effortLevel xhigh, four Opus-pinned agent types (explorer, code-researcher, history-researcher, narrator) in .claude/agents/, and AUTORUN.md/SKILL.md now launch those named types. Phase 5 split into 5a beats (main session) → 5b narrator agents. ADR 0001 + new CONTEXT.md glossary. Committed as e21d0d1, unpushed. Also rejected and rolled back an 'understated reportage' de-fluff pass on the mattpocock-skills narration — rich style stays; future tone work goes through beats, prototyped on one chapter."
created: 2026-07-10
status: completed
projects: [repo-story]
branch: main
---

# 2026-07-10 — Fable/Opus model split

## Work

1. Restructured the pipeline into "Fable plans, Opus executes": `.claude/settings.json` pins the session to `fable` at `effortLevel: xhigh`; four Opus-pinned agent types in `.claude/agents/` (explorer, code-researcher, history-researcher, narrator), each a thin wrapper over the existing `prompts/*.md` briefs.
2. AUTORUN.md + SKILL.md rewritten to launch the named agent types; Phase 5 split into 5a beats (`output/beats/<theme>.md`, written by main session) → 5b narrator agents; "write inline for 2–4 themes" rule removed; `beats/` added to folder convention and Phase 0 mkdir.
3. [[0001-fable-plans-opus-executes]] (docs/adr/) records the trade-off and the loud-failure choice; new `CONTEXT.md` glossary (unit, dossier, theme, beats, section, planning/execution phases, lens).
4. All committed as `e21d0d1` (single commit, unpushed; remote verified at `70af6f7`, plain push fast-forwards).

## Decisions

- Model split enforced structurally (agent frontmatter + settings.json), not via prose in AUTORUN or a Workflow script — prose drifts, scripts break the human-followable operator contract.
- If `fable` becomes unavailable: fail loudly, no fallback model.
- Phases 6–8 (build/publish) stay in the main loop — command execution needs no agent.
- Narration keeps the rich narrative style: an "understated reportage" register + sentence-level de-fluff pass across the 7 mattpocock-skills sections was reviewed and rejected (made content drier without fixing the fluff), fully rolled back. Any future tone work happens at the Phase 5a beats/structure level, prototyped on one chapter first.

## Discoveries

- `.claude/settings.json` supports `effortLevel` (low/medium/high/xhigh) alongside `model` — reasoning effort is codifiable per-repo. Subagents inherit session effort unless their frontmatter pins one.
- `git diff --no-index` reviews changes in gitignored run folders (needs a snapshot dir as "before"); `--word-diff=color` is the readable form for prose.

## Next Steps

- **Loose ends:** none new from this session.
- **Needs dedicated focus:**
  - [ ] If the narration-fluff complaint returns, redesign at the beats level (arc/framing, not word pruning) and prototype on one chapter for user judgment (~1–2 h; regression risk: changed chapters need their chunk WAVs re-rendered).
