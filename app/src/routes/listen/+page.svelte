<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { base } from '$app/paths';
	import { bundle } from '$lib/content';
	import { t } from '$lib/i18n';
	import { settings } from '$lib/settings';
	import { probe, type Capabilities } from '$lib/capabilities';
	import { PhraseMatcher } from '$lib/speech/match';
	import { engines, ON_DEVICE, type SpeechEngine, type EngineStatus, type Lang } from '$lib/speech/engine';
	import PhraseRow from '$lib/components/PhraseRow.svelte';

	// Mode B: speak (or type) in the volunteer's language, get matching VERIFIED phrases.
	// Recognized text is never shown to a patient; only the matched phrase card is.
	let caps = $state<Capabilities | null>(null);
	let statuses = $state<Record<string, EngineStatus>>({});
	let engine = $state<SpeechEngine | null>(null);
	let listening = $state(false);
	let transcript = $state('');
	let error = $state('');
	let typed = $state('');

	let lang = $derived(($settings.uiLang === 'en' ? 'en' : 'th') as Lang);
	let matcher = $derived(new PhraseMatcher(bundle.phrases.map((p) => ({ id: p.id, text: p.lang[lang].text ?? '' }))));
	let query = $derived(transcript || typed);
	let matches = $derived(query.trim() ? matcher.match(query) : []);

	onMount(async () => {
		caps = probe();
		for (const e of engines) statuses[e.id] = await e.status();
		engine = engines.find((e) => statuses[e.id]?.available) ?? null;
	});
	onDestroy(() => engine?.stop());

	async function toggle() {
		if (!engine) return;
		if (listening) {
			engine.stop();
			listening = false;
			return;
		}
		error = '';
		transcript = '';
		typed = '';
		listening = true;
		await engine.start(
			lang,
			(partial) => (transcript = partial),
			(final) => {
				transcript = final;
				listening = false;
			},
			(msg) => {
				error = msg;
				listening = false;
			}
		);
	}
	function phraseOf(id: string) {
		return bundle.phrases.find((p) => p.id === id)!;
	}
</script>

<h1 class="text-2xl font-bold mb-1">🎤 {$t('listen')}</h1>
<p class="text-sm mb-4" style="color: var(--muted)">{$t('listen_hint')}</p>

<section class="card p-4 mb-4 flex flex-col items-center gap-3">
	<button
		class="tap pressable rounded-full flex items-center justify-center text-4xl"
		style="width: 96px; height: 96px; background: {listening ? 'var(--danger)' : 'var(--brand)'}; color: var(--brand-ink); box-shadow: var(--shadow)"
		onclick={toggle}
		disabled={!engine}
		aria-pressed={listening}
		aria-label={listening ? $t('stop') : $t('speak')}
	>
		{listening ? '■' : '🎤'}
	</button>
	<p class="text-sm font-semibold">{listening ? $t('listening') : engine ? $t('tap_to_speak') : $t('no_engine')}</p>
	{#if engine}
		<p class="text-xs" style="color: var(--muted)">
			{engine.label}
			{#if statuses[engine.id]?.online}<span class="badge badge-machine ml-1">{$t('online_audio')}</span>{:else}<span class="badge badge-human ml-1">offline</span>{/if}
		</p>
	{/if}
	{#if transcript}
		<p class="w-full text-center text-lg" style="color: var(--muted)" aria-live="polite">“{transcript}”</p>
	{/if}
	{#if error}<p class="text-sm" style="color: var(--danger)">{error}</p>{/if}
</section>

<label class="block mb-4">
	<span class="text-xs font-semibold uppercase tracking-wide" style="color: var(--muted)">{$t('or_type')}</span>
	<input class="card-flat tap w-full px-4 mt-1" bind:value={typed} oninput={() => (transcript = '')} placeholder={lang === 'th' ? 'เช่น หายใจลำบาก' : 'e.g. trouble breathing'} autocomplete="off" />
</label>

{#if query.trim()}
	<h2 class="text-xs font-semibold uppercase tracking-wide mb-2" style="color: var(--muted)">{$t('matching_phrases')} · {matches.length}</h2>
	<div class="flex flex-col gap-2 mb-6">
		{#each matches as m (m.id)}
			<div class="relative">
				<PhraseRow phrase={phraseOf(m.id)} />
				<span class="absolute -top-2 right-3 badge badge-draft" title="match score">{Math.round(m.score * 100)}%</span>
			</div>
		{:else}
			<p class="card-flat p-4 text-sm" style="color: var(--muted)">{$t('no_results')} <a class="underline" href="{base}/">{$t('home')}</a></p>
		{/each}
	</div>
{/if}

<details class="card-flat p-4 text-sm" style="color: var(--muted)">
	<summary class="font-semibold" style="color: var(--text)">{$t('engines_and_device')}</summary>
	<ul class="mt-2 space-y-2">
		{#each engines as e (e.id)}
			<li>
				<strong style="color: var(--text)">{e.label}</strong>:
				{#if statuses[e.id]?.available}available{:else}{statuses[e.id]?.reason ?? '…'}{/if}
				{#if statuses[e.id]?.downloadMB}· ~{statuses[e.id].downloadMB} MB download{/if}
			</li>
		{/each}
	</ul>
	{#if caps}
		<p class="mt-3">Memory {caps.deviceMemoryGB ?? '?'} GB · {caps.cores ?? '?'} cores · {caps.online ? 'online' : 'offline'} · data saver {caps.saveData ? 'on' : 'off'} · WebGPU {caps.webgpu ? 'yes' : 'no'}</p>
	{/if}
	<p class="mt-3">On-device model planned: <code>{ON_DEVICE.modelId}</code> (~{ON_DEVICE.approxMB} MB, needs ≥{ON_DEVICE.minDeviceMemoryGB} GB). Burmese and Mon speech input are not offered here: Burmese would need a server or a cloud service, and Mon has no on-device path yet.</p>
</details>
