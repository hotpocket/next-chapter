#!/usr/bin/env bash
# test_build_book.sh — tests for scripts/build_book.sh staging + preflight.
# No GPU/TTS needed: everything runs through --stage-only except arg validation.
set -u

export REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BB="$REPO_ROOT/scripts/build_book.sh"
PASS=0 FAIL=0
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

ok()   { PASS=$((PASS+1)); echo "  ok: $*"; }
fail() { FAIL=$((FAIL+1)); echo "FAIL: $*"; }

assert_file()   { if [[ -f $1 ]]; then ok "exists: ${1#"$TMP"/}"; else fail "missing: ${1#"$TMP"/}"; fi; }
assert_absent() { if [[ ! -e $1 ]]; then ok "absent: ${1#"$TMP"/}"; else fail "should be absent: ${1#"$TMP"/}"; fi; }
assert_eq()     { if [[ $1 == "$2" ]]; then ok "$3"; else fail "$3 — expected [$2] got [$1]"; fi; }

# --- 1: no args exits nonzero with usage
if "$BB" >/dev/null 2>&1; then fail "no args should exit nonzero"; else ok "no args rejected"; fi

# --- 2: nonexistent chapters dir
if "$BB" "$TMP/nope" --stage-only >/dev/null 2>&1; then fail "missing dir should exit nonzero"; else ok "missing dir rejected"; fi

# --- 3: dir with no .txt/.md files
mkdir "$TMP/empty"
if "$BB" "$TMP/empty" --stage-only >/dev/null 2>&1; then fail "empty dir should exit nonzero"; else ok "empty dir rejected"; fi

# --- 4: happy path — default out inside book folder, sorted order, NN- prefix
#        stripped, .md -> .txt, content copied
SRC="$TMP/test-book"; OUT="$SRC/build"
mkdir "$SRC"
printf 'First chapter text.\n'  > "$SRC/01-first.txt"
printf 'Second chapter text.\n' > "$SRC/02-second.txt"
printf 'Tenth chapter text.\n'  > "$SRC/10-tenth.md"
if "$BB" "$SRC" --stage-only >/dev/null 2>&1; then ok "stage-only ran"; else fail "stage-only failed"; fi
assert_file "$OUT/sections/first.txt"
assert_file "$OUT/sections/second.txt"
assert_file "$OUT/sections/tenth.txt"
assert_eq "$(cat "$OUT/chapters.txt" 2>/dev/null)" $'first.txt\nsecond.txt\ntenth.txt' "chapters.txt in sorted source order"
assert_eq "$(cat "$OUT/sections/first.txt")" "First chapter text." "content copied verbatim"

# --- 5: changed chapter text invalidates only that chapter's chunk cache
CHUNKS="$OUT/audio/chunks"
mkdir -p "$CHUNKS"
touch "$CHUNKS/ch01_chunk_00000.wav" "$CHUNKS/ch02_chunk_00000.wav" "$CHUNKS/ch03_chunk_00000.wav"
printf 'Second chapter text, revised.\n' > "$SRC/02-second.txt"
"$BB" "$SRC" --stage-only >/dev/null 2>&1
assert_file   "$CHUNKS/ch01_chunk_00000.wav"
assert_absent "$CHUNKS/ch02_chunk_00000.wav"
assert_file   "$CHUNKS/ch03_chunk_00000.wav"
assert_eq "$(cat "$OUT/sections/second.txt")" "Second chapter text, revised." "revised content staged"

# --- 6: chapter list change (indices shift) clears the whole chunk cache
touch "$CHUNKS/ch01_chunk_00000.wav" "$CHUNKS/ch02_chunk_00000.wav" "$CHUNKS/ch03_chunk_00000.wav"
printf 'Intro text.\n' > "$SRC/00-intro.txt"
"$BB" "$SRC" --stage-only >/dev/null 2>&1
assert_absent "$CHUNKS/ch01_chunk_00000.wav"
assert_absent "$CHUNKS/ch02_chunk_00000.wav"
assert_absent "$CHUNKS/ch03_chunk_00000.wav"
assert_eq "$(cat "$OUT/chapters.txt")" $'intro.txt\nfirst.txt\nsecond.txt\ntenth.txt' "new chapter ordered in"

