<script lang="ts">
	import type { Status } from '$lib/types';
	import { t } from '$lib/i18n';
	import { statusLabel } from '$lib/content';
	import { settings } from '$lib/settings';
	let { status, reviewedBy, compact = false }: { status: Status; reviewedBy?: string; compact?: boolean } = $props();
	const icon: Record<Status, string> = { clinical: '✔︎✔︎', human: '✔︎', machine: '⚠︎', draft: '…' };
	let label = $derived(statusLabel[status][$settings.uiLang] ?? status);
</script>

<span class="badge badge-{status}" title={reviewedBy ? `${$t('reviewed_by')}: ${reviewedBy}` : label} aria-label={label}>
	<span aria-hidden="true">{icon[status]}</span>
	{#if !compact}{label}{/if}
</span>
