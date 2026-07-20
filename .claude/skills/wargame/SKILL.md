---
name: wargame
description: "Wargame a target — a concept, process, task, or architecture — instead of planning it: fight it on paper until it survives, then save the doc. Use when the user says wargame, stress-test, premortem, red-team, de-risk, 'fight this on paper', 'how does this fail', 'what am I missing', or invokes /wargame."
metadata:
  author: brandon
  version: "1.0"
license: MIT
---

# /wargame

Wargame the target, don't plan it. A plan lists steps; a wargame fights them —
each move carries its likely failure and a counter-move, forks carry triggers,
and the whole thing survives a self-run red-team before it's saved. Output is a
saved doc, not chat that scrolls away.

**Full method + provenance:** `references/fable.knowledge` (this skill's dir —
the wargamed recipe this skill operationalizes, Phase B). Read it for the
*why*; the load-bearing checklist (SUCCESS.md's 8 points) is inlined below.

## The shared spine (both modes)

**recon → unknowns matrix → fight it move-by-move → red-team until it survives → save.**

Only the exit criterion differs by mode.

1. **Recon, read-only.** Read/inspect what the target actually is before
   simulating. No state changes in this phase. Ground every later claim in
   something you read or ran this session — never assert from memory.
2. **Unknowns matrix — mandatory, non-negotiable.** Before fighting anything,
   ask *what am I likely missing?* and write the four boxes:
   - **known knowns** — settled facts you've verified
   - **known unknowns** — gaps you can name → mark each `RECON NEEDED` with the
     exact check that settles it
   - **unknown knowns** — things already true in this context you haven't applied
   - **unknown unknowns** — the pass whose job is to make them nameable
   Any unfilled required input is `BLOCKED` — list it, state what's needed, never
   invent it.
3. **Fight it move by move.** Each move: action → **EXPECT** (what you see if it
   worked) → **FAIL** (the likely failure, the cause it signals, the counter-move)
   → **FORK** (if you observe X, take route B — a trigger, not a judgment call).
   A move's failure must *change the route*, not just annotate it. If you produce
   a linear plan wearing wargame vocabulary, you've failed the step.
4. **Red-team, self-run and recorded.** Attack your own output at least once
   ("what kills this?"). Patch what lands. Record the attack that succeeded + its
   patch, and note attacks that failed. This is what separates a wargame from a
   plan.
5. **Save.** Write to `.war/<slug>.md` in the cwd; echo the path. Never write
   outside cwd without asking.
   - **Owned repo:** add `.war/` to `.gitignore` if absent (working scratch
     unless promoted).
   - **Repo you don't own** (per global conduct — check `git config user.email`
     / who owns the tree): do NOT edit the tree's `.gitignore` or drop conduct
     artifacts in it. Write the wargame to the repo's external memory home
     (`~/Documents/AgentMemory/<repo>/` if present) or a scratch path outside the
     tree, and say where it went. When unsure who owns it, ask before mutating.

## Mode detection

**Heuristic:** does the target have a concrete deliverable a *different*
agent/person would produce later?

- **Yes → route mode.** There's a downstream executor.
- **No → stress mode.** A concept/idea/architecture with nobody to hand a blueprint to.

Auto-detect. When genuinely ambiguous, state your pick + one-line why and
proceed — don't block on a question. Override with `/wargame route <x>` or
`/wargame stress <x>`.

**Modes can be sequential, not just exclusive.** A decide-*then*-build target
("should we cache X, and if so build it") is stress first; if the decision
survives, offer to route the resulting build as a second phase. Don't force one
mode when the target is really both.

## route mode — executable-blind blueprint

The output is a route a cheaper executor follows end-to-end without asking a
question. Open with a **WARGAME ORDER header** that names the actual executor and
tells it: *"You are wargaming this mission, not executing it. A cheaper executor
runs the brief later; your job is the route it follows."* Tailor the wargame to
that named executor.

