#!/usr/bin/env python3
"""
build_m4a.py — Encode chapter WAVs into per-chapter M4As + chapters_manifest.json.

This is the production audio format: the landry-ui player consumes per-chapter
M4As via chapters_manifest.json. In the next-chapter vendored setup these are
published on the parent repo's GitHub Pages site. The single-file M4B from
build_audio.py remains available as a standalone/legacy format.

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
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from chatterbook.audio import get_wav_duration
from chatterbook.manifest import write_chapters_manifest

from build_audio import find_sections, section_title


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
    titles_map = {}

    for i, (wav, section) in enumerate(zip(wavs, sections), 1):
        chapter_title = f"Chapter {i}: {section_title(section)}"
        titles_map[str(i)] = section_title(section)
        m4a = m4a_dir / f"chapter_{i:04d}.m4a"

        if m4a.exists() and m4a.stat().st_mtime > wav.stat().st_mtime:
            print(f"  Ch{i}: {chapter_title} — up to date")
        else:
            print(f"  Ch{i}: {chapter_title} — encoding...")
            encode_m4a(wav, m4a, chapter_title, args.title, args.artist, i, len(wavs))

    # Summary tracks (optional): build_audio writes summary-NN-*.wav beside
    # the chapter WAVs for chapters that have condensed text. Encode them as
    # chapter_NNNN.summary.m4a; attached to the manifest after the shared
    # writer runs (chatterbook's manifest format knows nothing of summaries).
    summaries = {}
    for i in range(1, len(wavs) + 1):
        match = sorted(audio_dir.glob(f"summary-{i:02d}-*.wav"))
        if not match:
            continue
        swav = match[0]
        sm4a = m4a_dir / f"chapter_{i:04d}.summary.m4a"
        if sm4a.exists() and sm4a.stat().st_mtime > swav.stat().st_mtime:
            print(f"  Ch{i} summary — up to date")
        else:
            print(f"  Ch{i} summary — encoding...")
            encode_m4a(swav, sm4a, f"Chapter {i} (summary): {titles_map[str(i)]}",
                       args.title, args.artist, i, len(wavs))
        summaries[i] = {
            "filename": sm4a.name,
            "duration_s": round(get_wav_duration(sm4a), 3),
            "size_bytes": sm4a.stat().st_size,
        }

    # Shared writer: sha8 content-hash version (replaces the old fixed "v1"),
    # duration cache keyed by (filename, size), atomic write.
    manifest_path = m4a_dir / "chapters_manifest.json"
    manifest = write_chapters_manifest(
        range(1, len(wavs) + 1), titles_map, m4a_dir, manifest_path,
        args.title, args.artist,
    )

    if summaries:
        for ch in manifest["chapters"]:
            if ch["n"] in summaries:
                ch["summary"] = summaries[ch["n"]]
        # Fold summary tuples into the version so summary-only changes still
        # bust caches (the shared writer hashes full tracks only).
        hasher = hashlib.sha256(manifest["version"].encode())
        for n in sorted(summaries):
            s = summaries[n]
            hasher.update(f"{s['filename']}:{s['size_bytes']}:{s['duration_s']}".encode())
        manifest["version"] = hasher.hexdigest()[:8]
        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"  Attached {len(summaries)} summary track(s) to the manifest")

    print(f"\nWrote {manifest_path}")
    print(f"  {len(manifest['chapters'])} chapters, "
          f"{manifest['book']['total_duration_s']/60:.1f} minutes")
    print("\nNext: build_transcripts.py, then register this book in [family-site-deploy]/books.json")


if __name__ == "__main__":
    main()
