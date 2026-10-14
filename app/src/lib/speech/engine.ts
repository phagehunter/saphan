/**
 * Speech engines for Mode B. Every engine produces text; the matcher turns text into verified
 * phrases. Nothing here ever shows raw recognized text to a patient.
 *
 *  - WebSpeechEngine: the phone's built-in recognizer (Chrome on Android sends audio to Google).
 *    Zero download, needs a connection, labeled "online" in the UI.
 *  - OnDeviceEngine: Whisper in the browser via transformers.js. Optional model download,
 *    works with no signal afterwards. Behind a feature flag until the package is approved.
 */
export type Lang = 'th' | 'en' | 'my';

export interface EngineStatus {
	available: boolean;
	reason?: string;
	online: boolean;
	downloadMB?: number;
}

export interface SpeechEngine {
	id: 'webspeech' | 'ondevice';
	label: string;
	status(): Promise<EngineStatus>;
	start(lang: Lang, onPartial: (text: string) => void, onFinal: (text: string) => void, onError: (msg: string) => void): Promise<void>;
	stop(): void;
}

const BCP47: Record<Lang, string> = { th: 'th-TH', en: 'en-US', my: 'my-MM' };

type SR = typeof window extends { SpeechRecognition: infer T } ? T : any;

export class WebSpeechEngine implements SpeechEngine {
	id = 'webspeech' as const;
	label = 'Phone speech recognition';
	private rec: any = null;

	private ctor(): SR | null {
		const w = window as any;
		return w.SpeechRecognition ?? w.webkitSpeechRecognition ?? null;
	}

	async status(): Promise<EngineStatus> {
		if (typeof window === 'undefined' || !this.ctor()) return { available: false, online: true, reason: 'This browser has no built-in speech recognition. Chrome on Android has it.' };
		if (!navigator.onLine) return { available: false, online: true, reason: 'Built-in recognition needs a connection.' };
		return { available: true, online: true };
	}

	async start(lang: Lang, onPartial: (t: string) => void, onFinal: (t: string) => void, onError: (m: string) => void) {
		const Ctor = this.ctor();
		if (!Ctor) return onError('no speech recognition');
		const rec = new Ctor();
		this.rec = rec;
		rec.lang = BCP47[lang];
		rec.interimResults = true;
		rec.maxAlternatives = 3;
		rec.continuous = false;
		let finalText = '';
		rec.onresult = (ev: any) => {
			let interim = '';
			for (let i = ev.resultIndex; i < ev.results.length; i++) {
				const r = ev.results[i];
				if (r.isFinal) finalText += r[0].transcript;
				else interim += r[0].transcript;
			}
			onPartial(finalText + interim);
		};
		rec.onerror = (ev: any) => onError(ev.error === 'not-allowed' ? 'Microphone permission was refused.' : ev.error === 'no-speech' ? 'No speech heard.' : String(ev.error));
		rec.onend = () => {
			if (finalText) onFinal(finalText);
			this.rec = null;
		};
		rec.start();
	}

	stop() {
		this.rec?.stop();
	}
}

export interface OnDeviceConfig {
	enabled: boolean;      // feature flag; the transformers.js package was approved and installed 2026-10-14
	modelId: string;       // Hub id (with '/') or a folder under /models/ on this site (no '/')
	dtype: 'q8' | 'q4' | 'fp32';
	approxMB: number;
	minDeviceMemoryGB: number;
}

export const ON_DEVICE: OnDeviceConfig = {
	enabled: true,
	modelId: 'onnx-community/whisper-base',
	dtype: 'q8',
	approxMB: 80,
	minDeviceMemoryGB: 3
};

export class OnDeviceEngine implements SpeechEngine {
	id = 'ondevice' as const;
	label = 'On-device recognition (download once)';
	private stopFn: (() => void) | null = null;

	async status(): Promise<EngineStatus> {
		if (!ON_DEVICE.enabled) return { available: false, online: false, downloadMB: ON_DEVICE.approxMB, reason: 'Not enabled in this build yet (needs the on-device speech package).' };
		const mem = (navigator as any).deviceMemory as number | undefined;
		if (mem !== undefined && mem < ON_DEVICE.minDeviceMemoryGB) return { available: false, online: false, downloadMB: ON_DEVICE.approxMB, reason: `Needs about ${ON_DEVICE.minDeviceMemoryGB} GB of memory; this phone reports ${mem} GB.` };
		if (typeof MediaRecorder === 'undefined') return { available: false, online: false, reason: 'No microphone API.' };
		return { available: true, online: false, downloadMB: ON_DEVICE.approxMB };
	}

	async start(lang: Lang, onPartial: (t: string) => void, onFinal: (t: string) => void, onError: (m: string) => void) {
		if (!ON_DEVICE.enabled) return onError('on-device engine disabled');
		// Capture up to 8 s of 16 kHz mono audio, then hand it to the transcriber.
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
			const ctx = new AudioContext({ sampleRate: 16000 });
			const src = ctx.createMediaStreamSource(stream);
			const proc = ctx.createScriptProcessor(4096, 1, 1);
			const chunks: Float32Array[] = [];
			proc.onaudioprocess = (e) => chunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
			src.connect(proc);
			proc.connect(ctx.destination);
			onPartial('…');
			const finish = async () => {
				proc.disconnect();
				src.disconnect();
				stream.getTracks().forEach((t) => t.stop());
				await ctx.close();
				const total = chunks.reduce((n, c) => n + c.length, 0);
				const audio = new Float32Array(total);
				let o = 0;
				for (const c of chunks) {
					audio.set(c, o);
					o += c.length;
				}
				// Whisper invents text on silence, so refuse clips with almost no energy.
				let energy = 0;
				for (let i = 0; i < audio.length; i++) energy += audio[i] * audio[i];
				const rms = Math.sqrt(energy / Math.max(1, audio.length));
				if (audio.length < 16000 * 0.5 || rms < 0.005) return onError('No speech heard.');
				try {
					const { transcribe } = await import('./ondevice');
					onFinal(await transcribe(audio, lang, ON_DEVICE.modelId, onPartial, ON_DEVICE.dtype));
				} catch (e) {
					onError('On-device transcription failed: ' + (e as Error).message);
				}
			};
			const timer = setTimeout(finish, 8000);
			this.stopFn = () => {
				clearTimeout(timer);
				void finish();
			};
		} catch {
			onError('Microphone permission was refused.');
		}
	}

	stop() {
		this.stopFn?.();
		this.stopFn = null;
	}
}

export const engines: SpeechEngine[] = [new OnDeviceEngine(), new WebSpeechEngine()];
