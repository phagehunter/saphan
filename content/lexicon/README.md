# Mon lexicon sources (reviewer-side term lookup)

These files feed the Lexicon screen in the app, a term lookup for translators and reviewers.
They are never shown to patients and never used to assemble sentences automatically.

| File | Source | Entries | Languages | License |
|---|---|---|---|---|
| `sources/nenemin95-mon-eng-mya-pali-lexicon.json` | https://huggingface.co/datasets/Nenemin95/mon-eng-mya-pali-lexicon (`Combined_Mon_Dict_AI_Format.json`) | 9,488 | Mon, English, Burmese, Pali | CC BY 4.0 |
| `sources/mondictdb-mon-thai-dict-processed.csv` | https://github.com/Barnista/MonDictDB (`csv/mon-thai-dict-processed.csv`) | 18,667 | Mon, Thai gloss, Thai pronunciation, part of speech | MIT (see `sources/LICENSE-MonDictDB.txt`) |

Downloaded 2026-10-13. Build the app file with:

```bash
python3 -m tools.build_lexicon
```

which writes `app/static/lexicon/mnw.json` (normalized, deduplicated, compact). The app loads
that file only when the Lexicon screen is opened, so the core phrasebook stays small.

Not included on purpose: the SEAlang export of Shorto's 1962 dictionary on the project lead's
laptop (copyright, permission not yet requested).
