#!/usr/bin/env python3
"""
build_transcripts.py — Generate transcript JSON from existing chunk WAVs + section text.

Reads section text files, splits them into chunks using the same logic as build_audio.py,
then probes each chunk WAV for its duration to build a time-aligned transcript.

Runs in seconds on any machine with ffprobe (no GPU needed).

Usage:
    python build_transcripts.py
    python build_transcripts.py --sections-dir output/sections --chunks-dir output/audio/chunks
    python build_transcripts.py --output output/site/transcripts.json
"""

import argparse
import json
import sys
from pathlib import Path

from build_audio import find_sections, get_wav_duration, section_title, split_into_chunks


def build_transcript(sections_dir: Path, chunks_dir: Path, book_slug: str) -> dict:
    """Build transcript data for a single book from section text + chunk WAVs."""
    sections = find_sections(sections_dir)
    chapters = []

    for chapter_idx, section_path in enumerate(sections, 1):
        text = section_path.read_text()
        title = section_title(section_path)
        chunks = split_into_chunks(text)
        chunk_records = []
        offset = 0.0

        for i, chunk_text in enumerate(chunks):
            wav_path = chunks_dir / f"ch{chapter_idx:02d}_chunk_{i:05d}.wav"
            if not wav_path.exists():
                print(f"Warning: missing {wav_path}, skipping chapter {chapter_idx}")
                break
            duration = get_wav_duration(wav_path)
            chunk_records.append({
                "index": i,
                "text": chunk_text,
                "start": round(offset, 3),
                "end": round(offset + duration, 3),
            })
            offset += duration

        chapters.append({
            "index": chapter_idx,
            "title": title,
            "chunks": chunk_records,
        })
        total_chunks = len(chunk_records)
        print(f"  Chapter {chapter_idx}: {title} — {total_chunks} chunks, {offset:.1f}s")

    return {"books": [{"slug": book_slug, "chapters": chapters}]}


def main():
    parser = argparse.ArgumentParser(description="Generate transcript JSON from chunk WAVs")
    parser.add_argument("--sections-dir", default="output/sections", help="Directory containing section-*.txt files")
    parser.add_argument("--chunks-dir", default="output/audio/chunks", help="Directory containing chunk WAV files")
    parser.add_argument("--output", default="output/site/transcripts.json", help="Output transcript JSON path")
    parser.add_argument("--slug", default="book", help="Book slug identifier")
    args = parser.parse_args()

    sections_dir = Path(args.sections_dir)
    chunks_dir = Path(args.chunks_dir)
    output_path = Path(args.output)

    if not sections_dir.exists():
        print(f"Sections directory not found: {sections_dir}")
        sys.exit(1)
    if not chunks_dir.exists():
        print(f"Chunks directory not found: {chunks_dir}")
        sys.exit(1)

    print("Building transcripts...")
    transcript = build_transcript(sections_dir, chunks_dir, args.slug)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(transcript, indent=2))

    total_chunks = sum(len(ch["chunks"]) for ch in transcript["books"][0]["chapters"])
    print(f"\nWrote {output_path} ({total_chunks} chunks across {len(transcript['books'][0]['chapters'])} chapters)")


if __name__ == "__main__":
    main()
