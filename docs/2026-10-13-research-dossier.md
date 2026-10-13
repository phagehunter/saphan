# Research dossier: multilingual medical communication aid (Thai / Burmese / Mon / English)

Date: 2026-10-13. Prepared by the system for the project lead.
Scope: everything needed to decide an architecture. Nothing here is built yet.
Items marked UNVERIFIED could not be confirmed from a primary source.

## 1. The source proposal: the myMediCon paper

Hay Man Htun, Ye Kyaw Thu, Hutchatai Chanlekha, Kotaro Funakoshi, Thepchai Supnithi.
"myMediCon: End-to-End Burmese Automatic Speech Recognition for Medical Conversations."
LREC-COLING 2024, pp. 12032-12039. https://aclanthology.org/2024.lrec-main.1051/

What the paper actually is:
- A Burmese speech corpus for the medical domain, read aloud from a text corpus.
- Text corpus: 14,592 doctor/nurse/patient sentences translated from an English clinical exam
  handbook (Samson Handbook of PLAB and Clinical Assessment) by three university students.
  232,999 words, 15,431 unique words.
- Speech: 12 speakers (3 male, 9 female, ages 20-30), 7 native Burmese and 5 from Pa'O, Kachin,
  Dawei, and Mon backgrounds speaking Burmese as a second language. Full recordings: ~94 hours.
  Experiments used an 11-hour subset (5,400 sentences, 450 per speaker).
- Models: ESPnet, RNN vs Transformer. Best result: RNN with syllable segmentation, CER 9.7%,
  WER 19.0%. Syllable-level segmentation (sylbreak) beat word-level by a wide margin.
- Error analysis: phonetic confusions, text-encoding inconsistencies, segmentation. Fix: more data
  and text normalization.
- Future work stated: publish the corpus, enlarge it, data augmentation, transfer learning.

What matters for an app: the paper is a recognition model, not a communication tool. Its real
reusable asset is the trilingual text corpus (next section). Its lesson is that Burmese must be
handled at the syllable level and that text normalization (Unicode, typing order) is a first-class
problem.

## 2. What was actually released (verified 2026-10-13)

| Asset | Where | Size | License | Notes |
|---|---|---|---|---|
| myMediCon text corpus v0.8 | https://github.com/ye-kyaw-thu/myMediCon (`text/ver0.8/`) | 14,592 lines each: `data.my` (Burmese), `paraphrase.en` (English), `data.th` (Thai) | CC BY-NC-SA 4.0 | Burmese human-translated. English paraphrased by Quillbot. Thai is Google Translate output, so treat it as unreviewed. Speech corpus marked "work in progress". |
| mediTalk-mm-rdy (successor speech corpus) | https://huggingface.co/datasets/LULab/mediTalk-mm-rdy | 29.2k rows, 6.1 GB | CC BY-NC-SA 4.0, gated, research only | "Still developing." Also `mymediTalk-MM`, `myMediEval_*` suites. |
| myMediWhisper paper (Aug 2026) | https://arxiv.org/abs/2608.11036 | 28 h validated Burmese medical speech | | Fine-tuned Whisper-medium reaches WER 23.44% on medical test set. Model release unclear (UNVERIFIED). LULab hosts Whisper-Small/Tiny checkpoints without cards. |
| sylbreak4all | https://github.com/ye-kyaw-thu/sylbreak4all | regex syllable breakers | MIT | Covers nine Myanmar-script languages including Mon (`mo`) and Burmese (`bm`). |
| myWord | https://github.com/ye-kyaw-thu/myWord | Burmese word segmenter + dictionaries | MIT | Burmese only. PyPI `myword`. |
| myG2P | https://github.com/ye-kyaw-thu/myG2P | Burmese grapheme-to-phoneme | not checked | Useful for pronunciation hints. |
| myPOS, myParaphrase | github.com/ye-kyaw-thu | 11k POS sentences; 40k paraphrase pairs | CC BY-NC-SA 4.0 | |
| myPar `my-th-medical` | https://github.com/ye-kyaw-thu/myPar | empty ("Preparing") | GPL-3.0 | Watch this folder. |

