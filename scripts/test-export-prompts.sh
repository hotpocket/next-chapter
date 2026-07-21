#!/usr/bin/env bash
# Red/green test for scripts/export-prompts. Runs against a fixture transcript.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
FAIL=0
check() { # desc, condition-result
  if [ "$2" -eq 0 ]; then echo "ok   - $1"; else echo "FAIL - $1"; FAIL=1; fi
}

# fixture transcript: 2 real prompts, 1 tool_result, 1 system notification, 1 assistant
cat > "$TMP/fixture.jsonl" <<'EOF'
{"type":"user","message":{"role":"user","content":"first real prompt about the app"}}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"assistant reply"}]}}
{"type":"user","message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"t1","content":"tool output not a prompt"}]}}
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"second real prompt with secret user@example.com inside"}]}}
{"type":"user","message":{"role":"user","content":"[SYSTEM NOTIFICATION - NOT USER INPUT]\nbackground task event"}}
{"type":"user","message":{"role":"user","content":"ran it from /home/testuser/git/proj and it worked"}}
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"<task-notification>\n<task-id>abc123</task-id>\n<result>agent result body</result>\n</task-notification>"}]}}
{"type":"user","message":{"role":"user","content":"Base directory for this skill: /home/x/.claude/skills/foo\n\n# foo skill body"}}
EOF

OUT_DIR="$TMP/vault/sessions"
mkdir -p "$OUT_DIR"
"$HERE/export-prompts" --transcript "$TMP/fixture.jsonl" --out-dir "$OUT_DIR" --name 2026-07-20-test >/dev/null 2>&1
RC=$?
OUT="$OUT_DIR/2026-07-20-test-prompts.md"

check "exits 0" "$RC"
[ -f "$OUT" ]; check "writes <name>-prompts.md" $?
grep -q "first real prompt" "$OUT"; check "includes string-content prompt" $?
grep -q "second real prompt" "$OUT"; check "includes array-content prompt" $?
grep -q "tool output not a prompt" "$OUT"; check "excludes tool_result" $((! $?))
grep -q "SYSTEM NOTIFICATION" "$OUT"; check "excludes system notifications" $((! $?))
grep -q "task-notification" "$OUT"; check "excludes task notifications" $((! $?))
grep -q "/home/testuser" "$OUT"; check "redacts home paths" $((! $?))
grep -q "~/git/proj" "$OUT"; check "home path becomes ~" $?
grep -q "foo skill body" "$OUT"; check "excludes skill-file expansions" $((! $?))
grep -q "user@example.com" "$OUT"; check "redacts email" $((! $?))
grep -q "REDACTED" "$OUT"; check "redaction marker present" $?
grep -q "^type: prompts" "$OUT"; check "frontmatter type: prompts" $?
grep -q "\[\[2026-07-20-test\]\]" "$OUT"; check "links companion recap note" $?

exit $FAIL
