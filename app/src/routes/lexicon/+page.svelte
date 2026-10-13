<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import { t } from '$lib/i18n';
	import { settings } from '$lib/settings';

	// Reviewer-side term lookup. Loaded only when this screen opens, so the core app stays small.
	type Entry = [mon: string, en: string, my: string, th: string, thPron: string, pos: string, src: string];
	let entries = $state<Entry[]>([]);
	let loading = $state(true);
	let failed = $state(false);
	let query = $state('');
	let lower: string[] = [];

	onMount(async () => {
		try {
			const res = await fetch(`${base}/lexicon/mnw.json`);
			const data = (await res.json()) as { entries: Entry[] };
			entries = data.entries;
			lower = entries.map((e) => `${e[0]} ${e[1]} ${e[2]} ${e[3]}`.toLowerCase());
			const q = page.url.searchParams.get('q');
			if (q) query = q;
		} catch {
			failed = true;
		} finally {
			loading = false;
		}
	});

	let results = $derived.by(() => {
		const q = query.trim().toLowerCase();
		if (!q || q.length < 2) return [] as Entry[];
		const out: Entry[] = [];
		for (let i = 0; i < entries.length && out.length < 60; i++) {
			if (lower[i].includes(q)) out.push(entries[i]);
		}
		// Exact or prefix matches first.
		return out.sort((a, b) => score(b, q) - score(a, q));
	});
	function score(e: Entry, q: string) {
		const fields = [e[0], e[1], e[2], e[3]].map((f) => f.toLowerCase());
		if (fields.some((f) => f === q)) return 3;
		if (fields.some((f) => f.startsWith(q))) return 2;
		return 1;
	}
</script>

<h1 class="text-2xl font-bold mb-1">📖 {$t('lexicon')}</h1>
<p class="text-sm mb-4" style="color: var(--muted)">{$t('lexicon_hint')}</p>

<label class="block relative mb-3">
	<span class="sr-only">{$t('lexicon')}</span>
	<span class="absolute left-4 top-1/2 -translate-y-1/2 text-lg opacity-60" aria-hidden="true">⌕</span>
	<input class="card tap w-full pl-11 pr-4 text-lg" type="search" bind:value={query} placeholder="fever · ဖျား · ไข้" autocomplete="off" autocapitalize="off" spellcheck="false" />
</label>

{#if loading}
	<p class="card-flat p-4 text-sm" style="color: var(--muted)">…</p>
{:else if failed}
	<p class="card-flat p-4 text-sm" style="color: var(--danger)">The lexicon file could not be loaded. Run <code>python3 -m tools.build_lexicon</code> and rebuild.</p>
{:else if query.trim().length >= 2}
	<p class="text-xs font-semibold uppercase tracking-wide mb-2" style="color: var(--muted)">{results.length}{results.length === 60 ? '+' : ''} · {entries.length.toLocaleString()} entries</p>
	<ul class="flex flex-col gap-2">
		{#each results as e, i (e[0] + e[1] + e[3] + i)}
			<li class="card-flat p-3 flex flex-col gap-1">
				<div class="flex items-baseline justify-between gap-3">
					<span class="font-my text-xl" lang="mnw">{e[0]}</span>
					{#if e[5]}<span class="badge badge-draft">{e[5]}</span>{/if}
				</div>
				{#if e[1]}<span class="text-sm" lang="en">{e[1]}</span>{/if}
				{#if e[2]}<span class="font-my text-sm" lang="my" style="color: var(--muted)">{e[2]}</span>{/if}
				{#if e[3]}<span class="text-sm" lang="th">{e[3]}{#if e[4]} <span style="color: var(--muted)">· {e[4]}</span>{/if}</span>{/if}
				<span class="text-[10px] uppercase tracking-wide" style="color: var(--muted)">{e[6] === 'mondictdb' ? 'MonDictDB · MIT' : 'Nenemin95 lexicon · CC BY 4.0'}</span>
			</li>
		{/each}
	</ul>
{:else}
	<div class="card-flat p-4 text-sm" style="color: var(--muted)">
		<p>{entries.length.toLocaleString()} entries from two open sources (see <a class="underline" href="{base}/about/">About</a>). Type at least two characters in Mon, English, Burmese, or Thai.</p>
	</div>
{/if}
