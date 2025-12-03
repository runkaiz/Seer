/**
 * Storage service for managing anime history
 * Author: Runkai Zhang
 */

import type { AnimeHistoryItem, AnimeHistory, WatchStatus } from './types';

const STORAGE_KEY = 'seer_anime_history';
const DEFAULT_WATCH_STATUS: WatchStatus = 'completed';
const WATCHING_STATUS: WatchStatus = 'watching';
const ALLOWED_WATCH_STATUSES: WatchStatus[] = ['watching', 'completed', 'backlog', 'ignored'];
const LEGACY_STATUS_MAP: Record<string, WatchStatus> = {
	watched: 'completed',
	watching: 'watching'
};

function normalizeHistoryItems(history: AnimeHistoryItem[]): AnimeHistoryItem[] {
	return history.map((item) => {
		const rawStatus = item.watch_status ?? (item.has_seen ? 'watched' : WATCHING_STATUS);
		const mappedStatus = LEGACY_STATUS_MAP[rawStatus as keyof typeof LEGACY_STATUS_MAP] ?? rawStatus;
		const watch_status: WatchStatus = (ALLOWED_WATCH_STATUSES.includes(mappedStatus as WatchStatus)
			? mappedStatus
			: WATCHING_STATUS) as WatchStatus;
		return {
			...item,
			watch_status,
			has_seen: watch_status === 'completed'
		};
	});
}

/**
 * Load anime history from localStorage
 */
export function loadHistory(): AnimeHistoryItem[] {
	if (typeof window === 'undefined') return [];

	try {
		const stored = localStorage.getItem(STORAGE_KEY);
		if (!stored) return [];

		const parsed = JSON.parse(stored) as AnimeHistory;
		return normalizeHistoryItems(parsed.anime_history || []);
	} catch (error) {
		console.error('Failed to load history from localStorage:', error);
		return [];
	}
}

/**
 * Save anime history to localStorage
 */
export function saveHistory(history: AnimeHistoryItem[]): void {
	if (typeof window === 'undefined') return;

	try {
		const data: AnimeHistory = { anime_history: normalizeHistoryItems(history) };
		localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
	} catch (error) {
		console.error('Failed to save history to localStorage:', error);
		throw error;
	}
}

/**
 * Export history as JSON file
 */
export function exportHistory(history: AnimeHistoryItem[]): void {
	const data: AnimeHistory = { anime_history: history };
	const json = JSON.stringify(data, null, 2);
	const blob = new Blob([json], { type: 'application/json' });
	const url = URL.createObjectURL(blob);

	const link = document.createElement('a');
	link.href = url;
	link.download = `seer_history_${new Date().toISOString().split('T')[0]}.json`;
	document.body.appendChild(link);
	link.click();
	document.body.removeChild(link);

	URL.revokeObjectURL(url);
}

/**
 * Import history from JSON file
 */
export function importHistory(file: File): Promise<AnimeHistoryItem[]> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();

		reader.onload = (e) => {
			try {
				const text = e.target?.result as string;
				const parsed = JSON.parse(text) as AnimeHistory;

				if (!parsed.anime_history || !Array.isArray(parsed.anime_history)) {
					throw new Error('Invalid history file format');
				}

				resolve(normalizeHistoryItems(parsed.anime_history));
			} catch (error) {
				reject(error);
			}
		};

		reader.onerror = () => reject(new Error('Failed to read file'));
		reader.readAsText(file);
	});
}

/**
 * Clear all history
 */
export function clearHistory(): void {
	if (typeof window === 'undefined') return;
	localStorage.removeItem(STORAGE_KEY);
}
