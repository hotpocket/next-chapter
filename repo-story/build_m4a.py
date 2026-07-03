#!/usr/bin/env python3
"""
build_m4a.py — Encode chapter WAVs into per-chapter M4As + chapters_manifest.json.

This is the production audio format: the landry-ui player consumes per-chapter
M4As via chapters_manifest.json (registered in [family-site-deploy]/books.json for the
[family-site]/books deploy). The single-file M4B from build_audio.py remains
the format for brandonlandry.com (see scripts/generate-manifest.sh).

Reads chapter WAVs produced by build_audio.py (output/audio/chapter-NN-*.wav)
and section text/order for titles. Encodes AAC 24kHz mono 64k +faststart with
per-chapter title metadata. Resume-safe: skips M4As newer than their WAV.

Usage (from a per-repo folder, per AUTORUN.md):
    python ../build_m4a.py --title "Book Title" --artist "Author"

Then register in [family-site-deploy]/books.json:
    {
      "slug": "<repo-folder>",
      "title": "<--title>",
      "artist": "<--artist>",
      "manifest": "<abs path>/output/m4a/chapters_manifest.json",
      "transcripts_path": "<abs path>/output/site/transcripts.json",
      "audio_prefix": "<repo-folder>/"
    }
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from build_audio import find_sections, section_title


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def encode_m4a(wav: Path, m4a: Path, chapter_title: str, book_title: str,
               artist: str, track: int, total: int):
    subprocess.run([
        "ffmpeg", "-y", "-i", str(wav),
        "-c:a", "aac", "-b:a", "64k", "-ar", "24000", "-ac", "1",
        "-movflags", "+faststart",
        "-metadata", f"title={chapter_title}",
        "-metadata", f"album={book_title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"track={track}/{total}",
        str(m4a),
    ], capture_output=True, check=True)


def main():
    parser = argparse.ArgumentParser(description="Encode chapter WAVs to per-chapter M4As + manifest")
    parser.add_argument("--title", required=True, help="Book title (manifest + M4A album metadata)")
    parser.add_argument("--artist", default="", help="Book artist/author")
    parser.add_argument("--audio-dir", default="output/audio", help="Directory containing chapter-NN-*.wav")
    parser.add_argument("--sections-dir", default="output/sections", help="Directory containing section-*.txt files")
    parser.add_argument("--m4a-dir", default="output/m4a", help="Output directory for M4As + manifest")
    args = parser.parse_args()

    audio_dir = Path(args.audio_dir)
    m4a_dir = Path(args.m4a_dir)
    sections = find_sections(Path(args.sections_dir))

    wavs = sorted(audio_dir.glob("chapter-*.wav"))
    if len(wavs) != len(sections):
        print(f"Chapter WAV count {len(wavs)} != section count {len(sections)}")
        print("Run build_audio.py first; it writes one chapter-NN-*.wav per section.")
        sys.exit(1)

    m4a_dir.mkdir(parents=True, exist_ok=True)
    chapters = []
    total_duration = 0.0

    for i, (wav, section) in enumerate(zip(wavs, sections), 1):
        chapter_title = f"Chapter {i}: {section_title(section)}"
        m4a = m4a_dir / f"chapter_{i:04d}.m4a"

        if m4a.exists() and m4a.stat().st_mtime > wav.stat().st_mtime:
            print(f"  Ch{i}: {chapter_title} — up to date")
        else:
            print(f"  Ch{i}: {chapter_title} — encoding...")
            encode_m4a(wav, m4a, chapter_title, args.title, args.artist, i, len(wavs))

        dur = ffprobe_duration(m4a)
        chapters.append({
            "n": i,
            "title": chapter_title,
            "filename": m4a.name,
            "duration_s": round(dur, 3),
            "size_bytes": m4a.stat().st_size,
        })
        total_duration += dur

    manifest = {
        "version": "v1",
        "book": {
            "title": args.title,
            "artist": args.artist,
            "total_duration_s": round(total_duration, 3),
            "chapter_count": len(chapters),
        },
        "chapters": chapters,
    }
    manifest_path = m4a_dir / "chapters_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"\nWrote {manifest_path}")
    print(f"  {len(chapters)} chapters, {total_duration/60:.1f} minutes")
    print("\nNext: build_transcripts.py, then register this book in [family-site-deploy]/books.json")


if __name__ == "__main__":
    main()
