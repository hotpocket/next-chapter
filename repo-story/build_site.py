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
import json
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


def generate_html(books: list[dict]) -> str:
    """Generate the single-page player HTML."""
    books_json = json.dumps(books, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Repo Story</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: #0f0f0f; color: #e0e0e0; min-height: 100vh; }}

.library {{ max-width: 900px; margin: 0 auto; padding: 2rem 1rem; }}
.library h1 {{ font-size: 1.5rem; font-weight: 300; margin-bottom: 2rem; color: #888; letter-spacing: 0.05em; }}

.book-list {{ display: flex; flex-direction: column; gap: 0.5rem; }}
.book-item {{ padding: 1rem 1.25rem; background: #1a1a1a; border-radius: 8px; cursor: pointer; transition: background 0.15s; display: flex; justify-content: space-between; align-items: center; }}
.book-item:hover {{ background: #252525; }}
.book-item .title {{ font-size: 1rem; }}
.book-item .meta {{ font-size: 0.8rem; color: #666; }}
.book-item .progress-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #333; flex-shrink: 0; }}
.book-item .progress-dot.in-progress {{ background: #4a9eff; }}
.book-item .progress-dot.complete {{ background: #34d399; }}

.player-view {{ max-width: 900px; margin: 0 auto; padding: 2rem 1rem; display: none; }}
.player-view.active {{ display: block; }}

.back-btn {{ background: none; border: none; color: #666; font-size: 0.9rem; cursor: pointer; padding: 0.5rem 0; margin-bottom: 1.5rem; }}
.back-btn:hover {{ color: #e0e0e0; }}

.now-playing {{ margin-bottom: 2rem; }}
.now-playing .book-title {{ font-size: 1.3rem; font-weight: 400; margin-bottom: 0.25rem; }}
.now-playing .chapter-title {{ font-size: 0.9rem; color: #4a9eff; }}

.player-controls {{ margin-bottom: 2rem; }}
.time-display {{ display: flex; justify-content: space-between; font-size: 0.75rem; color: #666; margin-bottom: 0.5rem; }}

.track-bar {{ position: relative; height: 6px; background: #333; border-radius: 3px; cursor: pointer; margin-bottom: 0.25rem; }}
.track-bar .progress {{ height: 100%; background: #4a9eff; border-radius: 3px; transition: width 0.1s; }}
.track-bar .chapter-mark {{ position: absolute; top: -2px; width: 1px; height: 10px; background: #555; }}

.controls {{ display: flex; align-items: center; justify-content: center; gap: 1.5rem; margin-top: 1rem; }}
.controls button {{ background: none; border: none; color: #e0e0e0; cursor: pointer; font-size: 1.2rem; padding: 0.5rem; }}
.controls button:hover {{ color: #fff; }}
.play-btn {{ font-size: 2rem !important; }}
.speed-btn {{ font-size: 0.8rem !important; color: #888 !important; min-width: 3em; text-align: center; }}

.chapter-list {{ list-style: none; }}
.chapter-list li {{ padding: 0.75rem 1rem; border-radius: 6px; cursor: pointer; display: flex; justify-content: space-between; font-size: 0.9rem; transition: background 0.15s; }}
.chapter-list li:hover {{ background: #1a1a1a; }}
.chapter-list li.active {{ background: #1a2a3a; color: #4a9eff; }}
.chapter-list li .ch-duration {{ color: #555; font-size: 0.8rem; }}
</style>
</head>
<body>

<div class="library" id="library">
  <h1>repo story</h1>
  <div class="book-list" id="book-list"></div>
</div>

<div class="player-view" id="player-view">
  <button class="back-btn" onclick="showLibrary()">&larr; Library</button>
  <div class="now-playing">
    <div class="book-title" id="book-title"></div>
    <div class="chapter-title" id="chapter-title"></div>
  </div>
  <div class="player-controls">
    <div class="time-display">
      <span id="current-time">0:00</span>
      <span id="total-time">0:00</span>
    </div>
    <div class="track-bar" id="track-bar" onclick="seekTo(event)">
      <div class="progress" id="progress"></div>
    </div>
    <div class="controls">
      <button onclick="skip(-30)">-30s</button>
      <button onclick="prevChapter()">&laquo;</button>
      <button class="play-btn" id="play-btn" onclick="togglePlay()">&#9654;</button>
      <button onclick="nextChapter()">&raquo;</button>
      <button onclick="skip(30)">+30s</button>
      <button class="speed-btn" id="speed-btn" onclick="cycleSpeed()">1x</button>
    </div>
  </div>
  <ul class="chapter-list" id="chapter-list"></ul>
</div>

<audio id="audio" preload="metadata"></audio>

<script>
const BOOKS = {books_json};

let currentBook = null;
let audio = document.getElementById('audio');
let speeds = [0.75, 1, 1.25, 1.5, 1.75, 2];
let speedIdx = 1;

function formatTime(s) {{
  if (isNaN(s)) return '0:00';
  let h = Math.floor(s / 3600);
  let m = Math.floor((s % 3600) / 60);
  let sec = Math.floor(s % 60);
  if (h > 0) return h + ':' + String(m).padStart(2, '0') + ':' + String(sec).padStart(2, '0');
  return m + ':' + String(sec).padStart(2, '0');
}}

function getProgress(bookIdx) {{
  let key = 'rs-progress-' + bookIdx;
  let val = localStorage.getItem(key);
  if (!val) return {{ time: 0, progress: 0 }};
  return JSON.parse(val);
}}

function saveProgress() {{
  if (!currentBook) return;
  let idx = BOOKS.indexOf(currentBook);
  let key = 'rs-progress-' + idx;
  let p = audio.currentTime / (audio.duration || 1);
  localStorage.setItem(key, JSON.stringify({{ time: audio.currentTime, progress: p }}));
}}

function renderLibrary() {{
  let list = document.getElementById('book-list');
  list.innerHTML = '';
  BOOKS.forEach((book, i) => {{
    let p = getProgress(i);
    let status = p.progress > 0.98 ? 'complete' : p.progress > 0.01 ? 'in-progress' : '';
    let div = document.createElement('div');
    div.className = 'book-item';
    div.onclick = () => openBook(i);
    div.innerHTML = '<div><div class="title">' + book.title + '</div>' +
      '<div class="meta">' + book.chapters.length + ' chapters &middot; ' + formatTime(book.duration) + '</div></div>' +
      '<div class="progress-dot ' + status + '"></div>';
    list.appendChild(div);
  }});
}}

function openBook(idx) {{
  currentBook = BOOKS[idx];
  document.getElementById('library').style.display = 'none';
  document.getElementById('player-view').classList.add('active');
  document.getElementById('book-title').textContent = currentBook.title;

  audio.src = 'audio/' + currentBook.filename;
  audio.load();

  let p = getProgress(idx);
  audio.addEventListener('loadedmetadata', function onload() {{
    audio.currentTime = p.time || 0;
    audio.removeEventListener('loadedmetadata', onload);
  }});

  renderChapters();
  updatePlayer();
}}

function showLibrary() {{
  saveProgress();
  audio.pause();
  document.getElementById('player-view').classList.remove('active');
  document.getElementById('library').style.display = 'block';
  renderLibrary();
}}

function renderChapters() {{
  let list = document.getElementById('chapter-list');
  let trackBar = document.getElementById('track-bar');
  list.innerHTML = '';
  // Remove old chapter marks
  trackBar.querySelectorAll('.chapter-mark').forEach(el => el.remove());

  currentBook.chapters.forEach((ch, i) => {{
    let li = document.createElement('li');
    li.id = 'ch-' + i;
    let dur = ch.end - ch.start;
    li.innerHTML = '<span>' + ch.title + '</span><span class="ch-duration">' + formatTime(dur) + '</span>';
    li.onclick = () => {{ audio.currentTime = ch.start; audio.play(); }};
    list.appendChild(li);

    if (i > 0 && currentBook.duration > 0) {{
      let mark = document.createElement('div');
      mark.className = 'chapter-mark';
      mark.style.left = (ch.start / currentBook.duration * 100) + '%';
      trackBar.appendChild(mark);
    }}
  }});
}}

function getCurrentChapter() {{
  if (!currentBook) return null;
  let t = audio.currentTime;
  return currentBook.chapters.find(ch => t >= ch.start && t < ch.end) || currentBook.chapters[0];
}}

function updatePlayer() {{
  requestAnimationFrame(updatePlayer);
  if (!currentBook) return;

  let t = audio.currentTime;
  let d = audio.duration || currentBook.duration;
  document.getElementById('current-time').textContent = formatTime(t);
  document.getElementById('total-time').textContent = formatTime(d);
  document.getElementById('progress').style.width = (t / d * 100) + '%';
  document.getElementById('play-btn').innerHTML = audio.paused ? '&#9654;' : '&#9646;&#9646;';

  let ch = getCurrentChapter();
  if (ch) {{
    document.getElementById('chapter-title').textContent = ch.title;
    document.querySelectorAll('.chapter-list li').forEach((li, i) => {{
      li.classList.toggle('active', i === ch.id);
    }});
  }}
}}

function togglePlay() {{ audio.paused ? audio.play() : audio.pause(); }}
function skip(s) {{ audio.currentTime = Math.max(0, audio.currentTime + s); }}

function prevChapter() {{
  let ch = getCurrentChapter();
  if (!ch || ch.id === 0) {{ audio.currentTime = 0; return; }}
  audio.currentTime = currentBook.chapters[ch.id - 1].start;
}}

function nextChapter() {{
  let ch = getCurrentChapter();
  if (!ch || ch.id >= currentBook.chapters.length - 1) return;
  audio.currentTime = currentBook.chapters[ch.id + 1].start;
}}

function seekTo(e) {{
  let bar = document.getElementById('track-bar');
  let pct = (e.clientX - bar.getBoundingClientRect().left) / bar.offsetWidth;
  audio.currentTime = pct * (audio.duration || currentBook.duration);
}}

function cycleSpeed() {{
  speedIdx = (speedIdx + 1) % speeds.length;
  audio.playbackRate = speeds[speedIdx];
  document.getElementById('speed-btn').textContent = speeds[speedIdx] + 'x';
}}

// Save progress periodically
setInterval(saveProgress, 5000);
audio.addEventListener('ended', saveProgress);

renderLibrary();
</script>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate static audiobook player site")
    parser.add_argument("--audio-dir", default="output", help="Directory containing M4B files")
    parser.add_argument("--output-dir", default="output/site", help="Output directory for static site")
    args = parser.parse_args()

    audio_dir = Path(args.audio_dir)
    output_dir = Path(args.output_dir)

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

    # Generate site
    output_dir.mkdir(parents=True, exist_ok=True)
    audio_out = output_dir / "audio"
    audio_out.mkdir(exist_ok=True)

    # Copy M4B files
    for m4b in m4b_files:
        dest = audio_out / m4b.name
        if not dest.exists() or dest.stat().st_size != m4b.stat().st_size:
            print(f"  Copying {m4b.name}...")
            import shutil
            shutil.copy2(m4b, dest)
        else:
            print(f"  {m4b.name} already copied")

    # Write HTML
    html = generate_html(books)
    index = output_dir / "index.html"
    index.write_text(html)
    print(f"\nSite generated at {output_dir}/")
    print(f"  {index}")
    print(f"  {audio_out}/")


if __name__ == "__main__":
    main()
