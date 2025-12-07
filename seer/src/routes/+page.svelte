<script lang="ts">
    import { onMount } from "svelte";
    import type {
        AnimeHistoryItem,
        AnimeRecommendation,
        RecommendationMode,
        WatchStatus,
    } from "$lib/types";
    import { getRecommendation } from "$lib/api";
    import {
        loadHistory,
        saveHistory,
        exportHistory,
        importHistory,
        clearHistory,
    } from "$lib/storage";

    import SearchView from "./SearchView.svelte";
    import RecommendationView from "./RecommendationView.svelte";
    import WatchlistView from "./WatchlistView.svelte";
    import PhilosophyView from "./PhilosophyView.svelte";
    import RateLimitIndicator from "$lib/components/RateLimitIndicator.svelte";

    // State
    let history = $state<AnimeHistoryItem[]>([]);
    let currentRecommendation = $state<AnimeRecommendation | null>(null);
    let isLoading = $state(false);
    let error = $state<string | null>(null);
    let view = $state<"search" | "recommendation" | "watchlist" | "philosophy">(
        "search",
    );
    let recommendationMode = $state<RecommendationMode>("explore");
    let sessionExcludedIds = $state<number[]>([]);

    const modeOptions: {
        id: RecommendationMode;
        label: string;
        description: string;
    }[] = [
        {
            id: "explore",
            label: "Explore",
            description: "Discover bold picks outside your comfort zone",
        },
        {
            id: "similar",
            label: "Similar",
            description: "Stay close to favorites with familiar vibes",
        },
    ];

    // Load history on mount
    onMount(() => {
        history = loadHistory();
        if (history.length > 0) {
            view = "recommendation";
        }
    });

    // Auto-save history when it changes
    $effect(() => {
        if (history.length > 0) {
            saveHistory(history);
        }
    });

    $effect(() => {
        if (history.length > 0 && view === "search") {
            view = "recommendation";
        }
    });

    function resetSessionExclusions() {
        sessionExcludedIds = [];
    }

    function addSessionExclude(id: number | null | undefined) {
        if (!id) return;
        const next = new Set(sessionExcludedIds);
        next.add(id);
        sessionExcludedIds = Array.from(next).slice(-200);
    }

    function buildExclusionList() {
        // Only send session exclusions (temporary dismissals)
        // Backend extracts history IDs from anime_history, no need to send them twice
        return sessionExcludedIds;
    }

    function handleAnimeSelected(anime: AnimeHistoryItem) {
        const alreadyExists = history.some(
            (item) => item.mal_id === anime.mal_id,
        );
        if (alreadyExists) return;
        const wasEmpty = history.length === 0;
        history = [...history, anime];
        if (wasEmpty) {
            resetSessionExclusions();
            view = "watchlist";
        }
    }

    async function fetchRecommendation() {
        if (history.length === 0) return;

        isLoading = true;
        error = null;

        try {
            // Get session exclusions (backend already filters by history)
            const exclusions = buildExclusionList();
            const response = await getRecommendation(
                history,
                recommendationMode,
                exclusions,
            );
            const recommendation = response.recommendation ?? null;

            if (!response || !recommendation) {
                throw new Error("Failed to get recommendation");
            }

            currentRecommendation = recommendation;
            view = "recommendation";
        } catch (err: any) {
            // Extract detailed error message from APIError
            if (err.detail) {
                error = err.detail;
            } else if (err.message) {
                error = err.message;
            } else {
                error = "Failed to get recommendation";
            }
            console.error("Recommendation error:", err);
        } finally {
            isLoading = false;
        }
    }

    function handleRating(
        rating: "positive" | "neutral" | "negative",
        options: { watchStatus?: WatchStatus; hasSeen?: boolean } = {},
    ) {
        if (!currentRecommendation) return;

        const ratingStatusMap: Record<
            "positive" | "neutral" | "negative",
            WatchStatus
        > = {
            positive: "completed",
            neutral: "backlog",
            negative: "ignored",
        };

        const watch_status = options.watchStatus ?? ratingStatusMap[rating];
        const has_seen = options.hasSeen ?? watch_status === "completed";

        const ratedAnime: AnimeHistoryItem = {
            ...currentRecommendation,
            has_seen,
            rating,
            watch_status,
        };

        history = [...history, ratedAnime];
        currentRecommendation = null;
    }

    function handleAddToWatchlist() {
        if (!currentRecommendation) return;

        const queuedAnime: AnimeHistoryItem = {
            ...currentRecommendation,
            has_seen: false,
            rating: null,
            watch_status: "backlog",
        };

        history = [...history, queuedAnime];
        currentRecommendation = null;
    }

    function handleAlreadyWatched(rating: "positive" | "neutral" | "negative") {
        handleRating(rating, { watchStatus: "completed", hasSeen: true });
    }

    async function handleNotInterested() {
        if (!currentRecommendation || isLoading) return;
        addSessionExclude(currentRecommendation.mal_id);
        handleRating("negative", { watchStatus: "ignored", hasSeen: false });
        await fetchRecommendation();
    }

    async function handleRegenerate() {
        if (currentRecommendation) {
            addSessionExclude(currentRecommendation.mal_id);
        }
        await fetchRecommendation();
    }

    function handleExport() {
        exportHistory(history);
    }

    async function handleImport(event: Event) {
        const input = event.target as HTMLInputElement;
        const file = input.files?.[0];
        if (!file) return;

        try {
            const importedHistory = await importHistory(file);
            history = importedHistory;
            saveHistory(history);
            view = "watchlist";
            resetSessionExclusions();
        } catch (err) {
            error =
                err instanceof Error
                    ? err.message
                    : "Failed to import watchlist";
            console.error("Import error:", err);
        }
    }

    function handleClearHistory() {
        if (confirm("Are you sure you want to clear your entire watchlist?")) {
            history = [];
            currentRecommendation = null;
            clearHistory();
            resetSessionExclusions();
            view = "search";
        }
    }

    function handleWatchStatusChange(index: number, status: WatchStatus) {
        history = history.map((item, i) => {
            if (i !== index) return item;
            const isWatched = status === "completed";
            return {
                ...item,
                watch_status: status,
                has_seen: isWatched,
            };
        });
    }

    function handleHistoryRatingChange(
        index: number,
        rating: "positive" | "neutral" | "negative",
    ) {
        history = history.map((item, i) => {
            if (i !== index) return item;
            if (item.watch_status !== "completed") return item;
            return {
                ...item,
                rating,
            };
        });
    }
