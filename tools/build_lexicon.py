"""Build the reviewer-side Mon lexicon for the app.

    python3 -m tools.build_lexicon

Reads content/lexicon/sources/* (see content/lexicon/README.md for licenses) and writes
app/static/lexicon/mnw.json as a compact array of entries:
    [mon, english, burmese, thai, thai_pronunciation, part_of_speech, source]
Strings are NFC-normalized and trimmed; exact duplicate (mon, gloss) pairs are dropped.
"""
from __future__ import annotations

import csv
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "lexicon" / "sources"
OUT = ROOT / "app" / "static" / "lexicon" / "mnw.json"


def norm(s: str | None) -> str:
    return unicodedata.normalize("NFC", (s or "").replace("﻿", "")).strip()


def main() -> int:
    rows: list[list[str]] = []
    seen: set[tuple[str, str]] = set()

    data = json.loads((SRC / "nenemin95-mon-eng-mya-pali-lexicon.json").read_text(encoding="utf-8"))
    for r in data:
        mon, en, my = norm(r.get("Mon")), norm(r.get("English")), norm(r.get("Myanmar"))
        if not mon or not (en or my):
            continue
        key = (mon, en or my)
        if key in seen:
            continue
        seen.add(key)
        rows.append([mon, en, my, "", "", norm(r.get("Part of speech")), "nenemin95"])

    with (SRC / "mondictdb-mon-thai-dict-processed.csv").open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            mon, th = norm(r.get("mon")), norm(r.get("th"))
            if not mon or not th:
                continue
            key = (mon, th)
            if key in seen:
                continue
            seen.add(key)
            rows.append([mon, "", "", th, norm(r.get("pronunciation")), norm(r.get("pos")), "mondictdb"])

    rows.sort(key=lambda r: r[0])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"fields": ["mon", "en", "my", "th", "th_pron", "pos", "src"], "entries": rows}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    size = OUT.stat().st_size
    print(f"{len(rows)} lexicon entries -> {OUT.relative_to(ROOT)} ({size/1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