Contact in the myMediCon README: ykt.nlp.ai[at]gmail.com (Ye Kyaw Thu, NECTEC / LU Lab).

## 3. Language coverage matrix (the decisive table)

ISO codes: Thai `tha`/`th`, Burmese `mya`/`my`, Mon `mnw`. Warning: `mon` is Mongolian.

| Capability | Thai | Burmese | Mon | Source |
|---|---|---|---|---|
| Whisper speech-to-text | yes, but needs Thai fine-tune | listed, unusable zero-shot (CER ~123%) | absent | https://github.com/openai/whisper/blob/main/whisper/tokenizer.py ; https://huggingface.co/BuzzASR/burmese |
| Meta MMS speech-to-text (mms-1b-all) | yes | yes | **yes** | https://dl.fbaipublicfiles.com/mms/misc/language_coverage_mms.html |
| Meta MMS text-to-speech (VITS) | `facebook/mms-tts-tha` | `facebook/mms-tts-mya` | **`facebook/mms-tts-mnw`** | all CC BY-NC 4.0, 36M params |
| NLLB-200 machine translation | yes | yes | absent | https://huggingface.co/facebook/nllb-200-distilled-600M |
| MADLAD-400 MT (3B, Apache-2.0) | yes | yes | **listed** (quality UNVERIFIED) | https://huggingface.co/google/madlad400-3b-mt |
| Google Translate | yes | yes | absent (not in 2024 expansion) | https://translate.google.com/intl/en/about/languages/ |
| Microsoft / Azure Translator | yes | yes | absent | https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support |
| Azure neural TTS voices | several | `my-MM-NilarNeural`, `my-MM-ThihaNeural` | none | https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts |
| Google Cloud TTS | 32 voices | none | none | https://docs.cloud.google.com/text-to-speech/docs/list-voices-and-types |
| Google Cloud STT v2 | yes | `my-MM` (chirp) | none | https://docs.cloud.google.com/speech-to-text/docs/languages |
| Seamless M4T v2 | all modes | speech in, text in/out, no speech out | absent | https://huggingface.co/facebook/seamless-m4t-v2-large |
| Piper TTS voices | `th_TH-tsync2-medium` | none | none | https://huggingface.co/rhasspy/piper-voices |
| Common Voice locale | large (173 h validated) | locale exists, hours UNVERIFIED | locale exists, assume ~0 h | https://commonvoice.mozilla.org/api/v1/languages |
| Open parallel text with English | FLORES, ALT, OPUS | ~13.7M pairs on OPUS incl. tico-19 (3,071 COVID health pairs) | ~10k pairs total (translatewiki 8,135; wikimedia 1,996; Tatoeba 9) | https://opus.nlpl.eu/ |
| Wikipedia | large | 108k articles | 4,541 articles | https://mnw.wikipedia.org/wiki/Special:Statistics |
| LLM (Claude, Gemini) quality | good | fair; Claude 3 Opus chrF++ 48.9 my->en vs Google 56.3 (2024 paper) | no benchmark exists anywhere | https://arxiv.org/pdf/2404.13813 |

Conclusion: Mon has speech recognition and synthesis (MMS only) but no machine translation worth
trusting. Mon content must be human-written and human-recorded. Burmese has machine translation
and cloud speech, but clinical quality is unvalidated. Thai is well served.

## 4. Thai speech models worth knowing

- Thonburian Whisper (Mahidol, Apache-2.0): `biodatlab/whisper-th-small-combined` WER 13.1,
  `biodatlab/whisper-th-medium-combined` WER 7.4. https://github.com/biodatlab/thonburian-whisper
- Pathumma Whisper (NECTEC, Apache-2.0): `nectec/Pathumma-whisper-th-large-v3`, no WER on card.
- Typhoon (SCB 10X): `typhoon-ai/typhoon-whisper-large-v3` (MIT, ~11,000 h);
  `typhoon-ai/typhoon-asr-realtime` 114M params, CER 0.098, CC-BY-4.0 plus terms.
  https://huggingface.co/typhoon-ai
- No tiny-size Thai fine-tune exists yet, so on-device Thai ASR in a browser means ~190 MB
  (small, q5) or training a tiny model.

