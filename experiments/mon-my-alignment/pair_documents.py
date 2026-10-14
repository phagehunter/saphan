"""Pair Mon and Burmese posts of the same outlet that report the same story.

Score = lexicon anchors shared between titles+leads, plus shared figures and Latin names, minus a
penalty for publication dates more than two days apart. One-to-one pairing, greedy by score.
Writes data/pairs/<outlet>.jsonl and prints a table for human inspection.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python3 -I from anywhere
from lexicon import Anchors

HERE = Path(__file__).resolve().parent
RAW, PAIRS = HERE / "data" / "raw", HERE / "data" / "pairs"


def load(outlet: str, lang: str) -> list[dict]:
    p = RAW / f"{outlet}.{lang}.jsonl"
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def when(d: str) -> datetime | None:
    try:
        return parsedate_to_datetime(d)
    except Exception:  # noqa: BLE001
        return None


def main() -> int:
    anchors = Anchors()
    PAIRS.mkdir(parents=True, exist_ok=True)
    for outlet in ("imna", "thanlwin"):
        mon, my = load(outlet, "mnw"), load(outlet, "my")
        if not mon or not my:
            print(f"{outlet}: missing a side ({len(mon)} mon, {len(my)} my)")
            continue
        cands = []
        for i, m in enumerate(mon):
            for j, b in enumerate(my):
                dm, db = when(m["date"]), when(b["date"])
                gap = abs((dm - db).days) if dm and db else 9
                if gap > 2:
                    continue
                head_m = m["title"] + "\n" + m["text"][:500]
                head_b = b["title"] + "\n" + b["text"][:500]
                lex, ent = anchors.shared(head_m, head_b)
                # Lexicon anchors are the primary evidence; names and large figures confirm.
                score = 1.5 * lex + ent - 0.75 * gap
                if lex >= 2 and score >= 4:
                    cands.append((score, lex, ent, gap, i, j))
        cands.sort(reverse=True)
        used_m, used_b, pairs = set(), set(), []
        for score, lex, ent, gap, i, j in cands:
            if i in used_m or j in used_b:
                continue
            used_m.add(i); used_b.add(j)
            pairs.append({"score": score, "lexicon_anchors": lex, "shared_entities": ent, "day_gap": gap, "mon": mon[i], "my": my[j]})
        (PAIRS / f"{outlet}.jsonl").write_text("\n".join(json.dumps(p, ensure_ascii=False) for p in pairs) + "\n", encoding="utf-8")
        print(f"\n{outlet}: {len(mon)} Mon x {len(my)} Burmese posts -> {len(pairs)} pairs")
        for p in pairs:
            print(f"  score {p['score']:.1f} (lex {p['lexicon_anchors']}, ent {p['shared_entities']}, gap {p['day_gap']}d)")
            print(f"    MON {p['mon']['title'][:80]}")
            print(f"    MYA {p['my']['title'][:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
