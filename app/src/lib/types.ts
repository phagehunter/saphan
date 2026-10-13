export type Lang = 'en' | 'th' | 'my' | 'mnw';
export type PatientLang = 'my' | 'mnw';
export type Status = 'draft' | 'machine' | 'human' | 'clinical';
export type Risk = 'low' | 'medium' | 'high';

export interface AudioClip {
	file: string;
	kind: 'human' | 'synthetic';
	recorded_by?: string;
	voice?: string;
	date?: string;
}

export interface LangEntry {
	text: string | null;
	display: string | null;
	status: Status;
	locked?: boolean;
	lock_reason?: 'unreviewed' | 'needs_clinical_review';
	audio?: AudioClip | null;
	reviewed_by?: string;
	variant_th?: { text: string; display: string; status: Status; audio?: AudioClip | null };
}

export interface Phrase {
	id: string;
	domain: string;
	intent: string;
	risk: Risk;
	expects: 'none' | 'yes_no' | 'date' | 'number' | 'choice' | 'free';
	choices: string[];
	pictogram: string;
	lang: Record<Lang, LangEntry>;
	source: string;
	notes: string;
}

export interface Answer {
	id: string;
	pictogram: string;
	lang: Record<Lang, { text: string | null; display: string | null; status: Status }>;
}

export interface Domain {
	id: string;
	pictogram: string;
	label: Record<Lang, string | null>;
	count: number;
	show_when_empty?: boolean;
}

export interface Bundle {
	version: string;
	domains: Domain[];
	phrases: Phrase[];
	answers: Answer[];
	sources: Record<string, { title: string; url: string; license: string; attribution: string }>;
	skipped: string[];
}
