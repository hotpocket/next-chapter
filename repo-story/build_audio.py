#!/usr/bin/env python3
"""
build_audio.py — Convert repo-story sections into a chaptered M4B audiobook.

Reads text sections from output/sections/, generates audio via Chatterbox TTS,
and assembles into a single M4B file with named chapters.

Usage:
    python build_audio.py --voice voices/my_voice.wav
    python build_audio.py --voice voices/my_voice.wav --output output/book.m4b
    python build_audio.py --voice voices/my_voice.wav --sections-dir output/sections/

Supports resume: skips chunks whose WAV files already exist.
Prints progress continuously throughout generation.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def find_sections(sections_dir: Path) -> list[Path]:
    """Find section files in chapter order from chapters.txt, or alphabetically as fallback."""
    chapters_file = sections_dir.parent / "chapters.txt"
    if chapters_file.exists():
        lines = [l.strip() for l in chapters_file.read_text().splitlines() if l.strip()]
        sections = []
        for filename in lines:
            path = sections_dir / filename
            if not path.exists():
                print(f"Chapter file not found: {path}")
                sys.exit(1)
            sections.append(path)
        if sections:
            return sections
    sections = sorted(sections_dir.glob("section-*.txt"))
    if not sections:
        print(f"No section-*.txt files found in {sections_dir}")
        sys.exit(1)
    return sections


def section_title(path: Path) -> str:
    """Extract a chapter title from a section filename."""
    stem = path.stem.removeprefix("section-")
    return stem.replace("-", " ").title()


def split_into_chunks(text: str, max_chars: int = 300) -> list[str]:
    """Split text into chunks at sentence boundaries, max_chars each."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current = ""
    for sentence in sentences:
        if current and len(current) + len(sentence) + 1 > max_chars:
            chunks.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}" if current else sentence
    if current.strip():
        chunks.append(current.strip())
    return chunks


def generate_chapter_audio(
    text: str,
    chapter_idx: int,
    chapter_title: str,
    chunks_dir: Path,
    model,
    voice_path: str,
    total_chapters: int,
) -> Path:
    """Generate audio for one chapter, chunk by chunk. Returns path to chapter WAV."""
    import torchaudio

    chunks = split_into_chunks(text)
    total_chunks = len(chunks)
    chapter_wav_path = chunks_dir.parent / f"chapter-{chapter_idx:02d}-{chapter_title.lower().replace(' ', '-')}.wav"

    # Clean up any temp files from a previously killed run
    for stale in chunks_dir.glob(f"ch{chapter_idx:02d}_chunk_*.tmp.wav"):
        stale.unlink()

    print(f"\n[Chapter {chapter_idx}/{total_chapters}] {chapter_title} — {total_chunks} chunks")

    chunk_wavs = []
    for i, chunk_text in enumerate(chunks):
        chunk_path = chunks_dir / f"ch{chapter_idx:02d}_chunk_{i:05d}.wav"
        chunk_wavs.append(chunk_path)

        if chunk_path.exists():
            print(f"  Chunk {i+1}/{total_chunks} — cached, skipping")
            continue

        t0 = time.time()
        wav = model.generate(chunk_text, audio_prompt_path=None)
        dt = time.time() - t0

        # Atomic write: temp file + rename so a kill mid-write can't leave a corrupt chunk
        tmp_path = chunk_path.with_name(chunk_path.stem + ".tmp.wav")
        torchaudio.save(str(tmp_path), wav, model.sr)
        tmp_path.rename(chunk_path)

        duration = wav.shape[-1] / model.sr
        rtf = dt / duration if duration > 0 else 0
        pct = (i + 1) / total_chunks * 100
        print(f"  Chunk {i+1}/{total_chunks} — {pct:.0f}% — {duration:.1f}s audio in {dt:.1f}s — RTF {rtf:.2f}x")
        del wav  # Free GPU memory immediately

    # Concatenate chunks into chapter WAV via ffmpeg (no memory accumulation)
    print(f"  Concatenating {total_chunks} chunks into chapter audio...")
    filelist = chunks_dir / f"ch{chapter_idx:02d}_filelist.txt"
    with open(filelist, "w") as f:
        for chunk_path in chunk_wavs:
            f.write(f"file '{chunk_path.resolve()}'\n")

    tmp_chapter = chapter_wav_path.with_name(chapter_wav_path.stem + ".tmp.wav")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(filelist), "-c", "copy", str(tmp_chapter),
    ], capture_output=True, check=True)
    tmp_chapter.rename(chapter_wav_path)
    filelist.unlink()

    chapter_duration = get_wav_duration(chapter_wav_path)
    print(f"  Chapter {chapter_idx} complete: {chapter_duration:.1f}s ({chapter_duration/60:.1f}m)")

    return chapter_wav_path


