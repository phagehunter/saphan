import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';
import { defineConfig } from 'vite';

// Avoids a dependency on @types/node just for one environment variable.
declare const process: { env: Record<string, string | undefined> };
const base = process.env.BASE_PATH ?? '';

export default defineConfig({
	// transformers.js is browser-only here and large; load it lazily, never during prerender.
	optimizeDeps: { exclude: ['@huggingface/transformers'] },
	ssr: { external: ['@huggingface/transformers'] },
	plugins: [
		tailwindcss(),
		sveltekit(),
		SvelteKitPWA({
			registerType: 'autoUpdate',
			strategies: 'generateSW',
			manifest: {
				name: 'Saphan: health phrases Thai / Burmese / Mon',
				short_name: 'Saphan',
				description: 'Verified clinical phrases with audio for health volunteers. Works offline.',
				start_url: `${base}/`,
				scope: `${base}/`,
				display: 'standalone',
				background_color: '#f6f8f7',
				theme_color: '#0f766e',
				lang: 'th',
				icons: [
					{ src: 'icons/icon-192.svg', sizes: '192x192', type: 'image/svg+xml', purpose: 'any' },
					{ src: 'icons/icon-512.svg', sizes: '512x512', type: 'image/svg+xml', purpose: 'any' }
				]
			},
			workbox: {
				// Precache everything the phrasebook needs, audio included, so Mode A works with no signal.
				globPatterns: ['client/**/*.{js,css,ico,png,svg,woff2,json}', 'prerendered/**/*.html', 'client/audio/**/*.{wav,ogg,opus,mp3}'],
				// The 2.9 MB lexicon is a reviewer tool: fetched on first open, then kept offline.
				globIgnores: ['client/lexicon/**', 'client/ort/**'],
				runtimeCaching: [
					{
						// ONNX runtime WASM (ours) and Whisper model files (Hugging Face): cache after first download.
						urlPattern: ({ url }) => url.pathname.includes('/ort/') || url.hostname === 'huggingface.co' || url.hostname.endsWith('.hf.co'),
						handler: 'CacheFirst',
						options: { cacheName: 'saphan-models', expiration: { maxEntries: 40, maxAgeSeconds: 60 * 60 * 24 * 365 }, cacheableResponse: { statuses: [0, 200] } }
					},
					{
						urlPattern: ({ url }) => url.pathname.includes('/lexicon/') && url.pathname.endsWith('.json'),
						handler: 'CacheFirst',
						options: { cacheName: 'saphan-lexicon', expiration: { maxEntries: 4 }, cacheableResponse: { statuses: [0, 200] } }
					}
				],
				maximumFileSizeToCacheInBytes: 10 * 1024 * 1024
			},
			kit: { includeVersionFile: true }
		})
	]
});
