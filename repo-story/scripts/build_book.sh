#!/usr/bin/env bash
# build_book.sh — chapter text files → standalone audiobook player site
#
# Usage:
#   scripts/build_book.sh --init <name>   new book skeleton under output/books/
#   scripts/build_book.sh <book_dir>      build it: chapters/*.txt → build/site/
#
# Options:
#   --title T       book title (default: from folder name)
#   --artist A      artist tag
#   --voice V.wav   voice sample (default: sole wav in voices/)
#   --out DIR       output root (default: <book_dir>/build/)
#   --stage-only    stage sections only — no TTS, no site
set -euo pipefail

# <book_dir> may contain chapter files directly or a chapters/ subfolder
# (--init layout: output/books/<name>/{chapters/, build/}); passing the
# chapters/ path itself also works. Chapter order = lexical filename sort.
# A summaries/ folder beside chapters/ holds optional per-chapter condensed
# text (same filenames); staged summaries become the player's Summary track.
# Pipeline: stage sections/ + summaries/ + chapters.txt → build_audio.py
# (chapter + summary WAVs + M4B) → build_m4a.py (per-chapter M4As + manifest,
# the format the player consumes) → build_transcripts.py → build_site.py
# --manifest with transcripts inlined as a data: URI, so site/ works from
# file:// with no server. Prints (never runs) the zip command.
#
# Chunk WAVs are content-addressed by build_audio.py (chNN_<variant>_<sha12>,
# hashed over the chunk text + voice + TTS params), so edited text misses the
# cache on its own. This script still clears a changed chapter's chunks, and
# the whole cache on any chapter-list change — belt-and-braces left from the
# index-keyed era, and now a needless re-render: it throws away chunks the
# hash would have reused. Its suite pins the clearing, so dropping it is a
# code+test change, not a comment fix.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Help text is the header comment above (single source of truth); usage()
# extracts it and colorizes headings, flags, and <placeholders> when stderr
# is a tty (respects NO_COLOR).
usage() {
  local B="" C="" Y="" R=""
  if [[ -t 2 && -z ${NO_COLOR:-} ]]; then
    B=$'\e[1m' C=$'\e[36m' Y=$'\e[33m' R=$'\e[0m'
  fi
  awk 'NR > 1 { if (!/^#/) exit; sub(/^# ?/, ""); print }' "${BASH_SOURCE[0]}" \
    | sed -E \
        -e "s/^(build_book\.sh)/${B}\1${R}/" \
        -e "s/^(Usage:|Options:)/${B}\1${R}/" \
        -e "s/--[a-z-]+/${C}&${R}/g" \
        -e "s/<[a-zA-Z_.-]+>/${Y}&${R}/g" >&2
  exit 2
}

CHAPTERS_DIR="" TITLE="" ARTIST="" VOICE="" OUT="" STAGE_ONLY=0 INIT=0
while [[ $# -gt 0 ]]; do
  case $1 in
    --title)  TITLE=$2;  shift 2 ;;
    --artist) ARTIST=$2; shift 2 ;;
    --voice)  VOICE=$2;  shift 2 ;;
    --out)    OUT=$2;    shift 2 ;;
    --stage-only) STAGE_ONLY=1; shift ;;
    --init)   INIT=1; shift ;;
    -h|--help) usage ;;
    -*) echo "Unknown option: $1" >&2; usage ;;
    *)  if [[ -n $CHAPTERS_DIR ]]; then usage; fi; CHAPTERS_DIR=$1; shift ;;
  esac
done
if [[ -z $CHAPTERS_DIR ]]; then usage; fi

