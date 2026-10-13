import { error } from '@sveltejs/kit';
import { bundle, domain, phrasesIn } from '$lib/content';
import type { PageLoad, EntryGenerator } from './$types';

export const entries: EntryGenerator = () => bundle.domains.map((d) => ({ domain: d.id }));

export const load: PageLoad = ({ params }) => {
	const d = domain(params.domain);
	if (!d) error(404, 'Unknown topic');
	return { domain: d, phrases: phrasesIn(params.domain) };
};