# --- 7: prefix-strip collision falls back to original names for ALL chapters
SRC2="$TMP/collide"; OUT2="$TMP/out2"
mkdir "$SRC2"
printf 'a\n' > "$SRC2/01-intro.txt"
printf 'b\n' > "$SRC2/02-intro.txt"
"$BB" "$SRC2" --stage-only --out "$OUT2" >/dev/null 2>&1
assert_eq "$(cat "$OUT2/chapters.txt" 2>/dev/null)" $'01-intro.txt\n02-intro.txt' "collision keeps original filenames"

# --- 8: --init creates the book skeleton
if "$BB" --init "$TMP/init-book" >/dev/null 2>&1 && [[ -d $TMP/init-book/chapters ]]; then
  ok "--init created book/chapters/"
else
  fail "--init should create $TMP/init-book/chapters/"
fi

# --- 9: book folder with chapters/ subdir — stages from it, builds to <book>/build
SRC3="$TMP/book3"; mkdir -p "$SRC3/chapters"
printf 'One.\n' > "$SRC3/chapters/01-one.txt"
"$BB" "$SRC3" --stage-only >/dev/null 2>&1
assert_file "$SRC3/build/sections/one.txt"
assert_eq "$(cat "$SRC3/build/chapters.txt" 2>/dev/null)" "one.txt" "chapters.txt from chapters/ subdir"

# --- 10: passing the chapters/ path directly resolves to the same book build dir
rm -rf "$SRC3/build"
"$BB" "$SRC3/chapters" --stage-only >/dev/null 2>&1
assert_file "$SRC3/build/sections/one.txt"

# PATH stubs so full-build tests never touch a real python env, GPU, or network
STUB_OK="$TMP/stub-ok"; STUB_BAD="$TMP/stub-bad"
mkdir -p "$STUB_OK" "$STUB_BAD"
printf '#!/bin/sh\nexit 0\n' > "$STUB_OK/python";  chmod +x "$STUB_OK/python"
printf '#!/bin/sh\nexit 1\n' > "$STUB_BAD/python"; chmod +x "$STUB_BAD/python"

# --- 11: full build auto-fetches the player via luinst; a failed fetch stops
#         the build before any TTS (LUINST stub keeps this offline)
if [[ -d $REPO_ROOT/player ]]; then
  echo "  skip: player/ present, not testing missing-player auto-fetch"
else
  ERR="$(PATH="$STUB_OK:$PATH" LUINST=/bin/false "$BB" "$SRC" --out "$TMP/out8" 2>&1)"; RC=$?
  if [[ $RC -ne 0 ]] && grep -q 'fetch failed' <<<"$ERR"; then ok "failed player fetch stops the build"; else fail "expected fetch-failed stop, rc=$RC: $ERR"; fi
fi

# --- 12: broken python env stops the build with the remedy, before fetch/TTS
ERR="$(PATH="$STUB_BAD:$PATH" LUINST=/bin/false "$BB" "$SRC" --out "$TMP/out12" 2>&1)"; RC=$?
if [[ $RC -ne 0 ]] && grep -q 'chatterbook' <<<"$ERR"; then ok "env preflight fails with chatterbook remedy"; else fail "expected chatterbook env error, rc=$RC: $ERR"; fi

# --- 13: build_site.py manifest mode — per-chapter books, audio copied,
#         transcripts inlined as data: URI (standalone file:// site)
M4A="$TMP/m4a"; mkdir -p "$M4A"
printf 'fake-m4a-bytes' > "$M4A/chapter_0001.m4a"
cat > "$M4A/chapters_manifest.json" <<'EOF'
{"version":"deadbeef",
 "book":{"title":"Test Book","artist":"Tester","total_duration_s":10.0,"chapter_count":1},
 "chapters":[{"n":1,"title":"Chapter 1: One","filename":"chapter_0001.m4a","duration_s":10.0,"size_bytes":15}]}
