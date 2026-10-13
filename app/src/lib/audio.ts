import { base } from '$app/paths';
import type { AudioClip } from './types';

let current: HTMLAudioElement | null = null;

/** Play a clip. Returns false if the file could not be played (missing or unsupported). */
export async function play(clip: AudioClip): Promise<boolean> {
	stop();
	const el = new Audio(`${base}/${clip.file}`);
	current = el;
	try {
		await el.play();
		return true;
	} catch {
		current = null;
		return false;
	}
}

export function stop() {
	if (current) {
		current.pause();
		current = null;
	}
}

/** Browser speech synthesis as a last resort for Thai only (Android ships a Thai voice;
 *  Burmese is unverified and Mon does not exist anywhere). Never used for patient-facing output. */
export function speakThai(text: string) {
	if (!('speechSynthesis' in window)) return false;
	const u = new SpeechSynthesisUtterance(text);
	u.lang = 'th-TH';
	window.speechSynthesis.speak(u);
	return true;
}
