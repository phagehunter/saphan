<script lang="ts">
	import '../app.css';
	import '@fontsource/noto-sans-thai/400.css';
	import '@fontsource/noto-sans-thai/700.css';
	import '@fontsource/padauk/400.css';
	import '@fontsource/padauk/700.css';
	import TopBar from '$lib/components/TopBar.svelte';
	import Disclaimer from '$lib/components/Disclaimer.svelte';
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import { t } from '$lib/i18n';
	import { settings } from '$lib/settings';
	let { children } = $props();
	const tabs = [
		{ href: '/', key: 'home', ico: '🏠' },
		{ href: '/listen/', key: 'listen', ico: '🎤' },
		{ href: '/translate/', key: 'translate', ico: '✍️' },
		{ href: '/record/', key: 'record', ico: '⏺' },
		{ href: '/about/', key: 'about', ico: 'ℹ️' }
	];
	function active(href: string) {
		const p = page.url.pathname.replace(base, '') || '/';
		return href === '/' ? p === '/' || p.startsWith('/d/') || p.startsWith('/p/') : p.startsWith(href);
	}
</script>

<svelte:head>
	<title>{$t('app_name')}</title>
	<meta name="description" content={$t('tagline')} />
	<meta name="theme-color" content="#0d7a6f" />
</svelte:head>

<div class="min-h-dvh flex flex-col" class:text-lg={$settings.largeText}>
	<TopBar />
	<main class="flex-1 px-4 py-4 max-w-2xl w-full mx-auto">
		{@render children()}
	</main>
	<Disclaimer />
	<nav class="tabbar sticky bottom-0 z-10">
		<div class="max-w-2xl mx-auto grid grid-cols-5">
			{#each tabs as tab (tab.href)}
				<a href="{base}{tab.href}" class="tab" aria-current={active(tab.href) ? 'page' : undefined}>
					<span class="ico" aria-hidden="true">{tab.ico}</span>{$t(tab.key)}
				</a>
			{/each}
		</div>
	</nav>
</div>
