# Wargame (stress): public-repo security + reviewer legibility

Target 1: this repo goes public without leaking private data.
Target 2: the recap+prompt-export process stays robust, and no system-level
dependency (hooks, skills, transcripts) obscures a Next Chapter reviewer's
understanding.

Mode: stress (no downstream executor). One doc, two theaters — shared terrain.
All claims grounded in reads/runs this session (2026-07-20).

## Unknowns matrix

**Known knowns (verified this session)**
- 0 commits; nothing pushed — no history to scrub. Remote does not exist yet.
- `gitleaks detect --no-git` on tree: clean. Ignore rules hold (`git check-ignore` passed for course/, .gstack/, docs/logs/).
- `scripts/test-export-prompts.sh` fixture contains the user's REAL email — would ship publicly. (Found by recon grep.)
- `.gstack/` holds browse network logs + `claude-available.json` (auth-adjacent); gitignored.
- `export-prompts` excludes tool output/system events/skill bodies; exits 1 on zero prompts (loud, not silent).
- Push is mechanically impossible for the agent (`deny-git-push.sh`); the human push is the final gate.

**Known unknowns**
- GitHub-side settings at repo creation (default visibility, Pages source). RECON NEEDED: at creation time, create **private**, verify rendered content, then flip public (Move T1-M2).
- Whether future vault recaps will quote secrets or paywalled course text pasted during debugging. RECON NEEDED: per-recap scan (T1-M3) — cannot be settled in advance.
- Claude Code transcript JSONL format stability across updates. RECON NEEDED: live smoke (`export-prompts` against real transcript) at each session end; 0-prompt error = format drift signal.

**Unknown knowns (true here, not yet applied)**
- gitleaks only catches regex-shaped secrets; personal context, names, paywalled prose sail through. The human pre-push read is the only gate for those.
- "Gitignored" ≠ "private" — force-add, `docs/reports/` screenshots, and published artifacts are alternate exit channels.
- This session predates the hygiene rules, and its prompt export WILL be published; verified: user prompts in it mention cookies but contain no secret values (tool outputs, which did carry cookies, are excluded).

**Unknown unknowns pass**
- New skills adopted mid-project appear in prompt history with zero explanation anywhere (glossary drift).
- A reviewer may read hook-enforced terseness ("Wrong: …", bare fragments) as rudeness or AI-authorship rather than a brevity discipline — a legibility gap no scanner flags.

## Theater 1 — securing the public repo

- **T1-M1 First-commit gate.** Action: `gitleaks detect --no-git` + manual `git status` review before the first commit. EXPECT: clean scan, file list matches intent. FAIL: a hit → fix in working tree (nothing is in history yet, cheapest possible moment). FORK: if a secret is ever found *after* a commit exists → `git filter-repo` before push; if already pushed → rotate the secret first, then rewrite; never rewrite-after-push without rotation.
- **T1-M2 Remote creation.** Action: create repo **private**, push, review rendered content on GitHub (README, vault notes, prompt files), then flip public. EXPECT: what renders matches what was reviewed locally. FAIL: repo created public by default → flip immediately; with 0 pushes the exposure window is empty. FORK: if anything unexpected renders (e.g. a file thought ignored) → flip private, fix, re-verify.
- **T1-M3 Steady state.** Action: per-commit staged-diff scan (CLAUDE.md rule), per-recap `export-prompts` redaction + gitleaks pass, human push as final read. EXPECT: every publish passes two machine gates + one human gate. FAIL: scanner misses a non-regex leak (name, course prose) → detection falls to the human read; keep diffs small so the read is real. FORK: any doubt on a diff → hold the push, ask.

## Theater 2 — robustness + reviewer legibility

Dependency inventory (what the reviewer cannot see): skill bodies (vault, gstack/browse, wargame, vet, conduct — live outside the repo), the three hooks (brevity, deny-git-push, claude-orient), global CLAUDE.md, Claude Code transcript store, jq/gitleaks.

- **T2-M1 The legend.** Action: config-history.md carries a **command glossary** covering every `/command` that appears in published prompts. EXPECT: reviewer maps any prompt-history invocation to a one-line meaning. FAIL: new skill enters use → glossary drifts stale. Counter: before publishing prompts, `grep -ho '^/[a-z-]*' vault/sessions/*-prompts.md | sort -u` vs the glossary — mechanical drift check. FORK: if a skill's *semantics* matter to a specific prompt sequence (e.g. a wargame verdict drove a build decision) → link the skill's output artifact (the .war/vet doc), don't vendor the skill body.
- **T2-M2 Terseness explanation.** Action: glossary notes that prompt style (fragments, "Wrong:", no pleasantries) is a hook-enforced brevity discipline. EXPECT: style reads as method, not mood. FAIL: omitted → reviewer misreads tone or suspects ghostwriting.
- **T2-M3 Export robustness.** Action: rely on `export-prompts` erroring on 0 prompts; session-end procedure treats that error as *stop and investigate*, never publish-empty. EXPECT: transcript-format drift surfaces loudly at the next recap. FAIL: partial drift (some prompts silently dropped, not all) → counter: sanity-check prompt count against session length at each recap; test fixture pins the format assumptions.
- **T2-M4 Reviewer-runnable boundary.** Action: README/config-history state plainly which scripts run anywhere (`vault-digest`) vs. which need this machine (`export-prompts`, `session-start.sh` — they read `~/.claude` state). EXPECT: reviewer never hits a mysterious failure trying to reproduce. FAIL: unstated → "script doesn't work" undermines the whole credibility play.

