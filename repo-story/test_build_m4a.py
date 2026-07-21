"""Regression test for build_m4a.py summary tracks.

Run: python test_build_m4a.py   (needs ffmpeg + chatterbook)
Covers: summary WAV → chapter_NNNN.summary.m4a encoding, manifest summary
attachment, and the manifest version hash changing when only a summary
track changes (cache-busting must key on ALL content, not just full tracks).
"""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).parent


def wav(path: Path, seconds: float):
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(seconds), str(path), "-loglevel", "error"], check=True)


def run_m4a(tmp: Path):
    subprocess.run([sys.executable, str(ROOT / "build_m4a.py"), "--title", "T",
                    "--audio-dir", str(tmp / "audio"), "--sections-dir", str(tmp / "sections"),
                    "--m4a-dir", str(tmp / "m4a")],
                   check=True, capture_output=True, text=True, cwd=tmp)
    return json.loads((tmp / "m4a" / "chapters_manifest.json").read_text())


def main():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "sections").mkdir()
        (tmp / "audio").mkdir()
        (tmp / "sections" / "section-one.txt").write_text("One.")
        (tmp / "chapters.txt").write_text("section-one.txt\n")
        wav(tmp / "audio" / "chapter-01-one.wav", 1.0)
        wav(tmp / "audio" / "summary-01-one.wav", 0.4)

        m1 = run_m4a(tmp)
        ch = m1["chapters"][0]
        assert ch.get("summary"), "manifest chapter missing summary"
        assert ch["summary"]["filename"] == "chapter_0001.summary.m4a"
        assert 0.1 < ch["summary"]["duration_s"] < 1.0, ch["summary"]
        assert (tmp / "m4a" / "chapter_0001.summary.m4a").exists()

        # Change ONLY the summary track → version must change
        time.sleep(0.02)
        wav(tmp / "audio" / "summary-01-one.wav", 0.8)
        (tmp / "m4a" / "chapter_0001.summary.m4a").unlink()  # force re-encode
        m2 = run_m4a(tmp)
        assert m2["chapters"][0]["summary"]["duration_s"] != ch["summary"]["duration_s"]
        assert m2["version"] != m1["version"], \
            f"version unchanged after summary change: {m1['version']}"
    print("ok")


if __name__ == "__main__":
    main()