## 5. Burmese speech models

- `BuzzASR/burmese` (whisper-large-v3 full fine-tune, MIT): FLEURS CER 24.0. Server only.
- `ToeLay/whisper_large_v3_turbo_mm`: WER 55.8 on OpenSLR-80.
- `thantzinphyo/whisper-tiny-myanmar-cashier`: domain tiny model, WER 38.2. Proof that tiny
  domain models are feasible.
- myMediWhisper (above): WER 23.4 on medical test set; the most relevant result.
- OpenSLR SLR80 Burmese TTS corpus (Google, CC BY-SA 4.0): https://openslr.org/80/
- Burmese WER is inflated by inconsistent word segmentation. Always compare CER.

## 6. Script, encoding, fonts, keyboards

- Zawgyi vs Unicode: Myanmar-market phones (Huawei, Samsung) often default to the non-standard
  Zawgyi encoding. Store and render Unicode only; detect Zawgyi input with Google's
  `myanmar-tools` (Apache-2.0, JS/Python/Java): https://github.com/google/myanmar-tools
  Its README warns rule-based detectors misflag Mon and Shan as Zawgyi; use the ML detector.
- Mon-specific Unicode characters in the Myanmar block (added Unicode 5.1): U+1028, U+1033,
  U+1034, U+105A-U+1060. Validators must allow them. https://www.compart.com/en/unicode/block/U+1000
- Fonts: Padauk (SIL, OFL, v6.000 Oct 2025, explicit Mon support incl. Thai-Mon variants)
  https://software.sil.org/padauk/ ; Noto Sans Myanmar (OFL, lists Mon; shaping quality
  UNVERIFIED); Pyidaungsu (Myanmar Computer Federation; a 2023 Mon Wikipedia thread said only
  Pyidaungsu rendered Mon correctly; license UNVERIFIED). Recommendation: bundle Padauk.
- Keyboards: Keyman `mon_anonta` (MIT, Android/iOS/web, 107k downloads)
  https://keyman.com/keyboards/mon_anonta ; Gboard Mon support UNVERIFIED.
- Line breaking: browsers use ICU's Burmese dictionary for all Myanmar-script text, so Mon
  wraps in wrong places. Fix: insert zero-width spaces at syllable boundaries from sylbreak4all
  when building content.
- No CLDR locale file for Mon, so no built-in date/number formatting; use Burmese or Thai
  formats as a fallback.

## 7. The people who would use it (Kanchanaburi)

Village Health Volunteers (อสม., VHV):
- ~1.07 million nationally; ~10 households each; 2,000 THB/month stipend since FY2024.
  https://washingtondc.thaiembassy.org/en/content/thailand-training-one-million-village-health-volun
- Official app "Smart อสม." (Department of Health Service Support) and AIS "อสม.ออนไลน์"; both
  are Thai-only reporting tools. Studies show moderate smartphone literacy (Chumphon: 50%
  moderate, 70% independent internet access) and recommend hands-on training.
  https://he01.tci-thaijo.org/index.php/JPHSR/article/view/282236

Migrant Health Workers (พสต., MHW) and Migrant Health Volunteers (อสต., MHV):
- MHWs are paid hospital interpreters (hired as "language coordinators" since 2016, ~6,900
  THB/month, high turnover). MHVs are unpaid community mediators who interpret when no MHW
  exists. Neither curriculum teaches interpreting, confidentiality, or terminology.
  Kosiyaporn et al. 2020, https://doi.org/10.1186/s41256-020-00181-0 (CC BY)
- Roughly 4,000-7,000 MHVs nationally vs ~3 million migrants.
- Pocock et al. 2020 (PLoS ONE): language barriers block informed consent and mental-health
  care; Thai system is more migrant-friendly than Malaysia because of MHW/MHV.
  https://doi.org/10.1371/journal.pone.0231154
- Sranacharoenpong et al. 2026: Myanmar-border primary care is NGO-dependent and fragmented;
  MHVs are "feasible and essential" but ad hoc. https://doi.org/10.1007/s10903-025-01845-0

