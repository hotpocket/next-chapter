#!/usr/bin/env python3
"""Tests for chunk_cache.py — migrate an index-keyed chunk cache to content
addressing, and sweep orphans (no TTS, no GPU).

Migration exists so the switch to content addressing does not throw away hours
of already-rendered audio: the WAV that sat at index 7 IS the audio for the
chunk currently at index 7, provided the text has not changed since it was
rendered (the caller's `.text-hash` guarantee).

Run: python3 repo-story/test_chunk_cache.py
"""
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_audio import chunk_filename, chunk_key, split_into_chunks  # noqa: E402

FAIL = 0
SR = 24000


def check(desc, cond):
    global FAIL
    print(f"{'ok  ' if cond else 'FAIL'} - {desc}")
    if not cond:
        FAIL = 1


def write_wav(path: Path, frames: int = 100):
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"\x00\x00" * frames)


def write_float32_wav(path: Path, frames: int = 100):
    """WAV with format tag 3 (IEEE float) — what torchaudio.save writes, and
    what Python's `wave` module refuses to open ("unknown format: 3")."""
    import struct
    data = b"\x00\x00\x00\x00" * frames
    fmt = struct.pack("<HHIIHH", 3, 1, SR, SR * 4, 4, 32)
    body = (b"WAVE" + b"fmt " + struct.pack("<I", len(fmt)) + fmt
            + b"data" + struct.pack("<I", len(data)) + data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"RIFF" + struct.pack("<I", len(body)) + body)


# Long enough to split into several chunks at the 300-char default, so the
# edit below lands inside one chunk and leaves its neighbours alone.
SECTION = " ".join(
    f"This is narration sentence number {n} and it runs long enough to push the "
    f"chunk splitter past its three hundred character boundary." for n in range(1, 10))
EDIT_FROM = "narration sentence number 5"
EDIT_TO = "narration sentence number 5 REVISED"
SUMMARY = "The summary track is shorter. It still splits into its own chunk."


def mk_book(root: Path) -> tuple[Path, Path, Path]:
    sections, summaries = root / "output" / "sections", root / "output" / "summaries"
    chunks = root / "output" / "audio" / "chunks"
    sections.mkdir(parents=True)
    summaries.mkdir(parents=True)
    chunks.mkdir(parents=True)
    (sections / "section-one.txt").write_text(SECTION)
    (summaries / "section-one.txt").write_text(SUMMARY)
    (root / "output" / "chapters.txt").write_text("section-one.txt\n")
    # Legacy index-named cache, as build_audio.py used to write it — float32
    # throughout, like real torchaudio output. A `wave`-module-only sample-rate
    # probe sees none of these and reports an empty cache.
    for i in range(len(split_into_chunks(SECTION))):
        write_float32_wav(chunks / f"ch01_chunk_{i:05d}.wav")
    for i in range(len(split_into_chunks(SUMMARY))):
        write_float32_wav(chunks / f"ch01_summary_{i:05d}.wav")
    return sections, summaries, chunks


def run(*args) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(HERE / "chunk_cache.py"), *args],
                          capture_output=True, text=True)


with tempfile.TemporaryDirectory() as td:
    root = Path(td) / "book"
    sections, summaries, chunks = mk_book(root)

    r = run("migrate", "--sections-dir", str(sections), "--summaries-dir", str(summaries),
            "--chunks-dir", str(chunks), "--voice", "narrator.wav")
    check("migrate exits 0", r.returncode == 0)
    check("float32 WAVs are not treated as an empty cache",
          "nothing to migrate" not in (r.stdout + r.stderr))

    params_file = chunks / "cache-params.json"
    check("records cache params for build_transcripts", params_file.exists())
    params = json.loads(params_file.read_text()) if params_file.exists() else {}
    check("params carry the voice", params.get("voice") == "narrator.wav")
    check("sample rate read from the existing audio", params.get("params", {}).get("sr") == SR)

    keyed = [chunk_filename(1, "chunk", chunk_key(c, "narrator.wav", params.get("params", {})))
             for c in split_into_chunks(SECTION)]
    check("every full-chapter chunk is now content-addressed",
          all((chunks / k).exists() for k in keyed))
    keyed_sum = [chunk_filename(1, "summary", chunk_key(c, "narrator.wav", params.get("params", {})))
                 for c in split_into_chunks(SUMMARY)]
    check("summary chunks migrate too", all((chunks / k).exists() for k in keyed_sum))
    check("no index-named WAVs left behind",
          not list(chunks.glob("ch01_chunk_000*.wav")))
    check("nothing was re-rendered — file count is unchanged",
          len(list(chunks.glob("*.wav"))) == len(keyed) + len(keyed_sum))

    r2 = run("migrate", "--sections-dir", str(sections), "--summaries-dir", str(summaries),
             "--chunks-dir", str(chunks), "--voice", "narrator.wav")
    check("migrate is idempotent (rc=0, nothing to do)", r2.returncode == 0)
    check("second migrate leaves the same files",
          len(list(chunks.glob("*.wav"))) == len(keyed) + len(keyed_sum))

    # An edit orphans exactly one chunk; gc removes it and keeps the rest.
    edited = SECTION.replace(EDIT_FROM, EDIT_TO)
    edited_keys = [chunk_filename(1, "chunk", chunk_key(c, "narrator.wav", params.get("params", {})))
                   for c in split_into_chunks(edited)]
    orphans = [k for k in keyed if k not in edited_keys]
    check("the edit orphans exactly one chunk", len(orphans) == 1)
    orphan = chunks / orphans[0]
    survivor = chunks / next(k for k in keyed if k in edited_keys)
    (sections / "section-one.txt").write_text(edited)
    r3 = run("gc", "--sections-dir", str(sections), "--summaries-dir", str(summaries),
             "--chunks-dir", str(chunks), "--voice", "narrator.wav")
    check("gc exits 0", r3.returncode == 0)
    check("gc drops the chunk the text no longer references", not orphan.exists())
    check("gc keeps chunks the text still references", survivor.exists())
    check("gc keeps the cache-params sidecar", params_file.exists())

sys.exit(FAIL)
