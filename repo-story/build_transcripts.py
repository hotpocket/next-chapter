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


def align_chunks(text: str, chunks_dir: Path, chapter_idx: int, variant: str) -> list[dict]:
    """Time-align a text's chunks against their WAVs. variant: 'chunk' (full) or 'summary'."""
    chunks = split_into_chunks(text)
    records = []
    offset = 0.0
    for i, chunk_text in enumerate(chunks):
        wav_path = chunks_dir / f"ch{chapter_idx:02d}_{variant}_{i:05d}.wav"
        if not wav_path.exists():
            print(f"Warning: missing {wav_path}, truncating chapter {chapter_idx} ({variant})")
            break
        duration = get_wav_duration(wav_path)
        records.append({
            "index": i,
            "text": chunk_text,
            "start": round(offset, 3),
            "end": round(offset + duration, 3),
        })
        offset += duration
    return records


def build_transcript(sections_dir: Path, chunks_dir: Path, book_slug: str,
                     summaries_dir: Path | None = None) -> dict:
    """Build transcript data for a single book from section text + chunk WAVs."""
    sections = find_sections(sections_dir)
    chapters = []

    for chapter_idx, section_path in enumerate(sections, 1):
        title = section_title(section_path)
        chunk_records = align_chunks(section_path.read_text(), chunks_dir, chapter_idx, "chunk")

        chapter = {
            "index": chapter_idx,
            "title": title,
            "chunks": chunk_records,
        }

        summary_path = summaries_dir / section_path.name if summaries_dir else None
        if summary_path and summary_path.exists():
            summary_records = align_chunks(summary_path.read_text(), chunks_dir, chapter_idx, "summary")
            if summary_records:
                chapter["summary_chunks"] = summary_records

        chapters.append(chapter)
        end = chunk_records[-1]["end"] if chunk_records else 0.0
        note = f" + {len(chapter['summary_chunks'])} summary" if "summary_chunks" in chapter else ""
        print(f"  Chapter {chapter_idx}: {title} — {len(chunk_records)} chunks{note}, {end:.1f}s")

    return {"books": [{"slug": book_slug, "chapters": chapters}]}


def main():
    parser = argparse.ArgumentParser(description="Generate transcript JSON from chunk WAVs")
    parser.add_argument("--sections-dir", default="output/sections", help="Directory containing section-*.txt files")
    parser.add_argument("--chunks-dir", default="output/audio/chunks", help="Directory containing chunk WAV files")
    parser.add_argument("--summaries-dir", default="output/summaries", help="Directory containing per-chapter summary text (optional)")
    parser.add_argument("--output", default="output/site/transcripts.json", help="Output transcript JSON path")
    parser.add_argument("--slug", default="book", help="Book slug identifier")
    args = parser.parse_args()

    sections_dir = Path(args.sections_dir)
    chunks_dir = Path(args.chunks_dir)
    summaries_dir = Path(args.summaries_dir)
    output_path = Path(args.output)

    if not sections_dir.exists():
        print(f"Sections directory not found: {sections_dir}")
        sys.exit(1)
    if not chunks_dir.exists():
        print(f"Chunks directory not found: {chunks_dir}")
        sys.exit(1)

    print("Building transcripts...")
    transcript = build_transcript(sections_dir, chunks_dir, args.slug,
                                  summaries_dir if summaries_dir.exists() else None)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(transcript, indent=2))

    total_chunks = sum(len(ch["chunks"]) for ch in transcript["books"][0]["chapters"])
    print(f"\nWrote {output_path} ({total_chunks} chunks across {len(transcript['books'][0]['chapters'])} chapters)")


if __name__ == "__main__":
    main()
