/**
 * Shared utility functions for the Seer application.
 * Author: Runkai Zhang
 */

import type { UserRating } from "./types";

export interface RatingOption {
  value: UserRating;
  emoji: string;
  label: string;
}

export const ratingOptions: RatingOption[] = [
  { value: "positive", emoji: "🙂", label: "Loved it" },
  { value: "neutral", emoji: "😐", label: "It was ok" },
  { value: "negative", emoji: "🤮", label: "Not for me" },
];

export function getRatingEmoji(rating: UserRating | string | null): string {
  const option = ratingOptions.find((opt) => opt.value === rating);
  return option?.emoji ?? "—";
}

export function getRatingColor(rating: UserRating | string | null): string {
  switch (rating) {
    case "positive":
      return "text-green-600 dark:text-green-400";
    case "neutral":
      return "text-slate-600 dark:text-slate-400";
    case "negative":
      return "text-red-600 dark:text-red-400";
    default:
      return "text-slate-400";
  }
}
