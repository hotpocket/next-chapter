---
tags: [session]
type: session
concerns: [ops, infra, api]
audience: []
summary: "Added privacy-preserving hit counting to the published site: GoatCounter, driven by an optional `analytics` key in scripts/trilogy.json so the site code has one source of truth and an opted-out build ships no third-party script. The site assembler also patches the copied sw.js with a cross-origin passthrough — landry-ui's shell handler caches every response by URL with no origin check, and the beacon's per-hit cache-buster would mint an unbounded run of quota-padded opaque entries. Public dashboard at next-chapter.goatcounter.com, disclosed in README. Also fixed export-prompts (Skill-tool-injected skill bodies were leaking into exports as prompts) and added scripts/check-session-wrapup, which re-derives published prompt counts and fails when the Session Log, README, prompt-history, or command glossary drift from the exports. Then content-addressed the audio pipeline's chunk cache (chunk text + voice + TTS params -> sha12 filename) so editing narration re-renders only the changed chunks: the stale-numeral fix in the next-chapter book cost 8 chunks out of 150 instead of a full book re-render, with all three books migrated in place at 0 misses. 43 new assertions across five suites; all green."
created: 2026-07-30
status: completed
projects: [next-chapter]
branch: main
---

# 2026-07-30 — Site analytics (GoatCounter)

Companion prompts: [[2026-07-30-site-analytics-prompts]]

## Work

1. `scripts/build-trilogy-site`: optional registry key `analytics` (`{"goatcounter": "<code>"}`) emits the counter snippet into the page `<head>`; endpoint derived from the code, or a full URL passed through for a custom domain. Absent key → no third-party script.
2. Same builder patches the copied `sw.js` on the way into `docs/` — prepends a cross-origin passthrough (`stopImmediatePropagation` + `respondWith(fetch)`).
3. `scripts/test_build_trilogy_site.py`: +4 assertions — endpoint derivation, opted-out build stays clean, guard applied once and rebuild-idempotent, upstream sw.js body survives the patch.
4. `scripts/trilogy.json`: site code `next-chapter`; public dashboard at https://next-chapter.goatcounter.com.
5. `docs/` rebuilt; README discloses what's counted (path, referrer, coarse browser/country) and what isn't (cookies, personal data, consent banner), and links the dashboard from both Live demo and Technologies Used.
6. `Skill(claude-api)` ask-permission added to this repo's gitignored `.claude/settings.local.json`; global config unchanged. Config mirror refreshed to match current global settings (picks up that ask rule, drops the separately-removed `model` pin); `sync-claude-mirror --check` clean.
7. `scripts/export-prompts` now drops `isMeta` records; `scripts/test-export-prompts.sh` +3 assertions (isMeta skill bodies and image-source lines excluded, user-typed `/commands` retained).
8. Session published across every index: recap + 11-prompt export (cross-linked), Session Log row, README table row and totals (158/6), and a curated section 6 in `prompt-history.md` with its `**Totals:**` line.
9. `scripts/check-session-wrapup` + `scripts/test-check-session-wrapup.sh` (8 assertions): re-derives each published count from the export files and fails on any index that disagrees — recap↔prompts cross-links, Session Log row, README and prompt-history entries + totals, glossary coverage of every `/command`. Wired into CLAUDE.md's session-conduct wrap-up and README's test list.
10. **Chunk WAVs are content-addressed.** `build_audio.py` gains `chunk_key` (sha12 over chunk text + voice + TTS params), `chunk_filename`, `tts_params`, `referenced_chunk_names`, and a `cache-params.json` sidecar; `build_transcripts.py` addresses the same files through the same helper instead of rebuilding the index name. `repo-story/test_build_audio.py` (13 assertions) pins key identity and the edit-one-chunk property.
11. `repo-story/chunk_cache.py` — `migrate` (legacy index cache → content addressing, rename-only, no re-render) and `gc` (sweep chunks the current text no longer references); `test_chunk_cache.py` (15 assertions) covers both, including a float32-WAV fixture.
12. `scripts/regen-trilogy-audio` no longer wipes a book on text change. It migrates when the recorded text hash proves the index map still valid, builds, then sweeps orphans. Its suite was flipped to assert preservation instead of wiping.
13. All three books migrated in place (148 chunks each, 0 misses — the keys reproduced the existing cache exactly), then the next-chapter book's chapter 3 re-rendered twice as the narration was corrected and then properly narrated: the final pass was **11 chunks re-rendered, 436 cache hits, 10 orphans swept**. Only `chapter_0003` and its summary track changed on disk; manifest, transcript timings and the M4A agree at 461.1s.
14. Narration repaired by the `narrator` agent (Opus), per the pipeline's own contract — four paragraphs across the section and its summary, every other byte untouched so the rest stayed cache hits. Every live count is gone from the book: "thirteen checks", "one hundred ten prompts across four sessions", and the per-session count list became claims that stay true, and the chapter now describes `check-session-wrapup` with its July thirtieth prompt attribution. Historical numerals (the July twenty-first count correction) are deliberately kept — they record what the counts *were* and cannot drift.
15. README documents the new regeneration granularity and lists the two new suites; `repo-story/CLAUDE.md` documents `chunk_key` and `chunk_cache.py`.

## Discoveries

