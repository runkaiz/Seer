/**
 * API client for the seer-api backend
 * Author: Runkai Zhang
 */

import type {
  AnimeHistoryItem,
  RecommendResponse,
  RecommendationMode,
  SearchResponse,
} from "./types";

import { env } from "$env/dynamic/public";

const API_BASE_URL = env.PUBLIC_API_URL || "http://localhost:8000/api";

export class APIError extends Error {
  constructor(
    message: string,
    public status?: number,
    public detail?: string,
  ) {
    super(message);
    this.name = "APIError";
  }
}

export interface RateLimitInfo {
  limit: number;
  remaining: number;
  reset: number;
}

export type ApiStatus = {
  status: "unknown" | "ok" | "error";
  updatedAt: number;
};

// Store for rate limit info
let currentRateLimitInfo: RateLimitInfo | null = null;
let currentApiStatus: ApiStatus = { status: "unknown", updatedAt: 0 };

export function getRateLimitInfo(): RateLimitInfo | null {
  return currentRateLimitInfo;
}

export function getApiStatus(): ApiStatus {
  return currentApiStatus;
}

function setApiStatus(status: ApiStatus["status"]) {
  currentApiStatus = { status, updatedAt: Date.now() };
}

function parseRateLimitHeaders(headers: Headers): RateLimitInfo | null {
  const limit = headers.get("X-RateLimit-Limit");
  const remaining = headers.get("X-RateLimit-Remaining");
  const reset = headers.get("X-RateLimit-Reset");

  if (limit && remaining && reset) {
    return {
      limit: parseInt(limit, 10),
      remaining: parseInt(remaining, 10),
      reset: parseInt(reset, 10),
    };
  }
  return null;
}

/**
 * Search for anime by title
 */
export async function searchAnime(
  query: string,
  limit: number = 5,
): Promise<SearchResponse> {
  try {
    const params = new URLSearchParams({
      query,
      limit: limit.toString(),
    });

    const response = await fetch(`${API_BASE_URL}/search?${params}`);

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      setApiStatus("error");
      throw new APIError(
        "Failed to search anime",
        response.status,
        error.detail || response.statusText,
      );
    }

    setApiStatus("ok");

    return response.json();
  } catch (err) {
    setApiStatus("error");
    throw err;
  }
}

/**
 * Get a recommendation based on anime history
 */
export async function getRecommendation(
  animeHistory: AnimeHistoryItem[],
  mode: RecommendationMode,
  excludeIds: number[] = [],
): Promise<RecommendResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/recommend`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        anime_history: animeHistory,
        mode,
        exclude_ids: excludeIds,
      }),
    });

    // Parse and store rate limit info
    const rateLimitInfo = parseRateLimitHeaders(response.headers);
    if (rateLimitInfo) {
      currentRateLimitInfo = rateLimitInfo;
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      setApiStatus("error");
      throw new APIError(
        "Failed to get recommendation",
        response.status,
        error.detail || response.statusText,
      );
    }

    setApiStatus("ok");

    return response.json();
  } catch (err) {
    setApiStatus("error");
    throw err;
  }
}

/**
 * Check API health
 */
export async function healthCheck(): Promise<{
  status: string;
  service: string;
  version: string;
}> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new APIError("API health check failed", response.status);
  }

  return response.json();
}
