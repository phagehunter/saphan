# Saphan (สะพาน) — verified health phrases in Thai, Burmese, Mon, and English

An offline-first phone app for village health volunteers (อสม.) and migrant
health volunteers (อสต.) in Kanchanaburi, Thailand. A volunteer taps a phrase
in Thai; the patient sees and hears it in Burmese or Mon. Every translation
carries a visible review badge, and nothing unreviewed ever reaches a patient.

Status: **scaffold with a worked example**. 34 phrases across four topics,
seeded from the myMediCon medical text corpus, a validator, a build step, the
app's phrasebook mode working end to end with synthetic Burmese audio, a 26,857-entry Mon
lexicon for reviewers, and the speech and free-text modes present as labeled stubs. Builds and type-checks
clean. Not deployed. No partners confirmed. Mon slots empty.

Working name only. See `docs/2026-10-13-decisions.md`.

## How it fits together

```
content/phrases/<topic>/<id>.json   one phrase: th / my / mnw / en, status, reviewer, audio, source
        │
        ▼  python3 -m tools.validate      refuses bad script, Zawgyi, unreviewed upgrades, missing provenance
        ▼  python3 -m tools.build         applies the safety gates, inserts syllable breaks, writes one bundle
        │
app/src/lib/content/bundle.json     shipped inside the app, so it works with no signal
        │
        ▼  pnpm run build (in app/)      SvelteKit static site + service worker  →  GitHub Pages
```

Topics in the example: triage and symptoms, medication, pregnancy and birth,
TB and malaria. The schema now allows fourteen topics ranked by the 2026-10-13
disease-burden report (fever, TB, child health, injury, pharmacy, diarrhea, registration,
NCD, mental health, skin); five burden-driven draft phrases sit in those folders and are
skipped at build until a Burmese or Mon reviewer fills them in.

## Run the checks (no installation needed, macOS system Python works)

From this folder:

```bash
python3 -m tools.validate
```

```bash
python3 -m tools.build
```

```bash
python3 -m tools.build_lexicon
```

```bash
python3 -m unittest discover -s tests
```

## Run the app locally (one-time install needed)

Requires Node 22+ and pnpm (both present on the project lead's Mac).

```bash
cd app
```

```bash
pnpm install
```

```bash
pnpm run dev
```

Then open the address it prints (usually http://localhost:5173). To build the
static site the way GitHub Pages will:

```bash
pnpm run build
```

## Regenerate placeholder audio (optional)

A Python environment already exists at `.venv-tts/` (ignored by git). From this folder:

```bash
.venv-tts/bin/python -m tools.synth_audio --lang my
```

It uses Meta's MMS voices (CC BY-NC 4.0), writes Opus clips, and marks every
clip "computer voice" in the app. Run it with `--lang mnw` once Mon text exists.
On a fresh clone, recreate the environment first: `uv venv .venv-tts --python 3.12`
then `uv pip install --python .venv-tts/bin/python torch transformers scipy soundfile`.

## Add a phrase or a translation

Read `docs/contributing-a-phrase.md`. It is written for people who do not
write code: edit one JSON file on GitHub, fill in the pull-request form, and
the checker tells you if anything is wrong.

## Folder map

| Path | What it is |
|---|---|
| `content/schema/phrase.schema.json` | the rules every phrase file must follow |
| `content/phrases/` | the phrases, one file each, grouped by topic |
| `content/answers/answers.json` | patient reply buttons (yes, no, a little, ...) |
| `content/sources.json` | where text came from and under what license |
| `content/lexicon/` | two open Mon dictionaries (CC BY 4.0, MIT) and the build step for the Lexicon screen |
| `content/domains.json` | topic order, labels, and pictograms; edit this to re-rank topics, no code change needed |
| `tools/` | validator, builder, syllable breaker, audio script |
| `tests/` | 22 unit tests for the tools and the safety gates |
| `app/` | the SvelteKit progressive web app |
| `app/static/audio/my/` | 34 synthetic Burmese clips (Meta MMS voice, Opus, 564 KB total), each labeled "computer voice" in the app |
| `app/pnpm-workspace.yaml` | lets esbuild run its install script; pnpm 11 blocks all others by default |
| `docs/` | research dossier, architecture, decisions, safety policy, contributor guide, draft email, Mon scoping report, disease-burden report |
| `.github/workflows/` | automatic checks on every pull request; deploy to GitHub Pages on main |
| `CODEOWNERS` | who must review which language (placeholders for now) |

## Licenses

Code: MIT (`LICENSE`). Content and audio: CC BY-NC-SA 4.0 (`LICENSE-CONTENT.md`),
inherited from the myMediCon corpus by Ye Kyaw Thu and colleagues. Non-commercial
means this cannot be sold; free distribution by health services is fine.

## What is deliberately not here yet

- Any Mon translation (needs Mon speakers; see docs/2026-10-13-research-dossier.md section 7 for partners).
- Any Thai review (the seed Thai is Google Translate output and is badged as such).
- Any trained speech model, any cloud key, any Play Store packaging.
- A GitHub remote: the local repository exists and has one commit; it has not been pushed.
