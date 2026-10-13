<script lang="ts">
	import { onMount } from 'svelte';
	import { probe, canRunLocalASR, type Capabilities } from '$lib/capabilities';
	import { t } from '$lib/i18n';
	let caps = $state<Capabilities | null>(null);
	onMount(() => (caps = probe()));
</script>

<h1 class="text-2xl font-bold mb-2">🎤 {$t('listen')} <span class="badge badge-draft">Mode B · not built yet</span></h1>
<p class="mb-4">Speak in Thai to find a phrase. Recognized speech is matched against the verified phrasebook; it is never shown to a patient as a translation.</p>

<section class="card p-4 mb-4">
	<h2 class="font-semibold mb-2">What this phone can do</h2>
	{#if caps}
		<ul class="text-sm grid grid-cols-2 gap-1">
			<li>Memory: {caps.deviceMemoryGB ?? '?'} GB</li>
			<li>CPU cores: {caps.cores ?? '?'}</li>
			<li>Online: {caps.online ? 'yes' : 'no'}</li>
			<li>Data saver: {caps.saveData ? 'on' : 'off'}</li>
			<li>WebGPU: {caps.webgpu ? 'yes' : 'no'}</li>
			<li>Microphone API: {caps.mediaRecorder ? 'yes' : 'no'}</li>
		</ul>
		<p class="mt-3 font-semibold" style="color: var({canRunLocalASR(caps) ? '--ok' : '--warn'})">
			{canRunLocalASR(caps) ? 'On-device Thai recognition would be offered on this phone (model download ~60-190 MB).' : 'This phone would get the lighter path only (typed search). On-device recognition needs about 3 GB of memory.'}
		</p>
	{/if}
</section>

<section class="card p-4 text-sm" style="color: var(--muted)">
	<h2 class="font-semibold mb-1" style="color: var(--text)">Planned pieces (see docs/2026-10-13-architecture-proposal.md)</h2>
	<ul class="list-disc pl-5 space-y-1">
		<li>Thai: Thonburian Whisper small (Apache-2.0) in WebAssembly, or a tiny Thai fine-tune once trained.</li>
		<li>Burmese: cloud only (Google or Azure) or a server running the myMediWhisper-style model; labeled "online".</li>
		<li>Mon: Meta MMS on a server, experimental; no on-device path exists.</li>
		<li>Output is always a list of matching verified phrases, never free text.</li>
	</ul>
</section>
