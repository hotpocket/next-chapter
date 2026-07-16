#!/usr/bin/env python3
"""
build_site.py — Generate a static audiobook player site from M4B files.

Extracts chapter metadata via ffprobe, generates a single-page HTML player,
and copies audio files into a deploy-ready directory.

Usage:
    ./build_site.py
    ./build_site.py --output-dir output/site --audio-dir output
"""

import argparse
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path


def extract_chapters(m4b_path: Path) -> list[dict]:
    """Extract chapter metadata from M4B via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_chapters", "-show_format", str(m4b_path)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"ffprobe failed on {m4b_path}: {result.stderr}")
        sys.exit(1)

    data = json.loads(result.stdout)
    chapters = []
    for ch in data.get("chapters", []):
        chapters.append({
            "id": ch.get("id", len(chapters)),
            "title": ch.get("tags", {}).get("title", f"Chapter {len(chapters) + 1}"),
            "start": float(ch.get("start_time", 0)),
            "end": float(ch.get("end_time", 0)),
        })

    format_info = data.get("format", {})
    duration = float(format_info.get("duration", 0))
    title = format_info.get("tags", {}).get("title", m4b_path.stem)

    return {"title": title, "duration": duration, "chapters": chapters, "filename": m4b_path.name}


def book_from_manifest(manifest_path: Path, slug: str) -> dict:
    """Build a player book dict from a build_m4a.py chapters_manifest.json.

    The player's per-chapter model: chapter.filename is fetched relative to
    audioBaseUrl, start/end are book-relative cumulative times.
    """
    data = json.loads(manifest_path.read_text())
    chapters = []
    offset = 0.0
    for ch in data["chapters"]:
        duration = float(ch["duration_s"])
        chapters.append({
            # Player contract: id is 0-based (indexes DOM arrays, id+1 →
            # transcript chapter index); manifest n is 1-based.
            "id": ch["n"] - 1,
            "n": ch["n"],
            "title": ch["title"],
            "filename": ch["filename"],
            "start": round(offset, 3),
            "end": round(offset + duration, 3),
            "duration": duration,
            "size": ch.get("size_bytes", 0),
        })
        offset += duration
    book = data["book"]
    return {
        "slug": slug,
        "title": book["title"],
        "artist": book.get("artist", ""),
        "duration": book["total_duration_s"],
        "chapters": chapters,
    }


def generate_html(books: list[dict], feedback_url: str = "",
                  transcript_url: str = "transcripts.json") -> str:
    """Generate the HTML shell that loads the external player component."""
    books_json = json.dumps(books, indent=2)

    feedback_config = ""
    if feedback_url:
        feedback_config = f",\n    feedbackUrl: '{feedback_url}'"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Repo Story</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="stylesheet" href="player.css">
</head>
<body>
<div id="app"></div>
<script src="feedback.js"></script>
<script src="player.js"></script>
<script>
RepoStoryPlayer.init({{
    container: document.getElementById('app'),
    books: {books_json},
    audioBaseUrl: 'audio/',
    transcriptUrl: {json.dumps(transcript_url)}{feedback_config}
}});
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate static audiobook player site")
    parser.add_argument("--audio-dir", default="output", help="Directory containing M4B files (legacy single-file mode)")
    parser.add_argument("--manifest", default="", help="chapters_manifest.json from build_m4a.py — per-chapter mode, the format the current player expects")
    parser.add_argument("--slug", default="book", help="Book slug (per-chapter mode; must match transcripts.json)")
    parser.add_argument("--transcripts-file", default="", help="Inline this transcripts JSON as a data: URI so the site works from file:// (standalone)")
    parser.add_argument("--output-dir", default="output/site", help="Output directory for static site")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_out = output_dir / "audio"
    audio_out.mkdir(exist_ok=True)

    if args.manifest:
        manifest_path = Path(args.manifest)
        book = book_from_manifest(manifest_path, args.slug)
        books = [book]
        print(f"Book: {book['title']} — {len(book['chapters'])} chapters, {book['duration']:.0f}s")
        wanted = {ch["filename"] for ch in book["chapters"]}
        for ch in book["chapters"]:
            src = manifest_path.parent / ch["filename"]
            dest = audio_out / ch["filename"]
            if not dest.exists() or dest.stat().st_size != src.stat().st_size:
                shutil.copy2(src, dest)
        for stale in audio_out.iterdir():
            if stale.name not in wanted:
                print(f"  Removing stale {stale.name}")
                stale.unlink()
        print(f"  Copied {len(book['chapters'])} chapter M4As")
    else:
        # Legacy single-M4B mode (brandonlandry.com deploy). NOTE: the current
        # player is per-chapter (chapter.filename) — this mode predates it.
        audio_dir = Path(args.audio_dir)
        m4b_files = sorted(audio_dir.glob("*.m4b"))
        if not m4b_files:
            print(f"No .m4b files found in {audio_dir}")
            sys.exit(1)

        print(f"Found {len(m4b_files)} audiobook(s):")
        books = []
        for m4b in m4b_files:
            print(f"  {m4b.name}")
            book = extract_chapters(m4b)
            books.append(book)
            print(f"    {len(book['chapters'])} chapters, {book['duration']:.0f}s")

        for m4b in m4b_files:
            dest = audio_out / m4b.name
            if not dest.exists() or dest.stat().st_size != m4b.stat().st_size:
                print(f"  Copying {m4b.name}...")
                shutil.copy2(m4b, dest)
            else:
                print(f"  {m4b.name} already copied")

    transcript_url = "transcripts.json"
    if args.transcripts_file:
        raw = Path(args.transcripts_file).read_bytes()
        transcript_url = "data:application/json;base64," + base64.b64encode(raw).decode()

    # Copy player component files
    player_dir = Path(__file__).parent / "player"
    for player_file in ["player.css", "player.js", "feedback.js", "sw.js", "manifest.webmanifest"]:
        src = player_dir / player_file
        dest = output_dir / player_file
        if src.exists():
            shutil.copy2(src, dest)
            print(f"  Copied {player_file}")
        else:
            print(f"  Warning: {src} not found")

    # Copy icons
    icons_src = player_dir / "icons"
    if icons_src.exists():
        icons_dest = output_dir / "icons"
        if icons_dest.exists():
            shutil.rmtree(icons_dest)
        shutil.copytree(icons_src, icons_dest)
        print(f"  Copied icons/")

    # Write HTML
    html = generate_html(books, feedback_url=args.feedback_url, transcript_url=transcript_url)
    index = output_dir / "index.html"
    index.write_text(html)
    print(f"\nSite generated at {output_dir}/")
    print(f"  {index}")
    print(f"  {audio_out}/")


if __name__ == "__main__":
    main()
