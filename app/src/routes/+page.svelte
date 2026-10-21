<script lang="ts">
	import { base } from '$app/paths';
	import { bundle, search, phrase } from '$lib/content';
	import { t, translate } from '$lib/i18n';
	import { settings } from '$lib/settings';
	import { listRecent, listFavorites } from '$lib/db';
	import PhraseRow from '$lib/components/PhraseRow.svelte';
	import Pictogram from '$lib/components/Pictogram.svelte';
	import { onMount } from 'svelte';

	let query = $state('');
	let results = $derived(search(query));
	let recent = $state<string[]>([]);
	let favorites = $state<string[]>([]);
	let ready = $derived(bundle.domains.filter((d) => d.count > 0));
	let upcoming = $derived(bundle.domains.filter((d) => d.count === 0));
	onMount(async () => {
		recent = await listRecent();
		favorites = await listFavorites();
	});
</script>

<section class="mb-4">
	<h1 class="text-2xl font-extrabold tracking-tight" style="color: var(--brand)">{$t('app_name')}</h1>
	<p class="text-sm mt-1" style="color: var(--muted)">{$t('home_intro')}</p>
	{#if $settings.uiLang !== 'en'}
		<p class="text-sm mt-1" lang="en" style="color: var(--muted)">{translate('home_intro', 'en')}</p>
	{/if}
</section>

<section class="mb-5">
	<label class="block relative">
		<span class="sr-only">{$t('search')}</span>
		<span class="absolute left-4 top-1/2 -translate-y-1/2 text-lg opacity-60" aria-hidden="true">⌕</span>
		<input
			class="card tap w-full pl-11 pr-4 text-lg"
			style="box-shadow: var(--shadow)"
			type="search"
			placeholder={$t('search')}
			bind:value={query}
			autocomplete="off"
			autocapitalize="off"
			spellcheck="false"
			inputmode="search"
			enterkeyhint="search"
		/>
	</label>
</section>

{#if query.trim()}
	<section aria-live="polite" class="flex flex-col gap-2">
		<p class="text-xs font-semibold uppercase tracking-wide" style="color: var(--muted)">{results.length} {$t('phrases')}</p>
		{#each results as p (p.id)}<PhraseRow phrase={p} />{:else}
			<p class="card-flat p-4" style="color: var(--muted)">{$t('no_results')}</p>
		{/each}
	</section>
{:else}
	<h2 class="text-xs font-semibold uppercase tracking-wide mb-2" style="color: var(--muted)">{$t('domains')}</h2>
	<div class="grid grid-cols-2 gap-3 mb-6">
		{#each ready as d (d.id)}
			<a href="{base}/d/{d.id}/" class="card tap pressable p-4 flex flex-col gap-2">
				<span style="color: var(--brand)"><Pictogram name={d.pictogram} size={36} /></span>
				<span class="font-bold leading-tight">{d.label[$settings.uiLang] ?? d.label.en}</span>
				<span class="text-xs font-semibold" style="color: var(--brand)">{d.count} {$t('phrases')}</span>
			</a>
		{/each}
		{#each upcoming as d (d.id)}
			<div class="card-flat tap p-4 flex flex-col gap-2 opacity-70" aria-disabled="true" style="border-style: dashed">
				<span style="color: var(--muted)"><Pictogram name={d.pictogram} size={36} /></span>
				<span class="font-bold leading-tight">{d.label[$settings.uiLang] ?? d.label.en}</span>
				<span class="text-xs" style="color: var(--muted)">{$t('no_translation')}</span>
			</div>
		{/each}
	</div>

	{#if favorites.length}
		<h2 class="text-xs font-semibold uppercase tracking-wide mb-2" style="color: var(--muted)">⭐ {$t('favorites')}</h2>
		<div class="flex flex-col gap-2 mb-6">
			{#each favorites as id (id)}{@const p = phrase(id)}{#if p}<PhraseRow phrase={p} />{/if}{/each}
		</div>
	{/if}
	{#if recent.length}
		<h2 class="text-xs font-semibold uppercase tracking-wide mb-2" style="color: var(--muted)">🕒 {$t('recent')}</h2>
		<div class="flex flex-col gap-2">
			{#each recent as id (id)}{@const p = phrase(id)}{#if p}<PhraseRow phrase={p} />{/if}{/each}
		</div>
	{/if}
{/if}
