# Mon language scoping report: can the app have real Mon translation capability?

Date: 2026-10-13. Prepared by the system for the project lead. American English.
Mon = ISO 639-3 `mnw` (Myanmar script). `mon` is Mongolian; filter on `mnw` everywhere.
Sources were fetched directly unless marked UNVERIFIED. Nothing was downloaded into the project.

## The short answer

- **Phrasebook-grade Mon: yes, with people.** Every tool needed to type, store, validate, display,
  and voice Mon already exists in the scaffold or in open repositories. What is missing is human
  translators and reviewers, and the partners for that are identifiable.
- **Open-domain machine translation for Mon: not today, but buildable to "draft quality."**
  No commercial or open model translates Mon. The raw material for a Mon–Burmese model is better
  than expected: two Mon news agencies publish the same stories in Mon and Burmese every day, which
  is document-aligned parallel text nobody has sentence-aligned yet. A 25,000-pair Mon–English
  corpus exists at the University of Computer Studies, Yangon (UCSY) but is unreleased. Realistic
  totals: 20,000 to 60,000 Mon–Burmese pairs and 10,000 to 25,000 Mon–English pairs. Comparable
  projects at that scale reach usable-but-imperfect output (chrF around 40). That is enough to
  draft phrases for humans to fix, not enough to speak to a patient unsupervised.
- **Recommendation:** keep the safety design as is (Mon is human-verified only). Add a
  "Mon drafting" pipeline on the maintainer side, not in the app: Burmese-pivot fine-tune of
  NLLB-200 plus the open Mon dictionaries, used to pre-fill the `mnw` slot as `machine` status
  for reviewers. Standardize on Myanmar-side Mon Unicode spelling with a Thai-Mon variant field.

## Part A. What you already have on this Mac (inventoried 2026-10-13)

### A1. `~/Downloads/Mon Dictionary.xlsx`
- A SEAlang export of H. L. Shorto, *A Dictionary of Modern Spoken Mon* (1962): 2,683 entries,
  five columns (English gloss, Mon orthography in Unicode, IPA, language, SEAlang id).
- Encoding is good: 985 cells use Mon-specific Unicode code points (U+1028, U+1033, U+1034,
  U+105A to U+1060), so the text is real Mon Unicode, not Burmese look-alikes or a legacy font.
- Coverage is the 1962 spoken vocabulary, not medicine. A probe of 58 everyday and clinical
  gloss words found: fever 1 ("to have a fever", ဇှ်), cough 1 (သ္ဍက်), blood 1 (ဆီ), vomit 1,
  pain/ache 2, breathe 1, but zero for pregnant, doctor, hospital, malaria, tablet, injection,
  wound, today, week, how. Modern clinical terms will come from partners, not from Shorto.
- License: SEAlang states the source is copyright 1962 H. L. Shorto, "used by permission of
  the Shorto family." It can sit on your laptop as a lookup aid; it cannot be committed to a
  public repository without written permission from SEAlang (CRCL) or the estate. The report
  recommends asking; a headword-plus-gloss subset for a non-commercial health tool is the kind
  of request SEAlang has granted before (UNVERIFIED; based on their stated policy only).

### A2. Mathias Jenny, *The Verb System of Mon* (302 pages)
- A full reference grammar (University of Zurich). Chapter 1 gives the phonology and the
  writing system; chapters 2 onward cover verbs, negation, aspect, modality, and sentence
  types, including interrogatives (1.4.1) and imperatives (1.4.2), which are exactly the two
  sentence types a clinical phrasebook is made of.
