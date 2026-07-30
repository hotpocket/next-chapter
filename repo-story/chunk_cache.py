#!/usr/bin/env python3
"""chunk_cache.py — maintenance for the content-addressed chunk cache.

    chunk_cache.py migrate --sections-dir D --chunks-dir D [--summaries-dir D] [--voice V]
    chunk_cache.py gc      --sections-dir D --chunks-dir D [--summaries-dir D] [--voice V]

migrate: rename a legacy index-keyed cache (chNN_<variant>_00007.wav) to content
addressing (chNN_<variant>_<sha12>.wav). Position N in the current text produced
the WAV at index N — true only while the text has not changed since that render,
which is exactly what the caller's `.text-hash` record proves. Run it ONLY when
that hash matches; otherwise the rename would cement stale audio under a key
claiming to be the new text. Nothing is re-rendered here.

gc: delete chunk WAVs the current text no longer references. Safe to run any
time — a missing chunk is re-rendered on the next build; a stale one is not.

The sample rate for the cache key is read from the existing audio rather than
guessed, so migrated keys match what build_audio.py computes from the model.
"""

import argparse
import subprocess
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_audio import (chunk_filename, chunk_key, find_sections, referenced_chunk_names,
                         save_cache_params, split_into_chunks)


def sample_rate(chunks_dir: Path) -> int | None:
    """Sample rate of the cached audio, read rather than assumed so migrated
    keys match what build_audio.py computes from the live model.

    Python's `wave` only handles PCM; torchaudio writes float32 (format tag 3),
    so ffprobe — already a hard dependency of this pipeline — is the fallback
    that actually reads the real cache."""
    for wav in sorted(chunks_dir.glob("*.wav")):
        try:
            with wave.open(str(wav), "rb") as w:
                return w.getframerate()
        except Exception:
            pass
        try:
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "a:0",
                 "-show_entries", "stream=sample_rate", "-of", "csv=p=0", str(wav)],
                capture_output=True, text=True, check=True).stdout.strip()
            if out:
                return int(out)
        except Exception:
            continue
    return None


def texts_by_chapter(sections_dir: Path, summaries_dir: Path | None):
    """(chapter_idx, variant, text) for every renderable text, chapter order."""
    for idx, section in enumerate(find_sections(sections_dir), start=1):
        yield idx, "chunk", section.read_text()
        if summaries_dir:
            summary = summaries_dir / section.name
            if summary.exists():
                yield idx, "summary", summary.read_text()


def migrate(args) -> int:
    chunks_dir = Path(args.chunks_dir)
    sr = sample_rate(chunks_dir)
    if sr is None:
        print(f"No WAVs in {chunks_dir} — nothing to migrate.")
        return 0
    params = {"sr": sr, "exaggeration": None, "cfg_weight": None}

    renamed = missing = already = 0
    for idx, variant, text in texts_by_chapter(Path(args.sections_dir),
                                               Path(args.summaries_dir) if args.summaries_dir else None):
        for i, chunk_text in enumerate(split_into_chunks(text)):
            new = chunks_dir / chunk_filename(idx, variant, chunk_key(chunk_text, args.voice, params))
            old = chunks_dir / f"ch{idx:02d}_{variant}_{i:05d}.wav"
            if new.exists():
                already += 1
                if old.exists():
                    old.unlink()  # duplicate from a half-finished migration
            elif old.exists():
                old.rename(new)
                renamed += 1
            else:
                missing += 1

    save_cache_params(chunks_dir, args.voice, params)
    print(f"migrate: {renamed} renamed, {already} already content-addressed, "
          f"{missing} absent (will render on next build)")
    leftovers = [p.name for p in chunks_dir.glob("ch*_*.wav") if p.stem.split("_")[-1].isdigit()]
    if leftovers:
        print(f"  note: {len(leftovers)} index-named WAVs no longer referenced by the "
              "current text — run `chunk_cache.py gc` to drop them")
    return 0


def gc(args) -> int:
    chunks_dir = Path(args.chunks_dir)
    live = referenced_chunk_names(
        Path(args.sections_dir),
        Path(args.summaries_dir) if args.summaries_dir else None,
        args.voice,
        {"sr": sample_rate(chunks_dir), "exaggeration": None, "cfg_weight": None},
    )
    removed = 0
    for wav in chunks_dir.glob("*.wav"):
        if wav.name not in live:
            wav.unlink()
            removed += 1
    print(f"gc: {removed} orphaned chunk WAVs removed, {len(live)} live")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=["migrate", "gc"])
    ap.add_argument("--sections-dir", required=True)
    ap.add_argument("--summaries-dir", default=None)
    ap.add_argument("--chunks-dir", required=True)
    ap.add_argument("--voice", default="")
    args = ap.parse_args()
    return migrate(args) if args.mode == "migrate" else gc(args)


if __name__ == "__main__":
    sys.exit(main())
