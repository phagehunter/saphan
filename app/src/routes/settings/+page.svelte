<script lang="ts">
	import { settings } from '$lib/settings';
	import { t } from '$lib/i18n';
	import { browser } from '$app/environment';
	let theme = $state(browser ? (document.documentElement.dataset.theme ?? 'auto') : 'auto');
	function setTheme(v: string) {
		theme = v;
		if (!browser) return;
		if (v === 'auto') delete document.documentElement.dataset.theme;
		else document.documentElement.dataset.theme = v;
	}
	let hotlineValid = $derived($settings.hotline === '' || /^[0-9+\-\s]{3,20}$/.test($settings.hotline));
</script>

<h1 class="text-2xl font-bold mb-4">⚙︎ {$t('settings')}</h1>

<div class="flex flex-col gap-4">
	<label class="card p-4 flex flex-col gap-1">
		<span class="font-semibold">{$t('ui_language')}</span>
		<select class="card tap px-3" bind:value={$settings.uiLang}>
			<option value="th">ไทย</option>
			<option value="en">English</option>
			<option value="my">မြန်မာ (unreviewed strings)</option>
		</select>
	</label>

	<label class="card p-4 flex flex-col gap-1">
		<span class="font-semibold">{$t('patient_language')}</span>
		<select class="card tap px-3" bind:value={$settings.patientLang}>
			<option value="my">{$t('burmese')}</option>
			<option value="mnw">{$t('mon')}</option>
		</select>
	</label>

	<label class="card p-4 flex items-center gap-3">
		<input type="checkbox" bind:checked={$settings.showEnglish} />
		<span class="font-semibold">{$t('show_english')}</span>
	</label>

	<label class="card p-4 flex items-center gap-3">
		<input type="checkbox" bind:checked={$settings.largeText} />
		<span class="font-semibold">Larger text</span>
	</label>

	<label class="card p-4 flex flex-col gap-1">
		<span class="font-semibold">{$t('interpreter_line')}</span>
		<input class="card tap px-3" type="tel" bind:value={$settings.hotline} placeholder="e.g. 034 xxx xxx" aria-invalid={!hotlineValid} />
		{#if !hotlineValid}<span class="text-sm" style="color: var(--danger)">Digits, spaces, + and - only.</span>{/if}
		<span class="text-xs" style="color: var(--muted)">Shown in the warning bar on every screen. Set it to your clinic's migrant health worker or interpreter number.</span>
	</label>

	<div class="card p-4 flex flex-col gap-1">
		<span class="font-semibold">Theme</span>
		<div class="flex gap-2">
			{#each ['auto', 'light', 'dark'] as v}
				<button class="card tap px-4" aria-pressed={theme === v} style={theme === v ? 'outline: 2px solid var(--brand)' : ''} onclick={() => setTheme(v)}>{v}</button>
			{/each}
		</div>
	</div>
</div>
