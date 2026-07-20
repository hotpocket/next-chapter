# Config History — The AI Workflow I'm Bringing to This Project

**For the reviewer:** before starting the Section 9 project, this documents the
AI working environment I've already built and use daily — where it came from
(git history, reconstructed 2026-07-19), and the four tools I reach for most.
The project you're reviewing was built inside this system.

## Scale and provenance

- `~/git/.configs`: my dotfiles repo since **2016** (267 commits). All AI
  tooling was added in a five-week burst, **2026-06-06 → 2026-07-10**, and is
  versioned there — `~/.claude` is just symlinks into it.
- Usage: **1,604 prompts across 28 projects in ~28 days** of Claude Code
  (2026-06-21 → 2026-07-19).

## The four pillars of my workflow

### 1. The vault — persistent memory in every repo

Each repo I work in gets a `vault/` folder (Obsidian-compatible markdown:
`Home.md`, `sessions/`, `todos/`) where the AI writes back what it learns —
session recaps, open todos, durable discoveries. Repos I don't own get an
external vault at `~/Documents/AgentMemory/<repo>` instead, so I never commit
my tooling into someone else's tree.

How it works day-to-day:
- A **SessionStart hook** (`claude-orient`) runs when Claude Code opens: it
  surfaces the latest recap and open-todo count, so every session starts
  oriented instead of cold.
- **`vault-digest`** reads note frontmatter with grep/awk — one-line summaries
  first, full note bodies only when a summary points there. Key design
  decision (2026-06-29): I dropped the Obsidian-app dependency so memory works
  headless and across parallel AI sessions.
- At session end: `/vault recap` writes the session back to memory.

This solves the core problem of AI collaboration: context loss between
sessions. The vault is the AI's long-term memory, and it lives in git.

### 2. `~/.claude` config — how I shape Claude's behavior

Three hooks in `settings.json` mechanically enforce my rules (not suggestions
— code that runs on every session/prompt/tool call):

| Hook | What it does | Why |
|------|--------------|-----|
| SessionStart → `claude-orient` | injects vault orientation into context | never start cold |
| UserPromptSubmit → brevity injector | re-states the brevity rule on **every prompt** | terse, outcome-level answers |
| PreToolUse → `deny-git-push.sh` | **blocks the AI from ever running `git push`** | I run pushes and deploys, always |

The global `CLAUDE.md` (symlinked, versioned) encodes the philosophy, each
rule dated to the commit that introduced it:
- **"Claude commits; the user pushes"** — my first-ever AI conduct rule
  (2026-06-06), later hardened into the mechanical hook above. The AI
  prepares; I execute anything outward-facing, watching it live.
- **Tests first, code second** (2026-07-06) — red → green.
- **Durable over accurate** (2026-07-06/07) — prefer constructs that survive
  commits, moves, and machine changes; learned the hard way in an earlier
  project.
- **Idempotent, reversible-by-default; report outcomes faithfully** — failed
  or skipped steps get said, not smoothed over.

### 3. gstack `/browse` — the AI sees what it built

From Garry Tan's open-source gstack suite (I'm a consumer — 2 downstream
commits of its 362; my role is wiring it into my system). `/browse` runs a
persistent headless Chromium the AI drives directly: navigate, click, fill
forms, import my logged-in browser cookies, take annotated screenshots, diff a
page before/after an action, read the JS console and network log.

This is how the AI **verifies instead of assumes**: after a change, it opens
the real page, exercises the flow, and shows me screenshots. For this project
it means the app gets tested in an actual browser at every step, not declared
done from code alone. (I maintain my own troubleshooting baseline for its
Playwright/Ubuntu quirks in my global CLAUDE.md — ownership of my stack.)

### 4. `/wargame` — fight the plan before building it

A skill I authored (2026-07-08, grown from an earlier `fablewar.sh` prototype):
take a plan or architecture and attack it on paper — move, counter-move —
until it survives or breaks, then save the resulting doc. I run this **before**
building, so weaknesses surface when they cost minutes, not days. The
companion `vet` skill (my newest) judges an idea's kernel first: proceed,
probe-first, or kill.

## Supporting cast

- **conduct** skill: stamps any repo with this whole setup (CLAUDE.md, vault
  scaffold, hooks) — idempotent, one command.
- **learn-video** (authored 2026-07-08): turns lesson videos into executable
  `.knowledge` recipes.
- Vendored with pinned upstreams: **vault** core (adamtylerlynch v2.2),
  **writing-great-skills** (mattpocock @896f14d) — which I used to
  design-audit my own skills the day I wrote them.

## Reading the prompt history — command glossary

Prompts in this repo's history invoke custom skills by slash-command. The
glossary below covers every command you'll encounter; if a new one appears in
later sessions it gets added here (checked mechanically before each publish).

| Command | What it does |
|---------|--------------|
| `/vault` (+ recap) | reads/writes the repo's persistent memory; `recap` writes the session note these prompts accompany |
| `/wargame` | stress-tests a plan move-by-move until it survives red-teaming; output saved as a doc |
| `/vet` | judges an idea's kernel before planning: proceed / probe-first / kill |
| `/conduct` | stamps a repo with this whole setup (CLAUDE.md, vault, scripts) |
| `/browse` (gstack) | drives a real headless browser: navigate, click, screenshot, verify |
| `/gstack` | router into the gstack skill suite (browse, qa, review, …) |

**On tone:** my prompts read terse — fragments, "Wrong:", no pleasantries.
That's a deliberate discipline enforced by a hook that re-injects a brevity
rule on every prompt (see the hooks table above), not carelessness. Corrections
like "Wrong: …" are me steering the AI, which is exactly the collaboration
being evaluated.

**Reproducibility boundary:** `scripts/vault-digest` runs anywhere;
`scripts/export-prompts` and `scripts/session-start.sh` read this machine's
`~/.claude` state and only run here. The artifacts they produce (session notes,
prompt files) are all in the repo.

**In-tree mirror — read the config yourself:** everything this document
describes (the three hooks' code and registration, the global CLAUDE.md, the
skill bodies behind every slash-command in the glossary) is mirrored inside
this repo at [`.claude/`](.claude/README.md), with a table mapping the
machine paths you'll see in vault notes (`~/bin/claude-orient`,
`~/.claude/skills/…`) to their in-repo copies. The mirror is generated from
the live config by `scripts/sync-claude-mirror` and drift-checked with
`--check` — you are reading the actual files I run, not a description of them.

## Condensed timeline

| Date | Event |
|------|-------|
| 2016-05-11 | `.configs` born (plain dotfiles) |
| 2026-06-06 | First AI conduct rule: the user pushes, not Claude |
| 2026-06-21 | Daily Claude Code use begins; `claude-conduct` repo started |
| 2026-06-22 | Brevity hook; `~/.claude` deployed via symlinks |
| 2026-06-29 | Vault goes file-first (`vault-digest`, `claude-orient`); global CLAUDE.md |
| 2026-07-03 | Push-block hook; `claude-conduct` subtree-merged into `.configs` |
| 2026-07-06/07 | Tests-first + durable-over-accurate rules |
| 2026-07-08 | wargame + learn-video authored; design-audited same day |
| 2026-07-10 | "i run push & deploy" — policy final form |

## Why this matters for the project

The through-line: **the AI does the work; I own the controls and the memory.**
Every rule exists because something went wrong once and I made the fix durable
— a wrong push became a mechanical block, session amnesia became the vault,
untested claims became `/browse` verification, weak plans became `/wargame`.
Expect to see these tools in this project's prompt history: wargaming the plan
before building, browse-verifying each feature, and vault recaps carrying
context between sessions.
