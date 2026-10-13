## What this change adds or fixes

<!-- One or two sentences. Example: "Adds Mon translations for the five antenatal questions." -->

## Language(s) touched

- [ ] Thai (th)
- [ ] Burmese (my)
- [ ] Mon (mnw)
- [ ] English (en)
- [ ] Audio
- [ ] Code or docs only

## Review record (required for any `human` or `clinical` status)

| Field | Answer |
|---|---|
| Who wrote or checked the translation (name, role, organization) | |
| Date | |
| Back-translation into English, done without looking at the original | |
| Did a clinician fluent in this language approve it? (name) | |
| Was the text typed in Unicode (not Zawgyi)? | yes / no |

## Checklist

- [ ] `python3 -m tools.validate` passes on my machine (or I am asking a maintainer to run it)
- [ ] Each changed record names its `source`
- [ ] I did not raise any status above what the review record above supports
- [ ] No dose, consent, or prognosis text was set to `clinical` without a clinician named above
