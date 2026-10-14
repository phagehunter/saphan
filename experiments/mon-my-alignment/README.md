# Mon–Burmese alignment experiment (pilot)

Goal: build the first Mon–Burmese parallel sentence corpus from news outlets that publish the
same stories in both languages, so a Burmese-pivot translation model can draft Mon phrases for
human reviewers (never patient-facing; see `docs/safety-policy.md`).

## Permission status

Permission requests went to IMNA (chiefeditor@monnews.org) and Thanlwin Times
(thanlwintime@gmail.com) on 2026-10-14. **Until they answer, this experiment touches only the
public RSS feeds (about ten recent posts per edition) and nothing is committed except code.**
`data/` is git-ignored. The archive crawl, sentence corpus release, and model training wait for
written permission.

## Pipeline (standard-library Python, run with `python3 -I`)

| Step | Script | What it does |
|---|---|---|
| 1 | `fetch_feeds.py` | pulls the Mon and Burmese RSS feeds of both outlets into `data/raw/<outlet>.<lang>.jsonl`. monnews.org returns 403 to scripts (bot filter); its feeds were captured through a browser and saved by hand. |
| 2 | `pair_documents.py` | pairs Mon and Burmese posts of the same outlet published within two days whose titles and leads share lexicon anchors (Mon↔Burmese entries from the open Nenemin95 lexicon, matched on syllable n-grams via sylbreak4all) plus Latin names and large figures. Day-of-month numbers are ignored because every dateline has them. One-to-one, greedy by score, requires at least two lexicon anchors. |
| 3 | `align_sentences.py` | splits paired articles at the Myanmar full stop (။), drops photo captions and feed boilerplate, and aligns with dynamic programming over 1-1, 1-2, 2-1 beads: cost = syllable-length mismatch (Mon runs about 15% longer) minus lexicon-anchor and name evidence. Writes `data/aligned/<outlet>.tsv` with a confidence score per bead. |
| shared | `lexicon.py` | anchor table (6,749 Mon syllable-string keys), syllable segmentation, name and figure extraction. |

## Pilot results, 2026-10-14

| Outlet | Posts (Mon × Burmese) | Document pairs | Sentence beads | Beads with evidence (score > 0) |
|---|---|---|---|---|
| IMNA | 10 × 10 | 2 | 29 | 14 |
| Thanlwin Times | 10 × 10 | 1 | 3 | 2 |

All three document pairs are correct on inspection (a drone strike in Kyaikto township, fighting
near Pulin village, the junta's reshuffle of civil and military posts). The highest-scoring
beads match sentence for sentence, for example the list of villages held by the KNLA in Tangon
Taing village tract, and the October 2 artillery fire from Division 44 headquarters with the
same 120 mm figure on both sides. Beads near zero are plausible but unconfirmed; negative beads
are usually the aligner bridging a sentence that has no counterpart.

Before the number-weighting fix, shared datelines produced four wrong pairs out of six; the
lexicon-first score removed them at the cost of recall (two IMNA stories that likely have
counterparts were not paired because their titles share no lexicon entry).

## What this says about the full archive

Roughly a fifth to a third of posts find a counterpart with the strict score; the earlier
research estimated 10,000 to 13,000 Mon posts per outlet. That points to 2,000 to 6,000
document pairs and 20,000 to 60,000 beads, matching the scoping report's range, with perhaps a
third of beads at high confidence without human checking.

## Next steps (in order)

1. Permission from IMNA and Thanlwin Times, then crawl the archives politely (one request per
   second, cached, with the project's contact in the user agent).
2. Improve recall: expand the anchor table with the MonDictDB Mon–Thai–Burmese entries and with
   frequent name transliterations learned from confirmed pairs; try pairing on the full body,
   not only title and lead.
3. Have a Mon-and-Burmese bilingual reviewer grade 200 random beads to measure precision and
   set a confidence threshold.
4. Fine-tune NLLB-200 (Burmese-initialized) on the high-confidence beads; evaluate with chrF on
   the UCSY health phrases if that corpus is shared.

## Run it

```bash
python3 -I experiments/mon-my-alignment/fetch_feeds.py
```

```bash
python3 -I experiments/mon-my-alignment/pair_documents.py
```

```bash
python3 -I experiments/mon-my-alignment/align_sentences.py
```
