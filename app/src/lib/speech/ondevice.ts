/**
 * On-device transcription with Whisper in the browser.
 *
 * NOT ACTIVE YET. This module is only imported when ON_DEVICE.enabled is true in engine.ts.
 * It needs the `@huggingface/transformers` package (Apache-2.0), which has not been added to
 * package.json pending the project lead's approval. When it is:
 *
 *   1. `pnpm add @huggingface/transformers` in app/
 *   2. uncomment the import below and delete the throw
 *   3. set ON_DEVICE.enabled = true in engine.ts
 *
 * Model choice: 'onnx-community/whisper-base' is multilingual and ~80 MB quantized; Thai
 * accuracy zero-shot is mediocre. A Thai fine-tune (Thonburian Whisper small, Apache-2.0)
 * exported to ONNX with optimum would be the real target (~190 MB). The model is downloaded
 * once and cached by the browser, so it works offline afterwards.
 */
// import { pipeline } from '@huggingface/transformers';

const WHISPER_LANG: Record<string, string> = { th: 'thai', en: 'english', my: 'burmese' };

export async function transcribe(
	_audio16k: Float32Array,
	_lang: 'th' | 'en' | 'my',
	_modelId: string,
	_onProgress?: (msg: string) => void
): Promise<string> {
	// const asr = await pipeline('automatic-speech-recognition', _modelId, {
	// 	dtype: 'q8',
	// 	progress_callback: (p: any) => _onProgress?.(p.status === 'progress' ? `Downloading model ${Math.round(p.progress)}%` : p.status)
	// });
	// const out = await asr(_audio16k, { language: WHISPER_LANG[_lang], task: 'transcribe' });
	// return Array.isArray(out) ? out.map((o) => o.text).join(' ') : out.text;
	void WHISPER_LANG;
	throw new Error('on-device package not installed');
}
