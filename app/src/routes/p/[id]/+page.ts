import { error } from '@sveltejs/kit';
import { bundle, phrase } from '$lib/content';
import type { PageLoad, EntryGenerator } from './$types';

export const entries: EntryGenerator = () => bundle.phrases.map((p) => ({ id: p.id }));

export const load: PageLoad = ({ params }) => {
	const p = phrase(params.id);
	if (!p) error(404, 'Unknown phrase');
	return { phrase: p };
};
