---
tags: [session]
type: session
concerns: [admissions-project, security, architecture, infra]
audience: []
summary: "Foundation session: mirrored the 65-lesson course, wrote config-history.md (reviewer legend + glossary), stamped conduct (CLAUDE.md, vault, export-prompts pipeline with tests), ran two wargames and two vets, recorded ADRs 0001-0006, audited and flipped landry-ui public, created private hotpocket/next-chapter with two commits (unpushed). V1 scope locked: static player of two self-narrating books (landry-ui + repo-story), Pages UI + S3 audio, local-only generation; V2 ingestion deferred."
created: 2026-07-20
status: completed
projects: [next-chapter]
branch: main
---

# 2026-07-20 — Foundation

Verbatim prompts for this session: [[2026-07-20-foundation-prompts]] (57 prompts).

## Work
1. `course/` mirror: all 65 Next Chapter lessons pulled via 10 parallel Opus agents through the gstack browse daemon (gitignored local reference; section 9 = project spec)
2. `config-history.md` — reviewer legend: AI-workflow history, command glossary, tone note, reproducibility boundary
3. `/conduct init`: CLAUDE.md (+ public-repo hygiene: staged gitleaks scan, never-track list, prompt-export rules), vault scaffold, `scripts/vault-digest` + `session-start.sh`
4. `scripts/export-prompts` (+11 tests, red→green): extracts session prompts from the Claude Code transcript, redacts, gitleaks-scans, writes `vault/sessions/<name>-prompts.md`
5. Wargames (promoted to `llm-docs/reports/` (renamed from docs/ 2026-07-21)): public-repo security + reviewer legibility; landry-ui public-flip audit (exhaustive full-history sweep)
6. Vets: config-history-as-reviewer-context (proceed); two-books journey frame (proceed — reviewer IS the listener)
7. ADRs 0001–0006 in `vault/decisions/`
8. landry-ui flipped **public** after audit + owner sign-off; `luinst` defaults to https clone (committed in landry-ui, unpushed)
9. Repo `hotpocket/next-chapter` created private; commits `Foundation` + `Foundation 2` (unpushed)
10. gitleaks installed, wired into commit gates and the export pipeline

## Discoveries
- gstack browse daemon crosses responses under concurrent `js` fetches — fetch sequentially and verify returned IDs (also in auto-memory)
- Chrome cookie import requires the exact host (`community.nextchapterproject.org`); bare domain imports 0 cookies
- repo-story's multi-agent refactor (2026-07-10) has never been run; the proven prose path is the 2026-03-26 prompt flow
- Wargame recon caught a real email in my own test fixture — fixtures are leak surface too

## Decisions
- V1 = static player of two pre-generated books (landry-ui + repo-story) served from this repo via Pages; audio in dedicated S3 bucket; local-only generation (Claude Code prompts + Chatterbox). V2 = on-demand ingestion (Lambda + Tailscale + OpenRouter), deferred — ADR 0004
- **Product = player + generator; the AI demonstration = their composition** into the shipped Pages site with hardened SSO-based S3 deploy — ADR 0006 (supersedes 0002)
- "Valuable to another person" resolved: the reviewer is the listener — vet flipped to proceed, ADR 0005 unconditional
- Cloned-voice audio publication: approved (recorded in ADR 0003)

## Next Steps

**Loose ends (cleanable now)**
- repo-story visibility: decide scrub-then-public vs private + SOURCES.md — minutes to decide, scrub itself may be longer

**Needs dedicated focus**
| item | what it is | est |
|---|---|---|
| site scaffold + vendor player | Pages layout in this repo, pinned landry-ui import, library page, manifests | hours |
| deploy script | S3 sync via local SSO profile; fail-loud credential checks per ADR 0001/0006 | hours |
| two generation runs | landry-ui + repo-story books on GPU (proven pipeline, resumable) — schedule early, long pole | hours each |
| SOURCES.md + provenance | pinned source hashes; per-book build provenance records | ~1h, with build |
| prompt-history.md curation | course-required curated index into per-session prompt files | ~1h, at end |
