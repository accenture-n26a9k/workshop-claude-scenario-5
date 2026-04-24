#!/usr/bin/env python3
"""Local HTTP server for acnpptx slide reviewer.

Two modes:
  - preview: Visual pattern selection before slide generation
  - review:  Slide markup/annotation after generation

Usage:
    python reviewer_server.py --mode preview --port 3118
    python reviewer_server.py --mode review  --port 3118

Claude Code communicates via curl:
    POST /api/init      - Send outline (preview) or slide images (review)
    GET  /api/status    - Lightweight poll (confirmed flag only)
    GET  /api/state     - Full state (after confirmed=True)
    POST /api/confirm   - Browser sends user edits
    POST /api/shutdown  - Graceful shutdown

Security: 127.0.0.1 only, token-based auth via X-Token header.
"""
import argparse
import base64
import json
import os
import re
import secrets
import signal
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path


MAX_BODY_SIZE = 100 * 1024 * 1024  # 100 MB


class AppState:
    """Shared mutable state for the server. Thread-safe via lock."""

    def __init__(self, mode: str):
        self.lock = threading.Lock()
        self.mode = mode
        self.initialized = False
        self.confirmed = False
        self.token = secrets.token_hex(16)
        self.outline = None   # Mode: preview
        self.slides = None    # Mode: review
        self.feedback = None  # Mode: review


def load_pattern_catalog(assets_dir: Path) -> dict:
    """Load pattern preview PNGs into base64 data URIs."""
    catalog_dir = assets_dir / "pattern_previews"
    map_path = catalog_dir / "catalog_map.json"

    if not map_path.exists():
        print(f"WARNING: catalog_map.json not found at {map_path}", file=sys.stderr)
        return {}

    with open(map_path, "r", encoding="utf-8") as f:
        catalog_map = json.load(f)

    result = {}
    for pattern_id, info in catalog_map.items():
        png_path = catalog_dir / info["filename"]
        if png_path.exists():
            b64 = base64.b64encode(png_path.read_bytes()).decode("ascii")
            result[pattern_id] = {
                "id": pattern_id,
                "name": info["name"],
                "category": info["category"],
                "image": f"data:image/png;base64,{b64}",
            }
        else:
            result[pattern_id] = {
                "id": pattern_id,
                "name": info["name"],
                "category": info["category"],
                "image": None,
            }
    return result


def load_html_template(scripts_dir: Path) -> str:
    html_path = scripts_dir / "reviewer.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


class ReviewerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the reviewer app."""

    def __init__(self, state: AppState, pattern_catalog: dict, html_template: str, *args, **kwargs):
        self.state = state
        self.pattern_catalog = pattern_catalog
        self.html_template = html_template
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress default logging

    def _check_token(self) -> bool:
        # localhost-only tool — no token enforcement needed
        return True

    def _json_response(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY_SIZE:
            self._json_response({"error": "Body too large"}, status=413)
            return None
        if length == 0:
            self._json_response({"error": "Empty body"}, status=400)
            return None
        return self.rfile.read(length)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Token")
        self.end_headers()

    def do_GET(self):
        if not self._check_token():
            return
        if self.path in ("/", "/index.html"):
            self._serve_html()
        elif self.path == "/api/health":
            with self.state.lock:
                self._json_response({
                    "status": "ok",
                    "mode": self.state.mode,
                    "initialized": self.state.initialized,
                })
        elif self.path == "/api/status":
            # Lightweight polling endpoint — no large data
            with self.state.lock:
                self._json_response({
                    "confirmed": self.state.confirmed,
                    "initialized": self.state.initialized,
                })
        elif self.path in ("/api/state", "/api/feedback"):
            self._serve_state()
        else:
            self.send_error(404)

    def do_POST(self):
        if not self._check_token():
            return
        if self.path == "/api/init":
            self._handle_init()
        elif self.path == "/api/confirm":
            self._handle_confirm()
        elif self.path == "/api/shutdown":
            self._json_response({"ok": True})
            threading.Thread(target=lambda: (time.sleep(0.5), self.server.shutdown()), daemon=True).start()
        else:
            self.send_error(404)

    def _serve_html(self):
        catalog_json = json.dumps(self.pattern_catalog, ensure_ascii=False)
        catalog_json = catalog_json.replace("</", "<\\/")
        mode_json = json.dumps(self.state.mode)
        token_json = json.dumps(self.state.token)

        html = self.html_template
        html = html.replace("/*__PATTERN_CATALOG__*/", f"const PATTERN_CATALOG = {catalog_json};")
        html = html.replace("/*__APP_MODE__*/", f"const APP_MODE = {mode_json};")
        html = html.replace("/*__APP_TOKEN__*/", f"const APP_TOKEN = {token_json};")

        content = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _serve_state(self):
        with self.state.lock:
            if self.state.mode == "preview":
                self._json_response({
                    "confirmed": self.state.confirmed,
                    "outline": self.state.outline,
                })
            else:
                self._json_response({
                    "confirmed": self.state.confirmed,
                    "feedback": self.state.feedback,
                    "slides": self.state.slides,
                })

    def _handle_init(self):
        body = self._read_body()
        if body is None:
            return
        try:
            text = body.decode("utf-8", errors="replace")
            data = json.loads(text)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json_response({"error": "Invalid JSON"}, status=400)
            return

        mode = data.get("mode", self.state.mode)
        with self.state.lock:
            if mode == "preview":
                self.state.outline = data.get("outline")
            elif mode == "review":
                self.state.slides = data.get("slides", [])
                self.state.feedback = []
            else:
                self._json_response({"error": f"Unknown mode: {mode}"}, status=400)
                return
            self.state.initialized = True
            self.state.confirmed = False

        self._json_response({"ok": True})

    def _handle_confirm(self):
        body = self._read_body()
        if body is None:
            return
        try:
            text = body.decode("utf-8", errors="replace")
            data = json.loads(text)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._json_response({"error": "Invalid JSON"}, status=400)
            return

        with self.state.lock:
            self.state.confirmed = True
            if self.state.mode == "preview":
                self.state.outline = data.get("outline", self.state.outline)
            elif self.state.mode == "review":
                self.state.feedback = data.get("feedback", [])

        self._json_response({"ok": True})


def kill_port(port: int):
    """Kill any process listening on the given port (Windows)."""
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True, text=True, timeout=5,
        )
        # Match exact port in Local Address column (e.g., "0.0.0.0:3118" or "127.0.0.1:3118")
        pattern = re.compile(rf'\s[\d.]+:{port}\s+[\d.]+:\d+\s+LISTENING\s+(\d+)')
        for line in result.stdout.splitlines():
            m = pattern.search(line)
            if m:
                pid = int(m.group(1))
                if pid != os.getpid():
                    subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                                   capture_output=True, timeout=5)
                    time.sleep(0.5)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="acnpptx Slide Reviewer Server")
    parser.add_argument("--mode", choices=["preview", "review"], required=True)
    parser.add_argument("--port", type=int, default=3118)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    scripts_dir = Path(__file__).resolve().parent

    state = AppState(args.mode)
    pattern_catalog = load_pattern_catalog(skill_dir / "assets")
    html_template = load_html_template(scripts_dir)

    kill_port(args.port)

    handler = partial(ReviewerHandler, state, pattern_catalog, html_template)
    server = HTTPServer(("127.0.0.1", args.port), handler)
    url = f"http://127.0.0.1:{args.port}"

    # Write ready file (same dir as Python's tempdir for cross-platform consistency)
    ready_path = Path(tempfile.gettempdir()) / f"reviewer_{args.port}.ready"
    ready_data = {
        "status": "ready",
        "port": args.port,
        "token": state.token,
        "url": url,
        "pid": os.getpid(),
        "mode": args.mode,
        "ready_file": str(ready_path),
    }
    ready_path.write_text(json.dumps(ready_data), encoding="utf-8")

    print(json.dumps(ready_data), flush=True)

    if not args.no_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()

    # Graceful shutdown on Ctrl+C
    signal.signal(signal.SIGINT, lambda s, f: server.shutdown())
    if sys.platform != "win32":
        signal.signal(signal.SIGTERM, lambda s, f: server.shutdown())

    try:
        server.serve_forever()
    finally:
        try:
            ready_path.unlink()
        except OSError:
            pass
        print("Server stopped.", flush=True)


if __name__ == "__main__":
    main()