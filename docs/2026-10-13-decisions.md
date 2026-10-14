# Decisions taken 2026-10-13

The project lead answered the open questions with "all recommended defaults, 4abcd, 11 none yet."
Recorded here so nobody has to reconstruct them from chat.

| # | Decision |
|---|---|
| 1 | First release: phrasebook only, offline, verified phrases. Speech and free-text modes stay stubs. |
| 2 | Primary user: Thai village health volunteer; Thai-first screen with a patient-language switch. |
| 3 | Mon is a first-class language with empty slots until partners fill them. |
| 4 | Worked-example domains: antenatal/delivery, medication, triage/symptoms, TB/malaria. |
| 5 | Content license CC BY-NC-SA 4.0, inherited from myMediCon. Code MIT. |
| 6 | Seed from the myMediCon text corpus, attributed per record. |
| 7 | Draft an email to the myMediCon authors (docs/2026-10-13-draft-email-to-mymedicon-authors.md). |
| 8 | No cloud services at runtime. Placeholder audio generated once, on the lead's Mac, by the maintainer. |
| 9 | GitHub home: the lead's own account `phagehunter`; repository name proposed `saphan`. |
| 10 | Working name "Saphan" (สะพาน, bridge). Easy to rename: it appears in i18n strings, the manifest, and docs. |
| 11 | No reviewers confirmed yet. CODEOWNERS holds placeholders; all `human` statuses in the seed rest on the corpus's documented human translation, not on a project reviewer. |
| 12 | Low-end Android only. iPhone is not a target; nothing prevents it from working there. |
| 13 | No usage logging. Favorites and recents stay in the phone's local database. |
| 14 | Pictograms: emoji for the scaffold; replaced 2026-10-14 by Health Icons (CC0), inlined and colored with CSS, emoji kept as fallback. |
| 15 | Synthetic placeholder clips with Meta MMS voices, labeled "computer voice". Script written, not yet run (needs install approval). |
