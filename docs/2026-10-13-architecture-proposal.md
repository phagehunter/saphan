# Architecture proposal: a validated multilingual medical communication aid

Date: 2026-10-13. Status: PROPOSAL, awaiting the project lead's answers to
`2026-10-13-open-questions.md`. Nothing is built.

Working title used in this document: **Saphan** (Thai สะพาน, "bridge"). Placeholder only.

## 1. What the thing is, in one paragraph

A free, open-source, offline-first phone app for Thai village health volunteers, migrant health
volunteers, and clinic staff in Kanchanaburi. Its core is a library of short, pre-approved
clinical phrases, each available as Thai text, Burmese text and audio, Mon text and audio, and
English text, with a visible verification badge on every translation. A volunteer taps a phrase
in Thai; the patient hears it in Burmese or Mon. Patients answer by tapping pictured responses
or pre-translated replies. Speech recognition and free-text machine translation are optional
add-ons, downloaded or enabled separately, and are never used for consent or medication dosing.
The content lives in a GitHub repository as plain data files that non-programmers can edit
through pull requests, with automated checks that refuse malformed or unverified entries.

## 2. Why this shape (from the research)

- Mon has no machine translation anywhere. Mon content must be human-made. The design must work
  with zero machine translation for its most important language.
- Under 10% of Myanmar workers read Thai; health literacy on the border is low; posters get
  misread. Audio, not text, is the patient-facing channel.
- Clinical machine translation is accurate per sentence but unreliable per conversation, and
  reviewers judge preset-phrase apps acceptable while free-text apps are not. So preset phrases
  are the product; machine translation is a labeled fallback.
- Volunteers already use Thai-only reporting apps and have mixed smartphone literacy. Keep the
  UI Thai-first, large, and offline.
- The myMediCon text corpus gives 14,592 Burmese/English/Thai medical sentences under
  CC BY-NC-SA. That is the seed, with the Thai side needing human review.

## 3. The four layers

```
┌──────────────────────────────────────────────────────────────────────┐
│ 4. CONTRIBUTION & GOVERNANCE                                         │
│    PR template, CODEOWNERS per language, review states, in-app       │
│    recorder, optional Tolgee/Crowdin, partner reviewers (MNHC etc.)  │
├──────────────────────────────────────────────────────────────────────┤
│ 3. APP (SvelteKit static PWA on GitHub Pages; later Play Store)      │
│    Mode A Phrasebook (core, offline)                                 │
│    Mode B Listen (optional speech-to-text, downloadable models)      │
│    Mode C Free text (optional, online, quality-scored, back-translated)│
├──────────────────────────────────────────────────────────────────────┤
│ 2. VALIDATION PIPELINE (GitHub Actions)                              │
│    schema, key parity, Unicode/Zawgyi, Mon character set, syllable   │
│    breaking, audio presence, status gates, build of content bundle   │
├──────────────────────────────────────────────────────────────────────┤
│ 1. CONTENT (the real asset)                                          │
│    one record per phrase: th / my / mnw / en text, audio, status,    │
│    reviewer, back-translation, codes, pictogram, domain, speaker     │
└──────────────────────────────────────────────────────────────────────┘
```

### Layer 1: Content model

