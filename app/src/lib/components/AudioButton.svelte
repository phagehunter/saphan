<script lang="ts">
	import type { AudioClip } from '$lib/types';
	import { play } from '$lib/audio';
	import { t } from '$lib/i18n';
	let { clip, big = false }: { clip: AudioClip | null | undefined; big?: boolean } = $props();
	let state = $state<'idle' | 'playing' | 'failed'>('idle');
	async function go() {
		if (!clip) return;
		state = 'playing';
		const ok = await play(clip);
		state = ok ? 'idle' : 'failed';
	}
</script>

{#if clip}
	<button class="tap btn-brand px-5 font-semibold flex items-center gap-2 {big ? 'text-2xl py-4 w-full justify-center' : ''}" onclick={go} aria-label={$t('play')}>
		<span aria-hidden="true">{state === 'playing' ? '🔊' : '▶︎'}</span>
		{$t('play')}
		<span class="text-xs opacity-80 font-normal">· {clip.kind === 'synthetic' ? $t('synthetic_voice') : $t('human_voice')}</span>
	</button>
	{#if state === 'failed'}
		<p class="text-sm" style="color: var(--danger)">{$t('no_audio')}</p>
	{/if}
{:else}
	<span class="badge badge-draft">🔇 {$t('no_audio')}</span>
{/if}
