"""Tests for scripts/build-trilogy-site — assembles docs/ (the Pages site)
from per-book run folders.

Run: python scripts/test_build_trilogy_site.py   (stdlib + ffmpeg-free)
Contract:
  - reads a books registry (slug/title/manifest/transcripts per book)
  - copies chapter + summary M4As into docs/audio/<slug>/
  - prefixes filenames with <slug>/ in the page's books JSON (one shared
    audioBaseUrl)
  - passes summary tracks through
  - merges per-book transcripts.json into one docs/transcripts.json and
    references it with a ?v=<content-hash> query (landry-ui cache-bust rule)
  - copies the player component and records provenance
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "build-trilogy-site"


def mk_book(base: Path, slug: str, with_summary: bool):
    d = base / slug / "output"
    (d / "m4a").mkdir(parents=True)
    (d / "site").mkdir(parents=True)
    (d / "m4a" / "chapter_0001.m4a").write_bytes(b"audio-" + slug.encode())
    ch = {"n": 1, "title": f"Chapter 1: {slug}", "filename": "chapter_0001.m4a",
          "duration_s": 10.0, "size_bytes": 8}
    if with_summary:
        (d / "m4a" / "chapter_0001.summary.m4a").write_bytes(b"sum-" + slug.encode())
        ch["summary"] = {"filename": "chapter_0001.summary.m4a",
                         "duration_s": 2.0, "size_bytes": 6}
    (d / "m4a" / "chapters_manifest.json").write_text(json.dumps({
        "version": "aaaa1111",
        "book": {"title": slug.title(), "artist": "A", "total_duration_s": 10.0,
                 "chapter_count": 1},
        "chapters": [ch],
    }))
    (d / "site" / "transcripts.json").write_text(json.dumps({
        "books": [{"slug": slug, "chapters": [
            {"index": 1, "title": "One",
             "chunks": [{"index": 0, "text": f"text {slug}", "start": 0, "end": 1}]}]}]
    }))
    return d


def main():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        b1 = mk_book(tmp, "alpha", with_summary=True)
        b2 = mk_book(tmp, "beta", with_summary=False)
        player = tmp / "player"
        player.mkdir()
        for f in ["player.js", "player.css", "feedback.js", "sw.js", "manifest.webmanifest"]:
            (player / f).write_text(f"/* {f} */")
        docs = tmp / "docs"
        registry = tmp / "trilogy.json"
        registry.write_text(json.dumps({"title": "Test Trilogy", "books": [
            {"slug": "alpha", "manifest": str(b1 / "m4a" / "chapters_manifest.json"),
             "transcripts": str(b1 / "site" / "transcripts.json")},
            {"slug": "beta", "manifest": str(b2 / "m4a" / "chapters_manifest.json"),
             "transcripts": str(b2 / "site" / "transcripts.json")},
        ]}))
        subprocess.run([sys.executable, str(SCRIPT), "--registry", str(registry),
                        "--docs-dir", str(docs), "--player-src", str(player)],
                       check=True, capture_output=True, text=True)

        html = (docs / "index.html").read_text()
        assert '"alpha/chapter_0001.m4a"' in html, "slug-prefixed filename"
        assert '"beta/chapter_0001.m4a"' in html
        assert '"alpha/chapter_0001.summary.m4a"' in html, "summary passthrough"
        assert (docs / "audio" / "alpha" / "chapter_0001.m4a").read_bytes() == b"audio-alpha"
        assert (docs / "audio" / "alpha" / "chapter_0001.summary.m4a").exists()
        assert (docs / "audio" / "beta" / "chapter_0001.m4a").exists()
        tr = json.loads((docs / "transcripts.json").read_text())
        assert {b["slug"] for b in tr["books"]} == {"alpha", "beta"}, "merged transcripts"
        assert "transcripts.json?v=" in html, "content-hash cache-bust"
        assert (docs / "player.js").exists() and (docs / "sw.js").exists()
        assert "Test Trilogy" in html
    print("ok")


if __name__ == "__main__":
    main()