def get_wav_duration(path: Path) -> float:
    """Get duration of a WAV file in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def assemble_m4b(chapter_paths: list[Path], chapter_titles: list[str], output_path: Path):
    """Assemble chapter WAVs into a single M4B with chapter metadata."""
    print(f"\nAssembling {len(chapter_paths)} chapters into M4B...")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create file list for concatenation
        filelist = tmpdir / "files.txt"
        with open(filelist, "w") as f:
            for path in chapter_paths:
                f.write(f"file '{path.resolve()}'\n")

        # Compute chapter timestamps
        metadata = tmpdir / "metadata.txt"
        with open(metadata, "w") as f:
            f.write(";FFMETADATA1\n")
            f.write("title=Repo Story\n")
            f.write("\n")

            offset_ms = 0
            for i, (path, title) in enumerate(zip(chapter_paths, chapter_titles)):
                duration_s = get_wav_duration(path)
                duration_ms = int(duration_s * 1000)

                f.write("[CHAPTER]\n")
                f.write("TIMEBASE=1/1000\n")
                f.write(f"START={offset_ms}\n")
                f.write(f"END={offset_ms + duration_ms}\n")
                f.write(f"title={title}\n")
                f.write("\n")

                print(f"  Chapter {i+1}: {title} — {duration_s:.1f}s (starts at {offset_ms/1000:.1f}s)")
                offset_ms += duration_ms

        # Concatenate into single audio file
        concat_path = tmpdir / "concat.wav"
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(filelist), "-c", "copy", str(concat_path),
        ], capture_output=True, check=True)

        # Convert to M4B with chapter metadata
        output_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "ffmpeg", "-y",
            "-i", str(concat_path),
            "-i", str(metadata),
            "-map", "0:a", "-map_metadata", "1",
            "-c:a", "aac", "-b:a", "128k",
            str(output_path),
        ], capture_output=True, check=True)

    total_duration = offset_ms / 1000
    print(f"\nDone: {output_path}")
    print(f"Total duration: {total_duration:.0f}s ({total_duration/60:.1f}m)")
    print(f"Chapters: {len(chapter_paths)}")


def main():
    parser = argparse.ArgumentParser(description="Build chaptered audiobook from repo-story sections")
    parser.add_argument("--voice", default=None, help="Path to voice reference WAV file (default: auto-detect from voices/)")
    parser.add_argument("--sections-dir", default="output/sections", help="Directory containing section-*.txt files")
    parser.add_argument("--output", default="output/book.m4b", help="Output M4B file path")
    parser.add_argument("--chunks-dir", default="output/audio/chunks", help="Directory for intermediate chunk WAVs")
    args = parser.parse_args()

    sections_dir = Path(args.sections_dir)
    output_path = Path(args.output)
    chunks_dir = Path(args.chunks_dir)

    # Auto-detect voice file if not specified
    if args.voice:
        voice_path = args.voice
    else:
        voices_dir = Path("voices")
        wavs = list(voices_dir.glob("*.wav")) if voices_dir.exists() else []
        if len(wavs) == 1:
            voice_path = str(wavs[0])
        elif len(wavs) > 1:
            print(f"Multiple voice files in voices/: {[w.name for w in wavs]}")
            print("Specify one with --voice")
            sys.exit(1)
        else:
            print("No voice file found. Place a .wav in voices/ or use --voice")
            sys.exit(1)

    if not Path(voice_path).exists():
        print(f"Voice file not found: {voice_path}")
        sys.exit(1)

    if output_path.exists():
        print(f"\n{output_path} already exists.")
        response = input("Overwrite? [y/N] or enter a new filename: ").strip()
        if response.lower() == 'y':
            pass
        elif response.lower() in ('', 'n'):
            print("Aborted.")
            sys.exit(0)
        else:
            output_path = Path(response) if response.endswith('.m4b') else Path(response + '.m4b')
            print(f"Output: {output_path}")

    sections = find_sections(sections_dir)
    print(f"Found {len(sections)} sections:")
    for s in sections:
        print(f"  {s.name}")

    # Load Chatterbox TTS
    print("\nLoading Chatterbox TTS model...")
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    model = ChatterboxTurboTTS.from_pretrained(device="cuda")
    model.prepare_conditionals(voice_path)
    print("Model loaded.")

    # Generate chapter audio
    chunks_dir.mkdir(parents=True, exist_ok=True)
    chapter_paths = []
    chapter_titles = []

    t_start = time.time()
    for i, section_path in enumerate(sections, 1):
        text = section_path.read_text()
        title = section_title(section_path)
        chapter_titles.append(title)

        chapter_path = generate_chapter_audio(
            text=text,
            chapter_idx=i,
            chapter_title=title,
            chunks_dir=chunks_dir,
            model=model,
            voice_path=voice_path,
            total_chapters=len(sections),
        )
        chapter_paths.append(chapter_path)

    t_generation = time.time() - t_start
    print(f"\nAll audio generated in {t_generation:.0f}s ({t_generation/60:.1f}m)")

    # Assemble into M4B
    assemble_m4b(chapter_paths, chapter_titles, output_path)


if __name__ == "__main__":
    main()
