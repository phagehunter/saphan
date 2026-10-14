import { derived } from 'svelte/store';
import { settings } from './settings';
import type { Lang } from './types';

// Interface strings only (no clinical content). Thai and English are complete.
// Burmese strings here were written by the scaffold author and are UNREVIEWED;
// anything missing falls back to English. Mon falls back to Burmese, then English.
const strings: Record<string, Partial<Record<Lang, string>>> = {
	app_name: { th: 'สะพาน', en: 'Saphan', my: 'တံတား' },
	tagline: { th: 'ประโยคสุขภาพ ไทย · พม่า · มอญ', en: 'Health phrases Thai · Burmese · Mon', my: 'ကျန်းမာရေးစကားစု ထိုင်း · မြန်မာ · မွန်' },
	search: { th: 'ค้นหาประโยค…', en: 'Search phrases…', my: 'စကားစုရှာရန်…' },
	domains: { th: 'หมวด', en: 'Topics', my: 'အကြောင်းအရာ' },
	recent: { th: 'ใช้ล่าสุด', en: 'Recent', my: 'မကြာသေးမီက' },
	favorites: { th: 'รายการโปรด', en: 'Favorites', my: 'အကြိုက်ဆုံး' },
	patient_language: { th: 'ภาษาของผู้ป่วย', en: 'Patient language', my: 'လူနာဘာသာစကား' },
	ui_language: { th: 'ภาษาของหน้าจอ', en: 'Screen language', my: 'မျက်နှာပြင်ဘာသာစကား' },
	burmese: { th: 'พม่า', en: 'Burmese', my: 'မြန်မာ' },
	mon: { th: 'มอญ', en: 'Mon', my: 'မွန်' },
	thai: { th: 'ไทย', en: 'Thai', my: 'ထိုင်း' },
	english: { th: 'อังกฤษ', en: 'English', my: 'အင်္ဂလိပ်' },
	play: { th: 'เล่นเสียง', en: 'Play audio', my: 'အသံဖွင့်ရန်' },
	no_audio: { th: 'ยังไม่มีเสียงบันทึก', en: 'No recording yet', my: 'အသံသွင်းချက်မရှိသေးပါ' },
	synthetic_voice: { th: 'เสียงคอมพิวเตอร์', en: 'Computer voice', my: 'ကွန်ပျူတာအသံ' },
	human_voice: { th: 'เสียงคนจริง', en: 'Human recording', my: 'လူအသံ' },
	thai_machine_warning: { th: 'ข้อความไทยนี้แปลด้วยเครื่องและยังไม่มีผู้ตรวจ อ่านอย่างระมัดระวังก่อนใช้', en: 'This Thai text is machine output and has not been reviewed. Read it critically before using it.', my: 'ဤထိုင်းစာသားသည် စက်ဘာသာပြန်ဖြစ်ပြီး မစစ်ဆေးရသေးပါ။' },
	locked_unreviewed: { th: 'ยังไม่ผ่านการตรวจ จึงไม่แสดงให้ผู้ป่วย', en: 'Not yet reviewed, so not shown to the patient', my: 'မစစ်ဆေးရသေးသဖြင့် လူနာကိုမပြပါ' },
	locked_clinical: { th: 'ประโยคความเสี่ยงสูง ต้องให้บุคลากรแพทย์ตรวจก่อน', en: 'High-risk phrase: needs a clinician to verify first', my: 'အန္တရာယ်မြင့်စကားစု၊ ဆရာဝန်စစ်ဆေးရန်လိုသည်' },
	no_translation: { th: 'ยังไม่มีคำแปล', en: 'No translation yet', my: 'ဘာသာပြန်မရှိသေးပါ' },
	help_translate: { th: 'ช่วยแปลประโยคนี้', en: 'Help translate this phrase', my: 'ဤစကားစုကို ဘာသာပြန်ကူညီပါ' },
	show_to_patient: { th: 'แสดงให้ผู้ป่วย', en: 'Show to patient', my: 'လူနာကိုပြရန်' },
	back: { th: 'กลับ', en: 'Back', my: 'နောက်သို့' },
	patient_may_answer: { th: 'ผู้ป่วยตอบได้โดยแตะ', en: 'The patient can answer by tapping', my: 'လူနာက နှိပ်၍ဖြေနိုင်သည်' },
	listen_hint: { th: 'พูดหรือพิมพ์เป็นภาษาไทย แล้วเลือกประโยคที่ผ่านการตรวจแล้ว เสียงที่จับได้จะไม่ถูกแสดงให้ผู้ป่วย', en: 'Speak or type in Thai, then pick a verified phrase. Recognized speech is never shown to the patient.', my: 'ထိုင်းလိုပြော သို့မဟုတ် ရိုက်ပြီး စစ်ဆေးပြီးစကားစုကိုရွေးပါ။' },
	speak: { th: 'พูด', en: 'Speak', my: 'ပြောရန်' },
	stop: { th: 'หยุด', en: 'Stop', my: 'ရပ်ရန်' },
	listening: { th: 'กำลังฟัง… พูดได้เลย', en: 'Listening… speak now', my: 'နားထောင်နေသည်… ပြောပါ' },
	tap_to_speak: { th: 'แตะแล้วพูด', en: 'Tap, then speak', my: 'နှိပ်ပြီးပြောပါ' },
	no_engine: { th: 'โทรศัพท์นี้ไม่มีระบบจดจำเสียง พิมพ์แทนได้', en: 'No speech recognition on this phone. Type instead.', my: 'ဤဖုန်းတွင် အသံမှတ်မိစနစ်မရှိပါ။ ရိုက်ပါ။' },
	online_audio: { th: 'ออนไลน์: เสียงถูกส่งไปประมวลผลภายนอก', en: 'online: audio is sent to the phone maker’s service', my: 'အွန်လိုင်း' },
	or_type: { th: 'หรือพิมพ์', en: 'Or type', my: 'သို့မဟုတ် ရိုက်ပါ' },
	matching_phrases: { th: 'ประโยคที่ใกล้เคียง', en: 'Matching phrases', my: 'ကိုက်ညီသောစကားစုများ' },
	engines_and_device: { th: 'ระบบจดจำเสียงและอุปกรณ์', en: 'Speech engines and this device', my: 'အသံစနစ်နှင့်စက်' },
	lexicon: { th: 'พจนานุกรมมอญ', en: 'Mon lexicon', my: 'မွန်အဘိဓာန်' },
	lexicon_hint: { th: 'สำหรับผู้แปลและผู้ตรวจ ค้นคำศัพท์มอญ อังกฤษ พม่า ไทย ไม่ใช้กับผู้ป่วยโดยตรง', en: 'For translators and reviewers. Look up Mon, English, Burmese, and Thai terms. Not for use with patients directly.', my: 'ဘာသာပြန်သူများအတွက်။ မွန်၊ အင်္ဂလိပ်၊ မြန်မာ၊ ထိုင်း ဝေါဟာရရှာရန်။' },
	thai_mon_wording: { th: 'สำนวนมอญฝั่งไทย', en: 'Thai-side Mon wording', my: 'ထိုင်းဘက်မွန်အသုံး' },
	show_thai: { th: 'แสดงภาษาไทย', en: 'Show Thai', my: 'ထိုင်းပြရန်' },
	english_machine_warning: { th: 'ข้อความอังกฤษนี้เป็นการถอดความด้วยเครื่องจากคู่มือต้นฉบับ', en: 'This English text is a software paraphrase of the source handbook, not a reviewed sentence.', my: 'ဤအင်္ဂလိပ်စာသားသည် ဆော့ဖ်ဝဲဖြင့်ပြန်ရေးထားခြင်းဖြစ်သည်။' },
	show_english: { th: 'แสดงภาษาอังกฤษ', en: 'Show English', my: 'အင်္ဂလိပ်ပြရန်' },
	risk_high: { th: 'ความเสี่ยงสูง', en: 'High risk', my: 'အန္တရာယ်မြင့်' },
	risk_medium: { th: 'ความเสี่ยงปานกลาง', en: 'Medium risk', my: 'အန္တရာယ်အလယ်အလတ်' },
	risk_low: { th: 'ความเสี่ยงต่ำ', en: 'Low risk', my: 'အန္တရာယ်နည်း' },
	disclaimer: { th: 'แอปนี้ไม่ใช่ล่าม ใช้เฉพาะประโยคที่ผ่านการตรวจแล้ว หากต้องขอความยินยอมหรือสั่งยา ให้ติดต่อล่าม', en: 'This app is not an interpreter. Use verified phrases only. For consent or medication dosing, call an interpreter.', my: 'ဤအက်ပ်သည် စကားပြန်မဟုတ်ပါ။ စစ်ဆေးပြီးစကားစုများသာသုံးပါ။' },
	interpreter_line: { th: 'สายด่วนล่าม', en: 'Interpreter hotline', my: 'စကားပြန်ဖုန်းလိုင်း' },
	offline: { th: 'ออฟไลน์: ใช้งานได้ตามปกติ', en: 'Offline: everything still works', my: 'အော့ဖ်လိုင်း' },
	listen: { th: 'ฟัง', en: 'Listen', my: 'နားထောင်ရန်' },
	translate: { th: 'แปลข้อความ', en: 'Translate', my: 'ဘာသာပြန်' },
	settings: { th: 'ตั้งค่า', en: 'Settings', my: 'ဆက်တင်' },
	about: { th: 'เกี่ยวกับ', en: 'About', my: 'အကြောင်း' },
	record: { th: 'บันทึกเสียง', en: 'Record', my: 'အသံသွင်းရန်' },
	home: { th: 'หน้าแรก', en: 'Home', my: 'ပင်မ' },
	phrases: { th: 'ประโยค', en: 'phrases', my: 'စကားစု' },
	no_results: { th: 'ไม่พบประโยค', en: 'No phrases found', my: 'စကားစုမတွေ့ပါ' },
	source: { th: 'ที่มา', en: 'Source', my: 'ရင်းမြစ်' },
	reviewed_by: { th: 'ตรวจโดย', en: 'Reviewed by', my: 'စစ်ဆေးသူ' },
	notes_for_reviewers: { th: 'หมายเหตุสำหรับผู้ตรวจ', en: 'Notes for reviewers', my: 'စစ်ဆေးသူများအတွက်မှတ်ချက်' }
};

export function translate(key: string, lang: Lang): string {
	const s = strings[key];
	if (!s) return key;
	return s[lang] ?? (lang === 'mnw' ? s.my : undefined) ?? s.en ?? key;
}

export const t = derived(settings, ($s) => (key: string) => translate(key, $s.uiLang));
