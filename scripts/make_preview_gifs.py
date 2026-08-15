#!/usr/bin/env python3
"""Scrolling GIF previews of the Nexify site for the README gallery.

The modern portfolio pattern: instead of static screenshots, show each
page as a short looping GIF that scrolls through it. Uses the same CDP
WebSocket helper as capture_screenshots.py (stdlib only).

Usage:
    python scripts/make_preview_gifs.py [--host 127.0.0.1] [--port 8471]
                                        [--out docs/screenshots]
                                        [--frames 20] [--width 720]
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capture_screenshots import WS, PAGES, find_chrome  # noqa: E402

from PIL import Image


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8471)
    ap.add_argument("--out", default="docs/screenshots")
    ap.add_argument("--frames", type=int, default=20)
    ap.add_argument("--width", type=int, default=720,
                    help="output GIF width (scaled down from 1440 viewport)")
    ap.add_argument("--wait", type=float, default=3.5)
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--debug-port", type=int, default=9224)
    ap.add_argument("--pages", default=None,
                    help="comma-separated page names (default: all)")
    args = ap.parse_args()

    chrome = args.chrome or find_chrome()
    os.makedirs(args.out, exist_ok=True)
    user_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chrome-profile-gif")
    os.makedirs(user_dir, exist_ok=True)

    if args.pages:
        wanted = {p.strip() for p in args.pages.split(",")}
        pages = [(n, u) for n, u in PAGES if n in wanted]
    else:
        pages = PAGES

    proc = subprocess.Popen(
        [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--no-proxy-server", f"--remote-debugging-port={args.debug_port}",
         f"--user-data-dir={user_dir}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        import urllib.request
        for _ in range(50):
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{args.debug_port}/json/version", timeout=2)
                break
            except OSError:
                time.sleep(0.2)
        else:
            raise SystemExit("Chrome did not open its debug port")

        targets = json.load(urllib.request.urlopen(
            f"http://127.0.0.1:{args.debug_port}/json/list"))
        page = next(t for t in targets if t["type"] == "page")
        ws = WS(page["webSocketDebuggerUrl"])
        ws.call("Page.enable")
        ws.call("Emulation.setDeviceMetricsOverride",
                {"width": args.width * 2, "height": 900,
                 "deviceScaleFactor": 1, "mobile": False})

        total = 0
        for name, path in pages:
            url = f"http://{args.host}:{args.port}{path}"
            ws.call("Page.navigate", {"url": url})
            time.sleep(args.wait)

            height = ws.call("Runtime.evaluate", {
                "expression": "document.documentElement.scrollHeight"})
            page_h = int(height["result"]["value"])
            vh = 900
            # ~4 frames per viewport → smooth scroll, proportional to page length
            n = max(8, min(args.frames, round((page_h / vh) * 4)))
            step = max(1, (page_h - vh) / max(1, n - 1))

            frames = []
            for i in range(n):
                y = int(round(i * step))
                ws.call("Runtime.evaluate", {
                    "expression": f"window.scrollTo(0, {y})"})
                time.sleep(0.22)
                shot = ws.call("Page.captureScreenshot", {"format": "png"})
                img = Image.open(
                    __import__("io").BytesIO(base64.b64decode(shot["data"])))
                img = img.convert("RGB")
                scale = args.width / img.size[0]
                frames.append(img.resize(
                    (args.width, int(img.size[1] * scale)), Image.LANCZOS))

            dest = os.path.join(args.out, name + ".gif")
            frames[0].save(dest, save_all=True, append_images=frames[1:],
                           duration=240, loop=0, optimize=True)
            size = os.path.getsize(dest)
            total += size
            print(f"{name:10s} {len(frames):2d} frames  {size/1024:7.0f} KB -> {dest}")
        print(f"TOTAL: {total/1024/1024:.2f} MB")
        ws.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    sys.exit(main())
