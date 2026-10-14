<script lang="ts">
	import icons from '$lib/icons/health.json';
	// Renders a Health Icons pictogram ("hi:category/name", CC0) inline so it takes the current
	// color, or falls back to the emoji string the record carries.
	let { name, size = 32, class: cls = '' }: { name: string; size?: number; class?: string } = $props();
	const map = icons as Record<string, { viewBox: string; body: string }>;
	let icon = $derived(name.startsWith('hi:') ? map[name.slice(3)] : undefined);
</script>

{#if icon}
	<svg class="shrink-0 {cls}" width={size} height={size} viewBox={icon.viewBox} fill="none" aria-hidden="true" role="img">{@html icon.body}</svg>
{:else}
	<span class="shrink-0 leading-none {cls}" style="font-size: {size * 0.85}px" aria-hidden="true">{name}</span>
{/if}
