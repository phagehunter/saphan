import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import type { Lang, PatientLang } from './types';

export type ProviderLang = 'th' | 'en';

export interface Settings {
	uiLang: Lang;
	patientLang: PatientLang;
	showEnglish: boolean;
	hotline: string;
	largeText: boolean;
}

const DEFAULTS: Settings = { uiLang: 'th', patientLang: 'my', showEnglish: false, hotline: '', largeText: false };
const KEY = 'saphan.settings.v1';

function load(): Settings {
	if (!browser) return DEFAULTS;
	try {
		const raw = localStorage.getItem(KEY);
		return raw ? { ...DEFAULTS, ...JSON.parse(raw) } : DEFAULTS;
	} catch {
		return DEFAULTS;
	}
}

export const settings = writable<Settings>(load());

if (browser) {
	settings.subscribe((v) => {
		try {
			localStorage.setItem(KEY, JSON.stringify(v));
		} catch {
			/* private mode or storage blocked: settings just do not persist */
		}
	});
}
