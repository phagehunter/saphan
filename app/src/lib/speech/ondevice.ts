/**
 * On-device transcription with Whisper in the browser (transformers.js, Apache-2.0).
 *
 * Loaded only when the user taps the microphone with the on-device engine selected, so the
 * core app never pays for it. The model is fetched from the Hugging Face Hub on first use and
 * kept in the browser's cache storage, so later use works with no signal. The ONNX runtime's
 * WebAssembly files are served from this site (static/ort/), not from a CDN, for the same
 * reason.
 *
 * Model: 'onnx-community/whisper-base' (multilingual). Thai accuracy zero-shot is mediocre;
 * the real target is a Thai fine-tune (Thonburian Whisper small) exported to ONNX, which needs
 * a one-time conversion on a laptop (see docs/mode-b-on-device.md).
 */
import { base } from '$app/paths';

const WHISPER_LANG: Record<string, string> = { th: 'thai', en: 'english', my: 'burmese' };

type Pipe = (audio: Float32Array, opts: Record<string, unknown>) => Promise<{ text: string } | { text: string }[]>;
let pipePromise: Promise<Pipe> | null = null;
let loadedModel = '';

async function load(modelId: string, onProgress?: (msg: string) => void): Promise<Pipe> {
	if (pipePromise && loadedModel === modelId) return pipePromise;
	loadedModel = modelId;
	pipePromise = (async () => {
		const tf = await import('@huggingface/transformers');
		tf.env.allowLocalModels = false;
		tf.env.useBrowserCache = true;
		// Serve the WASM runtime from our own origin so the PWA stays self-contained.
		tf.env.backends.onnx.wasm!.wasmPaths = `${base}/ort/`;
		const seen = new Map<string, number>();
		const asr = await tf.pipeline('automatic-speech-recognition', modelId, {
			dtype: 'q8',
			device: 'wasm',
			progress_callback: (p: { status: string; file?: string; progress?: number }) => {
				if (p.status === 'progress' && p.file) {
					seen.set(p.file, p.progress ?? 0);
					const avg = [...seen.values()].reduce((a, b) => a + b, 0) / seen.size;
					onProgress?.(`Downloading model ${Math.round(avg)}%`);
				} else if (p.status === 'ready') onProgress?.('Model ready');
			}
		});
		return asr as unknown as Pipe;
	})();
	return pipePromise;
}

export async function transcribe(
	audio16k: Float32Array,
	lang: 'th' | 'en' | 'my',
	modelId: string,
	onProgress?: (msg: string) => void
): Promise<string> {
	const asr = await load(modelId, onProgress);
	onProgress?.('Transcribing…');
	const out = await asr(audio16k, { language: WHISPER_LANG[lang], task: 'transcribe', chunk_length_s: 30 });
	const text = Array.isArray(out) ? out.map((o) => o.text).join(' ') : out.text;
	return text.trim();
}

/** Lets the Listen screen pre-download the model on request (e.g. while on Wi-Fi). */
export async function prefetch(modelId: string, onProgress?: (msg: string) => void) {
	await load(modelId, onProgress);
}
