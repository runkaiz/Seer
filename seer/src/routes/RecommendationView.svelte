<script lang="ts">
    import { onDestroy } from "svelte";
    import type {
        AnimeRecommendation,
        RecommendationMode,
        UserRating,
    } from "$lib/types";
    import { ratingOptions } from "$lib/utils";

    type DetailItem = { label: string; value: string };

    interface Props {
        recommendation: AnimeRecommendation | null;
        onRegenerate: () => void;
        onAddToWatchlist: () => void;
        onAlreadyWatched: (rating: UserRating) => void;
        onNotInterested: () => void | Promise<void>;
        mode: RecommendationMode;
    }

    let {
        recommendation,
        onRegenerate,
        onAddToWatchlist,
        onAlreadyWatched,
        onNotInterested,
        mode,
    }: Props = $props();

    let showDetails = $state(false);
    let showWatchedRating = $state(false);
    let isDismissing = $state(false);
    let dismissTimeout: ReturnType<typeof setTimeout> | null = null;

    const modeCopy: Record<
        RecommendationMode,
        { label: string; description: string; accent: string }
    > = {
        explore: {
            label: "Explore mode",
            description: "Casting a wide net to surprise you",
            accent: "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-200",
        },
        similar: {
            label: "Similar mode",
            description: "Staying close to your comfort picks",
            accent: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-200",
        },
    };

    let detailItems = $derived(
        (recommendation
            ? buildDetailItems(recommendation)
            : []) as DetailItem[],
    );

    function toggleWatchedRating() {
        showWatchedRating = !showWatchedRating;
    }

    function handleWatchedRatingSelect(value: UserRating) {
        onAlreadyWatched(value);
        showWatchedRating = false;
    }

    function handleNotInterestedClick() {
        if (isDismissing) return;
        isDismissing = true;
        if (dismissTimeout) {
            clearTimeout(dismissTimeout);
        }
        dismissTimeout = setTimeout(() => {
            const result = onNotInterested();
            if (result instanceof Promise) {
                result.finally(() => {
                    isDismissing = false;
                    dismissTimeout = null;
                });
            } else {
                isDismissing = false;
                dismissTimeout = null;
            }
        }, 200);
    }

    function toggleDetails() {
        showDetails = !showDetails;
    }

    const MAX_PREMISE_LENGTH = 180;

    function getPremise(text: string | null): string | null {
        if (!text) return null;
        const trimmed = text.trim();
        if (trimmed.length <= MAX_PREMISE_LENGTH) return trimmed;
        return `${trimmed.slice(0, MAX_PREMISE_LENGTH).trimEnd()}…`;
    }

    function buildDetailItems(rec: AnimeRecommendation): DetailItem[] {
        const items: DetailItem[] = [];
        const premise = getPremise(rec.synopsis);
        if (premise) {
            items.push({ label: "Premise", value: premise });
        }
        const toneTokens = [
            ...rec.genres.slice(0, 2),
            ...rec.themes.slice(0, 1),
        ];
        if (toneTokens.length > 0) {
            items.push({ label: "Tone", value: toneTokens.join(", ") });
        }
        const lengthTokens = [
            rec.episodes ? `${rec.episodes} eps` : null,
            rec.media_type ?? null,
            rec.demographics[0] ?? null,
        ].filter(Boolean) as string[];
        if (lengthTokens.length > 0) {
            items.push({ label: "Length", value: lengthTokens.join(" • ") });
        }
        if (rec.recommendation_reason) {
            items.push({
                label: "Why recommended",
                value: rec.recommendation_reason,
            });
        }
        if (items.length > 3) {
            const why = items.find((item) => item.label === "Why recommended");
            const trimmed = items
                .filter((item) => item.label !== "Why recommended")
                .slice(0, 2);
            return why ? [...trimmed, why] : trimmed;
        }
        return items;
    }

    $effect(() => {
        const currentId = recommendation?.mal_id ?? null;
        currentId;
        showWatchedRating = false;
        showDetails = false;
        isDismissing = false;
        if (dismissTimeout) {
            clearTimeout(dismissTimeout);
            dismissTimeout = null;
        }
    });

    onDestroy(() => {
        if (dismissTimeout) {
            clearTimeout(dismissTimeout);
        }
    });
