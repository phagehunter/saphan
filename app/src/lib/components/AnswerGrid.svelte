<script lang="ts">
	import { bundle } from '$lib/content';
	import { settings } from '$lib/settings';
	import { t } from '$lib/i18n';
	import type { Phrase } from '$lib/types';
	let { phrase, onpick }: { phrase: Phrase; onpick?: (id: string) => void } = $props();
	// Which reply buttons make sense for this phrase.
	const sets: Record<Phrase['expects'], string[]> = {
		yes_no: ['ans-yes', 'ans-no', 'ans-dont-know', 'ans-please-repeat'],
		date: ['ans-today', 'ans-yesterday', 'ans-days-ago', 'ans-weeks-ago', 'ans-dont-know'],
		number: ['ans-a-little', 'ans-a-lot', 'ans-dont-know'],
		choice: ['ans-dont-know', 'ans-please-repeat'],
		free: ['ans-dont-know', 'ans-please-repeat', 'ans-need-interpreter'],
		none: ['ans-please-repeat', 'ans-need-interpreter']
	};
	let answers = $derived(sets[phrase.expects].map((id) => bundle.answers.find((a) => a.id === id)!).filter(Boolean));
	let chosen = $state<string | null>(null);
</script>

<p class="text-sm mb-2" style="color: var(--muted)">{$t('patient_may_answer')}</p>
{#if phrase.expects === 'choice' && phrase.choices.length}
	<div class="grid grid-cols-2 gap-2 mb-2">
		{#each phrase.choices as c}
			<button class="card tap p-3 font-semibold" onclick={() => (chosen = c)} aria-pressed={chosen === c}>{c}</button>
		{/each}
	</div>
{/if}
<div class="grid grid-cols-2 gap-2">
	{#each answers as a (a.id)}
		{@const pl = a.lang[$settings.patientLang]}
		<button
			class="card tap p-3 text-left flex flex-col gap-1"
			style={chosen === a.id ? 'outline: 3px solid var(--brand)' : ''}
			onclick={() => { chosen = a.id; onpick?.(a.id); }}
			aria-pressed={chosen === a.id}
		>
			<span class="text-2xl" aria-hidden="true">{a.pictogram}</span>
			<span class="font-my text-xl leading-tight">{pl.text ? pl.display : (a.lang.my.display ?? '—')}</span>
			<span class="text-sm" style="color: var(--muted)">{a.lang.th.text}</span>
			{#if pl.status === 'draft'}<span class="badge badge-draft">draft</span>{/if}
		</button>
	{/each}
</div>
