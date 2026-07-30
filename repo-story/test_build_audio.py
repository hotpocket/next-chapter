#!/usr/bin/env python3
"""Tests for build_audio.py's chunk cache addressing (no TTS, no GPU).

Contract: a chunk WAV is identified by what it SAYS and how it was voiced, not
by where it sits in the chapter. That is what makes a one-sentence edit cost one
chunk of GPU time instead of a whole book:

  - the cache key is a hash of (chunk text, voice, TTS params)
  - editing/inserting a chunk leaves every other chunk's key untouched
  - changing the voice or a sampling param invalidates every key
  - build_transcripts.py addresses the same files through the same helper

Run: python3 repo-story/test_build_audio.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_audio import chunk_filename, chunk_key, split_into_chunks  # noqa: E402

FAIL = 0


def check(desc, cond):
    global FAIL
    print(f"{'ok  ' if cond else 'FAIL'} - {desc}")
    if not cond:
        FAIL = 1


VOICE = "/voices/narrator.wav"
PARAMS = {"exaggeration": 0.5, "cfg_weight": 0.5}

# --- key identity -----------------------------------------------------------
k1 = chunk_key("The pipeline renders one chunk at a time.", VOICE, PARAMS)
k2 = chunk_key("The pipeline renders one chunk at a time.", VOICE, PARAMS)
check("same text + voice + params -> same key", k1 == k2)
check("key is a short hex digest", len(k1) == 12 and all(c in "0123456789abcdef" for c in k1))

check("different text -> different key",
      chunk_key("Something else entirely.", VOICE, PARAMS) != k1)
check("different voice -> different key",
      chunk_key("The pipeline renders one chunk at a time.", "/voices/other.wav", PARAMS) != k1)
check("different TTS params -> different key",
      chunk_key("The pipeline renders one chunk at a time.", VOICE,
                {"exaggeration": 0.9, "cfg_weight": 0.5}) != k1)
check("param order does not affect the key",
      chunk_key("x", VOICE, {"a": 1, "b": 2}) == chunk_key("x", VOICE, {"b": 2, "a": 1}))

# --- filenames --------------------------------------------------------------
fn = chunk_filename(3, "chunk", k1)
check("filename carries chapter, variant and key", fn == f"ch03_chunk_{k1}.wav")
check("summary variant is a distinct file",
      chunk_filename(3, "summary", k1) == f"ch03_summary_{k1}.wav")
check("filename has no positional index",
      not any(part.isdigit() and len(part) == 5 for part in fn.split("_")))

# --- the property that makes incremental regeneration work ------------------
BEFORE = ("Alpha sentence one. Beta sentence two. Gamma sentence three. "
          "Delta sentence four. Epsilon sentence five.")
AFTER = ("Alpha sentence one. Beta sentence two REVISED. Gamma sentence three. "
         "Delta sentence four. Epsilon sentence five.")
# Force one chunk per sentence so the edit lands in a single chunk.
before_keys = [chunk_key(c, VOICE, PARAMS) for c in split_into_chunks(BEFORE, max_chars=25)]
after_keys = [chunk_key(c, VOICE, PARAMS) for c in split_into_chunks(AFTER, max_chars=25)]
check("editing one chunk changes exactly one key",
      len(set(before_keys) - set(after_keys)) == 1)
check("every other chunk keeps its key (cache hit)",
      len(set(before_keys) & set(after_keys)) == len(before_keys) - 1)

# An inserted sentence shifts every later index but no later key.
INSERTED = ("Alpha sentence one. Inserted brand new sentence. Beta sentence two. "
            "Gamma sentence three. Delta sentence four. Epsilon sentence five.")
inserted_keys = [chunk_key(c, VOICE, PARAMS) for c in split_into_chunks(INSERTED, max_chars=25)]
check("inserting a chunk invalidates nothing that follows it",
      set(before_keys).issubset(set(inserted_keys)))

# --- transcripts must address the same files --------------------------------
import build_transcripts  # noqa: E402

check("build_transcripts uses the shared key helper",
      getattr(build_transcripts, "chunk_filename", None) is chunk_filename)

sys.exit(FAIL)
