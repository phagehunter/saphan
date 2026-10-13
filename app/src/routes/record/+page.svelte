<script lang="ts">
	import { bundle } from '$lib/content';
	import { settings } from '$lib/settings';
	import { t } from '$lib/i18n';
	// Partner recording page. Records one phrase in the chosen patient language and offers
	// the clip as a download. The maintainer then adds it under app/static/audio/<lang>/ and
	// sets audio.<lang> in the phrase record with kind "human" and recorded_by.
	let phraseId = $state(bundle.phrases[0]?.id ?? '');
	let recorder: MediaRecorder | null = null;
	let chunks: Blob[] = [];
	let status = $state<'idle' | 'recording' | 'done' | 'error'>('idle');
	let url = $state<string | null>(null);
	let name = $state('');
	let phrase = $derived(bundle.phrases.find((p) => p.id === phraseId));
	let text = $derived(phrase?.lang[$settings.patientLang].text ?? null);

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
<p class="text-sm mb-4" style="color: var(--muted)">For translators and partners. Record the phrase as a native speaker would say it to a patient. The clip stays on this phone until you send it to the maintainer.</p>

<label class="block mb-3">
	<span class="text-sm">Phrase</span>
	<select class="card tap w-full px-3 mt-1" bind:value={phraseId}>
		{#each bundle.phrases as p (p.id)}<option value={p.id}>{p.id} · {p.lang.th.text}</option>{/each}
	</select>
</label>

{#if text}
	<p class="card p-4 font-my text-2xl mb-3" lang={$settings.patientLang}>{phrase?.lang[$settings.patientLang].display}</p>
{:else}
	<p class="card p-4 mb-3" style="color: var(--warn)">No {$settings.patientLang === 'my' ? 'Burmese' : 'Mon'} text for this phrase yet. Add the translation first (see docs/contributing-a-phrase.md), then record.</p>
{/if}

<label class="block mb-3">
	<span class="text-sm">Your name (goes into recorded_by)</span>
	<input class="card tap w-full px-3 mt-1" bind:value={name} placeholder="Name, role, organization" />
</label>

<div class="flex gap-2">
	<button class="tap btn-brand px-5 font-semibold" onclick={start} disabled={!text || status === 'recording'}>● Start</button>
	<button class="tap card px-5 font-semibold" onclick={stop} disabled={status !== 'recording'}>■ Stop</button>
</div>
{#if status === 'error'}<p class="mt-3" style="color: var(--danger)">Microphone permission was refused or the browser cannot record.</p>{/if}
{#if url}
	<div class="card p-4 mt-4 flex flex-col gap-2">
		<audio controls src={url}></audio>
		<a class="tap btn-brand px-5 font-semibold inline-flex items-center" href={url} download="{phraseId}.{$settings.patientLang}.webm">⬇︎ Save clip</a>
		<p class="text-xs" style="color: var(--muted)">Send the file plus your name to the maintainer, or attach it to a pull request. It will be converted to Opus and listed as a human recording.</p>
	</div>
{/if}
