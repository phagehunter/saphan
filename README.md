# Saphan (สะพาน)

**Verified health phrases in Thai, Burmese, Mon, and English, with audio, for health volunteers
on the Thailand–Myanmar border.**

Live app: **https://curtishoffmann.com/saphan/** (works offline after the first visit)

Saphan is a free, open-source phrasebook for village health volunteers (อสม.), migrant health
volunteers (อสต.), and clinic staff in Kanchanaburi, Thailand, who serve Burmese- and
Mon-speaking patients. A volunteer taps a phrase in Thai; the patient sees and hears it in
Burmese or Mon. Every translation carries a visible review badge, and nothing unreviewed ever
reaches a patient.

*Saphan* means "bridge" in Thai. It is a working name.

## Why

Under one in ten Myanmar workers in Thailand can read Thai. Interpreters are scarce outside
large hospitals. Machine translation covers Burmese unevenly and does not cover Mon at all.
Studies of machine translation in clinics find it acceptable for brief, everyday exchanges and
unsafe for consent, dosing, and discharge instructions. Saphan is built around that evidence:
a fixed set of human-verified phrases first, machine help only as a labeled assistant.

## What it does

- **Phrasebook.** Topics ranked by the region's disease burden (fever and malaria, cough and TB,
  pregnancy and birth, children and vaccines, injury and snakebite, medicines, and more). Each
  phrase shows the Thai question, the Burmese or Mon translation with its review status, a play
  button, and a full-screen patient view with tap-to-answer buttons.
- **Safety gates.** A phrase reaches a patient only when a fluent speaker has reviewed it;
  high-risk phrases (consent, doses, prognosis) also need a clinician. The checks run
  automatically on every change to the content.
- **Speech search.** Speak or type Thai and get matching verified phrases. Works with the
  phone's built-in recognizer (online) or a Thai Whisper model on the phone (offline after a
  one-time download).
- **Mon lexicon.** A 26,857-entry lookup across Mon, English, Burmese, and Thai for translators
  and reviewers.
- **Contributor tools.** A recording screen for native speakers, a Thai-side Mon wording field,
  and a plain pull-request workflow that needs no programming.
- **Offline-first.** Static site, installable on a phone, about 2.5 MB core.

## Status

Scaffold with a worked example, deployed and under active development.

| Area | State |
|---|---|
| Phrases | 39 records across 8 topics, seeded from the myMediCon medical corpus; Burmese human-translated, Thai machine-translated and awaiting review, Mon awaiting translators |
| Audio | synthetic Burmese voice (Meta MMS) as placeholders, labeled "computer voice"; human recordings replace them as they arrive |
| Reviewers | Thai, Burmese, and Mon reviewers being recruited; partners contacted October 2026 |
| Speech | Thai on-device model live (Thonburian Whisper small, converted to ONNX) |
| Machine translation | off by default; free-text mode exists as a safety mock-up only |

See `docs/` for the research dossier, architecture, decisions, safety policy, disease-burden
report, and the Mon scoping report.

## Contribute

- **Translators and clinicians:** read `docs/contributing-a-phrase.md`. Editing one JSON file on
  GitHub and filling a short review form is the whole process.
- **Mon speakers in particular:** the Mon column is empty. The lexicon tab and the recording
  screen are there for you.
- **Developers:** see below.

## Run it locally

Checks need only Python 3.9+ (macOS system Python works):

```bash
python3 -m tools.validate
```

```bash
python3 -m tools.build
```

```bash
python3 -m unittest discover -s tests
```

The app needs Node 22+ and pnpm:

```bash
cd app
```

```bash
pnpm install
```

```bash
pnpm run dev
```

Content bundles (`python3 -m tools.build`, `tools.build_lexicon`, `tools.build_icons`) are
committed, so the app runs without regenerating them.

## How it fits together

```
content/phrases/<topic>/<id>.json   one phrase: th / my / mnw / en, status, reviewer, audio, source
content/domains.json                topic order and labels (edit to re-rank)
        │
        ▼  python3 -m tools.validate      script, Zawgyi, legacy-font, status, provenance checks
        ▼  python3 -m tools.build         safety gates, syllable breaks, one bundle
        │
app/src/lib/content/bundle.json     shipped inside the app
        │
        ▼  pnpm run build                 SvelteKit static site + service worker  →  GitHub Pages
```

| Path | What it is |
|---|---|
| `content/` | phrases, answers, topics, sources, icons, lexicon sources |
| `tools/` | validator, builders, syllable breaker, audio synthesis |
| `tests/` | 23 Python tests; `app/tests/` has the speech-matcher tests |
| `app/` | SvelteKit progressive web app |
| `docs/` | research, architecture, policies, guides |
| `.github/workflows/` | checks on every pull request; deploy on push to main |

## Licenses and credits

- Code: MIT. Content and audio: CC BY-NC-SA 4.0 (`LICENSE-CONTENT.md`), inherited from the
  myMediCon corpus. Non-commercial means the content cannot be sold; free distribution by
  health services is fine.
- Seed sentences: myMediCon text corpus by Ye Kyaw Thu and colleagues (NECTEC / LU Lab),
  CC BY-NC-SA 4.0.
- Thai speech model: Thonburian Whisper (Mahidol University), Apache-2.0; our browser
  conversion at huggingface.co/phagehunter/whisper-th-small-onnx.
- Synthetic voices: Meta MMS-TTS, CC BY-NC 4.0.
- Pictograms: Health Icons, CC0.
- Mon lexicon: Nenemin95 Mon-Eng-Mya-Pali lexicon (CC BY 4.0) and MonDictDB (MIT).
- Mon syllable breaking: sylbreak4all by Ye Kyaw Thu et al., MIT.

## Contact

Curtis Hoffmann, curtis@operationoutbreak.org. Issues and pull requests welcome.