</script>

{#if recommendation}
    <div class="max-w-3xl mx-auto">
        <!-- Recommendation Card -->
        <div
            class="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-5 sm:p-8 mb-6 recommendation-card"
            class:is-dismissing={isDismissing}
        >
            <!-- Poster and Header Section -->
            <div class="flex gap-4 sm:gap-6 mb-6">
                <!-- Anime Poster -->
                {#if recommendation.image_url}
                    <div class="shrink-0 w-24 sm:w-32">
                        <img
                            src={recommendation.image_url}
                            alt={`${recommendation.title} poster`}
                            class="w-full rounded-lg shadow-lg object-cover"
                            loading="eager"
                        />
                    </div>
                {:else}
                    <div
                        class="shrink-0 w-24 sm:w-32 h-36 sm:h-48 bg-slate-200 dark:bg-slate-700 rounded-lg flex items-center justify-center"
                    >
                        <span class="text-4xl">🎬</span>
                    </div>
                {/if}

                <!-- Title and Basic Info -->
                <div class="flex-1 min-w-0">
                    <div class="mb-4">
                        <span
                            class="text-xs sm:text-sm font-medium text-indigo-600 dark:text-indigo-400"
                        >
                            Your Next Discovery
                        </span>
                        <h2
                            class="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100 mt-2 leading-tight"
                        >
                            {recommendation.title}
                        </h2>
                    </div>

                    <div class="flex flex-col gap-1 mb-4 text-sm">
                        <span
                            class={`inline-flex w-fit items-center gap-2 px-3 py-1 rounded-full font-medium ${modeCopy[mode].accent}`}
                        >
                            {modeCopy[mode].label}
                        </span>
                        <span
                            class="text-slate-500 dark:text-slate-400 text-xs"
                        >
                            {modeCopy[mode].description}
                        </span>
                    </div>

                    <div
                        class="flex items-center gap-3 sm:gap-4 text-xs sm:text-sm text-slate-600 dark:text-slate-400"
                    >
                        {#if recommendation.score}
                            <span class="flex items-center gap-1">
                                <svg
                                    class="w-4 h-4"
                                    fill="currentColor"
                                    viewBox="0 0 20 20"
                                >
                                    <path
                                        d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                                    />
                                </svg>
                                {recommendation.score}
                            </span>
                        {/if}
                        {#if recommendation.episodes}
                            <span>{recommendation.episodes} eps</span>
                        {/if}
                        {#if recommendation.studios.length > 0}
                            <span class="hidden sm:inline"
                                >{recommendation.studios.join(", ")}</span
                            >
                        {/if}
                    </div>
                </div>
            </div>

            <!-- Genre and Theme Tags -->
            <div class="flex flex-wrap gap-2 mb-4">
                {#each recommendation.genres as genre}
                    <span
                        class="px-3 py-1 text-sm rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 font-medium"
                    >
                        {genre}
                    </span>
                {/each}
                {#each recommendation.themes as theme}
                    <span
                        class="px-3 py-1 text-sm rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300"
                    >
                        {theme}
                    </span>
                {/each}
            </div>

            {#if recommendation.synopsis}
                <p
                    class="text-slate-700 dark:text-slate-300 mb-6 leading-relaxed"
                >
                    {recommendation.synopsis}
                </p>
            {/if}

            <!-- Recommendation Reason -->
            <div
                class="bg-linear-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-lg p-4 mb-6 border border-indigo-100 dark:border-indigo-800"
            >
                <h3
                    class="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2"
                >
                    Why this recommendation?
                </h3>
                <p
                    class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed"
                >
                    {recommendation.recommendation_reason}
                </p>
            </div>

            <!-- Decision Actions -->
            <div class="space-y-5">
                <div
                    class="rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50/70 dark:bg-slate-900/20 p-5 space-y-4"
                >
                    <button
                        type="button"
                        onclick={onAddToWatchlist}
                        class="w-full flex items-center justify-center gap-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-base py-3 transition-colors"
                    >
                        <span class="text-lg">▶︎</span>
                        <span>Start / Add to watchlist</span>
                    </button>
                    <p
                        class="text-xs text-center text-slate-500 dark:text-slate-400"
                    >
                        Lock it in now and we’ll pin it to your queue.
                    </p>

                    <div
                        class="flex flex-wrap items-center gap-2 sm:gap-3 text-xs sm:text-sm"
                    >
                        <button
                            type="button"
                            onclick={toggleWatchedRating}
                            class="flex items-center gap-1.5 font-medium text-slate-700 dark:text-slate-200 hover:text-emerald-600"
                        >
                            <span class="text-emerald-500">✓</span>
                            <span>Already watched</span>
                        </button>

                        <button
                            type="button"
                            onclick={handleNotInterestedClick}
                            class="flex items-center gap-1.5 text-slate-500 dark:text-slate-400 hover:text-red-500"
                        >
                            <span class="text-base">×</span>
                            <span>Not interested</span>
                        </button>

                        <button
                            type="button"
                            onclick={toggleDetails}
                            class="sm:ml-auto flex items-center gap-1 text-xs text-slate-500 dark:text-slate-400 hover:text-slate-800"
                        >
                            <span>ⓘ</span>
                            <span>{showDetails ? "Hide" : "Details"}</span>
                        </button>
                    </div>

                    {#if showWatchedRating}
                        <div
                            class="flex flex-wrap items-center justify-center gap-3 rounded-xl border border-emerald-200 dark:border-emerald-800 bg-white/80 dark:bg-slate-900/40 p-3 text-sm"
                        >
                            {#each ratingOptions as option}
                                <button
                                    type="button"
                                    onclick={() =>
                                        handleWatchedRatingSelect(option.value)}
                                    class="flex flex-col items-center gap-1 px-3 py-1.5 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-900/20 text-slate-700 dark:text-slate-200"
                                >
                                    <span class="text-2xl">{option.emoji}</span>
                                    <span class="text-xs">{option.label}</span>
                                </button>
                            {/each}
                        </div>
                    {/if}

                    {#if showDetails && detailItems.length > 0}
                        <ul
                            class="space-y-1.5 text-sm text-slate-600 dark:text-slate-300 list-none"
                        >
                            {#each detailItems as detail}
                                <li class="flex gap-2">
                                    <span class="text-slate-400">•</span>
                                    <span>
                                        <span class="font-semibold"
                                            >{detail.label}:</span
                                        >
                                        {detail.value}
                                    </span>
                                </li>
                            {/each}
                        </ul>
                    {/if}
                </div>

                <div class="text-center">
                    <button
                        type="button"
                        onclick={onRegenerate}
                        class="text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-indigo-600 hover:underline underline-offset-4"
                    >
                        Need another vibe? Try a different pick
                    </button>
                </div>
            </div>
        </div>
    </div>
{:else}
    <div class="max-w-2xl mx-auto text-center py-12">
        <div class="text-6xl mb-4">🎬</div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-2">
            Ready to discover something new?
        </h2>
        <p class="text-slate-600 dark:text-slate-400">
            Add a show to your watchlist, then use the Get recommendation button
            when you're ready.
        </p>
    </div>
{/if}

<style>
    .recommendation-card {
        transition:
            opacity 200ms ease,
            transform 200ms ease;
    }

    .recommendation-card.is-dismissing {
        opacity: 0;
        transform: translateY(8px);
    }
</style>
