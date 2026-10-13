"""Run with:  python3 -m unittest discover -s tests"""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools import build, sylbreak, validate
from tools.schema_check import validate as schema_validate

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "content/schema/phrase.schema.json").read_text(encoding="utf-8"))
SOURCES = json.loads((ROOT / "content/sources.json").read_text(encoding="utf-8"))
SAMPLE = json.loads((ROOT / "content/phrases/triage/triage-003.json").read_text(encoding="utf-8"))


class SylbreakTests(unittest.TestCase):
    def test_burmese_syllables(self):
        self.assertEqual(sylbreak.syllables("မင်္ဂလာပါ", "my"), ["မင်္ဂ", "လာ", "ပါ"])

    def test_burmese_zwsp(self):
        self.assertEqual(sylbreak.with_zwsp("ချောင်းဆိုး", "my"), "ချောင်း​ဆိုး")

    def test_mon_letters_are_syllable_starts(self):
        # U+105A MON NGA starts a syllable in Mon but is not a Burmese consonant.
        self.assertEqual(sylbreak.syllables("ကၚ", "mnw"), ["က", "ၚ"])
        self.assertEqual(sylbreak.syllables("ကၚ", "my"), ["ကၚ"])

    def test_whitespace_preserved(self):
        self.assertEqual(sylbreak.with_zwsp("က ခ", "my"), "က ခ")


class SchemaTests(unittest.TestCase):
    def test_sample_passes(self):
        self.assertEqual(schema_validate(SAMPLE, SCHEMA), [])

    def test_bad_status_rejected(self):
        rec = copy.deepcopy(SAMPLE)
        rec["status"]["my"] = "verified"
        errs = schema_validate(rec, SCHEMA)
        self.assertTrue(any("status.my" in e for e in errs), errs)

    def test_unknown_key_rejected(self):
        rec = copy.deepcopy(SAMPLE)
        rec["extra"] = 1
        self.assertTrue(any("unexpected key 'extra'" in e for e in schema_validate(rec, SCHEMA)))

    def test_missing_language_slot_rejected(self):
        rec = copy.deepcopy(SAMPLE)
        del rec["text"]["mnw"]
        self.assertTrue(any("missing required key 'mnw'" in e for e in schema_validate(rec, SCHEMA)))


class ValidateTests(unittest.TestCase):
    def _run(self, rec: dict):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / rec["domain"] / f"{rec['id']}.json"
            p.parent.mkdir()
            p.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
            # validate reports paths relative to ROOT; a temp path is outside ROOT, so patch
            old = validate.ROOT
            validate.ROOT = Path(d)
            try:
                return validate.check_phrase(p, SCHEMA, SOURCES)
            finally:
                validate.ROOT = old

    def test_seed_record_is_clean(self):
        errors, warns = self._run(copy.deepcopy(SAMPLE))
        self.assertEqual(errors, [])

    def test_zawgyi_suspect_burmese_is_rejected(self):
        rec = copy.deepcopy(SAMPLE)
        rec["text"]["my"] = "ေက်းဇူးၠ"  # U+1060 is a Zawgyi tell in Burmese text
        errors, _ = self._run(rec)
        self.assertTrue(any("Zawgyi" in e for e in errors), errors)

    def test_mon_may_use_mon_letters(self):
        rec = copy.deepcopy(SAMPLE)
        rec["text"]["mnw"] = "ၚ"
        rec["status"]["mnw"] = "human"
        rec["review"]["mnw"] = {"reviewer": "Test Person", "role": "native-speaker", "date": "2026-10-13"}
        errors, _ = self._run(rec)
        self.assertEqual(errors, [])

    def test_human_status_needs_reviewer(self):
        rec = copy.deepcopy(SAMPLE)
        rec["text"]["mnw"] = "ၚ"
        rec["status"]["mnw"] = "human"
        errors, _ = self._run(rec)
        self.assertTrue(any("needs a review entry" in e for e in errors), errors)

    def test_clinical_needs_clinician_role(self):
        rec = copy.deepcopy(SAMPLE)
        rec["status"]["my"] = "clinical"
        rec["review"]["my"] = {"reviewer": "Test Person", "role": "translator", "date": "2026-10-13"}
        errors, _ = self._run(rec)
        self.assertTrue(any("clinician reviewer role" in e for e in errors), errors)

    def test_null_text_must_be_draft(self):
        rec = copy.deepcopy(SAMPLE)
        rec["status"]["mnw"] = "human"
        errors, _ = self._run(rec)
        self.assertTrue(any("must be draft" in e for e in errors), errors)

    def test_thai_block_enforced(self):
        rec = copy.deepcopy(SAMPLE)
        rec["text"]["th"] = "คุณ" + "က"
        errors, _ = self._run(rec)
        self.assertTrue(any("outside the Thai block" in e for e in errors), errors)

    def test_legacy_font_soup_rejected(self):
        rec = copy.deepcopy(SAMPLE)
        rec["text"]["mnw"] = "u}c\\Ak'c AmX["  # what legacy-font Mon looks like when pasted as text
        rec["status"]["mnw"] = "draft"
        errors, _ = self._run(rec)
        self.assertTrue(any("legacy" in e for e in errors), errors)

    def test_thai_mon_variant_needs_reviewer(self):
        rec = copy.deepcopy(SAMPLE)
        rec["variants"] = {"mnw-TH": {"text": "ၚ", "status": "human"}}
        errors, _ = self._run(rec)
        self.assertTrue(any("variant mnw-TH" in e for e in errors), errors)

    def test_whole_content_folder_passes(self):
        self.assertEqual(validate.main(), 0)


class BuildTests(unittest.TestCase):
    def test_low_risk_burmese_unlocked(self):
        out = build.compile_phrase(copy.deepcopy(SAMPLE))
        self.assertIsNotNone(out)
        self.assertNotIn("locked", out["lang"]["my"])
        self.assertIn("​", out["lang"]["my"]["display"])

    def test_high_risk_locks_until_clinical(self):
        rec = copy.deepcopy(SAMPLE)
        rec["risk"] = "high"
        out = build.compile_phrase(rec)
        self.assertTrue(out["lang"]["my"]["locked"])
        self.assertEqual(out["lang"]["my"]["lock_reason"], "needs_clinical_review")
        rec["status"]["my"] = "clinical"
        rec["review"]["my"] = {"reviewer": "Dr Test", "role": "physician", "date": "2026-10-13"}
        out = build.compile_phrase(rec)
        self.assertNotIn("locked", out["lang"]["my"])

    def test_machine_only_patient_text_is_skipped(self):
        rec = copy.deepcopy(SAMPLE)
        rec["status"]["my"] = "machine"
        self.assertIsNone(build.compile_phrase(rec))

    def test_bundle_builds(self):
        with tempfile.TemporaryDirectory() as d:
            b = build.build(Path(d) / "bundle.json")
            self.assertGreaterEqual(len(b["phrases"]), 30)
            # Skipped records must be exactly those with no patient language at 'human' or better.
            shipped = {p["id"] for p in b["phrases"]}
            for path in (ROOT / "content/phrases").rglob("*.json"):
                rec = json.loads(path.read_text(encoding="utf-8"))
                ok = any(rec["status"][l] in ("human", "clinical") and rec["text"][l] for l in ("my", "mnw"))
                self.assertEqual(rec["id"] in shipped, ok and bool(rec["text"]["th"]), rec["id"])
                self.assertEqual(rec["id"] in b["skipped"], not (ok and bool(rec["text"]["th"])), rec["id"])


if __name__ == "__main__":
    unittest.main()
