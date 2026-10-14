"""Mon <-> Burmese lexical anchors from the open Nenemin95 lexicon (CC BY 4.0), plus syllable
segmentation (sylbreak4all regexes, MIT) so that Mon and Burmese text can be compared without
word boundaries."""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.sylbreak import syllables  # noqa: E402

LEX = ROOT / "content" / "lexicon" / "sources" / "nenemin95-mon-eng-mya-pali-lexicon.json"
MY_DIGITS = str.maketrans("၀၁၂၃၄၅၆၇၈၉", "0123456789")


def norm(s: str) -> str:
    return unicodedata.normalize("NFC", s).replace("​", "").strip()


def syls(text: str, lang: str) -> list[str]:
    """Syllables without whitespace or punctuation."""
    out = []
    for s in syllables(norm(text), lang):
        s = s.strip()
        if s and not re.fullmatch(r"[\s၊။,.;:!?()\[\]\"'«»…\-–—/]+", s):
            out.append(s)
    return out


def load_anchor_table() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Map Mon syllable n-grams (1-3) to Burmese syllable n-grams from lexicon entries, and back."""
    mon2my: dict[str, set[str]] = defaultdict(set)
    my2mon: dict[str, set[str]] = defaultdict(set)
    for r in json.loads(LEX.read_text(encoding="utf-8")):
        mon, my = norm(r.get("Mon") or ""), norm(r.get("Myanmar") or "")
        if not mon or not my:
            continue
        # Entries are often short phrases; keep ones up to 6 syllables on each side.
        ms, bs = syls(mon, "mnw"), syls(my, "my")
        if not ms or not bs or len(ms) > 6 or len(bs) > 6:
            continue
        mkey, bkey = "".join(ms), "".join(bs)
        mon2my[mkey].add(bkey)
        my2mon[bkey].add(mkey)
    return mon2my, my2mon


def ngrams(sy: list[str], nmax: int = 4) -> set[str]:
    out = set()
    for n in range(1, nmax + 1):
        for i in range(len(sy) - n + 1):
            out.add("".join(sy[i : i + n]))
    return out


def latin_tokens(text: str) -> set[str]:
    """Latin-script names and acronyms (KNLA, CRPH, A1) that survive translation unchanged."""
    return set(re.findall(r"[A-Za-z][A-Za-z0-9]{1,}", text))


def figures(text: str) -> set[str]:
    """Numbers that carry story identity: anything with 3+ digits or outside the 1-31 day range.
    Day-of-month and small counts occur in every dateline, so they are excluded."""
    t = text.translate(MY_DIGITS)
    out = set()
    for n in re.findall(r"\d+", t):
        if len(n) >= 3 or int(n) > 31:
            out.add(n)
    return out


def latin_and_numbers(text: str) -> set[str]:
    return latin_tokens(text) | figures(text)


class Anchors:
    def __init__(self) -> None:
        self.mon2my, self.my2mon = load_anchor_table()

    def shared(self, mon_text: str, my_text: str) -> tuple[int, int]:
        """(number of lexicon anchors shared, number of Latin/number tokens shared)."""
        mg = ngrams(syls(mon_text, "mnw"))
        bg = ngrams(syls(my_text, "my"))
        hits = 0
        for g in mg:
            targets = self.mon2my.get(g)
            if targets and targets & bg:
                hits += 1
        ln = 2 * len(latin_tokens(mon_text) & latin_tokens(my_text)) + len(figures(mon_text) & figures(my_text))
        return hits, ln


if __name__ == "__main__":
    a = Anchors()
    print("lexicon anchor keys:", len(a.mon2my))
    print(a.shared("ကောန်ၚာ် (၆) တၠပါလုပ်ကီု", "ကလေးငယ် ၆ ဦး"))
