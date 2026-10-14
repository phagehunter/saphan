# Mode B, on-device speech: how it works and how to upgrade the model

Enabled 2026-10-14 after the project lead approved the `@huggingface/transformers` package
(Apache-2.0).

## What happens on the phone
1. The Listen tab prefers the on-device engine when the phone reports at least 3 GB of memory
   and has a microphone API; otherwise it falls back to the phone's built-in recognizer.
2. On the first tap, the app downloads the Whisper model (`onnx-community/whisper-base`,
   about 80 MB in 8-bit form) from the Hugging Face Hub and the ONNX runtime (14 MB, served
   from this site under `/ort/`). Both are kept in the browser's cache, so later use is offline.
3. Audio is captured at 16 kHz for up to 8 seconds (or until Stop), transcribed in a
   WebAssembly worker, and matched against the verified phrases. The raw transcript is shown
   to the volunteer only.

## Expectations
- `whisper-base` is multilingual and was not tuned for Thai. Expect rough transcripts on
  short clinic phrases; the bigram matcher tolerates a lot, but a Thai-tuned model will do
  far better.
- Transcribing 5 seconds of audio takes several seconds on a mid-range phone in WebAssembly.
  WebGPU would be faster but is rare on low-end Android; the engine asks for `wasm`.

## Thai-tuned model: converted 2026-10-14

Thonburian Whisper small was exported and quantized on the project lead's Mac (approved
packages: optimum, onnx, onnxruntime, onnx-ir, torch, transformers in `.venv-export`). The
converted model lives outside the repository in
`project_myMediCon/2026-10-14-whisper-th-small-onnx/` with its own README and test results.
In the browser it transcribed three synthetic Thai clinic sentences nearly perfectly at 8-bit
(about 8.5 s per clip on a laptop; the matcher found the right phrase first every time, 82-92%).
Sizes: 8-bit 92 MB encoder + 195 MB decoder; 4-bit 60 MB + 137 MB (slower, same accuracy).

To switch the app to it once the files are hosted: set `ON_DEVICE.modelId` to the Hub repo id
(or to a folder name under `/models/` on this site), `dtype: 'q8'`, and `approxMB: 290`.

## How the conversion was done (for the record)
Thonburian Whisper small (`biodatlab/whisper-th-small-combined`, Apache-2.0, WER 13 on
Common Voice) is the target. It ships as PyTorch weights, so it must be exported to ONNX once:

```bash
uv venv .venv-export --python 3.12
```

```bash
uv pip install --python .venv-export/bin/python "optimum[exporters]" onnx onnxruntime transformers torch
```

```bash
.venv-export/bin/optimum-cli export onnx --model biodatlab/whisper-th-small-combined --task automatic-speech-recognition-with-past exported/whisper-th-small
```

Then quantize to 8-bit (transformers.js expects `onnx/encoder_model_quantized.onnx` and
`onnx/decoder_model_merged_quantized.onnx`), upload the folder to a Hugging Face repo under
the project, and change `ON_DEVICE.modelId` and `approxMB` in `app/src/lib/speech/engine.ts`.
Expect roughly 190 MB. These installs need the project lead's approval first.

## Files
- `app/src/lib/speech/engine.ts`: engine selection, capture, gating (`ON_DEVICE`).
- `app/src/lib/speech/ondevice.ts`: model loading, caching, transcription, prefetch.
- `app/scripts/copy-ort.mjs`: copies the ONNX runtime from `node_modules` into `static/ort/`
  before `dev` and `build` (not committed).
- `app/vite.config.ts`: keeps the package out of prerendering; service worker caches `/ort/`
  and Hugging Face model files after first download.
