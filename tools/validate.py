"""Validate every phrase record. Run from the repository root:

    python3 -m tools.validate

Exit code 0 means everything passed. Problems are printed one per line as
ERROR (blocks merge) or WARN (allowed, but a reviewer should look).

Checks, in order:
 1. JSON parses; file name matches the record id; domain folder matches domain.
 2. Record matches content/schema/phrase.schema.json.
 3. Unicode hygiene: text is NFC-normalized; Thai text uses the Thai block;
    Burmese and Mon text use the Myanmar block; no Zawgyi look-alike sequences.
 4. Mon sanity: Mon text may use Mon-specific letters; a Burmese-only letter
    that never occurs in Mon is only a warning.
 5. Status rules: a status of 'human' or 'clinical' needs a review entry with a
    named reviewer; text that is null must have status 'draft'; high-risk
    phrases warn until every patient language is 'clinical'.
 6. Provenance: source id exists in content/sources.json.
 7. Audio: referenced files exist under app/static/; synthetic clips name a voice.
 8. Answers file follows the same text/status conventions.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

from .schema_check import validate as schema_validate

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
STATIC = ROOT / "app" / "static"

LANGS = ("en", "th", "my", "mnw")
PATIENT_LANGS = ("my", "mnw")
STATUS_RANK = {"draft": 0, "machine": 1, "human": 2, "clinical": 3}
ZAWGYI_MIN_LEN = 12      # characters; below this the ML detector guesses
ZAWGYI_THRESHOLD = 0.85  # above this the record is rejected; 0.5-0.85 is a warning
DOMAIN_IDS = {d["id"] for d in json.loads((CONTENT / "domains.json").read_text(encoding="utf-8"))["domains"]}

THAI_BLOCK = re.compile(r"^[฀-๿\s0-9A-Za-z.,;:!?()\-/'\"%]+$")
MYANMAR_BLOCK = re.compile(r"^[က-႟ꩠ-ꩿꧠ-꧿\s0-9A-Za-z.,;:!?()\-/'\"%​]+$")
MON_ONLY_LETTERS = set("ဨဳဴၚၛၜၝၞၟၠ")
# Letters that appear in Burmese spelling but essentially never in Mon orthography.
BURMESE_ONLY_HINT = set("ဧ")  # U+1027 LETTER E is Burmese; Mon uses U+1028 MON E
# Zawgyi tells: code points Zawgyi repurposes that Unicode Burmese/Mon text should not contain.
ZAWGYI_SUSPECT = re.compile(r"[ဳဴၚၠ-႗]")


def zawgyi_probability(text: str) -> float | None:
    """Use Google's myanmar-tools model when installed; otherwise None."""
    try:
        from myanmartools import ZawgyiDetector  # type: ignore
    except Exception:
        return None
    return float(ZawgyiDetector().get_zawgyi_probability(text))


LEGACY_FONT_MIN_LEN = 6


def looks_like_legacy_font(text: str) -> bool:
    """Legacy (non-Unicode) Mon and Burmese fonts map glyphs onto Latin letters and symbols, so
    'Mon text' typed in such a font arrives as a soup of ASCII with few Myanmar code points."""
    body = [c for c in text if not c.isspace()]
    if len(body) < LEGACY_FONT_MIN_LEN:
        return False
    myanmar = sum(1 for c in body if "\u1000" <= c <= "\u109f")
    latin = sum(1 for c in body if c.isascii() and (c.isalpha() or c in "@#$%^&*[]{}|<>~`"))
    return latin >= 3 and latin > myanmar


def check_text(lang: str, text: str, is_mon_allowed: bool, where: str, errors: list[str], warns: list[str]) -> None:
    if unicodedata.normalize("NFC", text) != text:
        errors.append(f"{where}: {lang} text is not NFC-normalized")
    if lang in PATIENT_LANGS and looks_like_legacy_font(text):
        errors.append(f"{where}: {lang} text looks like a legacy (non-Unicode) font encoding; retype it with a Unicode keyboard")
        return
    if lang == "th" and not THAI_BLOCK.match(text):
        errors.append(f"{where}: th text contains characters outside the Thai block")
    if lang in PATIENT_LANGS:
        if not MYANMAR_BLOCK.match(text):
            errors.append(f"{where}: {lang} text contains characters outside the Myanmar block")
        mon_chars = MON_ONLY_LETTERS.intersection(text)
        if lang == "my" and mon_chars:
            # In Burmese these code points are a strong Zawgyi signal.
            errors.append(f"{where}: my text contains Mon-only or Zawgyi code points {sorted(mon_chars)}")
        if lang == "mnw" and BURMESE_ONLY_HINT.intersection(text):
            warns.append(f"{where}: mnw text contains U+1027 (Burmese E); Mon normally uses U+1028")
        if lang == "my":
            # The ML detector is unreliable on very short strings (a four-letter "I don't know"
            # scored 0.59), so short text gets the code-point heuristic only, and longer text
            # needs a high probability before it is treated as an error.
            p = zawgyi_probability(text) if len(text) >= ZAWGYI_MIN_LEN else None
            if ZAWGYI_SUSPECT.search(text):
                errors.append(f"{where}: my text has Zawgyi-suspect code points")
            elif p is not None and p > ZAWGYI_THRESHOLD:
                errors.append(f"{where}: my text looks like Zawgyi (probability {p:.2f})")
            elif p is not None and p > 0.5:
                warns.append(f"{where}: my text might be Zawgyi (probability {p:.2f}); a reviewer should look")


