#!/usr/bin/env bash
# test-regen-trilogy-audio.sh — red/green suite for scripts/regen-trilogy-audio.
# Uses a stub PYTHON and a temp registry/repo layout; never touches real books
# and never invokes a GPU.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
script="$here/regen-trilogy-audio"

fails=0
check() { # check <desc> <cmd...>
  local desc="$1"; shift
  if "$@" >/dev/null 2>&1; then echo "ok   $desc"; else echo "FAIL $desc"; fails=$((fails+1)); fi
}

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# Fake repo-story dir with two ready books + one broken one
rs="$tmp/rs"
for slug in alpha beta; do
  mkdir -p "$rs/$slug/output/sections" "$rs/$slug/output/summaries"
  echo "text" > "$rs/$slug/output/sections/section-x.txt"
  echo "section-x.txt" > "$rs/$slug/output/chapters.txt"
done
mkdir -p "$rs/gamma/output/sections"   # no chapters.txt → must fail
touch "$rs/build_audio.py" "$rs/build_m4a.py" "$rs/build_transcripts.py"
mkdir -p "$rs/voices"
touch "$rs/voices/solo.wav"            # exactly one → auto-resolved --voice

# Registries
cat > "$tmp/reg.json" <<'EOF'
{"books": [{"slug": "alpha"}, {"slug": "beta"}]}
EOF
cat > "$tmp/reg-broken.json" <<'EOF'
{"books": [{"slug": "gamma"}]}
EOF

# Stub python: logs cwd + args
stub="$tmp/stub-python"
log="$tmp/calls.log"
cat > "$stub" <<EOF
#!/usr/bin/env bash
echo "\$PWD :: \$*" >> "$log"
EOF
chmod +x "$stub"

[ -x "$script" ] || { echo "FAIL script missing/not executable: $script"; exit 1; }

# --- Run against the two good books ---
: > "$log"
PYTHON="$stub" "$script" --registry "$tmp/reg.json" --repo-story "$rs" --artist "Test Artist" >/dev/null

check "6 build calls (2 books x 3 scripts)" test "$(wc -l < "$log")" = 6
check "alpha build_audio ran in alpha dir"  grep -q "^$rs/alpha :: ../build_audio.py" "$log"
check "alpha title flag"                    grep -q "build_audio.py --title alpha --artist Test Artist" "$log"
check "alpha m4a"                           grep -q "^$rs/alpha :: ../build_m4a.py --title alpha --artist Test Artist" "$log"
check "alpha transcripts slug"              grep -q "^$rs/alpha :: ../build_transcripts.py --slug alpha" "$log"
check "beta covered too"                    grep -q "^$rs/beta :: ../build_audio.py" "$log"
check "registry order (alpha before beta)"  bash -c "head -1 '$log' | grep -q alpha"
check "voice auto-resolved from rs/voices"  grep -q -- "--voice $rs/voices/solo.wav" "$log"

# --- Dry run: prints plan, invokes nothing ---
: > "$log"
out="$(PYTHON="$stub" "$script" --registry "$tmp/reg.json" --repo-story "$rs" --dry-run)"
check "dry-run invokes nothing"        test ! -s "$log"
check "dry-run prints plan"            bash -c "echo \"\$1\" | grep -q 'build_audio.py --title alpha'" _ "$out"

# --- Missing chapters.txt fails loudly ---
check "missing chapters.txt → nonzero, names book" bash -c "
  set +e
  out=\$(PYTHON='$stub' '$script' --registry '$tmp/reg-broken.json' --repo-story '$rs' 2>&1)
  status=\$?
  [ \$status -ne 0 ] && echo \"\$out\" | grep -q gamma"

# --- VOICE env passes through ---
: > "$log"
PYTHON="$stub" VOICE="$tmp/v.wav" "$script" --registry "$tmp/reg.json" --repo-story "$rs" >/dev/null
check "VOICE forwarded to build_audio" grep -q -- "--voice $tmp/v.wav" "$log"

# --- Full regen on text change: stale audio wiped, keyed by content hash ---
aout="$rs/alpha/output"
mkdir -p "$aout/audio/chunks" "$aout/m4a" "$aout/site"
touch "$aout/audio/chunks/ch00_chunk_00000.wav" "$aout/audio/chapter-00-x.wav" \
      "$aout/m4a/chapter_0000.m4a" "$aout/book.m4b" "$aout/site/transcripts.json"
rm -f "$aout/.text-hash"   # no hash recorded → treat as changed → wipe
PYTHON="$stub" "$script" --registry "$tmp/reg.json" --repo-story "$rs" >/dev/null
check "no recorded hash → chunks wiped"      test ! -e "$aout/audio/chunks/ch00_chunk_00000.wav"
check "no recorded hash → chapter wav wiped" test ! -e "$aout/audio/chapter-00-x.wav"
check "no recorded hash → m4a wiped"         test ! -e "$aout/m4a/chapter_0000.m4a"
check "no recorded hash → m4b wiped"         test ! -e "$aout/book.m4b"
check "hash recorded after run"              test -s "$aout/.text-hash"

# Same text again → cache preserved (resume for interrupted runs)
mkdir -p "$aout/audio/chunks"
touch "$aout/audio/chunks/ch00_chunk_00000.wav"
PYTHON="$stub" "$script" --registry "$tmp/reg.json" --repo-story "$rs" >/dev/null
check "unchanged text → chunks preserved" test -e "$aout/audio/chunks/ch00_chunk_00000.wav"

# Text edited → wiped again
echo "revised text" > "$rs/alpha/output/sections/section-x.txt"
PYTHON="$stub" "$script" --registry "$tmp/reg.json" --repo-story "$rs" >/dev/null
check "changed text → chunks wiped" test ! -e "$aout/audio/chunks/ch00_chunk_00000.wav"

if [ "$fails" -eq 0 ]; then echo "ALL TESTS PASSED"; else echo "TESTS FAILED: $fails"; exit 1; fi
