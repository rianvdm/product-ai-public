#!/usr/bin/env python3
"""Render a visual-eli5 share card (og-card.html) to og.png with headless Chrome.

    python3 build-og.py PAGE_DIR            # PAGE_DIR/og-card.html -> PAGE_DIR/og.png
    python3 build-og.py CARD.html OUT.png   # explicit paths

Standard library only, same Chrome discovery as check-page.py. The card is a
self-contained 1200x630 HTML file; the PNG is verified to have those dimensions.
"""

from __future__ import annotations

import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

WIDTH, HEIGHT = 1200, 630

_STANDARD_CHROME_PATHS = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/google-chrome-stable"),
    Path("/usr/bin/chromium"),
    Path("/usr/bin/chromium-browser"),
)


def find_chrome() -> Path | None:
    override = os.environ.get("CHROME_BIN")
    if override and Path(override).exists():
        return Path(override)
    for candidate in _STANDARD_CHROME_PATHS:
        if candidate.exists():
            return candidate
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return Path(found)
    return None


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise SystemExit(f"{path} is not a PNG")
    return struct.unpack(">II", header[16:24])


def main(argv: list[str]) -> int:
    if len(argv) == 2:
        page_dir = Path(argv[1]).resolve()
        card, out = page_dir / "og-card.html", page_dir / "og.png"
    elif len(argv) == 3:
        card, out = Path(argv[1]).resolve(), Path(argv[2]).resolve()
    else:
        print(__doc__, file=sys.stderr)
        return 2
    if not card.is_file():
        print(f"missing card: {card}", file=sys.stderr)
        return 1
    chrome = find_chrome()
    if chrome is None:
        print("no Chrome binary found (set CHROME_BIN)", file=sys.stderr)
        return 1
    args = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={WIDTH},{HEIGHT}",
        "--virtual-time-budget=3000",
        f"--screenshot={out}",
        card.as_uri(),
    ]
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    width, height = png_size(out)
    if (width, height) != (WIDTH, HEIGHT):
        print(f"{out} is {width}x{height}, expected {WIDTH}x{HEIGHT}", file=sys.stderr)
        return 1
    print(f"wrote {out} ({width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