- Three facts from pages 37-41 that shape the software: (1) Mon spelling is not one-to-one
  with pronunciation; "there is often more than one way to write a given syllable," so
  search must be by orthography and by dictionary headword, never by phonetic guess;
  (2) Literary Mon (the written norm) and Spoken Mon diverge enough that a sentence written
  by a Myanmar-educated Mon reviewer may read as "bookish" to a Sangkhlaburi speaker; the
  record format should allow a spoken-register variant; (3) two major dialect groups
  (Pan Hla's comparative tables) exist, and the app's Mon audio must say which one it is.
- The PDF's Mon script is embedded in a legacy font, so the Mon examples do not copy out as
  Unicode; the grammar is a human reference, not machine-readable data.

### A3. Jenny's three shorter papers (Reference-Literature)
- "The Mon language: recipient and donor between Burmese and Thai" (23 pp.),
  "2000 years of history: the Mon language in Thailand and Myanmar" (Yangon seminar, 2015,
  35 pp.), and "Language Contact in Myanmar" (2011, 42 pp.). Together they document how much
  Burmese and Thai vocabulary sits inside modern Mon on each side of the border. Practical
  consequence: Thai-side Mon speakers in Kanchanaburi may use Thai loanwords for clinical
  concepts where Myanmar-side Mon uses Burmese loans. A single "Mon" column is not enough for
  terminology; the phrase record should carry an optional `mnw-TH` variant.

### A4. The Mon COVID-19 picture booklet (8 page images, `Covid19-Booklet-Mon-Language/`)
- Title ဝေၚ်ပါယဲကဝ်ရဝ်နာ ("Avoiding the corona disease"), illustrations by Elaine Vitikainen,
  content adapted from WHO advice, "Version 8.4.2020, Covid-19 Asian version, Mon."
  Six content pages: hand washing, do not touch the face, cough into the elbow, keep 2 meters,
  stay home when sick, get information from reliable sources.
- This is the only existing Mon-language health text found so far with simple, patient-facing
  sentences and pictures. The text is in the images only; it must be transcribed into Unicode
  by a Mon reader (or found as a text PDF, see Part B) before it can seed records.
- Its license and publisher are resolved in Part B.

### A5. The wider library (`Mon-History-Library/`, `Reference-Literature/`, phone photos)
- Mostly history, ethnography, and politics in English; valuable for the project's cultural
  framing and for partner outreach (Mon Forum issues in Mon, Burmese, and English;
  HURFOM and Rehmonnya reports; the Mon seminar at Chulalongkorn, 2007). Three items carry
  parallel text that could become bitext after extraction: the New Mon Forum issues published
  in both Mon and Burmese (2015-2019), the HURFOM FDI report in Burmese and English, and the
  Asia Foundation decentralization report in Burmese and English (no Mon). None is medical.
- The phone-photo folders ("Mon Heritage & Writing", 307 files) may contain photographed Mon
  signage or manuscripts; they were not opened.

## Part B. What exists online (survey of 2026-10-13)

### B1. Mon news media with Mon ↔ Burmese parallel stories (the key find)

| Outlet | Mon edition | Burmese edition | Size | Encoding | License |
|---|---|---|---|---|---|
| Independent Mon News Agency (IMNA) | https://mon.monnews.org/ (RSS /feed/), posts 2011 to today, ~406 pages | https://burmese.monnews.org/ (2017 to today) | roughly 10,000+ Mon posts | genuine Unicode with Mon-only code points | All rights reserved; permission needed |
| Thanlwin Times (Mawlamyine) | https://mon.thanlwintimes.com/ (RSS), ~864 pages × 15 posts ≈ 13,000 posts | https://burmese.thanlwintimes.com/ | ≈13,000 Mon posts; English edition ended May 2024 | Unicode | No license stated |

Verified from the RSS feeds on 2026-10-13: three of the five newest IMNA Mon items had same-day
Burmese counterparts (a dog-bite story in Thaton, a paddy-pest story, a Thayetchaung killing).
Thanlwin Times showed the same pattern. This is a comparable corpus at document level; sentence
alignment would need a Mon-aware aligner since Mon is absent from the usual multilingual
embedding models. Both outlets are also candidate partners for reviewers.

Other media: Guiding Star (IMNA's print monthly since 1999) has no website; DVB's ethnic radio
ended around 2014; RFA, BBC, and JW.org have no Mon service (JW.org's language list was checked
directly: nothing between Mongolian Sign Language and Montenegrin). HURFOM / rehmonnya.org
publish in English and Burmese only (UNVERIFIED for Mon). Facebook pages are not usable.

### B2. Religious and classical text: weaker than for most minority languages
- Mon Bible: one translation (British and Foreign Bible Society, NT 1847, full Bible 1928, last
  printed 1951). Available only as page scans on archive.org (about 165 images, some missing).
  No text edition exists on eBible.org or YouVersion. Faith Comes By Hearing has a Mon Bible app
  (UNVERIFIED contents). OCR with the open Mon OCR model (below) is the only route to text.
- Buddhist Mon: the iPitaka Mon iOS app (28 texts as PDFs), a FlipHTML5 library of a few hundred
  digitized books as page images, and the printed "Book of Four Languages" (English, Mon,
  Burmese, Pali) from Kharaik Sam Monastery in Ye, which is the main source of the UCSY corpus.

### B3. Health and NGO materials in Mon
- MIMU "Awareness Materials in Ethnic Languages": 13 Mon items with direct links, including
  two COVID audio messages, a "Prevention Ways of COVID-19" guide (PDF and JPG), four WHO /
  UNICEF / Gavi vaccine infographics, and a PSEA message after Cyclone Mocha.
  https://www.themimu.info/awareness-materials-ethnic-languages
  Burmese and English originals are not on the page and must be matched by hand. Whether the
  PDFs are text or images is UNVERIFIED (not downloaded).
- The COVID picture booklet in your folder belongs to a family of community literacy-team
  adaptations of one illustrated WHO text. The Akha edition (Akha Literacy Team, translator
  Ah Suhn, illustrations by Ari and Elaine Vitikainen, version 27.3.2020) is explicitly
  CC BY-NC-SA 4.0 with illustrations CC BY-NC 4.0. The Mon edition (version 8.4.2020) very
  likely carries the same license, but its PDF, publisher, and Burmese/English siblings were
  NOT found online. Next step: ask Elaine Vitikainen (ev-visuals.com) or the SIL-linked
  literacy teams in Myanmar for the Mon text file and the English source.
- Mon National Education Committee textbooks (UNICEF-funded, tens of thousands printed) have
  no public PDFs. The Mon National Health Committee website was suspended at fetch time.
- A CC0 Mon audio course by Ven. Nai Suriya (8 lessons, 66 MB) exists on archive.org, and
  Jenny's 11-page "Short Introduction to the Mon Language" (2001) uses a legacy font.

### B4. Lexical data (open, machine-readable)

| Resource | Size | Languages | License |
|---|---|---|---|
| Nenemin95/mon-eng-mya-pali-lexicon (Hugging Face) | 9,488 rows with part of speech | Mon, English, Burmese, Pali | CC BY 4.0 |
| Nenemin95/mon_eng_dict_instructions | 112,324 rows (dictionary entries recast as instructions) | Mon, English | CC BY 4.0 |
| Nenemin95/mon-words-dataset | 18,523 Mon words/phrases from a keyboard app | Mon | CC BY 4.0 |
| MonDictDB (github.com/Barnista/MonDictDB) | CSV, about 1 MB each; Mon–Thai dictionary plus processed form | Mon, Thai, Burmese | MIT |
| English Wiktionary Mon lemmas / Kaikki export | 1,059 lemmas, ~1,700 senses | Mon to English | CC BY-SA |
| Mon Wikipedia | 4,542 articles, ~10 million indexed words | Mon | CC BY-SA |
| Your SEAlang Shorto export | 2,683 entries with IPA | Mon, English | copyright; permission needed |
| Nai Tun Way, Modern Mon-English Dictionary (2000, 1,308 pp) | print only | Mon, English | copyright |

MonDictDB matters for Kanchanaburi because it is the only Mon–Thai lexical resource found.
Spellcheckers: none exist for Mon. Keyboards: five on Keyman, two MIT-licensed
(`mon_anonta`, `sil_mon`), with a 17 MB Mon predictive-text wordlist on GitHub.

### B5. Mon NLP work and tooling
- UCSY paper (Tun, Shwe Sin, Soe, IAENG Int. J. Computer Science 52(11), 2025): ~25,000
  Mon–English pairs from the "Book of Four Languages," Nai Sac Lun's English grammar in Mon,
  and manually translated UCSY sentences; topics include "healthcare and emergency services."
  Best results BLEU 41 (Mon to English) and 27 to 39 (English to Mon) in-domain. No release URL.
  https://www.iaeng.org/IJCS/issues_v52/issue_11/IJCS_52_11_11.pdf
- MonDevHub (github.com/MonDevHub): awesome-mon-nlp list; MonCorpusCollection (1.25 million
  lines, 124 MB, monolingual, mixed licenses with IMNA and social-media shards unresolved);
  monocr (Mon OCR, ONNX, CER 0.01 on synthetic lines, untested on scans); mon-language-detector;
  a Mon tokenizer; a legacy-font-to-Unicode converter (talachanmon/mon2uni-Converter).
- wikilangs/mnw: MIT tokenizers, n-grams, embeddings from Mon Wikipedia.
- Speech: Meta MMS covers Mon (ASR, TTS, language ID); Meta's Omnilingual ASR (Nov 2025) lists
  `mnw_Mymr`. Audio data: freococo "RFA Mon Language Voices," 14.8 hours, 3,634 clips, no
  transcripts, non-commercial. Common Voice has no Mon. The MMS Mon voice model is already
  installed on this Mac's project environment but has not been run (no Mon text yet).
- Hugging Face `language:mnw`: 82 datasets tagged; substantive ones are Wikipedia, FineWeb-2
  (6 MB), finetranslations (32 MB of Mon web text machine-translated to English by Gemma 3,
  synthetic), MADLAD-400 data (3 MB), GlotCC, UDHR, Bloom Library books, and the sets above.
  MADLAD-400's 3B translation model does NOT list Mon in its README; treat MADLAD Mon
  translation as unsupported (corrects the earlier dossier).

### B6. Orthography and variation (what the validator must know)
- Real Mon text on the news sites uses U+105A ၚ, U+105C ၜ, U+105E ၞ, U+105F ၟ, U+1060 ၠ,
  U+1033 ဳ, U+1034 ဴ plus the shared Burmese letters. The scaffold validator already allows
  these for `mnw` and rejects them for `my` (where they signal Zawgyi).
- Thai Mon and Burma Mon share the script and mostly the spelling; differences are mainly
  phonetic, plus distinct Thai-Mon letter shapes that Unicode treats as font variants (Padauk
  has a `mnw-TH` feature). All digital corpora are Burma Mon. Rule: store Myanmar-side spelling;
  allow an optional `mnw-TH` wording variant; render with Padauk.
- No official standardization body. De facto norms come from the Mon Literature and Culture
  Committees (Yangon, Mawlamyine) and the Mon National Education Committee curriculum.
- Legacy non-Unicode Mon fonts persist (an iOS keyboard app ships one). The validator should
  run a legacy-font detector on pasted input (mon-language-detector plus mon2uni logic).

## Part C. What "real translation capability" would take

### C1. Three tiers, from cheapest to hardest

| Tier | What it gives | Data needed | Effort | Verdict |
|---|---|---|---|---|
| 1. Verified phrasebook (current design) | Exact, safe sentences with audio | none; human translators | partner time, ~2 weeks of a translator for 300 phrases | Do first |
| 2. Term lookup and assisted drafting | Mon word suggestions for reviewers; draft Mon from Burmese | the open lexicons (B4) plus your Shorto export | 1 to 2 weeks of engineering | Do second |
| 3. Mon–Burmese neural MT (Burmese pivot) | "Draft quality" sentence translation, chrF ~40 | 20k to 60k aligned news pairs with IMNA / Thanlwin permission, plus the UCSY corpus if shared | 4 to 8 weeks plus GPU time; needs an aligner for Mon | Research project, maintainer-side only |

Tier 3 never goes into the patient-facing app under the safety policy. It feeds reviewers.

### C2. Pivot through Burmese, not English
Burmese is well supported by NLLB-200 and MADLAD, Mon borrows heavily from Burmese, the script
is shared, and the parallel news text is Mon–Burmese. The sensible model is: Thai or English
to Burmese with an existing model, Burmese to Mon with the fine-tuned model, each step shown
to a reviewer. English-to-Mon directly has only the unreleased UCSY data behind it.

### C3. Concrete next actions, in order
1. Ask the lead to contact three people: UCSY (Khin Mar Soe) for the 25k Mon–English corpus;
   IMNA and Thanlwin Times for permission to align their Mon–Burmese archives for a
   non-commercial health tool; Elaine Vitikainen or the literacy team for the Mon COVID
   booklet text. Draft emails can be written on request.
2. Add the open lexicons (Nenemin95 lexicon, MonDictDB, Wiktionary export) to the repo as a
   `content/lexicon/mnw/` folder with their licenses, and build a reviewer-side term lookup
   in the Record and contribution pages. This is additive and license-clean.
3. Run the MMS Mon voice on a first batch of human-translated phrases to test intelligibility
   with Mon speakers in Sangkhlaburi before relying on it.
4. Add `mnw-TH` as an optional variant field in the phrase schema, and a legacy-font check in
   the validator.
5. Only after 1 and 2: a maintainer-side alignment and fine-tuning experiment on the news
   corpus, reported with chrF against a held-out set of the UCSY health phrases.

### C4. What this changes in the earlier dossier
- MADLAD-400 Mon translation support: listed as "listed" in the dossier; the model README does
  not include Mon. Corrected to unsupported.
- Mon–English open bitext: the dossier said ~10k pairs (OPUS); add the synthetic
  finetranslations set and the OCR-able 1951 Bible as possible sources, and the unreleased
  25k UCSY corpus as the prize.
- Mon news sites were not in the dossier; they are now the main Mon–Burmese data source.

## Flagged UNVERIFIED
Mon COVID booklet PDF, publisher, and siblings; MIMU PDFs text-vs-image; FCBH Bible app
contents; Global Recordings Network Mon audio details; UNICEF "Mother Teach Me" Mon edition;
Bloom Library Mon book count; PanLex Mon coverage; HURFOM / Kao Wao Mon editions; whether
RFA Burmese aired Mon segments; SEAlang's willingness to license the Shorto export.
