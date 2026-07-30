#!/usr/bin/env bash
# Red/green test for scripts/check-session-wrapup — the gate that keeps a
# session's downstream indexes (Session Log, README, prompt-history, glossary)
# from drifting out of sync with its recap + prompts pair.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
FAIL=0
check() { # desc, condition-result
  if [ "$2" -eq 0 ]; then echo "ok   - $1"; else echo "FAIL - $1"; FAIL=1; fi
}

# Build a fixture repo whose indexes are all mutually consistent: two sessions,
# 3 + 2 prompts, latest is 2026-01-02-demo.
mk_fixture() { # dest
  local r=$1
  mkdir -p "$r/vault/sessions" "$r/scripts"
  cat > "$r/vault/sessions/Session Log.md" <<'EOF'
# Session Log

| Date | Recap | Project | Branch | Summary |
|---|---|---|---|---|
| 2026-01-01 | [[2026-01-01-first]] | p | main | first |
| 2026-01-02 | [[2026-01-02-demo]] | p | main | demo |
EOF
  printf 'Companion prompts: [[2026-01-01-first-prompts]]\n' > "$r/vault/sessions/2026-01-01-first.md"
  printf 'Companion to [[2026-01-01-first]].\n\n## Prompt 1\n\na\n\n## Prompt 2\n\nb\n' \
    > "$r/vault/sessions/2026-01-01-first-prompts.md"
  printf 'Companion prompts: [[2026-01-02-demo-prompts]]\n' > "$r/vault/sessions/2026-01-02-demo.md"
  printf 'Companion to [[2026-01-02-demo]].\n\n## Prompt 1\n\nran /vault recap\n\n## Prompt 2\n\nb\n\n## Prompt 3\n\nc\n' \
    > "$r/vault/sessions/2026-01-02-demo-prompts.md"
  cat > "$r/README.md" <<'EOF'
# fixture

published verbatim — **5 prompts across 2 sessions** — pair per session:

| Session | Recap | Prompts |
|---------|-------|---------|
| 2026-01-01 — First | [recap](vault/sessions/2026-01-01-first.md) | [2 prompts](vault/sessions/2026-01-01-first-prompts.md) |
| 2026-01-02 — Demo | [recap](vault/sessions/2026-01-02-demo.md) | [3 prompts](vault/sessions/2026-01-02-demo-prompts.md) |
EOF
  cat > "$r/prompt-history.md" <<'EOF'
# curated

## 1 — 2026-01-01 · First ([2 prompts](vault/sessions/2026-01-01-first-prompts.md))

## 2 — 2026-01-02 · Demo ([3 prompts](vault/sessions/2026-01-02-demo-prompts.md))

**Totals:** 5 prompts across 2 sessions.
EOF
  printf '# config\n\n| `/vault` (+ recap) | memory |\n' > "$r/config-history.md"
}

run() { # root -> prints output, sets RC
  OUT=$("$HERE/check-session-wrapup" --root "$1" 2>&1); RC=$?
}

T=$(mktemp -d); trap 'rm -rf "$T"' EXIT

# 1. Everything consistent -> pass
mk_fixture "$T/ok"; run "$T/ok"
check "passes a fully-updated wrap-up (rc=0)" "$RC"

# 2. prompt-history missing the newest session -> fail, and say so
mk_fixture "$T/ph"; sed -i '/2026-01-02-demo-prompts/d' "$T/ph/prompt-history.md"; run "$T/ph"
[ "$RC" -ne 0 ]; check "fails when prompt-history.md lacks the session" $?
printf '%s' "$OUT" | grep -qi "prompt-history"; check "names prompt-history.md in the failure" $?

# 3. README count that disagrees with the actual prompt file -> fail
mk_fixture "$T/cnt"; sed -i 's/\[3 prompts\]/[9 prompts]/' "$T/cnt/README.md"; run "$T/cnt"
[ "$RC" -ne 0 ]; check "fails on README per-session count mismatch" $?

# 4. Totals line that no longer sums -> fail
mk_fixture "$T/tot"; sed -i 's/5 prompts across 2 sessions/4 prompts across 2 sessions/' "$T/tot/README.md"; run "$T/tot"
[ "$RC" -ne 0 ]; check "fails on README totals mismatch" $?

# 5. Recap that never links its prompts companion -> fail
mk_fixture "$T/lnk"; printf 'no companion link\n' > "$T/lnk/vault/sessions/2026-01-02-demo.md"; run "$T/lnk"
[ "$RC" -ne 0 ]; check "fails when recap omits the [[*-prompts]] link" $?

# 6. A /command used in the prompts but absent from the glossary -> fail
mk_fixture "$T/gls"; printf '# config\n\nno glossary rows\n' > "$T/gls/config-history.md"; run "$T/gls"
[ "$RC" -ne 0 ]; check "fails on glossary drift (/vault not documented)" $?

# 7. Filesystem paths in prompts must not be mistaken for slash commands
mk_fixture "$T/pth"
printf 'Companion to [[2026-01-02-demo]].\n\n## Prompt 1\n\nran /vault recap on /tmp/x and ~/.claude/skills/foo\n\n## Prompt 2\n\nb\n\n## Prompt 3\n\nc\n' \
  > "$T/pth/vault/sessions/2026-01-02-demo-prompts.md"
run "$T/pth"
check "does not flag /tmp or path segments as commands" "$RC"

exit $FAIL
