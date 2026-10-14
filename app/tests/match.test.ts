// @ts-nocheck -- run by Node's test runner (`pnpm run test`); svelte-check lacks Node's type
// definitions and we keep @types/node out of the dependency list on purpose.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { PhraseMatcher, normalize } from '../src/lib/speech/match.ts';

const phrases = [
	{ id: 'triage-003', text: 'คุณมีอาการหายใจลำบากหรือไม่?' },
	{ id: 'triage-004', text: 'คุณมีอาการไอหรือไม่?' },
	{ id: 'triage-005', text: 'คุณมีอาการเจ็บหน้าอกหรือไม่?' },
	{ id: 'antenatal-001', text: 'ประจำเดือนครั้งสุดท้ายของคุณคือเมื่อไหร่?' },
	{ id: 'medication-001', text: 'คุณแพ้อะไรไหม?' },
	{ id: 'en-1', text: 'Are you having trouble breathing?' }
];

test('normalize strips spaces, punctuation, and polite particles', () => {
	assert.equal(normalize('คุณ ไอ ไหม ครับ?'), 'คุณไอไหม');
	assert.equal(normalize('Are you OK?'), 'areyouok');
});

test('exact Thai sentence matches itself first', () => {
	const m = new PhraseMatcher(phrases);
	const r = m.match('คุณมีอาการไอหรือไม่');
	assert.equal(r[0].id, 'triage-004');
	assert.ok(r[0].score > 0.9);
});

test('recognizer-style variant still finds the right phrase', () => {
	const m = new PhraseMatcher(phrases);
	// What a recognizer might return: no question mark, particle, slightly different wording.
	const r = m.match('มีอาการหายใจลำบากไหมคะ');
	assert.equal(r[0].id, 'triage-003');
});

test('short key word ranks the allergy question', () => {
	const m = new PhraseMatcher(phrases);
	const r = m.match('แพ้ยา');
	assert.ok(r.length > 0);
	assert.equal(r[0].id, 'medication-001');
});

test('english works too and unrelated text returns nothing', () => {
	const m = new PhraseMatcher(phrases);
	assert.equal(m.match('trouble breathing')[0].id, 'en-1');
	assert.equal(m.match('xyzzy').length, 0);
});
