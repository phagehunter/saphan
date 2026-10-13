import Dexie, { type EntityTable } from 'dexie';
import { browser } from '$app/environment';

// Local-only storage: favorites and recently used phrases. Nothing leaves the phone
// (open question 13: no usage logging).
interface Recent { id: string; at: number }
interface Favorite { id: string; at: number }

class SaphanDB extends Dexie {
	recents!: EntityTable<Recent, 'id'>;
	favorites!: EntityTable<Favorite, 'id'>;
	constructor() {
		super('saphan');
		this.version(1).stores({ recents: 'id, at', favorites: 'id, at' });
	}
}

export const db = browser ? new SaphanDB() : (null as unknown as SaphanDB);

export async function touchRecent(id: string) {
	if (!db) return;
	await db.recents.put({ id, at: Date.now() });
	const all = await db.recents.orderBy('at').reverse().toArray();
	if (all.length > 20) await db.recents.bulkDelete(all.slice(20).map((r) => r.id));
}

export async function listRecent(): Promise<string[]> {
	if (!db) return [];
	return (await db.recents.orderBy('at').reverse().limit(8).toArray()).map((r) => r.id);
}

export async function toggleFavorite(id: string): Promise<boolean> {
	if (!db) return false;
	const existing = await db.favorites.get(id);
	if (existing) {
		await db.favorites.delete(id);
		return false;
	}
	await db.favorites.put({ id, at: Date.now() });
	return true;
}

export async function listFavorites(): Promise<string[]> {
	if (!db) return [];
	return (await db.favorites.orderBy('at').reverse().toArray()).map((f) => f.id);
}

export async function isFavorite(id: string): Promise<boolean> {
	if (!db) return false;
	return !!(await db.favorites.get(id));
}
