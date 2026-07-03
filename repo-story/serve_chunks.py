#!/usr/bin/env python3
"""Serve a chunks dir as a live HLS playlist on the LAN.

Point Android VLC at http://<host>:<port>/playlist.m3u8 — it will re-poll the
playlist as new chunks are written and let you seek backward through what's
already aired.
"""

import argparse
import os
import socket
import sys
import time
import wave
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn, TCPServer


class ThreadingHTTPServer(ThreadingMixIn, TCPServer):
    allow_reuse_address = True
    daemon_threads = True


CHUNK_SIZE = 64 * 1024
_duration_cache: dict[str, tuple[float, int, float]] = {}


def wav_duration(path: Path) -> float:
    """Duration in seconds, cached on (mtime, size)."""
    st = path.stat()
    key = str(path)
    cached = _duration_cache.get(key)
    if cached and cached[0] == st.st_mtime and cached[1] == st.st_size:
        return cached[2]
    with wave.open(str(path), 'rb') as w:
        dur = w.getnframes() / float(w.getframerate())
    _duration_cache[key] = (st.st_mtime, st.st_size, dur)
    return dur


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


def make_handler(chunks_dir: Path, mtime_grace: float):

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            if args and isinstance(args[0], str) and args[0].startswith('code'):
                return
            super().log_message(format, *args)

        def _build_playlist(self) -> bytes:
            now = time.time()
            entries: list[tuple[str, float]] = []
            max_dur = 1.0
            for p in sorted(chunks_dir.glob('*.wav')):
                try:
                    st = p.stat()
                except FileNotFoundError:
                    continue
                if now - st.st_mtime < mtime_grace:
                    continue  # likely still being written
                try:
                    dur = wav_duration(p)
                except (wave.Error, EOFError, OSError):
                    continue
                entries.append((p.name, dur))
                if dur > max_dur:
                    max_dur = dur

            lines = [
                '#EXTM3U',
                '#EXT-X-VERSION:3',
                '#EXT-X-PLAYLIST-TYPE:EVENT',
                f'#EXT-X-TARGETDURATION:{int(max_dur) + 1}',
                '#EXT-X-MEDIA-SEQUENCE:0',
            ]
            for name, dur in entries:
                lines.append(f'#EXTINF:{dur:.3f},')
                lines.append(f'chunks/{name}')
            # No #EXT-X-ENDLIST — keeps stream live so VLC keeps re-polling.
            return ('\n'.join(lines) + '\n').encode('utf-8')

        def _send_playlist(self, body_only: bool = False):
            body = self._build_playlist()
            self.send_response(200)
            self.send_header('Content-Type', 'application/vnd.apple.mpegurl')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            if not body_only:
                self.wfile.write(body)

        def _resolve_chunk(self) -> Path | None:
            path = self.path.split('?', 1)[0]
            prefix = '/chunks/'
            if not path.startswith(prefix):
                return None
            name = path[len(prefix):]
            if '/' in name or '\\' in name or name.startswith('.'):
                return None
            p = chunks_dir / name
            return p if p.is_file() else None

        def _send_chunk(self, p: Path, body_only: bool = False):
            file_size = p.stat().st_size
            range_header = self.headers.get('Range')
            if range_header and not body_only:
                spec = range_header.replace('bytes=', '')
                parts = spec.split('-')
                start = int(parts[0]) if parts[0] else 0
                end = int(parts[1]) if parts[1] else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1
                self.send_response(206)
                self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
            else:
                start = 0
                length = file_size
                self.send_response(200)
            self.send_header('Content-Type', 'audio/wav')
            self.send_header('Content-Length', str(length))
            self.send_header('Accept-Ranges', 'bytes')
            self.end_headers()
            if body_only:
                return
            try:
                with open(p, 'rb') as f:
                    f.seek(start)
                    remaining = length
                    while remaining > 0:
                        buf = f.read(min(CHUNK_SIZE, remaining))
                        if not buf:
                            break
                        self.wfile.write(buf)
                        remaining -= len(buf)
            except (ConnectionResetError, BrokenPipeError):
                pass

        def do_GET(self):
            path = self.path.split('?', 1)[0]
            if path in ('/', '/playlist.m3u8'):
                return self._send_playlist()
            p = self._resolve_chunk()
            if p is not None:
                return self._send_chunk(p)
            self.send_error(404)

        def do_HEAD(self):
            path = self.path.split('?', 1)[0]
            if path in ('/', '/playlist.m3u8'):
                return self._send_playlist(body_only=True)
            p = self._resolve_chunk()
            if p is None:
                return self.send_error(404)
            return self._send_chunk(p, body_only=True)

    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serve audio chunks as a live HLS playlist on the LAN')
    parser.add_argument('-d', '--directory', default='mattpocock-skills/output/audio/chunks',
                        help='Directory of .wav chunks to serve (default: %(default)s)')
    parser.add_argument('-p', '--port', type=int, default=8000)
    parser.add_argument('--mtime-grace', type=float, default=1.0,
                        help='Skip chunks whose mtime is within N seconds of now to avoid half-written files (default: %(default)s)')
    args = parser.parse_args()

    chunks_dir = Path(args.directory).resolve()
    if not chunks_dir.is_dir():
        print(f'Error: {chunks_dir} is not a directory', file=sys.stderr)
        sys.exit(1)

    handler = make_handler(chunks_dir, args.mtime_grace)
    server = ThreadingHTTPServer(('', args.port), handler)
    ip = lan_ip()
    print(f'Serving {chunks_dir}')
    print(f'  LAN: http://{ip}:{args.port}/playlist.m3u8')
    print(f'  Local: http://localhost:{args.port}/playlist.m3u8')
    print('Open the LAN URL in VLC for Android (Stream → paste URL).')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down.')
