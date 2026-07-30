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
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Shared audiobook engine (~/git/chatterbook, on sys.path via .pth).
# is_speakable is the ch-1073 voice-sample-leak guard — imported, not
# mirrored, so wbt and repo-story can no longer drift.
from chatterbook.audio import get_wav_duration  # noqa: F401  (re-exported to build_transcripts.py)
from chatterbook.text import is_speakable


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
    # Drop degenerate chunks (no word characters, e.g. '"..."'): Chatterbox
    # given near-zero phonetic content can hallucinate the conditioning
    # sample's transcript instead (voice-sample leak, wbt ch 1073).
    # Dropping shifts positions, which used to poison the index-keyed cache;
    # chunks are content-addressed now (see chunk_key), so a shift is harmless.
    return [c for c in chunks if is_speakable(c)]


def chunk_key(text: str, voice_path: str, params: dict) -> str:
    """Content address for one chunk's audio: hash of what it says and how it
    is voiced. Position is deliberately NOT in the key — that is what lets an
    edited sentence re-render alone while every other chunk stays a cache hit,
    even though the edit shifted their indices.

    voice and params belong in the key too: same words in a different voice (or
    at a different exaggeration) are different audio, and an index-keyed cache
    silently served the old one."""
    payload = json.dumps(
        {"text": text, "voice": Path(voice_path).name if voice_path else "",
         "params": params},
        sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def chunk_filename(chapter_idx: int, variant: str, key: str) -> str:
    """chNN_<variant>_<key>.wav — the one place this name is spelled. Imported
    by build_transcripts.py so the writer and the reader cannot drift."""
    return f"ch{chapter_idx:02d}_{variant}_{key}.wav"


def tts_params(model) -> dict:
    """Sampling params that affect the rendered audio, for the cache key."""
    return {
        "sr": getattr(model, "sr", None),
        "exaggeration": getattr(model, "exaggeration", None),
        "cfg_weight": getattr(model, "cfg_weight", None),
    }


CACHE_PARAMS_FILE = "cache-params.json"


def save_cache_params(chunks_dir: Path, voice_path: str, params: dict):
    """Record what the cached chunks were voiced with, so build_transcripts.py
    can recompute the same keys without loading the TTS model."""
    chunks_dir.mkdir(parents=True, exist_ok=True)
    (chunks_dir / CACHE_PARAMS_FILE).write_text(
        json.dumps({"voice": Path(voice_path).name if voice_path else "", "params": params},
                   sort_keys=True, indent=2))


def load_cache_params(chunks_dir: Path) -> tuple[str, dict]:
    p = chunks_dir / CACHE_PARAMS_FILE
    if not p.exists():
        print(f"No {p} — run build_audio.py first (it records the voice/params "
              "the chunk cache was keyed with).")
        sys.exit(1)
    data = json.loads(p.read_text())
    return data.get("voice", ""), data.get("params", {})


def referenced_chunk_names(sections_dir: Path, summaries_dir: Path | None,
                           voice_path: str, params: dict) -> set[str]:
    """Every chunk filename the current text should produce — the live set an
    orphan sweep keeps and everything else can be dropped."""
    names: set[str] = set()
    for idx, section in enumerate(find_sections(sections_dir), start=1):
        for text, variant in ((section.read_text(), "chunk"),):
            for c in split_into_chunks(text):
                names.add(chunk_filename(idx, variant, chunk_key(c, voice_path, params)))
        if summaries_dir:
            summary = summaries_dir / section.name
            if summary.exists():
                for c in split_into_chunks(summary.read_text()):
                    names.add(chunk_filename(idx, "summary", chunk_key(c, voice_path, params)))
    return names


def generate_chapter_audio(
    text: str,
    chapter_idx: int,
    chapter_title: str,
    chunks_dir: Path,
    model,
    voice_path: str,
    total_chapters: int,
    variant: str = "chunk",
) -> Path:
    """Generate audio for one chapter, chunk by chunk. Returns path to chapter WAV.

    variant: 'chunk' (full chapter) or 'summary' (condensed track) — controls
    the chunk-cache prefix (chNN_<variant>_*) and the output WAV name
    (chapter-NN-*.wav vs summary-NN-*.wav, keeping summaries out of
    build_m4a's chapter-*.wav glob and the M4B).
    """
    import torchaudio

    chunks = split_into_chunks(text)
    total_chunks = len(chunks)
    slug = chapter_title.lower().replace(' ', '-')
    prefix = "chapter" if variant == "chunk" else "summary"
    chapter_wav_path = chunks_dir.parent / f"{prefix}-{chapter_idx:02d}-{slug}.wav"

    # Clean up any temp files from a previously killed run
    for stale in chunks_dir.glob(f"ch{chapter_idx:02d}_{variant}_*.tmp.wav"):
        stale.unlink()

    label = chapter_title if variant == "chunk" else f"{chapter_title} (summary)"
    print(f"\n[Chapter {chapter_idx}/{total_chapters}] {label} — {total_chunks} chunks")

    params = tts_params(model)
    chunk_wavs = []
    for i, chunk_text in enumerate(chunks):
        chunk_path = chunks_dir / chunk_filename(
            chapter_idx, variant, chunk_key(chunk_text, voice_path, params))
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
    filelist = chunks_dir / f"ch{chapter_idx:02d}_{variant}_filelist.txt"
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


def assemble_m4b(chapter_paths: list[Path], chapter_titles: list[str], output_path: Path,
                 title: str = "Repo Story", artist: str = "", date: str = ""):
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
            f.write(f"title={title}\n")
            f.write("album=Repo Story\n")
            if artist:
                f.write(f"artist={artist}\n")
            if date:
                f.write(f"date={date}\n")
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
            "-movflags", "+faststart",
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
    parser.add_argument("--summaries-dir", default="output/summaries", help="Directory containing per-chapter summary text (optional; generates the player's Summary track)")
    parser.add_argument("--output", default="output/book.m4b", help="Output M4B file path")
    parser.add_argument("--chunks-dir", default="output/audio/chunks", help="Directory for intermediate chunk WAVs")
    parser.add_argument("--title", default="Repo Story", help="Episode title (M4B title tag; album is always 'Repo Story')")
    parser.add_argument("--artist", default="", help="Artist tag for the M4B")
    parser.add_argument("--date", default="", help="Date tag for the M4B (YYYY-MM-DD)")
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

    # Generate chapter audio. Record the cache key's inputs first:
    # build_transcripts.py recomputes chunk names from them.
    chunks_dir.mkdir(parents=True, exist_ok=True)
    save_cache_params(chunks_dir, voice_path, tts_params(model))
    chapter_paths = []
    chapter_titles = []

    summaries_dir = Path(args.summaries_dir)

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

        # Optional condensed track: same TTS path, separate chunk cache and
        # WAV name; never enters the M4B (per-chapter M4A/manifest only).
        summary_path = summaries_dir / section_path.name
        if summary_path.exists():
            generate_chapter_audio(
                text=summary_path.read_text(),
                chapter_idx=i,
                chapter_title=title,
                chunks_dir=chunks_dir,
                model=model,
                voice_path=voice_path,
                total_chapters=len(sections),
                variant="summary",
            )

    t_generation = time.time() - t_start
    print(f"\nAll audio generated in {t_generation:.0f}s ({t_generation/60:.1f}m)")

    # Assemble into M4B
    assemble_m4b(chapter_paths, chapter_titles, output_path,
                 title=args.title, artist=args.artist, date=args.date)


if __name__ == "__main__":
    main()
