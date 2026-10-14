<script lang="ts">
	import { bundle } from '$lib/content';
	import { settings } from '$lib/settings';
	import { t } from '$lib/i18n';
	import StatusBadge from '$lib/components/StatusBadge.svelte';
	// Partner recording page. Records one phrase in the chosen language and offers the clip as a
	// download. The maintainer then adds it under app/static/audio/<lang>/ and sets audio.<lang>
	// (or variants.mnw-TH.audio for the Thai-side Mon wording) with kind "human" and recorded_by.
	type RecLang = 'my' | 'mnw' | 'mnw-TH';
	let phraseId = $state(bundle.phrases[0]?.id ?? '');
	let recLang = $state<RecLang>($settings.patientLang);
	let recorder: MediaRecorder | null = null;
	let chunks: Blob[] = [];
	let status = $state<'idle' | 'recording' | 'done' | 'error'>('idle');
	let url = $state<string | null>(null);
	let name = $state('');
	let phrase = $derived(bundle.phrases.find((p) => p.id === phraseId));
	let entry = $derived.by(() => {
		if (!phrase) return null;
		if (recLang === 'mnw-TH') {
			const v = phrase.lang.mnw.variant_th;
			return v ? { text: v.text, display: v.display, status: v.status } : null;
		}
		const e = phrase.lang[recLang];
		return e.text ? { text: e.text, display: e.display ?? e.text, status: e.status } : null;
	});
	let fileSuffix = $derived(recLang === 'mnw-TH' ? 'mnw.th' : recLang);
	let langLabel = $derived(recLang === 'my' ? $t('burmese') : recLang === 'mnw' ? $t('mon') : $t('thai_mon_wording'));

	async function start() {
		try {
			const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
			chunks = [];
			recorder = new MediaRecorder(stream);
			recorder.ondataavailable = (e) => chunks.push(e.data);
			recorder.onstop = () => {
				const blob = new Blob(chunks, { type: recorder?.mimeType || 'audio/webm' });
				url = URL.createObjectURL(blob);
				status = 'done';
				stream.getTracks().forEach((t) => t.stop());
			};
			recorder.start();
			status = 'recording';
		} catch {
			status = 'error';
		}
	}
	function stop() {
		recorder?.stop();
	}
</script>

<h1 class="text-2xl font-bold mb-2">⏺ {$t('record')}</h1>
<p class="text-sm mb-4" style="color: var(--muted)">{$t('record_hint')}</p>

<div class="grid grid-cols-1 gap-3 mb-3">
	<label class="block">
		<span class="text-xs font-semibold uppercase tracking-wide" style="color: var(--muted)">{$t('phrases')}</span>
		<select class="card-flat tap w-full px-3 mt-1" bind:value={phraseId}>
			{#each bundle.phrases as p (p.id)}<option value={p.id}>{p.id} · {p.lang.th.text}</option>{/each}
		</select>
	</label>
	<label class="block">
		<span class="text-xs font-semibold uppercase tracking-wide" style="color: var(--muted)">{$t('record_language')}</span>
		<select class="card-flat tap w-full px-3 mt-1" bind:value={recLang}>
			<option value="my">{$t('burmese')}</option>
			<option value="mnw">{$t('mon')}</option>
			<option value="mnw-TH">{$t('thai_mon_wording')}</option>
		</select>
	</label>
</div>

{#if entry}
	<div class="card p-4 mb-3 flex flex-col gap-2">
		<div class="flex items-center justify-between">
			<span class="text-xs font-semibold uppercase tracking-wide" style="color: var(--muted)">{langLabel}</span>
			<StatusBadge status={entry.status} />
		</div>
		<p class="font-my text-2xl leading-relaxed" lang="mnw">{entry.display}</p>
		{#if entry.status === 'draft' || entry.status === 'machine'}
			<p class="text-xs" style="color: var(--warn)">{$t('record_unreviewed_note')}</p>
		{/if}
	</div>
{:else}
	<p class="card-flat p-4 mb-3" style="color: var(--warn)">{$t('record_no_text')} ({langLabel})</p>
{/if}

<label class="block mb-3">
	<span class="text-xs font-semibold uppercase tracking-wide" style="color: var(--muted)">{$t('your_name')}</span>
	<input class="card-flat tap w-full px-3 mt-1" bind:value={name} placeholder="Name, role, organization" />
</label>

<div class="flex gap-2">
	<button class="tap btn-brand px-5" onclick={start} disabled={!entry || status === 'recording'}>● {$t('start')}</button>
	<button class="tap btn-ghost px-5" onclick={stop} disabled={status !== 'recording'}>■ {$t('stop')}</button>
</div>
{#if status === 'error'}<p class="mt-3" style="color: var(--danger)">{$t('mic_refused')}</p>{/if}
{#if url}
	<div class="card p-4 mt-4 flex flex-col gap-2">
		<audio controls src={url}></audio>
		<a class="tap btn-brand px-5 inline-flex items-center justify-center" href={url} download="{phraseId}.{fileSuffix}.webm">⬇︎ {$t('save_clip')}</a>
		<p class="text-xs" style="color: var(--muted)">{$t('record_send_note')}</p>
	</div>
{/if}
