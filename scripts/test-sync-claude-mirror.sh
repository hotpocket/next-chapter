#!/usr/bin/env bash
# Tests for scripts/sync-claude-mirror. Runs against FAKE sources in a temp dir
# (CLAUDE_GLOBAL_DIR / CLAUDE_BIN_DIR / CLAUDE_MIRROR_DIR overrides) — never
# touches the real ~/.claude or this repo's .claude/.
set -u
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
sync="$here/sync-claude-mirror"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
global="$tmp/global" bin="$tmp/bin" mirror="$tmp/mirror" real="$tmp/real-skills"

fail=0
check() { # check <desc> <cmd...>
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "ok   $desc"; else echo "FAIL $desc"; fail=1; fi
}
check_not() {
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "FAIL $desc"; fail=1; else echo "ok   $desc"; fi
}

# --- build fake sources -----------------------------------------------------
mkdir -p "$bin" "$global/skills" "$real"
printf '#!/bin/sh\necho orient\n' > "$bin/claude-orient"
printf '#!/bin/sh\nexit 0\n' > "$bin/deny-git-push.sh"
chmod +x "$bin/claude-orient" "$bin/deny-git-push.sh"
echo '# global conduct' > "$global/CLAUDE.md"
echo '{"hooks":{}}' > "$global/settings.json"
printf '#!/bin/bash\necho statusline\n' > "$global/statusline-command.sh"

# full-mirror skills — vault is a SYMLINK (like the real ~/.claude/skills/*)
mkdir -p "$real/vault/commands" "$real/conduct/templates" "$real/vet" \
         "$real/wargame/references" "$real/wargame/tests"
echo v > "$real/vault/SKILL.md"; echo r > "$real/vault/commands/recap.md"
echo c > "$real/conduct/SKILL.md"; echo t > "$real/conduct/templates/CLAUDE.md"
echo x > "$real/vet/SKILL.md"
echo w > "$real/wargame/SKILL.md"; echo m > "$real/wargame/references/missions.md"
echo private > "$real/wargame/tests/dogfood.md"   # must NOT be mirrored
for s in vault conduct vet wargame; do ln -s "$real/$s" "$global/skills/$s"; done

# gstack — big repo, only a slim allowlist is mirrored
mkdir -p "$real/gstack/browse" "$real/gstack/node_modules" "$real/gstack/docs"
echo g > "$real/gstack/SKILL.md"; echo b > "$real/gstack/browse/SKILL.md"
echo MIT > "$real/gstack/LICENSE"; echo 1.2.0 > "$real/gstack/VERSION"
echo big > "$real/gstack/node_modules/blob.js"; echo d > "$real/gstack/docs/x.md"
ln -s "$real/gstack" "$global/skills/gstack"

run() { CLAUDE_GLOBAL_DIR="$global" CLAUDE_BIN_DIR="$bin" CLAUDE_MIRROR_DIR="$mirror" "$sync" "$@"; }

# --- 1: sync populates the mirror -------------------------------------------
run --sync || { echo "FAIL sync exited $?"; fail=1; }
check "bin/claude-orient copied"            test -f "$mirror/bin/claude-orient"
check "bin/claude-orient executable"        test -x "$mirror/bin/claude-orient"
check "bin/deny-git-push.sh copied"         test -f "$mirror/bin/deny-git-push.sh"
check "global CLAUDE.md -> CLAUDE.global.md" grep -q 'global conduct' "$mirror/CLAUDE.global.md"
check "settings.json -> settings.global.json" test -f "$mirror/settings.global.json"
check "statusline copied"                   test -f "$mirror/statusline-command.sh"
check "vault skill (via symlink) copied"    test -f "$mirror/skills/vault/commands/recap.md"
check "conduct templates copied"            test -f "$mirror/skills/conduct/templates/CLAUDE.md"
check "vet copied"                          test -f "$mirror/skills/vet/SKILL.md"
check "wargame references copied"           test -f "$mirror/skills/wargame/references/missions.md"
check_not "skill tests/ excluded"           test -e "$mirror/skills/wargame/tests"
check "gstack SKILL.md copied"              test -f "$mirror/skills/gstack/SKILL.md"
check "gstack browse/SKILL.md copied"       test -f "$mirror/skills/gstack/browse/SKILL.md"
check "gstack LICENSE copied"               test -f "$mirror/skills/gstack/LICENSE"
check_not "gstack node_modules excluded"    test -e "$mirror/skills/gstack/node_modules"
check_not "gstack docs excluded"            test -e "$mirror/skills/gstack/docs"

# --- 2: clean mirror passes --check ------------------------------------------
check "--check clean after sync" run --check

# --- 3: source drift is detected, resync clears it ---------------------------
echo changed >> "$real/vault/SKILL.md"
check_not "--check flags source drift" run --check
run --sync >/dev/null
check "resync clears drift" run --check

# --- 4: hand-edits / stale files in mirror are removed by sync ---------------
echo stale > "$mirror/skills/vault/stale.md"
run --sync >/dev/null
check_not "stale mirror file removed" test -e "$mirror/skills/vault/stale.md"

# --- 5: hand-written mirror docs are left alone ------------------------------
echo readme > "$mirror/README.md"; echo proj > "$mirror/settings.json"
run --sync >/dev/null
check "mirror README.md untouched"     grep -q readme "$mirror/README.md"
check "mirror settings.json untouched" grep -q proj "$mirror/settings.json"

# --- 6: missing source fails loudly ------------------------------------------
rm "$bin/claude-orient"
check_not "missing source errors" run --sync

[ "$fail" -eq 0 ] && echo "ALL TESTS PASSED" || echo "TESTS FAILED"
exit "$fail"
