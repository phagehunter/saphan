import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

// BASE_PATH is "/<repo-name>" on GitHub Pages and empty when running locally.
const base = process.env.BASE_PATH ?? '';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({ pages: 'build', assets: 'build', fallback: '404.html', strict: true }),
		paths: { base },
		prerender: { entries: ['*'], handleHttpError: 'warn' }
	}
};

export default config;
