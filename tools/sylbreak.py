"""Syllable breaking for Burmese and Mon.

The regular expressions are taken from sylbreak4all by Ye Kyaw Thu and
contributors (MIT License, https://github.com/ye-kyaw-thu/sylbreak4all),
languages "bm" (Burmese) and "mo" (Mon). Reference: Ye Kyaw Thu et al. (2021),
"sylbreak4all: Regular expression based syllable breaking tool for nine major
ethnic languages of Myanmar", iSAI-NLP 2021.

Why it matters here: browsers wrap all Myanmar-script text with a Burmese
dictionary, which breaks Mon in the wrong places. The build step inserts a
zero-width space (U+200B) between syllables so wrapping is always safe.
"""
from __future__ import annotations

import re

MY_CONSONANT = r"က-အ"
EN_CHAR = r"a-zA-Z0-9"
SS_SYMBOL = "္"  # virama (asat stacker)
ATHAT = "်"
OTHER_CHAR = r"ဣဤဥဦဧဩဪဿ၌၍၎၏၀-၉႐-႙၊။!-/:-@[-`’“”{-~\s…"
MO_CONSONANT = r"ကခဂဃၚစဆဇၛဉညဋဌဍဎဏတထဒဓနပဖဗဘမယရလဝသဟဠၜအၝ"

PATTERNS = {
    "my": re.compile(rf"((?<!{SS_SYMBOL})[{MY_CONSONANT}](?![{ATHAT}{SS_SYMBOL}])|[{EN_CHAR}{OTHER_CHAR}])"),
    "mnw": re.compile(rf"((?<!{SS_SYMBOL})[{MO_CONSONANT}](?![{ATHAT}{SS_SYMBOL}])|[{EN_CHAR}{OTHER_CHAR}])"),
}

ZWSP = "​"


def syllables(text: str, lang: str) -> list[str]:
    """Split text into syllables. lang is 'my' or 'mnw'. Whitespace is kept as its own token."""
    pattern = PATTERNS[lang]
    marked = pattern.sub(lambda m: "\u0001" + m.group(1), text)
    return [s for s in marked.split("\u0001") if s != ""]


def with_zwsp(text: str, lang: str) -> str:
    """Return text with a zero-width space between syllables (not next to existing whitespace)."""
    out: list[str] = []
    for i, syl in enumerate(syllables(text, lang)):
        if i > 0 and not syl[0].isspace() and not out[-1][-1].isspace():
            out.append(ZWSP)
        out.append(syl)
    return "".join(out)


if __name__ == "__main__":
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else "my"
    for line in sys.stdin:
        print("|".join(syllables(line.rstrip("\n"), lang)))