def check_phrase(path: Path, schema: dict, sources: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    where = str(path.relative_to(ROOT))
    try:
        rec = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{where}: invalid JSON ({e})"], []

    errors.extend(f"{where}: {e}" for e in schema_validate(rec, schema))
    if errors:
        return errors, warns

    if rec["id"] != path.stem:
        errors.append(f"{where}: id '{rec['id']}' does not match file name")
    if rec["domain"] != path.parent.name:
        errors.append(f"{where}: domain '{rec['domain']}' does not match folder '{path.parent.name}'")

    for lang in LANGS:
        text = rec["text"][lang]
        status = rec["status"][lang]
        if text is None:
            if status != "draft":
                errors.append(f"{where}: {lang} has no text but status is '{status}' (must be draft)")
            continue
        check_text(lang, text, lang == "mnw", where, errors, warns)
        if STATUS_RANK[status] >= STATUS_RANK["human"] and lang not in rec["review"]:
            # The seed import is the one allowed exception: a documented human translation
            # from a cited corpus counts as 'human' with the source as the reviewer.
            if not (rec["source"]["id"] == "mymedicon-text-v0.8" and lang == "my" and status == "human"):
                errors.append(f"{where}: {lang} status '{status}' needs a review entry naming the reviewer")
        if status == "clinical":
            role = rec["review"].get(lang, {}).get("role")
            if role not in ("nurse", "physician", "pharmacist", "midwife"):
                errors.append(f"{where}: {lang} status 'clinical' needs a clinician reviewer role")

    for vname, var in rec.get("variants", {}).items():
        check_text("mnw", var["text"], True, f"{where} [{vname}]", errors, warns)
        if STATUS_RANK[var["status"]] >= STATUS_RANK["human"] and "review" not in var:
            errors.append(f"{where}: variant {vname} status '{var['status']}' needs a review entry")
        if rec["text"]["mnw"] is None:
            warns.append(f"{where}: variant {vname} given but the main mnw text is empty; fill mnw first")

    if rec["risk"] == "high":
        unverified = [l for l in PATIENT_LANGS if rec["status"][l] != "clinical"]
        if unverified:
            warns.append(f"{where}: high-risk phrase; patient output stays locked for {unverified} until clinically verified")

    pic = rec["pictogram"]
    if pic.startswith("hi:") and not (CONTENT / "icons" / "healthicons" / (pic[3:].replace("/", "__") + ".svg")).exists():
        errors.append(f"{where}: pictogram '{pic}' has no file in content/icons/healthicons/")

    if rec["domain"] not in DOMAIN_IDS:
        errors.append(f"{where}: domain '{rec['domain']}' is not listed in content/domains.json")

    if rec["source"]["id"] not in sources:
        errors.append(f"{where}: unknown source id '{rec['source']['id']}'")

    for lang, clip in rec["audio"].items():
        if clip is None:
            continue
        if not (STATIC / clip["file"]).exists():
            errors.append(f"{where}: audio file app/static/{clip['file']} does not exist")
        if clip["kind"] == "synthetic" and not clip.get("voice"):
            errors.append(f"{where}: synthetic audio for {lang} must name its voice model")
        if clip["kind"] == "human" and not clip.get("recorded_by"):
            errors.append(f"{where}: human audio for {lang} must say who recorded it")
        if rec["text"][lang] is None:
            errors.append(f"{where}: audio for {lang} but no text")

    return errors, warns


def check_answers(sources_unused: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    path = CONTENT / "answers" / "answers.json"
    where = str(path.relative_to(ROOT))
    data = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for ans in data["answers"]:
        if ans["id"] in seen:
            errors.append(f"{where}: duplicate answer id {ans['id']}")
        seen.add(ans["id"])
        for lang in LANGS:
            text = ans["text"].get(lang)
            status = ans["status"].get(lang)
            if status not in STATUS_RANK:
                errors.append(f"{where}: {ans['id']} {lang} has invalid status {status!r}")
            if text is None and status != "draft":
                errors.append(f"{where}: {ans['id']} {lang} has no text but status {status}")
            if text is not None:
                check_text(lang, text, lang == "mnw", f"{where}:{ans['id']}", errors, warns)
    return errors, warns


def main() -> int:
    schema = json.loads((CONTENT / "schema" / "phrase.schema.json").read_text(encoding="utf-8"))
    sources = json.loads((CONTENT / "sources.json").read_text(encoding="utf-8"))
    files = sorted((CONTENT / "phrases").rglob("*.json"))
    all_errors: list[str] = []
    all_warns: list[str] = []
    ids: dict[str, Path] = {}
    for path in files:
        e, w = check_phrase(path, schema, sources)
        all_errors.extend(e)
        all_warns.extend(w)
        if path.stem in ids:
            all_errors.append(f"duplicate id {path.stem} in {path} and {ids[path.stem]}")
        ids[path.stem] = path
    e, w = check_answers(sources)
    all_errors.extend(e)
    all_warns.extend(w)

    for w in all_warns:
        print("WARN ", w)
    for e in all_errors:
        print("ERROR", e)
    print(f"\n{len(files)} phrase records checked: {len(all_errors)} errors, {len(all_warns)} warnings")
    if zawgyi_probability("test") is None:
        print("note: myanmar-tools not installed; Zawgyi check used the code-point heuristic only")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
