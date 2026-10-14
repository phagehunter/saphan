<script lang="ts">
	import { onMount } from 'svelte';
	import { base } from '$app/paths';
	import { settings } from '$lib/settings';
	import { t } from '$lib/i18n';
	import { bundle } from '$lib/content';
	import { touchRecent, toggleFavorite, isFavorite } from '$lib/db';
	import StatusBadge from '$lib/components/StatusBadge.svelte';
	import AudioButton from '$lib/components/AudioButton.svelte';
	import AnswerGrid from '$lib/components/AnswerGrid.svelte';
	import Pictogram from '$lib/components/Pictogram.svelte';

	let { data } = $props();
	let p = $derived(data.phrase);
	let patient = $derived(p.lang[$settings.patientLang]);
	let primary = $derived(($settings.uiLang === 'en' ? 'en' : 'th') as 'en' | 'th');
	let secondary = $derived((primary === 'en' ? 'th' : 'en') as 'en' | 'th');
	let fav = $state(false);
	let patientMode = $state(false);
	onMount(async () => {
		await touchRecent(p.id);
		fav = await isFavorite(p.id);
	});
	const riskKey = { low: 'risk_low', medium: 'risk_medium', high: 'risk_high' } as const;
</script>

{#if patientMode}
	<!-- Patient-facing screen: only verified, unlocked content; huge text; one button. -->
	<section class="fixed inset-0 z-20 flex flex-col p-6 gap-6" style="background: var(--surface)">
		<button class="self-start tap px-4 card" onclick={() => (patientMode = false)}>← {$t('back')}</button>
		<div class="flex-1 flex flex-col justify-center gap-6">
			<p class="flex justify-center" style="color: var(--brand)"><Pictogram name={p.pictogram} size={96} /></p>
			{#if patient.text && !patient.locked}
				<p class="font-my text-4xl leading-relaxed text-center" lang={$settings.patientLang}>{patient.display}</p>
				<AudioButton clip={patient.audio} big />
			{:else}
				<p class="text-2xl text-center" style="color: var(--lock)">🔒 {$t(patient.lock_reason === 'needs_clinical_review' ? 'locked_clinical' : patient.text ? 'locked_unreviewed' : 'no_translation')}</p>
			{/if}
		</div>
		<AnswerGrid phrase={p} />
	</section>
{/if}

<article class="flex flex-col gap-4">
	<header class="flex items-start gap-3">
		<span style="color: var(--brand)"><Pictogram name={p.pictogram} size={56} /></span>
		<div class="flex-1">
			<h1 class="text-2xl font-bold leading-snug" lang={primary}>{p.lang[primary].text}</h1>
			<div class="flex flex-wrap gap-2 mt-1 items-center">
				<StatusBadge status={p.lang[primary].status} reviewedBy={p.lang[primary].reviewed_by} />
				<span class="badge" style="color: var({p.risk === 'high' ? '--danger' : p.risk === 'medium' ? '--warn' : '--ok'})">{$t(riskKey[p.risk])}</span>
				<button class="badge" onclick={async () => (fav = await toggleFavorite(p.id))} aria-pressed={fav}>{fav ? '⭐' : '☆'} {$t('favorites')}</button>
			</div>
		</div>
	</header>

	{#if p.lang[primary].status === 'machine'}
		<p class="card p-3 text-sm" style="background: var(--warn-bg); color: var(--warn)">⚠︎ {$t(primary === 'th' ? 'thai_machine_warning' : 'english_machine_warning')}</p>
	{/if}

	<label class="flex items-center gap-2 text-sm">
		<input type="checkbox" bind:checked={$settings.showEnglish} /> {$t(primary === 'en' ? 'show_thai' : 'show_english')}
	</label>
	{#if $settings.showEnglish}
		<p class="card p-3" lang={secondary}>{p.lang[secondary].text} <StatusBadge status={p.lang[secondary].status} /></p>
	{/if}

	{#each ['my', 'mnw'] as const as lang (lang)}
		{@const e = p.lang[lang]}
		<section class="card p-4 flex flex-col gap-2" style={$settings.patientLang === lang ? 'outline: 2px solid var(--brand)' : ''}>
			<div class="flex items-center justify-between">
				<h2 class="font-semibold">{$t(lang === 'my' ? 'burmese' : 'mon')}</h2>
				<StatusBadge status={e.status} reviewedBy={e.reviewed_by} />
			</div>
			{#if e.text}
				<p class="font-my text-2xl leading-relaxed" lang={lang} style={e.locked ? 'color: var(--lock)' : ''}>{e.display}</p>
				{#if e.locked}
					<p class="text-sm" style="color: var(--lock)">🔒 {$t(e.lock_reason === 'needs_clinical_review' ? 'locked_clinical' : 'locked_unreviewed')}</p>
				{:else}
					<AudioButton clip={e.audio} />
				{/if}
				{#if e.variant_th}
					<div class="card-flat p-3 mt-1" style="background: var(--surface-2)">
						<p class="text-xs font-semibold uppercase tracking-wide mb-1" style="color: var(--muted)">{$t('thai_mon_wording')}</p>
						<p class="font-my text-xl" lang="mnw">{e.variant_th.display}</p>
						{#if !e.locked}<AudioButton clip={e.variant_th.audio} />{/if}
					</div>
				{/if}
			{:else}
				<p style="color: var(--muted)">{$t('no_translation')}</p>
				<div class="flex flex-wrap gap-3 text-sm">
					<a class="underline" href="{base}/lexicon/?q={encodeURIComponent((p.lang.en.text ?? '').split(' ').slice(0, 2).join(' ').replace(/[?.,]/g, ''))}">📖 {$t('lexicon')}</a>
					<a class="underline" href="https://github.com/phagehunter/saphan/blob/main/docs/contributing-a-phrase.md" rel="noopener">{$t('help_translate')} →</a>
				</div>
			{/if}
		</section>
	{/each}

	<button class="tap btn-brand w-full text-xl font-bold py-4" onclick={() => (patientMode = true)}>
		📱 {$t('show_to_patient')}
	</button>

	<section class="card p-4">
		<AnswerGrid phrase={p} />
	</section>

	<details class="text-sm" style="color: var(--muted)">
		<summary>{$t('source')} · {$t('notes_for_reviewers')}</summary>
		<p class="mt-2">{bundle.sources[p.source]?.title} — {bundle.sources[p.source]?.license}</p>
		{#if p.notes}<p class="mt-2" style="color: var(--warn)">{p.notes}</p>{/if}
		<p class="mt-2">id: <code>{p.id}</code> · intent: <code>{p.intent}</code></p>
	</details>
</article>