One YAML file per phrase, grouped by domain folder (`content/phrases/antenatal/anc-001.yaml`).
Draft schema (final form after the lead's answers):

```yaml
id: anc-001
domain: antenatal
intent: ask_last_period          # stable machine name
speaker: provider                # provider | patient | either
risk: low                        # low | medium | high (high = consent, dosing: never machine)
expects: date                    # what kind of answer: yes_no | date | number | choice | free
choices: [ ]                     # optional pictured answer set
codes:
  icd11: "http://id.who.int/icd/entity/..."   # optional anchor
text:
  en: "When was the first day of your last period?"
  th: "ประจำเดือนครั้งล่าสุดมาวันแรกเมื่อไหร่"
  my: "..."
  mnw: "..."
status:
  en: clinically-verified
  th: human-reviewed
  my: human-reviewed
  mnw: draft                     # draft | machine | human-reviewed | clinically-verified
review:
  my: {reviewer: "Dr. X (MNHC)", date: 2026-11-02, back_translation: "..."}
audio:
  my: audio/my/anc-001.opus      # human recording preferred; synthetic clips are tagged
  mnw: null
source: mymedicon-text-v0.8:L1234   # provenance, required
license: CC-BY-NC-SA-4.0
```

Rules the pipeline enforces: a phrase appears in the app only when its text status is at least
`human-reviewed`; `high` risk phrases require `clinically-verified`; audio marked synthetic
shows a "computer voice" icon; every record names its source.

Seed content plan: select roughly 200-400 of the 14,592 myMediCon sentences that match the
priority domains (antenatal, medication, triage, TB/malaria, insurance/consent), keep Burmese as
`human-reviewed` (it was human-translated), mark Thai as `machine` until a Thai reviewer passes
it, and add Mon as `draft` placeholders for partners to fill. Add the Refugee Phrasebook CC0
medical set as a second seed where languages overlap.

### Layer 2: Validation pipeline

GitHub Actions on every pull request:
1. JSON Schema validation of every phrase file (check-jsonschema).
2. Key parity: every phrase has all four language slots, even if `null`.
3. Unicode hygiene: NFC normalization, Zawgyi probability via Google myanmar-tools ML model
   (reject Burmese or Mon text that looks like Zawgyi), reject characters outside the Myanmar
   block for `my`/`mnw`, outside Thai block for `th`.
4. Mon character sanity: allow Mon-specific code points; flag Burmese-only letters that never
   occur in Mon if the field is `mnw` (heuristic, warn only).
5. Syllable segmentation with sylbreak4all (`bm` for Burmese, `mo` for Mon) and insertion of
   zero-width spaces at syllable boundaries into the built bundle so browsers wrap correctly.
6. Status gates and provenance presence.
7. Audio: referenced files exist, are Opus, under a size cap, and have a `recorded_by` entry.
8. Build: compile all passing phrases into one versioned JSON bundle plus a search index, and
   publish the app.

### Layer 3: App

Stack: SvelteKit 2, adapter-static, @vite-pwa/sveltekit (service worker precaches the phrase
bundle, fonts, and audio), Dexie for favorites and recent phrases, Paraglide for the UI strings
(Thai, Burmese, Mon, English), Tailwind + shadcn-svelte for components, Padauk and Noto Sans
Thai bundled.

Three modes, in order of trust:
- **Mode A Phrasebook (default, offline).** Thai-first search with Thai and Burmese syllable
  tolerance; domain tiles with pictograms; tap to play Burmese or Mon audio; big "patient
  answers" buttons; a conversation strip showing what has been said; verification badge and
  reviewer on every card; "show English" toggle for foreign clinicians.
- **Mode B Listen (optional download).** On-device Thai speech-to-text (Thonburian or a tiny
  Thai fine-tune) to find a phrase by speaking; Burmese speech-to-text only through cloud
  (Google/Azure) or a server, labeled online; Mon speech-to-text only via MMS on a server,
  experimental. Recognized speech is matched to the phrasebook, never shown as a translation.
- **Mode C Free text (optional, online, off by default).** Typed sentence sent to a translation
  service (Google/Azure for Burmese; Claude as a second opinion), shown with a quality-estimate
  band, a back-translation, and a required "read the back-translation" checkbox before display
  to the patient; disabled for `high` risk topics; not offered for Mon.

Device tiers: core app plus all audio under ~50 MB; models are optional downloads gated on
device memory and connection; everything degrades to Mode A.

UX validations (input side): language auto-detection of typed text with a prompt if it looks
like Zawgyi; empty-input and length limits; large-target confirmation before playing audio to
a patient; offline indicator; a persistent "this is not an interpreter" line with the local
MHW/hotline number configurable per clinic.

### Layer 4: Contribution and governance

- Pull-request template asks for: language, source, back-translation, reviewer name and role,
  and whether a clinician checked it.
- CODEOWNERS routes `content/**/mnw` to named Mon reviewers, `my` to Burmese reviewers, `th` to
  Thai clinical reviewers; required reviews before merge.
- In-app recorder page (MediaRecorder, Opus) for partners to record phrases; output is a zip
  the maintainer attaches to a pull request. Common Voice-style second-reviewer approval.
- Licenses: code MIT; content CC BY-NC-SA 4.0 (inherits from myMediCon) unless the lead prefers
  fresh phrases under CC BY 4.0; models used as-is under their own licenses (MMS is CC BY-NC).

## 4. What the scaffold (next step) will contain

Folder `project_myMediCon/2026-10-13-saphan-scaffold/` (name to change with the lead's answer):

- `README.md` for a non-programmer: what it is, how to run, how to add a phrase.
- `content/schema/phrase.schema.json` and `content/phrases/<domain>/*.yaml` with ~30 example
  phrases drawn from myMediCon (attributed) across three domains, with realistic status mixes.
- `tools/validate.py` (schema, parity, Unicode, Zawgyi, sylbreak4all) and `tools/build.py`
  (bundle + zero-width-space insertion), each runnable with one command.
- `.github/workflows/validate.yml` running the tools on every pull request.
- `app/` SvelteKit PWA implementing Mode A completely with the sample content, Mode B and C as
  clearly labeled stubs behind feature flags, Thai-first UI with language switcher, verification
  badges, pictogram tiles, audio playback (with synthetic placeholder clips marked as such).
- `docs/` with this proposal, the dossier, a content-contributor guide, and a safety policy.
- `tests/` for the validator and the bundle builder.
- `.github/PULL_REQUEST_TEMPLATE.md` and `CODEOWNERS` with placeholder reviewers.

Not in the scaffold: any trained model, any cloud key, any Play Store packaging, any real Mon
translations (placeholders only, clearly marked `draft`).

## 5. Risks and honest limits

- Mon depends entirely on human partners (MNHC, Kwai River Christian Hospital, Mon community).
  Without them, Mon ships as empty slots.
- The myMediCon Thai text is machine output; it must be reviewed before any Thai phrase is
  shown as verified.
- Non-commercial licenses (myMediCon text, MMS voices) rule out any paid distribution.
- Nobody has measured whisper or MMS speed on Android Go phones in a browser; Mode B may need
  a native wrapper.
- Clinical sign-off is a governance problem, not a software one; the app can only make the
  state of review visible.