- **landry-ui's audiobook service worker caches cross-origin responses it should skip.** The shell handler is network-first and stores every response keyed by URL with no origin check. An analytics beacon carries a per-hit cache-buster, so each pageview mints a fresh entry; cross-origin entries are opaque, which browsers pad to a fixed multi-MB size against the origin's storage quota. Slow-burn quota growth that can crowd out the cached audio.
- **It does not break the request.** That `cache.put` is fire-and-forget — not returned, not awaited — so its rejection can never reach the handler's offline `.catch()`. A failed put is an unhandled rejection, not a `503 Offline` response. Recorded because the handler *looks* like it would swallow the request.
- Guard is **prepended** rather than edited into upstream's handler: `repo-story/player/` is gitignored (luinst-fetched from landry-ui), so an in-place edit is lost on re-fetch and a text substitution breaks on upstream drift. First-registered listener + `stopImmediatePropagation` wins without the second listener throwing `InvalidStateError`.
- No client-side analytics answers "who" — only when and where-from. A `?ref=` suffix on a shared link is how you isolate a specific visitor's hits.
- `~/.claude/settings.json` is a symlink into `~/git/.configs` — edits must target the resolved path.
- **`isMeta: true` is the durable marker for harness-injected user-role transcript records** — skill bodies loaded by the Skill tool (which carry no "Base directory for this skill:" prefix, so the old prefix filter missed them) and image-attachment source lines. What the human typed is never meta, including `/command` invocation blocks. A Skill-tool body had leaked ~3,600 lines into this session's prompt export before the filter was added.
- **The audio pipeline's chunk cache was index-keyed, and that is what made narration expensive to fix.** `build_audio.py` had always rendered per-chunk WAVs, but named them `chNN_<variant>_00007.wav` — so a single edited sentence shifted every later index and the cache would have served the wrong audio. `regen-trilogy-audio` compensated with a book-wide `rm -rf` on any text change: one word cost a full re-render. Content-addressing the chunk turns a 1–2h job into ~8 chunks. The same "content hashes, not incidental state" rule was already applied at the book level and in `transcripts.json?v=` — it just hadn't been pushed down.
- **Migration beats re-rendering.** The WAV at index N *is* the audio for chunk N as long as the text hasn't changed since that render — which the existing `.text-hash` record already proves. That made the switchover a rename of 148 files per book instead of hours of GPU time, and the 0-miss result independently confirmed the new keys reproduce the old cache.
- **Python's `wave` module can't read the pipeline's own audio.** torchaudio writes float32 (format tag 3); `wave.open` raises on it. The first cut of the sample-rate probe reported "no WAVs" against a cache of 148 real files. ffprobe (already a hard dependency) is the fallback, and the test fixture now writes float32 WAVs so it can't regress.

## Decisions

- **GoatCounter over GA4.** Cookieless (no consent banner), ~3KB, less adblocked in a developer/reviewer audience where GA commonly drops 30–50% of hits. Rejected: GA4 (named in the original ask), and running both.
- **Site code in the registry, not the HTML.** `scripts/trilogy.json` is the one source of truth; `docs/index.html` is generated, so an edit to the output dies on the next build.
- **Public dashboard.** A reviewer can watch their own visit land; the transparency is worth more than hiding traffic numbers.
- **The wrap-up is enforced, not remembered.** A recap fans out to five other files (Session Log, README table, README totals, prompt-history section, prompt-history totals) plus the glossary; `prompt-history.md` was missed this session precisely because it was a prose checklist item. The checker re-derives counts from the export files rather than comparing copied literals, so it can't drift with them. Rejected: a longer checklist in CLAUDE.md.
- **Narration goes through the `narrator` agent, not inline edits.** `SKILL.md` and ADR 0001 say sections are written only by that agent type (pinned to Opus); the first fix here was hand-patched straight into the section file and rendered. It read as patched — a five-item spoken list where the rules ban list shapes, no session-date attribution, a transition never composed with its paragraph. The pipeline's own contract exists to catch exactly that, and the cheap chunk cache is what made honouring it affordable.
- **Narration made drift-proof, not re-pinned.** The stale numerals were replaced with claims that stay true ("asserts every rule the exporter is supposed to enforce") rather than today's counts. A book that quotes live numbers goes stale every session; one that describes the mechanism does not. Rejected: re-pinning 17 checks / 158 prompts.
- **The chunk-cache work belongs in this repo, not upstream.** `repo-story/` here is a scrubbed commit replay of the private original, but the pipeline has been developed in-tree since (the summary-track feature, `3fb196b`), so this copy is the live source. Editing `~/git/repo-story` and re-vendoring would have discarded that.
- **Not upstreaming the guard to landry-ui.** That component ships no analytics and no cross-origin resources, so the caching path is unexercised there. The build-time patch in this repo covers the only consumer that exercises it. Revisit if landry-ui ever gains a third-party embed.

## Next Steps

Nothing loose. Analytics shipped; the narration drift that would have been a loose end was fixed instead, because making it cheap to fix was the better answer than deciding it wasn't worth fixing.

`llm-docs/reports/2026-07-23_interview-prep-plan-vs-reality.md` says "all five sessions" and stays that way — it is a dated retrospective, accurate as of its date, not a live index.
