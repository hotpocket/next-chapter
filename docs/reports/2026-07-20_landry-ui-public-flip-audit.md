# Wargame (stress): flipping landry-ui public

Target: is `github.com/hotpocket/landry-ui` safe to make public? Audit + attack
pass, all claims grounded in commands run 2026-07-20.

## Unknowns matrix

**Known knowns (verified)**
- 63 commits, single branch (main), no tags, no stashes, single author identity (githotpocket@gmail.com — already public on GitHub).
- `gitleaks detect` over FULL history: clean. All-revision pattern grep (password/secret/key/token/private-key/aws): one benign hit (the word "tokens" in a vault-digest comment).
- Complete inventory of every file ever committed: code, icons, docs, vault notes. No .env, no keys, no audio, no voice files ever added.
- Emails in any blob: only `git@github.com`. URLs: localhost, [feedback-endpoint]/events, [family-site], raw.githubusercontent.com self-reference.
- GitHub side: 0 issues, 0 PRs, no wiki, no Pages, 0 forks — nothing else flips.
- Vault/docs notes (192 lines total) read in full: engineering content only.

**Known unknowns**
- None remaining that a command can settle — the repo is small enough that the sweep was exhaustive, not sampled.

**Unknown knowns**
- Two commit messages carry owner-context: `Rename PWA to "Audiobooks for [family-member]"` (family first name — already public via the live [family-site] domain) and `sw: evict chapter_1073.m4a from PWA audio cache (voice-sample leak recall)` — documents a past incident where a generated chapter leaked reference-voice audio on the public site. The audio was never in this repo; the *record of the incident* becomes public.
- `scripts/luinst` clones over SSH — anonymous consumers of a public repo can't run it (usability, not security).
- Public repo = the feedback endpoint URL (`[feedback-endpoint]/events`) gets marginally more discoverable; it's already visible in deployed site JS. Its abuse surface (open POST → DynamoDB) belongs to repo-story's infra, not this flip.

## Attack pass

- "Secret in a deleted file / old revision" — **blocked**: all-revision grep + full-history gitleaks + complete added-file inventory.
- "Sensitive branch/tag/stash flips with the repo" — **blocked**: only main exists.
- "GitHub metadata (issues/PRs/wiki) exposes drafts" — **blocked**: all empty/disabled.
- "Commit message leaks what file contents don't" — **LANDED** (the two messages above). Not secrets; owner-acknowledgment items. History rewrite would cost more than it protects — both facts are already public or benign.
- "Repo becomes load-bearing upstream for the admissions project; future pushes leak" — residual: hygiene going forward (existing conduct stack + scan habits cover it).

## Verdict

**SAFE TO FLIP** — no secrets in any revision, message, or metadata. Two
owner-acknowledgment items (both already-public or benign): the "[family-member]" naming
and the voice-leak-recall commit message. One post-flip usability fix: document
an https clone path in luinst/README. Abort condition: none triggered.

## Owner sign-off

2026-07-20 — Both acknowledgment items accepted ([family-member] naming, voice-leak-recall
commit message); owner flipped the repo public himself.
