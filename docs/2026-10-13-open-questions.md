# Open questions for the project lead

Date: 2026-10-13. Answer by number; a short reply like "1a, 2c, 3b ..." is enough.
Each has a recommended default marked (rec). Unanswered questions take the default.

1. **First release scope.**
   a) Phrasebook only, offline, verified phrases (rec)
   b) Phrasebook plus Thai speech search
   c) Everything including free-text machine translation
2. **Who holds the phone first?**
   a) Thai village health volunteer, Thai-first UI (rec)
   b) Migrant health volunteer, Burmese-first UI
   c) Both, with a language switch on the home screen
3. **How hard to push Mon now?**
   a) Mon as a first-class language with empty slots until partners fill them (rec)
   b) Burmese first; Mon only as a scaffolded placeholder
   c) Mon before Burmese
4. **Which domains in the worked example?** (pick up to three)
   a) Antenatal/delivery (rec)  b) Medication instructions (rec)  c) Triage/symptoms (rec)
   d) TB/malaria follow-up  e) Insurance/registration/consent  f) NCD counseling
5. **Content license.**
   a) CC BY-NC-SA 4.0, inherit from myMediCon and reuse its sentences (rec)
   b) CC BY 4.0, write fresh phrases, no direct reuse of myMediCon text
6. **Seed from myMediCon text?**
   a) Yes, select matching sentences and attribute (rec)
   b) No, start from the CC0 Refugee Phrasebook and our own
7. **Contact the myMediCon authors?** (Ye Kyaw Thu, NECTEC / LU Lab)
   a) Yes, draft an email for you to send asking about collaboration and the gated speech data (rec)
   b) Not yet
8. **Cloud services allowed?**
   a) None; fully offline, synthetic audio generated once at build time by the maintainer (rec)
   b) Allow Azure Burmese voices and Google Translate at runtime with a key you hold
   c) Allow Claude API for free-text second opinions too
9. **Where does it live on GitHub?**
   a) Your account `phagehunter`, repo name to decide (rec)
   b) A new organization for the project
10. **Project name.**
    a) "Saphan" (placeholder, Thai for bridge)  b) Keep "myMediCon" in the name (risk: it is the
    corpus authors' name)  c) You propose one
11. **Reviewers you can reach.** Do you already have (yes/no each): a Thai clinician, a Burmese
    speaker with clinical background, a Mon speaker, anyone at MNHC or Kwai River Christian
    Hospital? This decides whether CODEOWNERS has real names or placeholders.
12. **Devices.** a) Low-end Android only (rec)  b) Android and iPhone  c) Also tablets at a desk
13. **Usage logging.** a) None, nothing leaves the phone (rec)  b) Anonymous counts of which
    phrases get used, for improving content
14. **Pictograms.** a) Use an open icon set (OpenMoji / Health Icons, CC0/MIT) (rec)  b) Commission
    or draw our own later
15. **Synthetic audio placeholders in the scaffold.** a) Generate Burmese/Mon clips with the
    Meta MMS voices on this Mac, clearly labeled "computer voice" (rec)  b) Silent placeholders
    until humans record
