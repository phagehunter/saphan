"""Sentence-align paired Mon/Burmese articles.

Sentences end at the Myanmar-script full stop (။). Alignment is dynamic programming over
1-1, 1-2, 2-1 beads (Gale-Church style): cost = length mismatch in syllables, reduced by lexicon
anchors shared between the bead's sentences. Writes data/aligned/<outlet>.tsv
(score, mon, my) and prints a quality summary with sample beads.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python3 -I from anywhere
from lexicon import Anchors, syls

HERE = Path(__file__).resolve().parent
PAIRS, ALIGNED = HERE / "data" / "pairs", HERE / "data" / "aligned"
RATIO = 1.15  # Mon runs ~15% longer than Burmese in syllables (estimated from the pilot; tune later)


BOILERPLATE = re.compile(r"Photo\s*[-–—]|\[…\]|\[&#8230;\]|appeared first on|^ပရိုၚ်-|^သတင်း-|^Source\b", re.I)


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=။)\s*|\n+", text)
    return [p.strip() for p in parts if len(p.strip()) >= 6 and not BOILERPLATE.search(p)]


def cost(anchors: Anchors, mon: list[str], my: list[str]) -> float:
    lm = sum(len(syls(s, "mnw")) for s in mon)
    lb = sum(len(syls(s, "my")) for s in my) * RATIO
    if lm == 0 or lb == 0:
        return 10.0
    length_term = abs(math.log((lm + 1) / (lb + 1))) * 4
    lex, ent = anchors.shared(" ".join(mon), " ".join(my))
    return length_term - 1.2 * lex - 2.0 * ent + (1.5 if len(mon) + len(my) > 2 else 0.0)


def align(anchors: Anchors, mon: list[str], my: list[str]) -> list[tuple[float, str, str]]:
    n, m = len(mon), len(my)
    INF = float("inf")
    best = [[INF] * (m + 1) for _ in range(n + 1)]
    back: list[list[tuple[int, int] | None]] = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    beads = [(1, 1), (1, 2), (2, 1), (1, 0), (0, 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if best[i][j] == INF:
                continue
            for di, dj in beads:
                ii, jj = i + di, j + dj
                if ii > n or jj > m:
                    continue
                c = 6.0 if (di == 0 or dj == 0) else cost(anchors, mon[i:ii], my[j:jj])
                if best[i][j] + c < best[ii][jj]:
                    best[ii][jj] = best[i][j] + c
                    back[ii][jj] = (di, dj)
    out = []
    i, j = n, m
    while (i, j) != (0, 0):
        di, dj = back[i][j]  # type: ignore[misc]
        if di and dj:
            out.append((-cost(anchors, mon[i - di : i], my[j - dj : j]), " ".join(mon[i - di : i]), " ".join(my[j - dj : j])))
        i, j = i - di, j - dj
    return list(reversed(out))


def main() -> int:
    anchors = Anchors()
    ALIGNED.mkdir(parents=True, exist_ok=True)
    total = 0
    for pf in sorted(PAIRS.glob("*.jsonl")):
        rows = []
        for line in pf.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            p = json.loads(line)
            ms, bs = sentences(p["mon"]["text"]), sentences(p["my"]["text"])
            if len(ms) < 2 or len(bs) < 2:
                continue
            for score, a, b in align(anchors, ms, bs):
                rows.append((score, a, b, p["mon"]["link"]))
        out = ALIGNED / (pf.stem + ".tsv")
        out.write_text("score\tmon\tmy\tsource\n" + "\n".join(f"{s:.2f}\t{a}\t{b}\t{u}" for s, a, b, u in rows) + "\n", encoding="utf-8")
        good = [r for r in rows if r[0] > 0]
        total += len(rows)
        print(f"{pf.stem}: {len(rows)} aligned beads, {len(good)} with positive confidence (lexical or entity evidence)")
        for s, a, b, _ in sorted(rows, reverse=True)[:5]:
            print(f"  [{s:+.1f}] MON {a[:90]}")
            print(f"         MYA {b[:90]}")
    print(f"\ntotal beads: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
