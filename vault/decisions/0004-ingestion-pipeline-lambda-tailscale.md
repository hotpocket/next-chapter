---
tags: [adr]
type: decision
summary: "V2 (deferred, 2026-07-20): visitor submits GitHub URL → Lambda → Tailscale → home GPU runs pipeline via OpenRouter → completion Lambda → status UI. V1 ships without it."
status: deferred
created: 2026-07-20
concerns: [architecture, security, aws, scope]
---

# ADR 0004 — On-demand ingestion pipeline (V2 — deferred)

> **Deferred (V2), and note (2026-07-21):** this design presumed the S3 architecture retired by [[0008-audio-in-repo-pages-only|ADR 0008]] — reviving it means redesign, not resumption.

**Scope decision (2026-07-20):** V1 (the admissions submission) is rendering/
reading/playing of a pre-generated book — generation on the local machine,
artifacts uploaded to S3, UI on Pages (ADRs 0001–0003). Everything below is V2,
built after V1 ships; the library page may still land in V1 as a static feature.

## Context
Improvement idea: accept a GitHub URL from the web UI, dispatch generation to the home GPU box over Tailscale via a Lambda, home machine signals completion through a second Lambda, UI shows per-stage status, and a library page lists generated books. This is the feature that would justify Lambdas (ADR 0001 holds: playback needs none).

## Sketch
1. Pages UI → `submit` Lambda (URL + validation) → job record (DynamoDB) → forwarded to home server over Tailscale.
2. Home box runs prose + TTS pipeline, uploads artifacts to S3.
3. Home box → `complete` Lambda → job status updated.
4. UI polls a status endpoint; library page renders from a generated `books.json`.

## Concerns to resolve before accepting (each needs an answer, not optimism)
- **Feasibility — prose gen routes to OpenRouter (owner decision, 2026-07-20).** Verified in repo-story git history: the multi-agent orchestration (e21d0d1, 2026-07-10, "Fable plans, Opus executes") has **never been run** — it was a token-saving refactor. Every produced book came from the original 2026-03-26 **prompt-based** skill. Port target is therefore the proven prompt flow, which maps naturally onto staged OpenRouter API calls — materially smaller than porting the agent orchestration. Quality parity still unproven headless. Load-bearing probe: one-chapter headless run via OpenRouter on a small repo; compare against a produced chapter before building any AWS plumbing.
- **API key custody.** The OpenRouter key lives on the home box only — never in a Lambda env var, never client-side. Hard **spend cap on the key** before the endpoint exists.
- **Abuse surface.** A public submit endpoint now burns dollars (OpenRouter credits) plus GPU hours and disk. Minimum: auth on submit (even a shared token for the demo), queue depth 1, allowlist or size cap on target repos, job dedupe, key spend cap as the backstop.
- **Home-network exposure.** The Lambda joins my tailnet (or hits a funnel endpoint). Scope it: Tailscale ACLs so the Lambda's node key reaches exactly one host:port; the home listener validates payloads and runs nothing but the pipeline entrypoint; no inbound shell surface.
- **Long-running job ≠ Lambda.** Lambdas only dispatch and record (seconds); the hours-long work stays on the GPU box. Status lives in DynamoDB, not a held connection.
- **Scope vs. the 4–12h admissions budget.** This roughly doubles the project: two Lambdas, DynamoDB, Tailscale ACLs, status UI, library page, hardening. It also weakens ADR 0001's clean "no request-time backend" story if half-finished.

## Recommendation (pending owner decision)
Phase it: **submit + library as static-era features first** (library page over `books.json` is pure static and valuable now; "request a repo" can open a GitHub issue as MVP intake). Accept 0004 as a **post-submission or stretch phase**, gated on the headless-prose probe passing. If accepted for the submission, /wargame the security design before any Lambda is created.
