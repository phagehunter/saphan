"""Generate placeholder audio clips with Meta's MMS text-to-speech voices.

NOT RUN YET. Needs approval to install, in a separate virtual environment:
    uv venv .venv-tts
    uv pip install --python .venv-tts/bin/python torch transformers scipy soundfile
Then:
    .venv-tts/bin/python -m tools.synth_audio --lang my
    .venv-tts/bin/python -m tools.synth_audio --lang mnw

Models downloaded on first run (CC BY-NC 4.0, non-commercial):
    facebook/mms-tts-mya   Burmese
    facebook/mms-tts-mnw   Mon
    facebook/mms-tts-tha   Thai (only if a Thai clip is ever wanted)

What it does: for every phrase whose text in --lang is at status 'human' or
'clinical' and has no audio yet, synthesize a clip, write it to
app/static/audio/<lang>/<id>.ogg (Opus, ~1/10 the size of WAV), and set audio.<lang> in the record to
{"file": ..., "kind": "synthetic", "voice": "<model id>", "date": today}.
The app shows a "computer voice" icon for synthetic clips. Replace them with
human recordings whenever a partner records the phrase.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = {"my": "facebook/mms-tts-mya", "mnw": "facebook/mms-tts-mnw", "th": "facebook/mms-tts-tha"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=MODELS, required=True)
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--only", help="phrase id to synthesize")
    args = ap.parse_args()
    try:
        import torch
        from transformers import VitsModel, AutoTokenizer
        import soundfile as sf
    except ImportError as e:
        print("missing dependency:", e)
        print(__doc__)
        return 2

    model_id = MODELS[args.lang]
    tok = AutoTokenizer.from_pretrained(model_id)
    model = VitsModel.from_pretrained(model_id)
    torch.manual_seed(7)  # VITS has a stochastic duration predictor; fix the seed for repeatable clips
    outdir = ROOT / "app" / "static" / "audio" / args.lang
    outdir.mkdir(parents=True, exist_ok=True)
    done = 0
    for path in sorted((ROOT / "content" / "phrases").rglob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if args.only and rec["id"] != args.only:
            continue
        text = rec["text"].get(args.lang)
        if not text or rec["status"][args.lang] not in ("human", "clinical"):
            continue
        if rec["audio"].get(args.lang) and not args.overwrite:
            continue
        inputs = tok(text, return_tensors="pt")
        with torch.no_grad():
            out = model(**inputs).waveform[0].numpy()
        rel = f"audio/{args.lang}/{rec['id']}.ogg"
        sf.write(ROOT / "app" / "static" / rel, out, model.config.sampling_rate, format="OGG", subtype="OPUS")
        rec["audio"][args.lang] = {"file": rel, "kind": "synthetic", "voice": model_id, "date": date.today().isoformat()}
        path.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        done += 1
        print("wrote", rel)
    print(f"{done} clips written with {model_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