## Premortem

*It failed: the repo leaked / the reviewer bounced.* Working backward:
1. Real data in a fixture shipped (ALREADY LIVE — the test email; patched below).
2. A debugging session pasted a cookie into a prompt; redaction missed its shape; human skimmed the diff.
3. A vault recap quoted paywalled course prose; no scanner flags prose.
4. Reviewer opened prompt history, met 30 unexplained slash-commands and hook-terse fragments, concluded "tool soup, AI did everything," closed the tab.
5. Claude Code update changed transcript schema; exports quietly thinned; prompt history published incomplete — evidence of thinking evaporated.

## Risk triage (surviving risks: prevention / detection / verification)

- **TIGER — real email in test fixture** (verified live). Prevention: fixtures use `user@example.com`, rule added to hygiene section. Detection: recon grep + gitleaks. Verification: patched this session; tests re-run green.
- **TIGER — secrets pasted into prompts during future debugging.** Prevention: inline redaction in export; habit of not pasting live credentials. Detection: gitleaks on export + staged scan. Verification: redaction tests; per-recap scan output.
- **TIGER — glossary drift as new skills enter use.** Prevention: glossary in config-history.md + drift-check grep at publish time. Detection: the grep. Verification: run it before each prompts publish.
- **TIGER — transcript-format drift thins exports.** Prevention: format assumptions pinned in test fixture. Detection: 0-prompt hard error + count sanity check at recap. Verification: live smoke each session end.
- **PAPER TIGER — `.gstack/` tokens, `course/` mirror.** Gitignored + CLAUDE.md hard rule + human push gate.
- **PAPER TIGER — session-start.sh global-router dependency.** Harmless if run standalone; boundary documented (T2-M4).
- **ELEPHANT — "gitignored = safe" mindset.** Ignore rules protect `git add .`, nothing else. Alternate channels (reports/, artifacts, screenshots) carry the same data; the hygiene scan mentally scopes to *commits* only. Named here so it stays named.
- **ELEPHANT — the reviewer must trust unverifiable process claims.** Hooks and vault flow can't be reproduced from the repo. Mitigation: corroboration, not proof — git timestamps, recap notes, and prompt files cross-reference; interview closes the loop.

## Red-team record

- Attack: "a fixture with real data ships." **LANDED** (recon grep found the real email). Patch: fixture → `user@example.com`; hygiene rule extended to fixtures/examples.
- Attack: "glossary never exists / drifts; prompts unreadable." **LANDED.** Patch: glossary section added to config-history.md + mechanical drift check (T2-M1).
- Attack: "export silently publishes nothing after format drift." **Blocked** — script exits 1 on zero prompts (code read); residual partial-drift risk tracked as tiger with count sanity check.
- Attack: "force-add of an ignored dir." **Blocked** — CLAUDE.md hard rule + agent cannot push + human final read.
- Attack: "flip-to-public exposes unreviewed history." **Blocked** by T1-M2 order (private → verify → public) and empty-history starting point.

## Verdict

Both theaters survivable with patches applied this session: fixture email fix,
`.war/` gitignored, glossary + terseness note in config-history.md, recap
procedure gains the 0-prompt stop rule. Abort condition for the whole strategy:
any secret found in a *pushed* commit → rotate first, rewrite second, and
re-wargame the gate that let it through.

## Addendum (2026-07-20, later session)

The T2 dependency inventory ("what the reviewer cannot see: skill bodies, the
three hooks, global CLAUDE.md") and the second ELEPHANT ("the reviewer must
trust unverifiable process claims") are now materially reduced: that config is
mirrored in-tree at `.claude/` (generated by `scripts/sync-claude-mirror`,
drift-checked with `--check`, hygiene-scanned before commit like any other
tracked content). Skill `tests/` dirs and the 1.7 GB gstack upstream are
deliberately excluded — see `.claude/README.md`. Still outside the repo:
Claude Code itself, the transcript store, and proof the mirrored hooks were
active at any given moment — corroboration, not proof, remains the posture.
