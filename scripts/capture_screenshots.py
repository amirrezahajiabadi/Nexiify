#!/usr/bin/env python3
"""Full-page screenshots of the Nexify site for the README gallery.

Uses Chrome DevTools Protocol over a raw WebSocket (stdlib only — no pip
installs). Waits for real time after navigation so reveal animations,
counters and fonts settle, then captures the ENTIRE page (not just the
viewport) as PNG.

Usage:
    python scripts/capture_screenshots.py [--host 127.0.0.1] [--port 8471]
                                          [--out docs/screenshots] [--wait 4]

Requirements:
    - The Django dev server must be running (e.g. `python manage.py runserver`)
    - Google Chrome installed (path auto-detected, override with --chrome)
"""
import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.request
from urllib.parse import urlparse

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
PAGES = [
    ("home", "/"),
    ("services", "/services/"),
    ("projects", "/projects/"),
    ("blog", "/blog/"),
    ("about", "/about/"),
    ("contact", "/contact/"),
    ("login", "/accounts/login/"),
    ("register", "/accounts/register/"),
]


class WS:
    """Minimal RFC-6455 WebSocket client (client frames are masked)."""

    def __init__(self, url):
        u = urlparse(url)
        self.sock = socket.create_connection((u.hostname, u.port), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {u.path} HTTP/1.1\r\n"
            f"Host: {u.hostname}:{u.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        self._id = 0

    def _recv_exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("socket closed")
            buf += chunk
        return buf

    def call(self, method, params=None):
        self._id += 1
        mid = self._id
        data = json.dumps({"id": mid, "method": method, "params": params or {}}).encode()
        mask = os.urandom(4)
        header = bytearray([0x81])
        ln = len(data)
        if ln < 126:
            header.append(0x80 | ln)
        elif ln < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", ln)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", ln)
        header += mask
        self.sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))
        while True:
            msg = self._recv_message()
            if msg is None:
                raise ConnectionError("socket closed")
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    def _recv_message(self):
        hdr = self._recv_exact(2)
        op = hdr[0] & 0x0F
        ln = hdr[1] & 0x7F
        if ln == 126:
            ln = struct.unpack(">H", self._recv_exact(2))[0]
        elif ln == 127:
            ln = struct.unpack(">Q", self._recv_exact(8))[0]
        if op == 0x9:  # ping -> pong
            self.sock.sendall(b"\x8a\x00")
            return self._recv_message()
        if op == 0x8:  # close
            return None
        payload = b""
        while len(payload) < ln:
            chunk = self.sock.recv(min(65536, ln - len(payload)))
            if not chunk:
                break
            payload += chunk
        if op == 0x1:
            return json.loads(payload.decode())
        if op == 0x2:
            return {"__binary__": payload}
        return self._recv_message()

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


def find_chrome():
    candidates = [
        os.environ.get("CHROME_PATH"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    raise SystemExit("Chrome not found. Set CHROME_PATH or pass --chrome.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8471)
    ap.add_argument("--out", default="docs/screenshots")
    ap.add_argument("--width", type=int, default=1440, help="viewport width (desktop)")
    ap.add_argument("--wait", type=float, default=4.0,
                    help="seconds to wait after navigation (reveal animations settle)")
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--debug-port", type=int, default=9223)
    args = ap.parse_args()

    chrome = args.chrome or find_chrome()
    os.makedirs(args.out, exist_ok=True)
    user_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chrome-profile")
    os.makedirs(user_dir, exist_ok=True)

    proc = subprocess.Popen(
        [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--no-proxy-server", f"--remote-debugging-port={args.debug_port}",
         f"--user-data-dir={user_dir}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{args.debug_port}/json/version", timeout=2)
                break
            except OSError:
                time.sleep(0.2)
        else:
            raise SystemExit("Chrome did not open its debug port")

        targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{args.debug_port}/json/list"))
        page = next(t for t in targets if t["type"] == "page")
        ws = WS(page["webSocketDebuggerUrl"])
        ws.call("Page.enable")
        # Deterministic desktop viewport regardless of OS window size
        ws.call("Emulation.setDeviceMetricsOverride",
                {"width": args.width, "height": 900,
                 "deviceScaleFactor": 1, "mobile": False})

        for name, path in PAGES:
            url = f"http://{args.host}:{args.port}{path}"
            ws.call("Page.navigate", {"url": url})
            time.sleep(args.wait)
            result = ws.call("Page.captureScreenshot",
                             {"format": "png", "captureBeyondViewport": True})
            data = base64.b64decode(result["data"])
            dest = os.path.join(args.out, name + ".png")
            with open(dest, "wb") as f:
                f.write(data)
            print(f"{name:10s} {len(data):8d} bytes -> {dest}")
        ws.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    sys.exit(main())
