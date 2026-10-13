<script lang="ts">
	import { base } from '$app/paths';
	import { t } from '$lib/i18n';
	import { settings } from '$lib/settings';
	import { browser } from '$app/environment';
	let online = $state(browser ? navigator.onLine : true);
	if (browser) {
		window.addEventListener('online', () => (online = true));
		window.addEventListener('offline', () => (online = false));
	}
</script>

<header class="topbar sticky top-0 z-10">
	<div class="max-w-2xl mx-auto px-4 h-14 flex items-center gap-3">
		<a href="{base}/" class="flex items-center gap-2 font-extrabold text-lg tracking-tight" style="color: var(--brand)">
			<span aria-hidden="true">🌉</span>{$t('app_name')}
		</a>
		{#if !online}<span class="badge badge-draft" title={$t('offline')}>📴 offline</span>{/if}
		<span class="flex-1"></span>
		<label class="flex items-center">
			<span class="sr-only">{$t('patient_language')}</span>
			<select class="card-flat tap px-3 text-sm font-semibold" style="min-height: 40px" bind:value={$settings.patientLang} aria-label={$t('patient_language')}>
				<option value="my">🗣 {$t('burmese')}</option>
				<option value="mnw">🗣 {$t('mon')}</option>
			</select>
		</label>
		<a href="{base}/settings/" class="tap pressable flex items-center justify-center w-10" style="min-height: 40px" aria-label={$t('settings')}>⚙︎</a>
	</div>
</header>
