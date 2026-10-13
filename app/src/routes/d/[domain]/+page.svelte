<script lang="ts">
	import PhraseRow from '$lib/components/PhraseRow.svelte';
	import { settings } from '$lib/settings';
	import { t } from '$lib/i18n';
	let { data } = $props();
</script>

<h1 class="text-2xl font-bold mb-3"><span aria-hidden="true">{data.domain.pictogram}</span> {data.domain.label[$settings.uiLang] ?? data.domain.label.en}</h1>
<label class="flex items-center gap-2 mb-3 text-sm">
	<input type="checkbox" bind:checked={$settings.showEnglish} /> {$t('show_english')}
</label>
<div class="flex flex-col gap-2">
	{#each data.phrases as p (p.id)}<PhraseRow phrase={p} />{/each}
</div>