**No mission brief yet?** Author it first — template, brief-craft rules, and 10
credited domain exemplars in `references/missions.md` (this skill's dir).

**Exit gate — the 8-point SUCCESS standard. All eight must hold:**
1. Every move states its expected observation.
2. Every move carries its most likely failure + the cause it signals + the counter-move.
3. Every fork has a trigger — no judgment calls left to the executor.
4. Every unsettled assumption is marked `RECON NEEDED` with its settling check.
5. Abort conditions exist — when to stop and flag rather than improvise.
6. Verification is spelled out: which runs the executor performs, and what pass looks like for each.
7. It survived a red-team pass; the attack + patch are recorded.
8. It's executable blind — a mid-tier model runs it end-to-end, zero questions.

When a verification run assumes a tool the executor may lack (a headless browser,
a specific CLI), give it a fallback in the same clause ("if no browser, verify by
reading the logic and state which method") — a missing tool otherwise becomes a
blocking question. (Learned from the B6 route dogfood.)

**Blind-executor validation (opt-in, route-only).** After the wargame passes
self-grade, offer to spawn a subagent that reads *only* the wargame + brief, runs
it blind, and logs `QUESTIONS.md`. Every question it asks is a hole (missing
trigger or RECON) → patch the wargame. 0 questions = the payoff holds.
- **Never spawn it as `subagent_type: fork`** — a fork inherits this whole
  conversation, so it already knows everything and the question-count metric is
  worthless. Use a fresh type (`general-purpose` / `claude`), default
  `model: sonnet`, which starts with a clean context.
- If the executor cites any fact not in the wargame doc, isolation leaked — abort
  and re-spawn clean.
- Skip silently in stress mode.

## stress mode — de-risked judgment

No executor exists, so "executable-blind" is the wrong bar. After the shared
spine, the output is de-risked judgment. Add:

- **Premortem** — assume it already failed; work backward to the causes.
- **Risk triage vocabulary** — tag every surviving risk:
  - **tiger** — verified, high-severity risk
  - **paper tiger** — a risk already mitigated
  - **elephant** — an unspoken systemic concern nobody's naming
- Every surviving risk gets **prevention + detection + verification**.
- **No executor is spawned.**
- **Promote-on-exit:** end by offering to promote the findings into an *existing*
  ledger home — an ADR draft, or `docs/YYYY-MM-DD_<name>.md` — never a new
  `docs/war/` silo. The `.war/` file is the scratch; the ledger is where a real
  decision record belongs.

## Scale — single vs batch

- **Single target** → one `.war/<slug>.md`. No folders.
- **Batch** — a directory arg, or ≥2 enumerable targets, or explicit
  `/wargame batch <dir>`. **Announce first** ("detected N targets → building
  `fablewar/`"), then escalate to the folder machine:
  - `fablewar/tasks/` — one mission brief per file
  - `fablewar/wargames/` — one wargame per task
  - `fablewar/SUCCESS.md` — the 8-point standard
  - `fablewar/LEDGER.md` — every grade, patch, blocker
  Work breadth-first: rough-draft every wargame before polishing any; then refine
  the *current weakest* draft (grade → red-team the breaking move → patch →
  re-grade) until each survives a kill attempt. Grade with a fresh session/model
  than the drafter — author-graded drafts score uniformly high. Log per-cycle
  grades in `LEDGER.md` so deltas are computable.
  **Stop rule:** end the refinement loop when every wargame is DONE or BLOCKED,
  **or** two consecutive full cycles improve no grade. Per-item DONE bar is
  unaffected: all 8 points hold AND one honest kill attempt fails. Never soften
  the grading to finish faster — a draft that passes on paper but dies at first
  contact is a failure of the loop. `/loop` is the natural runner for the
  refinement cycle.
  **Never create `fablewar/` silently** — the announcement is the guardrail
  against surprise folder creation.

## Fable-5 hygiene (baked in)

- Never ask the planner to reproduce its own reasoning in the output — trips the
  `reasoning_extraction` classifier. Ask for the artifact (the wargame, the
  findings, the attack+patch), not a narration of how you thought.
- Ground every claim against something actually read or run this session.
- One well-specified pass up front beats drip-feeding instructions.
