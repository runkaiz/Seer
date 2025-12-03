/**
 * Type definitions for the anime recommendation API
 * Author: Runkai Zhang
 */

export type UserRating = "positive" | "neutral" | "negative";
export type WatchStatus = "watching" | "completed" | "backlog" | "ignored";
export type RecommendationMode = "similar" | "explore";

export interface AnimeBase {
  mal_id: number;
  title: string;
  genres: string[];
  themes: string[];
  demographics: string[];
  studios: string[];
  episodes: number | null;
  score: string | null;
  synopsis: string | null;
  media_type?: string;
  rating?: string | null;
  source?: string;
  image_url?: string | null;
  rank?: number | null;
  popularity?: number | null;
}

export interface AnimeHistoryItem extends AnimeBase {
  has_seen: boolean;
  rating: UserRating | null;
  watch_status: WatchStatus;
}

export interface PreferenceProfile {
  preferred_genres: string[];
  preferred_themes: string[];
  avoided_genres: string[];
  avoided_themes: string[];
  preferred_episode_range: string | null;
  preferred_demographics: string[];
  content_notes: string;
}

export interface AnimeRecommendation extends AnimeBase {
  recommendation_reason: string;
}

export interface RecommendResponse {
  recommendation: AnimeRecommendation;
  preference_profile?: PreferenceProfile;
}

export interface SearchResponse {
  results: AnimeBase[];
}

export interface AnimeHistory {
  anime_history: AnimeHistoryItem[];
}
