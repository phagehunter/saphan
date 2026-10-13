<script lang="ts">
	import { t } from '$lib/i18n';
	import { settings } from '$lib/settings';
</script>

<aside class="px-4 py-2 text-xs leading-snug" style="background: var(--warn-bg); color: var(--warn)">
	<div class="max-w-2xl mx-auto flex items-start gap-2">
		<span aria-hidden="true">⚠︎</span>
		<span>{$t('disclaimer')}
			{#if $settings.hotline}<a href="tel:{$settings.hotline}" class="font-bold underline ml-1">{$t('interpreter_line')}: {$settings.hotline}</a>{/if}
		</span>
	</div>
</aside>