</script>

<main
    class="min-h-screen bg-linear-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800"
>
    <!-- Header -->
    <header
        class="border-b border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-10"
    >
        <div class="max-w-5xl mx-auto px-4 py-3 sm:py-4">
            <div class="flex items-center justify-between mb-2 sm:mb-0">
                <div class="flex items-center gap-2 sm:gap-3">
                    <h1
                        class="text-xl sm:text-2xl font-bold bg-linear-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"
                    >
                        Seer
                    </h1>
                    <RateLimitIndicator />
                </div>

                <div class="flex items-center gap-1 sm:gap-2">
                    <button
                        onclick={() =>
                            (view =
                                history.length > 0
                                    ? "recommendation"
                                    : "search")}
                        class="px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        class:bg-slate-100={view === "recommendation" ||
                            view === "search"}
                        class:dark:bg-slate-800={view === "recommendation" ||
                            view === "search"}
                    >
                        Home
                    </button>
                    <button
                        onclick={() => (view = "watchlist")}
                        class="px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        class:bg-slate-100={view === "watchlist"}
                        class:dark:bg-slate-800={view === "watchlist"}
                    >
                        <span class="hidden sm:inline">Watchlist</span>
                        <span class="sm:hidden">List</span>
                        <span class="ml-1">({history.length})</span>
                    </button>
                    <button
                        onclick={() => (view = "philosophy")}
                        class="px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                        class:bg-slate-100={view === "philosophy"}
                        class:dark:bg-slate-800={view === "philosophy"}
                    >
                        Philosophy
                    </button>
                    <button
                        onclick={handleExport}
                        disabled={history.length === 0}
                        class="px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        Export
                    </button>
                    <label
                        class="px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                    >
                        Import
                        <input
                            type="file"
                            accept=".json"
                            onchange={handleImport}
                            class="hidden"
                        />
                    </label>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="max-w-5xl mx-auto px-4 py-8">
        {#if error}
            <div
                class="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
            >
                <p class="text-sm text-red-800 dark:text-red-200">{error}</p>
                <button
                    onclick={() => (error = null)}
                    class="mt-2 text-xs text-red-600 dark:text-red-400 hover:underline"
                >
                    Dismiss
                </button>
            </div>
        {/if}

        {#if view !== "philosophy" && history.length > 0}
            <div class="mb-6">
                <div
                    class="bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 flex flex-col gap-4"
                >
                    <div>
                        <p
                            class="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400 font-semibold mb-2"
                        >
                            Ready for something new?
                        </p>
                        <p class="text-sm text-slate-600 dark:text-slate-300">
                            Choose your vibe and get a personalized
                            recommendation based on your watchlist.
                        </p>
                    </div>

                    <!-- Mode Selector -->
                    <div class="flex flex-col gap-2">
                        <p
                            class="text-xs font-medium text-slate-700 dark:text-slate-300"
                        >
                            Recommendation Mode
                        </p>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {#each modeOptions as option}
                                <button
                                    type="button"
                                    onclick={() =>
                                        (recommendationMode = option.id)}
                                    disabled={isLoading}
                                    class="text-left px-4 py-3 rounded-lg border transition-all disabled:opacity-50 disabled:cursor-not-allowed {recommendationMode ===
                                    option.id
                                        ? 'border-indigo-500 bg-indigo-50/70 dark:bg-indigo-900/20 text-indigo-900 dark:text-indigo-50 shadow-sm'
                                        : 'border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:border-slate-300 dark:hover:border-slate-500'}"
                                >
                                    <div class="font-semibold text-sm mb-1">
                                        {option.label}
                                    </div>
                                    <div class="text-xs opacity-80">
                                        {option.description}
                                    </div>
                                </button>
                            {/each}
                        </div>
                    </div>

                    <div class="flex flex-col gap-2">
                        <button
                            type="button"
                            onclick={currentRecommendation
                                ? handleRegenerate
                                : fetchRecommendation}
                            disabled={history.length === 0 || isLoading}
                            class="px-5 py-2.5 rounded-lg text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 disabled:text-slate-500 disabled:cursor-not-allowed transition-colors"
                        >
                            {isLoading
                                ? "Finding your next anime..."
                                : currentRecommendation
                                  ? "Get another recommendation"
                                  : "Get recommendation"}
                        </button>
                        {#if history.length === 0}
                            <p
                                class="text-xs text-center text-slate-500 dark:text-slate-400"
                            >
                                Add a show to your watchlist to enable
                                recommendations.
                            </p>
                        {/if}
                    </div>
                </div>
            </div>
        {/if}

        {#if isLoading}
            <div class="flex items-center justify-center py-20 animate-fade-in">
                <div class="text-center">
                    <div
                        class="inline-block h-10 w-10 animate-spin rounded-full border-4 border-solid border-indigo-600 border-r-transparent mb-4"
                    ></div>
                    <p
                        class="text-lg font-medium text-slate-700 dark:text-slate-300"
                    >
                        Finding your next anime...
                    </p>
                    <p class="text-sm text-slate-500 dark:text-slate-400 mt-2">
                        Analyzing your preferences
                    </p>
                </div>
            </div>
        {:else if view === "search" && history.length === 0}
            <div class="animate-fade-in">
                <SearchView {history} onAnimeSelected={handleAnimeSelected} />
            </div>
        {:else if view === "recommendation"}
            <div class="animate-fade-in">
                <RecommendationView
                    recommendation={currentRecommendation}
                    onAddToWatchlist={handleAddToWatchlist}
                    onAlreadyWatched={handleAlreadyWatched}
                    onNotInterested={handleNotInterested}
                    onRegenerate={handleRegenerate}
                    mode={recommendationMode}
                />
            </div>
        {:else if view === "watchlist"}
            <div class="animate-fade-in">
                <WatchlistView
                    {history}
                    onBack={() =>
                        (view =
                            history.length > 0 ? "recommendation" : "search")}
                    onClear={handleClearHistory}
                    onUpdateStatus={handleWatchStatusChange}
                    onUpdateRating={handleHistoryRatingChange}
                />
            </div>
        {:else if view === "philosophy"}
            <div class="animate-fade-in">
                <PhilosophyView />
            </div>
        {/if}
    </div>
</main>
