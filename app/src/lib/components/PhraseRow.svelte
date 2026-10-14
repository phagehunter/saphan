<script lang="ts">
	import type { Phrase } from '$lib/types';
	import { base } from '$app/paths';
	import { settings } from '$lib/settings';
	import StatusBadge from './StatusBadge.svelte';
	import Pictogram from './Pictogram.svelte';
	let { phrase }: { phrase: Phrase } = $props();
	let patient = $derived(phrase.lang[$settings.patientLang]);
	let primary = $derived(($settings.uiLang === 'en' ? 'en' : 'th') as 'en' | 'th');
	let secondary = $derived((primary === 'en' ? 'th' : 'en') as 'en' | 'th');
</script>

<a href="{base}/p/{phrase.id}/" class="card-flat tap pressable flex items-center gap-3 p-3">
	<span class="w-9 flex justify-center shrink-0" style="color: var(--brand)"><Pictogram name={phrase.pictogram} size={30} /></span>
	<span class="flex-1 min-w-0">
		<span class="block font-semibold leading-snug">{phrase.lang[primary].text}</span>
		{#if $settings.showEnglish || primary === 'en'}
			<span class="block text-xs" style="color: var(--muted)">{phrase.lang[secondary].text}</span>
		{/if}
		<span class="block font-my text-sm truncate" style="color: var(--muted)">
			{#if patient.text}{patient.locked ? '🔒 ' : ''}{patient.display}{:else}—{/if}
		</span>
	</span>
	<span class="flex flex-col items-end gap-1 shrink-0">
		<StatusBadge status={phrase.lang[primary].status} compact />
		{#if phrase.risk === 'high'}<span class="badge badge-danger" title="high risk">!</span>{/if}
	</span>
</a>
