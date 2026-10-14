"""Compile the content folder into one bundle the app can load offline.

    python3 -m tools.build            # writes app/src/lib/content/bundle.json
    python3 -m tools.build --out X    # writes somewhere else

Gate rules (the heart of the safety design):
 * A phrase is included when it has Thai text (any status) AND at least one
   patient language (Burmese or Mon) at status 'human' or better.
 * For each patient language, the bundle carries `locked: true` with a reason
   when its status is below 'human', or below 'clinical' for high-risk phrases.
   The app shows locked languages greyed out and never plays or displays them
   to a patient.
 * Provider-facing Thai and English are always carried with their status so
   the app can show a warning badge on machine or draft text.
 * Burmese and Mon display strings get zero-width spaces between syllables.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .sylbreak import with_zwsp

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DEFAULT_OUT = ROOT / "app" / "src" / "lib" / "content" / "bundle.json"
STATUS_RANK = {"draft": 0, "machine": 1, "human": 2, "clinical": 3}
PATIENT_LANGS = ("my", "mnw")

DOMAINS_FILE = CONTENT / "domains.json"


def load_domains() -> list[dict]:
    """Topic order and labels live in content/domains.json so they can change without code."""
    return json.loads(DOMAINS_FILE.read_text(encoding="utf-8"))["domains"]



def required_rank(risk: str) -> int:
    return STATUS_RANK["clinical"] if risk == "high" else STATUS_RANK["human"]


def compile_phrase(rec: dict) -> dict | None:
    if not rec["text"]["th"]:
        return None
    patient_ok = any(STATUS_RANK[rec["status"][l]] >= STATUS_RANK["human"] for l in PATIENT_LANGS if rec["text"][l])
    if not patient_ok:
        return None
    need = required_rank(rec["risk"])
    langs = {}
    for lang in ("en", "th", "my", "mnw"):
        text = rec["text"][lang]
        status = rec["status"][lang]
        entry = {"text": text, "status": status, "display": text}
        if text and lang in PATIENT_LANGS:
            entry["display"] = with_zwsp(text, lang)
            if STATUS_RANK[status] < need:
                entry["locked"] = True
                entry["lock_reason"] = "needs_clinical_review" if rec["risk"] == "high" else "unreviewed"
            clip = rec["audio"].get(lang)
            entry["audio"] = clip if clip and not entry.get("locked") else None
        if lang in rec.get("review", {}):
            r = rec["review"][lang]
            entry["reviewed_by"] = f"{r['reviewer']} ({r['role']}, {r['date']})"
        if lang == "mnw" and "mnw-TH" in rec.get("variants", {}):
            var = rec["variants"]["mnw-TH"]
            locked = STATUS_RANK[var["status"]] < need
            entry["variant_th"] = {
                "text": var["text"], "display": with_zwsp(var["text"], "mnw"), "status": var["status"],
                "audio": None if locked else var.get("audio"), "locked": locked,
                "lock_reason": ("needs_clinical_review" if rec["risk"] == "high" else "unreviewed") if locked else None,
            }
        langs[lang] = entry
    return {
        "id": rec["id"],
        "domain": rec["domain"],
        "intent": rec["intent"],
        "risk": rec["risk"],
        "expects": rec["expects"],
        "choices": rec.get("choices", []),
        "pictogram": rec["pictogram"],
        "lang": langs,
        "source": rec["source"]["id"],
        "notes": rec.get("notes", ""),
    }


def build(out: Path) -> dict:
    phrases = []
    skipped = []
    for path in sorted((CONTENT / "phrases").rglob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        compiled = compile_phrase(rec)
        if compiled is None:
            skipped.append(rec["id"])
        else:
            phrases.append(compiled)
    answers_raw = json.loads((CONTENT / "answers" / "answers.json").read_text(encoding="utf-8"))["answers"]
    answers = []
    for a in answers_raw:
        lang = {}
        for l in ("en", "th", "my", "mnw"):
            t = a["text"].get(l)
            lang[l] = {"text": t, "status": a["status"][l], "display": with_zwsp(t, l) if t and l in PATIENT_LANGS else t}
        answers.append({"id": a["id"], "pictogram": a["pictogram"], "lang": lang})
    sources = json.loads((CONTENT / "sources.json").read_text(encoding="utf-8"))
    domains = load_domains()
    known = {d["id"] for d in domains}
    unknown = sorted({p["domain"] for p in phrases} - known)
    if unknown:
        raise SystemExit(f"domains.json has no entry for: {unknown}")
    bundle = {
        "version": date.today().isoformat(),
        "domains": [
            {**d, "count": sum(p["domain"] == d["id"] for p in phrases)}
            for d in domains
            if any(p["domain"] == d["id"] for p in phrases) or d.get("show_when_empty")
        ],
        "phrases": phrases,
        "answers": answers,
        "sources": sources,
        "skipped": skipped,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return bundle


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    b = build(args.out)
    locked = sum(1 for p in b["phrases"] for l in PATIENT_LANGS if p["lang"][l].get("locked"))
    print(f"bundle {b['version']}: {len(b['phrases'])} phrases in {len(b['domains'])} domains, "
          f"{len(b['answers'])} answers, {locked} locked patient-language slots, {len(b['skipped'])} skipped -> {args.out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