if [[ $INIT -eq 1 ]]; then
  if [[ $CHAPTERS_DIR == */* ]]; then BOOK="$CHAPTERS_DIR"; else BOOK="$REPO_ROOT/output/books/$CHAPTERS_DIR"; fi
  mkdir -p "$BOOK/chapters"
  echo "Initialized book skeleton:"
  echo "  $BOOK/chapters/   <- drop chapter files here (01-intro.txt, 02-...)"
  echo "Then build:"
  echo "  scripts/build_book.sh $BOOK"
  exit 0
fi

if [[ ! -d $CHAPTERS_DIR ]]; then echo "Chapters dir not found: $CHAPTERS_DIR" >&2; exit 1; fi

# Resolve book folder vs chapters folder: accept either.
if [[ -d $CHAPTERS_DIR/chapters ]]; then
  BOOK_DIR="$CHAPTERS_DIR"
  CHAPTERS_DIR="$CHAPTERS_DIR/chapters"
elif [[ $(basename "$CHAPTERS_DIR") == chapters ]]; then
  BOOK_DIR="$(dirname "$CHAPTERS_DIR")"
else
  BOOK_DIR="$CHAPTERS_DIR"
fi

mapfile -t SRC_FILES < <(find "$CHAPTERS_DIR" -maxdepth 1 -type f \( -name '*.txt' -o -name '*.md' \) -printf '%f\n' | LC_ALL=C sort)
if [[ ${#SRC_FILES[@]} -eq 0 ]]; then echo "No .txt/.md chapter files in $CHAPTERS_DIR" >&2; exit 1; fi

BOOK_BASE="$(basename "$(realpath "$BOOK_DIR")")"
SLUG="$(echo "$BOOK_BASE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
if [[ -z $TITLE ]]; then TITLE="$(echo "$BOOK_BASE" | sed -E 's/[-_]+/ /g; s/\b(.)/\u\1/g')"; fi
OUT="$(realpath -m "${OUT:-$BOOK_DIR/build}")"

# Preflights before any expensive work.
# 1. Python env: the pyenv pin (.python-version → chatterbox) is untracked
#    and machine-specific, so check it structurally and say how to fix it.
if [[ $STAGE_ONLY -eq 0 ]] && ! python -c 'import chatterbook' >/dev/null 2>&1; then
  echo "Python env not ready: 'import chatterbook' failed." >&2
  echo "  This machine: pyenv local chatterbox" >&2
  echo "  Elsewhere: python3.10+ env with chatterbox-tts + chatterbook (pip install -e ~/git/chatterbook)" >&2
  exit 1
fi
# 2. Player component: the site is unusable without it, so fetch it when
#    missing (LUINST env overrides, for tests).
if [[ $STAGE_ONLY -eq 0 && ! -f $REPO_ROOT/player/player.js ]]; then
  echo "player/ missing — fetching it: ./luinst audiobook/vanilla player/"
  if ! "${LUINST:-$REPO_ROOT/luinst}" audiobook/vanilla "$REPO_ROOT/player/"; then
    echo "luinst fetch failed — check network/SSH, or run it manually:" >&2
    echo "  cd $REPO_ROOT && ./luinst audiobook/vanilla player/" >&2
    exit 1
  fi
fi

SECTIONS="$OUT/sections"
CHUNKS="$OUT/audio/chunks"
mkdir -p "$SECTIONS"

# Staged name: strip a leading NN- ordering prefix (order lives in
# chapters.txt; section_title() derives chapter titles from these names),
# normalize extension to .txt. If stripping collides, keep every original name.
STAGED=()
COLLIDE=0
declare -A SEEN=()
for f in "${SRC_FILES[@]}"; do
  stem="${f%.*}"
  s="$(sed -E 's/^[0-9]+[-_. ]*//' <<<"$stem")"
  if [[ -z $s ]]; then s=$stem; fi
  if [[ -n ${SEEN[$s]:-} ]]; then COLLIDE=1; fi
  SEEN[$s]=1
  STAGED+=("$s.txt")
done
if [[ $COLLIDE -eq 1 ]]; then
  STAGED=()
  for f in "${SRC_FILES[@]}"; do STAGED+=("${f%.*}.txt"); done
  if [[ $(printf '%s\n' "${STAGED[@]}" | sort -u | wc -l) -ne ${#STAGED[@]} ]]; then
    echo "Chapter filenames collide after staging (.md/.txt same stem?) — rename them" >&2
    exit 1
  fi
fi

NEW_LIST="$(printf '%s\n' "${STAGED[@]}")"
OLD_LIST="$(cat "$OUT/chapters.txt" 2>/dev/null || true)"
if [[ -n $OLD_LIST && $OLD_LIST != "$NEW_LIST" && -d $CHUNKS ]]; then
  echo "Chapter list changed — clearing whole chunk cache (chapter indices shifted)"
  rm -f "$CHUNKS"/ch*_chunk_*.wav "$CHUNKS"/ch*_summary_*.wav
fi

for i in "${!SRC_FILES[@]}"; do
  src="$CHAPTERS_DIR/${SRC_FILES[$i]}"
  dst="$SECTIONS/${STAGED[$i]}"
  idx="$(printf 'ch%02d' $((i + 1)))"
  if [[ -f $dst ]] && ! cmp -s "$src" "$dst"; then
    if compgen -G "$CHUNKS/${idx}_chunk_*.wav" >/dev/null; then
      echo "Chapter $((i + 1)) (${STAGED[$i]}) text changed — clearing its cached chunks"
      rm -f "$CHUNKS/${idx}"_chunk_*.wav
    fi
  fi
done
# Stale staged sections from a renamed/removed chapter would confuse nobody
# (chapters.txt is authoritative) but clean them anyway.
for existing in "$SECTIONS"/*.txt; do
  [[ -e $existing ]] || continue
  if ! grep -qxF "$(basename "$existing")" <<<"$NEW_LIST"; then rm -f "$existing"; fi
done
for i in "${!SRC_FILES[@]}"; do
  cp "$CHAPTERS_DIR/${SRC_FILES[$i]}" "$SECTIONS/${STAGED[$i]}"
done
printf '%s\n' "${STAGED[@]}" > "$OUT/chapters.txt"

# Stage summaries/ (optional): same source names as chapters, same staged
# names as sections — a chapter's summary is summaries/<staged-section-name>.
# Change detection mirrors sections: changed text clears that chapter's
# summary chunks; stale/orphan staged summaries are removed.
SUMMARIES_SRC="$BOOK_DIR/summaries"
SUMMARIES="$OUT/summaries"
mkdir -p "$SUMMARIES"
STAGED_SUMS=0
for i in "${!SRC_FILES[@]}"; do
  ssrc=""
  for cand in "$SUMMARIES_SRC/${SRC_FILES[$i]}" "$SUMMARIES_SRC/${SRC_FILES[$i]%.*}.txt" "$SUMMARIES_SRC/${SRC_FILES[$i]%.*}.md"; do
    if [[ -f $cand ]]; then ssrc=$cand; break; fi
  done
  sdst="$SUMMARIES/${STAGED[$i]}"
  idx="$(printf 'ch%02d' $((i + 1)))"
  if [[ -z $ssrc ]]; then
    if [[ -f $sdst ]]; then rm -f "$sdst" "$CHUNKS/${idx}"_summary_*.wav; fi
    continue
  fi
  if [[ -f $sdst ]] && ! cmp -s "$ssrc" "$sdst"; then
    if compgen -G "$CHUNKS/${idx}_summary_*.wav" >/dev/null; then
      echo "Chapter $((i + 1)) (${STAGED[$i]}) summary changed — clearing its cached summary chunks"
      rm -f "$CHUNKS/${idx}"_summary_*.wav
    fi
  fi
  cp "$ssrc" "$sdst"
  STAGED_SUMS=$((STAGED_SUMS + 1))
done
if [[ $STAGED_SUMS -gt 0 ]]; then echo "Staged $STAGED_SUMS summaries → $SUMMARIES"; fi

echo "Staged ${#SRC_FILES[@]} chapters → $SECTIONS"
if [[ $STAGE_ONLY -eq 1 ]]; then exit 0; fi

M4B="$OUT/$SLUG.m4b"
AUDIO_ARGS=(--sections-dir "$SECTIONS" --chunks-dir "$CHUNKS" --output "$M4B"
            --summaries-dir "$SUMMARIES"
            --title "$TITLE" --date "$(date +%F)")
if [[ -n $ARTIST ]]; then AUDIO_ARGS+=(--artist "$ARTIST"); fi
if [[ -n $VOICE ]];  then AUDIO_ARGS+=(--voice "$VOICE"); fi

# cwd = repo root: build_audio's voices/ auto-detect and build_site's player/
# lookup are both repo-relative. Herestring answers the overwrite prompt on
# re-runs (chunks are cached; re-assembly is cheap).
cd "$REPO_ROOT"
python build_audio.py "${AUDIO_ARGS[@]}" <<<'y'

M4A_ARGS=(--title "$TITLE" --audio-dir "$OUT/audio" --sections-dir "$SECTIONS" --m4a-dir "$OUT/m4a")
if [[ -n $ARTIST ]]; then M4A_ARGS+=(--artist "$ARTIST"); fi
python build_m4a.py "${M4A_ARGS[@]}"

python build_transcripts.py --sections-dir "$SECTIONS" --chunks-dir "$CHUNKS" \
  --summaries-dir "$SUMMARIES" --output "$OUT/transcripts.json" --slug "$SLUG"
python build_site.py --manifest "$OUT/m4a/chapters_manifest.json" --slug "$SLUG" \
  --transcripts-file "$OUT/transcripts.json" --output-dir "$OUT/site"

echo
echo "Book built: $OUT/site/ — standalone, no server needed"
echo "Test: open $OUT/site/index.html in a browser"
echo "Zip:  (cd \"$OUT\" && zip -r \"$SLUG.zip\" site)"
