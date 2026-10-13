# Adding or translating a phrase (for people who do not write code)

You need a GitHub account and a browser. No software to install.

## A. Translate an existing phrase into Mon or Burmese

1. Open the phrase file on GitHub, for example
   `content/phrases/triage/triage-003.json`.
2. Click the pencil icon ("Edit this file").
3. Find the line `"mnw": null` under `"text"` and replace `null` with your
   translation in quotes, typed in **Unicode** (not Zawgyi). Example:
   `"mnw": "..."`.
4. Under `"status"`, change `"mnw": "draft"` to `"mnw": "human"`.
5. Under `"review"`, add your record:
   ```json
   "mnw": { "reviewer": "Your Name", "role": "native-speaker", "organization": "MNHC", "date": "2026-11-02", "back_translation": "Are you having trouble breathing?" }
   ```
   Roles allowed: translator, native-speaker, nurse, physician, pharmacist,
   midwife, health-volunteer, other. Use `clinical` as the status only if you
   are a nurse, physician, pharmacist, or midwife and wrote that role.
6. Scroll down, choose "Create a new branch and start a pull request", and
   click "Propose changes". Fill in the form that appears.
7. The automatic checker runs within a minute. Green check: a maintainer will
   merge. Red X: click "Details" to read which line it did not like.

## A2. Thai-side Mon wording (optional)

If the Myanmar-side Mon sentence would sound foreign in Sangkhlaburi, add a `variants` block
next to `text` with the local wording. It needs its own status and reviewer:

```json
"variants": { "mnw-TH": { "text": "...", "status": "human", "review": { "reviewer": "Your Name", "role": "native-speaker", "date": "2026-11-02" } } }
```

The app shows it under the main Mon text as "Thai-side Mon wording."

## A3. Looking up words

Open the app's Lexicon tab (📖). It searches 26,857 entries from two open dictionaries in Mon,
English, Burmese, and Thai. It is a reviewer tool: never paste a dictionary phrase straight into
a record without a fluent speaker checking the sentence.

## B. Add a brand-new phrase

Copy an existing file in the same topic folder, rename it to the next number
(`triage-014.json`), change `"id"` to match, write the Thai and English text,
set `"source": {"id": "saphan-authored", "license": "CC-BY-NC-SA-4.0"}`, set
every language status honestly (your own Thai is `human` only if you are a
fluent Thai speaker and you add a review record), and open a pull request.

## C. Record audio

Open the app, go to Record, choose the phrase and your language, record, save
the file, and email it to the maintainer or attach it to a pull request. The
maintainer converts it and adds it to `app/static/audio/<lang>/`.

## What the checker refuses

- Text with characters from the wrong script, Zawgyi-encoded Burmese, or Mon typed in a legacy (non-Unicode) font, which arrives as Latin-letter soup.
- A status of `human` or `clinical` with no reviewer named.
- `clinical` with a non-clinician role.
- A missing language slot (every phrase must list en, th, my, mnw, even if null).
- Audio files that do not exist, or synthetic audio with no voice model named.
