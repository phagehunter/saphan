# Safety policy

This app is a phrasebook, not an interpreter. These rules are enforced by the
build step (`tools/build.py`) and the validator (`tools/validate.py`), not by
good intentions.

1. **Only reviewed text reaches a patient.** A Burmese or Mon phrase is shown
   or played to a patient only when its status is `human` or `clinical`.
2. **High-risk phrases need a clinician.** Phrases marked `risk: high`
   (consent, medication doses, prognosis, anything whose misunderstanding could
   cause harm) stay locked for patients until a clinician fluent in that
   language is named in the review record.
3. **Machine text is labeled.** Thai text that came from Google Translate is
   shown to the volunteer with an amber "machine, unreviewed" badge. It is
   never spoken or shown to a patient.
4. **Free-text machine translation is off by default** and, when enabled,
   always shows a quality band and a back-translation the volunteer must read.
   It is blocked for consent, dosing, diagnosis, and prognosis. It is never
   offered for Mon because no Mon machine translation exists.
5. **Every record names its source and its reviewer.** Status cannot be raised
   in a pull request without a review record.
6. **A permanent notice** on every screen says the app is not an interpreter and
   shows the clinic's interpreter or migrant health worker number.
7. **Nothing leaves the phone.** No analytics, no logging of what was said.

Evidence behind these rules is in docs/2026-10-13-research-dossier.md,
section 9.
