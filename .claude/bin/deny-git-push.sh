#!/usr/bin/env bash
# PreToolUse(Bash) guard: deny ANY git push — force or not.
# Conduct policy: the agent never pushes; the human pushes manually. This is a
# mechanical block, not advice — it removes the ability to push, so no rule has
# to be remembered or obeyed (prose rules get rationalized around; a hook does
# not). Registered ONCE globally in ~/.claude/settings.json so it covers every
# repo, owned or not — consistent with the global SessionStart router, not a
# per-repo project hook.
#
# Matching strategy: split the command on shell separators ( ; && || | & and
# newlines ) into segments, then deny iff some segment is a git invocation
# (git is its leading token) whose subcommand chain contains `push` as a
# standalone token. This:
#   - catches  cd x && git push  /  foo; git push  /  git -C d push  /  --force*
#   - does NOT trip on the words "git push" appearing as an ARGUMENT (e.g. a
#     grep pattern), because there git is not the segment's leading token
#   - does NOT trip on non-push subcommands containing the word push
#     (git stash push, git commit -m 'push it'): only flag tokens (-C dir,
#     -c k=v, --git-dir=x — each optionally followed by one value token) may
#     sit between git and push.
cmd=$(jq -r '.tool_input.command // ""')

if printf '%s' "$cmd" \
  | sed -E 's/(\|\||&&|[;&|])/\n/g' \
  | grep -Eq '^[[:space:]]*git[[:space:]]+(-[^[:space:]]+[[:space:]]+([^-[:space:]][^[:space:]]*[[:space:]]+)?)*push([[:space:]]|$)'; then
  cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"git push is blocked by conduct policy: the agent never pushes (and never force-pushes) — the human pushes manually. This is a hard mechanical block; do not suggest a push command as a workaround."}}
EOF
fi
exit 0
