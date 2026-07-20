---
name: vet
description: "Build and judge an idea from its kernel — frame audit, kill-tested decomposition, wargamed hostile pass, proceed/probe-first/kill verdict — kept in a living doc. /vet <idea> to start; /vet <path> to re-vet after probes report."
disable-model-invocation: true
metadata:
  author: brandon
  version: "1.0"
license: MIT
---

# /vet

Vet the idea, don't just elaborate it. Planning grows structure; vetting
decides whether the structure deserves to exist. Output is a verdict —
**proceed / probe-first / kill** — carried by a living doc in which every
claim names the real-world test that could kill it, and which updates as
those tests report. The plan corrects instead of drifts.

Method, in one breath: reflection is cheap and self-rewarding — by the third
meta-pass it produces the *feeling* of depth with no new information (the
**whirlpool**). Exogenous bits — experiments, data, other people — are
expensive and correcting. So ration recursion, make every claim buy depth
with new information, and route all confidence through named contact with
reality (**feeds**).

## Aiming

Args aim the skill, never describe the process.

- `/vet` — target = the idea currently under discussion. Several candidates →
  ask one question, then proceed.
- `/vet <idea text>` — explicit target; steering welcome ("frame is fixed",
  "chat-only, no doc").
- `/vet <path-to-doc>` — **re-entry** on an existing vet doc (see Re-entry).

## Scope

Right-sized target: an idea or plan worth at least a session of work whose
*existence* is up for judgment.

- Smaller than a session → answer directly; the machinery costs more than the idea.
- Code-change planning → plan mode.
- Already-committed thing needing only failure modes → the wargame skill, directly.

## Phases

**0 — Kernel.** Compress the idea to one sentence: *what changes in the
world, and why that's worth it.* Complete when the sentence exists and the
user accepts it. If it won't compress, the idea isn't understood yet — say
so and stop.

**1 — Frame audit — the one mandatory pause.** State the question the kernel
answers. Generate 2–3 rival framings: different questions this kernel might
*really* be answering. Present them (AskUserQuestion fits) and stop for the
user's pick or merge. Frame errors are the expensive ones, and the user is
the adversary this skill must keep in the loop — a solo pipeline loses the
"that's shallow" correction that makes vetting work. Complete when the user
has chosen.

**2 — Decompose once.** Break the kernel into its supporting claims, one
level only. Each node:

`- [tag] claim — feed: <concrete test/datum/question that could kill it>`

Tags are coarse by design — **load-bearing / likely / speculative** — point
numbers are false precision. A claim that cannot name a feed *is*
speculative; tag it so. Complete when every node is tagged and fed.

**3 — Rationed recursion.** Recurse only into nodes that are load-bearing
AND uncertain AND pass the **paraphrase test**: would the children contain
new information, or restate the parent in finer words? Paraphrase →
whirlpool detected → stop. Depth cap 3: past that, the missing information
lives in the world, not in further thought. Complete when every leaf is
either actionable-in-one-sitting or converted into a probe ("run the 1-hour
probe, then re-vet this branch").

**4 — Hostile pass.** Release the predator: invoke the **wargame** skill
(stress mode) on the tree. Fold what lands back in — surviving risks become
nodes with feeds; killed branches stay, struck through (the graveyard is
data). `.war/` scratch stays scratch; the vet doc owns the conclusions.

**5 — Verdict.** Exactly one:

- **proceed** — load-bearing claims confirmed, or cheap enough to be wrong about
- **probe-first** — verdict blocked on named probes; list them, cheapest kill first
- **kill** — a load-bearing claim died; name it and what it took down

Chat output is the decision layer only: the verdict, the top 1–3 probes
ranked by information-per-hour, and what result would flip the verdict. The
doc holds the tree; the chat holds the decision.

## The doc

Home is derived at runtime, never hardcoded: repo with an adopted vault →
`vault/vets/<slug>.md`; repo you don't own → `~/Documents/AgentMemory/<repo>/vets/<slug>.md`;
no vault → offer `docs/` or chat-only.

Frontmatter follows house vault style so `vault-digest` indexes it
(`type vet` lists every vet with its kernel):

```yaml
---
tags: [vet]
type: vet
summary: "<the kernel sentence>"
status: probing | ready | killed
created: YYYY-MM-DD
concerns: [...]
---
```

Body sections: `## Tree` (tagged nodes, feeds, per-claim status
pending/confirmed/killed), `## Hostile pass`, `## Probes`, `## Verdict`
(dated, append-only history), `## Open questions` (the user's, not yours).

**Probe grammar — load-bearing, machine-read.** Every open probe is one line
under `## Probes`:

`- [ ] probe: <concrete action> → <which claim it confirms/kills>`

`vault-digest probes` greps exactly `^- [ ] probe:` across `vets/`, and
session-start orientation surfaces the count — that derivation is the only
mirror; the doc is the single source of truth. When a probe runs, flip its
box to `- [x]` and record the result at its claim. The checkbox is the
*action's* state; the claim's status is the *belief's* state — two facts,
one home each.

## Re-entry

`/vet <path>`: read the doc, ingest new probe results (ask for them if the
user didn't volunteer), flip checkboxes, update claim statuses and tags,
prune dead branches (strike, keep), re-run Phase 5, append the dated
verdict. Re-vet on new data only — **one meta-level, maximum**: a plan may
be vetted; a vet is re-vetted only when a probe has reported. The skill
obeys its own whirlpool rule.

## Hygiene

- Ground every claim in something read or run this session; what you can't
  settle gets `RECON NEEDED` plus the exact check that would settle it.
- Produce artifacts (the doc, the verdict, the probes), not narrations of
  your own reasoning.