EOF
printf '{"books":[{"slug":"test-book","chapters":[]}]}' > "$TMP/tr.json"
mkdir -p "$TMP/site13/audio"
printf 'stale' > "$TMP/site13/audio/old-book.m4b"
python3 "$REPO_ROOT/build_site.py" --manifest "$M4A/chapters_manifest.json" --slug test-book \
  --output-dir "$TMP/site13" --transcripts-file "$TMP/tr.json" >/dev/null 2>&1
assert_file "$TMP/site13/audio/chapter_0001.m4a"
assert_absent "$TMP/site13/audio/old-book.m4b"
if grep -q 'data:application/json;base64' "$TMP/site13/index.html" 2>/dev/null; then ok "transcripts inlined as data URI"; else fail "transcripts not inlined"; fi
if grep -q 'chapter_0001.m4a' "$TMP/site13/index.html" 2>/dev/null; then ok "per-chapter book json in page"; else fail "chapter filename missing from books json"; fi
if grep -q '"slug": "test-book"' "$TMP/site13/index.html" 2>/dev/null; then ok "book slug matches transcripts"; else fail "book slug missing"; fi
# player contract: chapter ids are 0-based (it does id+1 for transcript lookup
# and indexes DOM arrays by id); manifest n is 1-based
if grep -q '"id": 0' "$TMP/site13/index.html" 2>/dev/null; then ok "chapter ids 0-based"; else fail "chapter id should be n-1 (0-based)"; fi

# --- 14: summaries/ staged alongside chapters (same NN- strip, .md -> .txt)
SRC4="$TMP/book4"; mkdir -p "$SRC4/chapters" "$SRC4/summaries"
printf 'Full one.\n' > "$SRC4/chapters/01-one.txt"
printf 'Full two.\n' > "$SRC4/chapters/02-two.txt"
printf 'Short one.\n' > "$SRC4/summaries/01-one.txt"
"$BB" "$SRC4" --stage-only >/dev/null 2>&1
assert_file "$SRC4/build/summaries/one.txt"
assert_absent "$SRC4/build/summaries/two.txt"
assert_eq "$(cat "$SRC4/build/summaries/one.txt" 2>/dev/null)" "Short one." "summary content staged verbatim"

# --- 15: changed summary text clears only that chapter's summary chunks
CH4="$SRC4/build/audio/chunks"; mkdir -p "$CH4"
touch "$CH4/ch01_chunk_00000.wav" "$CH4/ch01_summary_00000.wav" "$CH4/ch02_chunk_00000.wav"
printf 'Short one, revised.\n' > "$SRC4/summaries/01-one.txt"
"$BB" "$SRC4" --stage-only >/dev/null 2>&1
assert_file   "$CH4/ch01_chunk_00000.wav"
assert_absent "$CH4/ch01_summary_00000.wav"
assert_file   "$CH4/ch02_chunk_00000.wav"

# --- 16: chapter-list change clears summary chunks along with full chunks
touch "$CH4/ch01_summary_00000.wav"
printf 'Zero.\n' > "$SRC4/chapters/00-zero.txt"
"$BB" "$SRC4" --stage-only >/dev/null 2>&1
assert_absent "$CH4/ch01_chunk_00000.wav"
assert_absent "$CH4/ch01_summary_00000.wav"

# --- 17: build_site passes manifest summary through to the page and copies
#         summary M4As (and keeps them out of the stale sweep)
M4A2="$TMP/m4a2"; mkdir -p "$M4A2"
printf 'fake-m4a' > "$M4A2/chapter_0001.m4a"
printf 'fake-sum' > "$M4A2/chapter_0001.summary.m4a"
cat > "$M4A2/chapters_manifest.json" <<'EOF'
{"version":"deadbeef",
 "book":{"title":"Sum Book","artist":"Tester","total_duration_s":10.0,"chapter_count":1},
 "chapters":[{"n":1,"title":"Chapter 1: One","filename":"chapter_0001.m4a","duration_s":10.0,"size_bytes":8,
              "summary":{"filename":"chapter_0001.summary.m4a","duration_s":2.0,"size_bytes":8}}]}
