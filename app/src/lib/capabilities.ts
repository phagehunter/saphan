// Device gating for optional heavy features (Mode B, Mode C). Read-only probes.
export interface Capabilities {
	online: boolean;
	deviceMemoryGB: number | null;
	cores: number | null;
	saveData: boolean;
	webgpu: boolean;
	mediaRecorder: boolean;
	speechRecognition: boolean;
}

export function probe(): Capabilities {
	const nav = navigator as Navigator & { deviceMemory?: number; connection?: { saveData?: boolean }; gpu?: unknown };
	return {
		online: navigator.onLine,
		deviceMemoryGB: nav.deviceMemory ?? null,
		cores: navigator.hardwareConcurrency ?? null,
		saveData: !!nav.connection?.saveData,
		webgpu: 'gpu' in navigator,
		mediaRecorder: typeof MediaRecorder !== 'undefined',
		speechRecognition: 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window
	};
}

/** Whisper-tiny in WebAssembly needs roughly 300 MB of memory. */
export function canRunLocalASR(c: Capabilities): boolean {
	return (c.deviceMemoryGB ?? 0) >= 3 && !c.saveData;
}
