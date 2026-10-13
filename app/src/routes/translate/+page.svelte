<script lang="ts">
	import { t } from '$lib/i18n';
	let text = $state('');
	let confirmed = $state(false);
	// Mock-up only. Nothing is sent anywhere. This shows what Mode C would look like when enabled.
	const mock = {
		my: 'ဤသည်မှာ နမူနာဘာသာပြန်ဖြစ်သည်။',
		back: 'This is an example translation.',
		score: 0.62
	};
	let band = $derived(mock.score >= 0.8 ? 'good' : mock.score >= 0.6 ? 'uncertain' : 'poor');
</script>

<h1 class="text-2xl font-bold mb-2">✍️ {$t('translate')} <span class="badge badge-draft">Mode C · disabled by default</span></h1>
<p class="mb-4 text-sm" style="color: var(--muted)">Free-text machine translation is off (open question 8: no cloud services). This page is a working mock-up of the safety layout: a quality band, a back-translation the volunteer must read, and a hard block for consent and dosing topics. Mon is never offered here because no machine translation exists for Mon.</p>

<label class="block mb-3">
	<span class="text-sm">Thai sentence</span>
	<textarea class="card w-full p-3 mt-1" rows="3" bind:value={text} placeholder="พิมพ์ประโยคภาษาไทย…"></textarea>
</label>
<button class="tap btn-brand px-5 font-semibold" disabled={!text.trim()}>Translate to Burmese (mock)</button>

{#if text.trim()}
	<section class="card p-4 mt-4 flex flex-col gap-3">
		<div class="flex items-center justify-between">
			<h2 class="font-semibold">Burmese (machine)</h2>
			<span class="badge" style="color: var({band === 'good' ? '--ok' : band === 'uncertain' ? '--warn' : '--danger'})">quality {Math.round(mock.score * 100)}% · {band}</span>
		</div>
		<p class="font-my text-2xl" lang="my">{mock.my}</p>
		<div class="card p-3" style="background: var(--surface-2)">
			<p class="text-xs uppercase tracking-wide" style="color: var(--muted)">Back-translation (read this before showing)</p>
			<p>{mock.back}</p>
		</div>
		<label class="flex items-center gap-2 text-sm">
			<input type="checkbox" bind:checked={confirmed} /> I read the back-translation and it says what I meant.
		</label>
		<button class="tap btn-brand w-full font-semibold" disabled={!confirmed}>📱 {$t('show_to_patient')}</button>
		<p class="text-xs" style="color: var(--danger)">Blocked topics in Mode C: consent, medication doses, diagnoses, prognosis. Use a verified phrase or an interpreter for those.</p>
	</section>
{/if}