EOF
printf '{"books":[{"slug":"sum-book","chapters":[]}]}' > "$TMP/tr2.json"
python3 "$REPO_ROOT/build_site.py" --manifest "$M4A2/chapters_manifest.json" --slug sum-book \
  --output-dir "$TMP/site17" --transcripts-file "$TMP/tr2.json" >/dev/null 2>&1
assert_file "$TMP/site17/audio/chapter_0001.summary.m4a"
if grep -q '"summary"' "$TMP/site17/index.html" 2>/dev/null && \
   grep -q 'chapter_0001.summary.m4a' "$TMP/site17/index.html" 2>/dev/null; then
  ok "summary track in page books json"
else
  fail "summary track missing from books json"
fi
# re-run: summary file must survive the stale sweep
python3 "$REPO_ROOT/build_site.py" --manifest "$M4A2/chapters_manifest.json" --slug sum-book \
  --output-dir "$TMP/site17" --transcripts-file "$TMP/tr2.json" >/dev/null 2>&1
assert_file "$TMP/site17/audio/chapter_0001.summary.m4a"

# --- 18: build_transcripts emits summary_chunks from ch*_summary_* WAVs
TR="$TMP/tr-run"; mkdir -p "$TR/sections" "$TR/summaries" "$TR/chunks"
printf 'One sentence.\n' > "$TR/sections/one.txt"
printf 'one.txt\n' > "$TR/chapters.txt"
printf 'Summary sentence.\n' > "$TR/summaries/one.txt"
# Chunk WAVs are content-addressed, so the fixture derives its filenames the
# same way the renderer does, and ships the cache-params sidecar the renderer
# writes — build_transcripts.py reads the voice/params back from it to
# recompute the names.
printf '{"voice": "t.wav", "params": {"sr": 24000, "exaggeration": null, "cfg_weight": null}}\n' \
  > "$TR/chunks/cache-params.json"
eval "$(python3 - "$TR" <<'PY'
import sys
sys.path.insert(0, __import__("os").environ["REPO_ROOT"])
from build_audio import chunk_filename, chunk_key, split_into_chunks
p = {"sr": 24000, "exaggeration": None, "cfg_weight": None}
full = split_into_chunks(open(f"{sys.argv[1]}/sections/one.txt").read())[0]
summ = split_into_chunks(open(f"{sys.argv[1]}/summaries/one.txt").read())[0]
print(f"FULL_WAV={chunk_filename(1, 'chunk', chunk_key(full, 't.wav', p))}")
print(f"SUMM_WAV={chunk_filename(1, 'summary', chunk_key(summ, 't.wav', p))}")
PY
)"
ffmpeg -y -f lavfi -i anullsrc=r=24000:cl=mono -t 0.3 "$TR/chunks/$FULL_WAV" -loglevel error
ffmpeg -y -f lavfi -i anullsrc=r=24000:cl=mono -t 0.3 "$TR/chunks/$SUMM_WAV" -loglevel error
python3 "$REPO_ROOT/build_transcripts.py" --sections-dir "$TR/sections" --chunks-dir "$TR/chunks" \
  --summaries-dir "$TR/summaries" --output "$TR/transcripts.json" --slug t >/dev/null 2>&1
if python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
ch=d["books"][0]["chapters"][0]
sc=ch.get("summary_chunks")
assert sc and sc[0]["text"]=="Summary sentence." and sc[0]["end"]>0, sc
' "$TR/transcripts.json" 2>/dev/null; then ok "summary_chunks in transcripts.json"; else fail "summary_chunks missing/wrong"; fi

echo
echo "$PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
