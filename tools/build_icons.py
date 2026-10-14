"""Bundle the Health Icons SVGs the content uses into one JSON map for the app.

    python3 -m tools.build_icons   ->  app/src/lib/icons/health.json

Each SVG is reduced to its viewBox and inner markup with fills set to currentColor, so the app
can color it with CSS and inline it without extra network requests.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "icons" / "healthicons"
OUT = ROOT / "app" / "src" / "lib" / "icons" / "health.json"


def main() -> int:
    icons: dict[str, dict[str, str]] = {}
    for svg in sorted(SRC.glob("*.svg")):
        name = svg.stem.replace("__", "/")
        text = svg.read_text(encoding="utf-8")
        m = re.search(r'viewBox="([^"]+)"', text)
        inner = re.sub(r"^.*?<svg[^>]*>", "", text, count=1, flags=re.S)
        inner = re.sub(r"</svg>\s*$", "", inner, flags=re.S)
        inner = re.sub(r'fill="(?!none)[^"]*"', 'fill="currentColor"', inner)
        inner = re.sub(r'stroke="(?!none)[^"]*"', 'stroke="currentColor"', inner)
        inner = re.sub(r"\s+", " ", inner).strip()
        icons[name] = {"viewBox": m.group(1) if m else "0 0 48 48", "body": inner}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(icons, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"{len(icons)} icons -> {OUT.relative_to(ROOT)} ({OUT.stat().st_size/1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
