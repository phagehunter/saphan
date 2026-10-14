/**
 * Match recognized speech to phrasebook entries.
 *
 * Thai has no spaces between words, and speech recognizers return a single run of characters
 * with their own tokenization. So instead of word overlap we compare character bigrams
 * (Dice coefficient) after stripping spaces, punctuation, and a few interchangeable forms.
 * This is language-agnostic enough to work for English and Burmese too.
 */
export interface Candidate {
	id: string;
	text: string;
}

export interface Match {
	id: string;
	score: number; // 0..1
}

const PUNCT = /[\s\p{P}\p{S}]+/gu;

export function normalize(text: string): string {
	return text
		.normalize('NFC')
		.toLowerCase()
		.replace(PUNCT, '')
		// Thai: treat the two common spellings of "mai" (question particle) and "lae/la" alike.
		.replace(/ไหม|มั้ย/g, 'ไหม')
		.replace(/ค่ะ|คะ|ครับ|นะ|จ้ะ|จ๊ะ/g, '');
}

export function bigrams(s: string): Map<string, number> {
	const m = new Map<string, number>();
	if (s.length < 2) {
		if (s.length === 1) m.set(s, 1);
		return m;
	}
	for (let i = 0; i < s.length - 1; i++) {
		const g = s.slice(i, i + 2);
		m.set(g, (m.get(g) ?? 0) + 1);
	}
	return m;
}

export function dice(a: Map<string, number>, b: Map<string, number>): number {
	let inter = 0;
	let na = 0;
	let nb = 0;
	for (const v of a.values()) na += v;
	for (const v of b.values()) nb += v;
	if (na === 0 || nb === 0) return 0;
	for (const [g, va] of a) {
		const vb = b.get(g);
		if (vb) inter += Math.min(va, vb);
	}
	return (2 * inter) / (na + nb);
}

export class PhraseMatcher {
	private index: { id: string; norm: string; grams: Map<string, number> }[];

	constructor(candidates: Candidate[]) {
		this.index = candidates
			.filter((c) => c.text)
			.map((c) => {
				const norm = normalize(c.text);
				return { id: c.id, norm, grams: bigrams(norm) };
			});
	}

	/** Top matches above `minScore`, best first. Substring containment gets a boost. */
	match(spoken: string, limit = 8, minScore = 0.25): Match[] {
		const q = normalize(spoken);
		if (!q) return [];
		const qg = bigrams(q);
		const out: Match[] = [];
		for (const e of this.index) {
			let s = dice(qg, e.grams);
			if (q.length >= 3 && (e.norm.includes(q) || q.includes(e.norm))) s = Math.max(s, 0.6 + 0.4 * (Math.min(q.length, e.norm.length) / Math.max(q.length, e.norm.length)));
			if (s >= minScore) out.push({ id: e.id, score: s });
		}
		return out.sort((a, b) => b.score - a.score).slice(0, limit);
	}
}