Kanchanaburi specifics:
- Isarabhakdi 2004: migrants in Kanchanaburi are Burmese, Karen, and Mon; top barriers are legal
  status, cost, and inability to speak Thai; ethnicity determines service use.
  https://repository.li.mahidol.ac.th/handle/123456789/21827
- Wang Ka Mon village (Sangkhlaburi), founded ~1947-49; many residents without Thai ID.
  https://ethnicredb.sac.or.th/en/research_detail.php?id=610
- Mon speakers in Thailand ~100-120k; many ethnic Mon are Thai- or Burmese-dominant; "few young
  people speak Mon." https://minorityrights.org/communities/mon-and-khmer/
- Mon National Health Committee (MNHC), Sangkhlaburi: 19 clinics, 21 mobile clinics, >100
  medics. The natural Mon-language partner.
  https://cpintl.org/wp-content/uploads/2024/09/2019-10_mnhc_poa_2018-2021_web.pdf
- Kwai River Christian Hospital (Huay Malai, Sangkhlaburi): ~20,000 visits/yr, serves Thais,
  migrants, refugees; a volunteer listing says it uses Thai/Karen/Mon translators.
  https://cwsglobal.org/kwai-river-christian-hospital
- Sangkhlaburi Hospital, Phaholpolpayuhasena Hospital (provincial), IOM Migration Health Unit
  Sangkhlaburi, M-FUND (Dreamlopments) low-cost insurance with Sai Yok as a listed site.
- Thai proficiency of Myanmar workers (southern Thailand, n=1,050): under 50% reach CEFR A1
  speaking, under 10% reading. https://doi.org/10.1371/journal.pone.0312571
  Implication: Burmese/Mon audio for the patient, Thai text for the provider.
- Health literacy on the border (SMRU, n=525 women): 37% adequate; posters misread; verbal and
  audiovisual messaging essential. https://doi.org/10.1371/journal.pone.0218138
- Documented harm from missing translation: Samut Sakhon Hospital began Burmese medication
  labels after a patient misused a vaginal suppository (Bangkok Post, Apr 2018).

Priority phrase domains supported by the evidence, in order:
1. Antenatal care, delivery, postpartum (top migrant OPD and IPD reason in border hospitals)
2. Medication instructions and pharmacy counseling (documented harm)
3. Triage and symptom intake
4. TB and malaria follow-up and adherence (migrant loss-to-follow-up 21.5% vs 2.3% Thai)
5. Insurance, registration, and consent
6. Non-communicable disease counseling

## 8. Existing apps and content (what exists, what does not)

| App | Burmese | Mon | Clinical | Notes |
|---|---|---|---|---|
| MiTA, IOM Migration Translation App | yes | no | no | Pre-recorded first-contact questions, offline, 16 languages. Closest design precedent. https://apps.apple.com/app/id1488571838 |
| Canopy Speak, MediBabble, CALD Assist, Universal Doctor | no | no | yes | Fixed-phrase medical apps for other languages. |
| Google Translate / Microsoft Translator | yes | no | general | Used informally by clinicians; accuracy for medical phrases ~58% in a 2016 advisory. |
| Tarjimly | sought | no | human | Volunteer human interpreters. |

No app covers Mon at all. No Thai-base clinical phrasebook app exists. No open Thai-Burmese-Mon
medical phrasebook or glossary was found anywhere, including MOPH, IOM, Raks Thai, World Vision.
This project would be the first.

Reusable open content:
- Refugee Phrasebook (CC0), medical set of ~150 items, GitHub + Google Sheets:
  https://github.com/refugee-phrasebook/refugee-phrasebook.github.io
- tico-19 COVID health translation set, Burmese-English 3,071 pairs (OPUS).
- MedlinePlus Burmese health topics (33) and Immunize.org Burmese vaccine information
  statements (CDC content is US-government public domain; confirm per item).
  https://medlineplus.gov/languages/burmese.html
- WHO Myanmar Burmese IEC materials (CC BY-NC-SA 3.0 IGO by default).
- Drum Publications English / S'gaw Karen / Burmese medical glossary (2008).
  https://drumpublications.org/memdic/download.php
