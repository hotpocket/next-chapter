"""Regression test for build_site.py manifest mode.

Run: python test_build_site.py
Guards the --feedback-url argparse wiring (a vendor-scrub once dropped the
add_argument while generate_html still read args.feedback_url) and the basic
manifest-mode build contract.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent


def build(tmp: Path, extra_args: list[str]) -> Path:
    m4a_dir = tmp / "m4a"
    m4a_dir.mkdir(parents=True)
    (m4a_dir / "chapter_0001.m4a").write_bytes(b"\x00" * 64)
    manifest = m4a_dir / "chapters_manifest.json"
    manifest.write_text(json.dumps({
        "book": {"title": "T", "artist": "A", "total_duration_s": 1.0},
        "chapters": [{"n": 1, "title": "C1", "filename": "chapter_0001.m4a",
                      "duration_s": 1.0, "size_bytes": 64}],
    }))
    out = tmp / "site"
    subprocess.run(
        [sys.executable, str(ROOT / "build_site.py"),
         "--manifest", str(manifest), "--slug", "t",
         "--output-dir", str(out)] + extra_args,
        check=True, cwd=tmp, capture_output=True, text=True)
    return out


def main():
    with tempfile.TemporaryDirectory() as d:
        out = build(Path(d) / "a", extra_args=[])
        html = (out / "index.html").read_text()
        assert "feedbackUrl" not in html, "no feedbackUrl when flag omitted"
        assert 'rel="icon"' in html, "favicon link missing"
        assert (out / "audio" / "chapter_0001.m4a").exists()

        out = build(Path(d) / "b", extra_args=["--feedback-url", "https://x.example/events"])
        html = (out / "index.html").read_text()
        assert "feedbackUrl: 'https://x.example/events'" in html
    print("ok")


if __name__ == "__main__":
    main()
