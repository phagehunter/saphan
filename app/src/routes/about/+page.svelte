<script lang="ts">
	import { base } from '$app/paths';
	import { bundle } from '$lib/content';
	import { t } from '$lib/i18n';
	const locked = bundle.phrases.flatMap((p) => (['my', 'mnw'] as const).filter((l) => p.lang[l].locked)).length;
	const mon = bundle.phrases.filter((p) => p.lang.mnw.text).length;
</script>

<h1 class="text-2xl font-bold mb-3">ℹ️ {$t('about')}</h1>
<section class="card p-4 mb-4">
	<p>Saphan (สะพาน, "bridge") is a free, offline phrasebook for health volunteers who serve Burmese- and Mon-speaking patients in Kanchanaburi, Thailand. It is open source and non-commercial.</p>
	<ul class="mt-3 text-sm grid grid-cols-2 gap-1">
		<li>Content version: {bundle.version}</li>
		<li>Phrases: {bundle.phrases.length}</li>
		<li>Topics: {bundle.domains.length}</li>
		<li>Locked patient slots: {locked}</li>
		<li>Phrases with Mon text: {mon}</li>
		<li>Skipped at build: {bundle.skipped.length}</li>
	</ul>
</section>
<section class="card p-4 mb-4 text-sm">
	<h2 class="font-semibold mb-2">How to read the badges</h2>
	<ul class="space-y-1">
		<li><span class="badge badge-clinical">✔︎✔︎ clinical</span> checked by a clinician fluent in that language. Required before any high-risk phrase reaches a patient.</li>
		<li><span class="badge badge-human">✔︎ human</span> written or checked by a fluent speaker. Enough for low- and medium-risk phrases.</li>
		<li><span class="badge badge-machine">⚠︎ machine</span> produced by software and not yet reviewed. Shown to volunteers with a warning, never to patients.</li>
		<li><span class="badge badge-draft">… draft</span> placeholder. Nothing to show.</li>
	</ul>
</section>
<section class="card p-4 text-sm">
	<h2 class="font-semibold mb-2">Sources and licenses</h2>
	{#each Object.values(bundle.sources) as s}
		<p class="mb-2"><strong>{s.title}</strong> — {s.license}{#if s.url} · <a class="underline" href={s.url} rel="noopener">{s.url}</a>{/if}<br /><span style="color: var(--muted)">{s.attribution}</span></p>
	{/each}
	<p class="mb-2"><strong>Mon lexicon</strong> (reviewer tool): Nenemin95 Mon-Eng-Mya-Pali lexicon, CC BY 4.0, <a class="underline" href="https://huggingface.co/datasets/Nenemin95/mon-eng-mya-pali-lexicon" rel="noopener">huggingface.co</a>; MonDictDB Mon-Thai dictionary, MIT, <a class="underline" href="https://github.com/Barnista/MonDictDB" rel="noopener">github.com/Barnista/MonDictDB</a>.</p>
	<p>App code: MIT. Content: CC BY-NC-SA 4.0. Synthetic voices, when present: Meta MMS-TTS, CC BY-NC 4.0.</p>
	<p class="mt-3"><a class="underline" href="{base}/translate/">Free-text translation mock-up (Mode C, disabled)</a></p>
</section>