- CLEAR Global / Translators without Borders glossaries (Myanmar; reuse license UNVERIFIED).
- Hesperian "Where Women Have No Doctor" Mon translation listed "in progress" via CPPSM,
  Sangkhlaburi: https://languages.hesperian.org/pages/mnw/find_books.html
- MIMU "Awareness Materials in Ethnic Languages" (>250 items, 24 languages; Mon presence
  UNVERIFIED, site blocks automated access): https://www.themimu.info/awareness-materials-ethnic-languages

## 9. Safety evidence for machine translation in care

- Kong et al. 2025 (BMJ Qual Saf): GPT-4 and Google Translate were 90%+ accurate per sentence
  for English to Spanish and Chinese but 16-66% of instruction sets had at least one error;
  harm potential small per sentence, larger per set. Supports MT for low-stakes text only.
- Hudelson et al. 2024 (JGIM): voice-to-voice MT in 60 real consultations, goals met 83% but
  clinicians satisfied only 54%; worse for non-European languages.
- Genovese et al. 2024 systematic review: accuracy 83-98% translating from English but 36-76%
  translating into English; AI used as last resort and for brief communications.
- Mehandru et al. 2023 (EMNLP): quality-estimation scores improved physicians' calibrated
  trust; back-translation caught critical errors QE missed; recommend showing both.
  https://arxiv.org/pdf/2310.16924
- 2019 JMIR review of 15 apps: preset-phrase apps acceptable for everyday talk; consent,
  assessment, treatment, discharge deemed unsuitable for apps. https://mhealth.jmir.org/2019/4/e11316
- WHO 2024 LMM guidance warns of automation bias; nothing translation-specific.

Design consequences: pre-approved phrases by default; free-text MT opt-in, never for consent or
dosing, always shown with a quality score band and a back-translation; verification state is a
data field with reviewer and date; a permanent "not a substitute for an interpreter" notice with
the MHW/interpreter contact.

## 10. Technical stack facts that constrain the design

- GitHub Pages: 100 MB per file, ~1 GB site, no custom headers. Service worker and manifest must
  live under the repo subpath.
- SvelteKit + adapter-static + @vite-pwa/sveltekit is the lowest-risk offline-first shell given
  existing SvelteKit experience on this machine. https://github.com/vite-pwa/sveltekit
- Model sizes: whisper tiny q5 ~32 MB, base q5 ~60 MB, small q5 ~190 MB; NLLB-600M int8 ~900 MB
  (too big); MMS-TTS ~36-72 MB per language after fp16/int8 export (no published ONNX ports for
  tha/mya/mnw; must export ourselves; naive int8 yields noise).
- Low-end Android: gate heavy features on `navigator.deviceMemory` and connection type; keep
  the core under ~50 MB; make models optional downloads.
- Android packaging later via Bubblewrap/PWABuilder (Trusted Web Activity) or Capacitor if
  native speech libraries are wanted. Google Play requires targeting API 36 from Aug 31, 2026.
- Content validation in CI: JSON Schema (`check-jsonschema`), key parity script, Unicode and
  Zawgyi checks, audio presence; CODEOWNERS per language.
- Translation review platforms free for open source: Crowdin (application), Tolgee (self-host
  or OSS plan), Weblate (terms UNVERIFIED). A plain pull-request template with CODEOWNERS may be
  simpler and keeps provenance in git.
- Coding anchors: ICD-11 API has no Thai or Burmese labels; anchor phrases to ICD-11 Foundation
  URIs and keep our own labels. Thailand is a SNOMED member; store concept IDs only.

## 11. Open gaps the research could not close

- Hours of Burmese and Mon audio in Common Voice.
- Whether the 11-hour myMediCon audio will ever be released; whether myMediWhisper weights are
  public.
- Mon quality of MADLAD-400, MMS-TTS-mnw, and any LLM. Must be tested with Mon speakers.
- Whether Noto Sans Myanmar shapes Mon correctly; Pyidaungsu license.
- Interpreter staffing at Sangkhlaburi, Thong Pha Phum, and Sai Yok hospitals.
- Whether MIMU hosts Mon-language health materials.
- Whether Chrome's Web Speech API accepts `my-MM`.
- Real-time speed of Whisper in WebAssembly on Android Go phones.
