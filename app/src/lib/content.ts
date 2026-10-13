import type { Bundle, Phrase, Lang } from './types';
import raw from './content/bundle.json';

// The bundle is produced by `python3 -m tools.build` and shipped inside the app,
// so every phrase and its review state is available with no network at all.
export const bundle = raw as unknown as Bundle;

const byId = new Map(bundle.phrases.map((p) => [p.id, p]));

export function phrase(id: string): Phrase | undefined {
	return byId.get(id);
}

export function phrasesIn(domain: string): Phrase[] {
	return bundle.phrases.filter((p) => p.domain === domain);
}

export function domain(id: string) {
	return bundle.domains.find((d) => d.id === id);
}

/** Case-insensitive substring search across all languages. Thai and Burmese have no
 *  word spaces, so substring matching is the honest baseline; a syllable index can come later. */
export function search(query: string, langs: Lang[] = ['th', 'en', 'my', 'mnw']): Phrase[] {
	const q = query.trim().toLowerCase();
	if (!q) return [];
	return bundle.phrases.filter((p) =>
		langs.some((l) => {
			const t = p.lang[l]?.text;
			return t ? t.toLowerCase().includes(q) : false;
		})
	);
}

export const statusLabel: Record<string, Record<Lang, string>> = {
	clinical: { th: 'ตรวจโดยบุคลากรแพทย์', en: 'Clinically verified', my: 'ဆေးဘက်စစ်ဆေးပြီး', mnw: 'Clinically verified' },
	human: { th: 'ตรวจโดยเจ้าของภาษา', en: 'Human reviewed', my: 'လူစစ်ဆေးပြီး', mnw: 'Human reviewed' },
	machine: { th: 'แปลด้วยเครื่อง ยังไม่ตรวจ', en: 'Machine, unreviewed', my: 'စက်ဘာသာပြန်', mnw: 'Machine, unreviewed' },
	draft: { th: 'ฉบับร่าง', en: 'Draft', my: 'မူကြမ်း', mnw: 'Draft' }
};
