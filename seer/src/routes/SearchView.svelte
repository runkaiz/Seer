<script lang="ts">
    import type { AnimeBase, AnimeHistoryItem } from "$lib/types";
    import { searchAnime } from "$lib/api";

    interface Props {
        onAnimeSelected: (anime: AnimeHistoryItem) => void;
        history: AnimeHistoryItem[];
    }

    let { onAnimeSelected, history }: Props = $props();

    let query = $state("");
    let results = $state<AnimeBase[]>([]);
    let isSearching = $state(false);
    let searchError = $state<string | null>(null);
    let searchTimeout: ReturnType<typeof setTimeout> | null = null;

    const trimmedQuery = $derived(query.trim());

    const getNumericScore = (score: AnimeBase["score"]) => {
        const parsedScore =
            score === null ? Number.NEGATIVE_INFINITY : Number(score);
        return Number.isFinite(parsedScore)
            ? parsedScore
            : Number.NEGATIVE_INFINITY;
    };

    async function performSearch(searchQuery: string) {
        if (searchQuery.length < 2) {
            results = [];
            return;
        }

        isSearching = true;
        searchError = null;

        try {
            const response = await searchAnime(searchQuery);
            results = [...response.results].sort(
                (a, b) => getNumericScore(b.score) - getNumericScore(a.score),
            );
        } catch (error) {
            searchError =
                error instanceof Error ? error.message : "Search failed";
            results = [];
            console.error("Search error:", error);
        } finally {
            isSearching = false;
        }
    }

    // Debounced auto-search effect
    $effect(() => {
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }

        if (trimmedQuery.length < 2) {
            results = [];
            searchError = null;
            return;
        }

        searchTimeout = setTimeout(() => {
            performSearch(trimmedQuery);
        }, 400);
    });

    function selectAnime(anime: AnimeBase) {
        if (history.length > 0) return;
        const historyItem: AnimeHistoryItem = {
            ...anime,
            has_seen: true,
            rating: "positive",
            watch_status: "completed",
        };
        onAnimeSelected(historyItem);
    }
</script>

<div class="max-w-2xl mx-auto">
    <!-- Welcome Message -->
    <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-slate-900 dark:text-slate-100 mb-3">
            Welcome to Seer
        </h2>
        <p class="text-lg text-slate-600 dark:text-slate-400 mb-2">
            Start by searching for an anime you recently enjoyed
        </p>
        <p class="text-sm text-slate-500 dark:text-slate-500">
            We'll use this to understand your tastes and recommend something new
        </p>
    </div>

    <!-- Search Input -->
    <div class="mb-6">
        <div class="relative">
            <input
                type="text"
                bind:value={query}
                placeholder="Start typing an anime title... (e.g., 'Cowboy Bebop')"
                class="w-full px-4 py-3 pr-12 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
                autocomplete="off"
            />
            {#if isSearching}
                <div class="absolute right-4 top-1/2 -translate-y-1/2">
                    <div
                        class="inline-block h-5 w-5 animate-spin rounded-full border-2 border-solid border-indigo-600 border-r-transparent"
                    ></div>
                </div>
            {/if}
        </div>

        {#if searchError}
            <p class="mt-2 text-sm text-red-600 dark:text-red-400">
                {searchError}
            </p>
        {:else if trimmedQuery.length > 0 && trimmedQuery.length < 2}
            <p class="mt-2 text-xs text-slate-500 dark:text-slate-400">
                Type at least 2 characters to search
            </p>
        {/if}
    </div>

    <!-- Search Results -->
    {#if results.length > 0}
        <div class="space-y-3 animate-fade-in">
            <h3 class="text-sm font-medium text-slate-700 dark:text-slate-300">
                Select the anime you watched:
            </h3>

            {#each results as anime, index (anime.mal_id)}
                <button
                    onclick={() => selectAnime(anime)}
                    class="w-full p-4 rounded-xl border text-left transition-all bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:border-indigo-500 dark:hover:border-indigo-400 hover:shadow-lg hover:-translate-y-0.5 animate-slide-in"
                    style="animation-delay: {index * 50}ms"
                >
                    <div class="flex gap-4">
                        <!-- Anime Poster -->
                        {#if anime.image_url}
                            <div class="shrink-0 w-20 sm:w-24">
                                <img
                                    src={anime.image_url}
                                    alt={`${anime.title} poster`}
                                    class="w-full rounded-lg shadow-md object-cover"
                                    loading="lazy"
                                />
                            </div>
                        {:else}
                            <div
                                class="shrink-0 w-20 sm:w-24 h-28 sm:h-32 bg-slate-200 dark:bg-slate-700 rounded-lg flex items-center justify-center"
                            >
                                <span class="text-2xl">🎬</span>
                            </div>
                        {/if}

                        <div class="flex-1 min-w-0">
                            <h4
                                class="font-semibold text-slate-900 dark:text-slate-100 mb-1"
                            >
                                {anime.title}
                            </h4>
                            {#if anime.genres.length > 0}
                                <div class="flex flex-wrap gap-1.5 mb-2">
                                    {#each anime.genres.slice(0, 4) as genre}
                                        <span
                                            class="px-2 py-0.5 text-xs rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300"
                                        >
                                            {genre}
                                        </span>
                                    {/each}
                                </div>
                            {/if}

                            {#if anime.synopsis}
                                <p
                                    class="text-sm text-slate-600 dark:text-slate-400 line-clamp-2"
                                >
                                    {anime.synopsis}
                                </p>
                            {/if}

                            <div
                                class="flex items-center gap-3 mt-2 text-xs text-slate-500 dark:text-slate-500"
                            >
                                {#if anime.score}
                                    <span>Score: {anime.score}</span>
                                {/if}
                                {#if anime.episodes}
                                    <span>{anime.episodes} episodes</span>
                                {/if}
                            </div>
                        </div>
                    </div>
                </button>
            {/each}
        </div>
    {:else if !isSearching && trimmedQuery.length >= 2}
        <div class="text-center py-12 text-slate-500 dark:text-slate-400">
            <div class="text-4xl mb-3">🔍</div>
            <p class="font-medium">No results found for "{trimmedQuery}"</p>
            <p class="text-sm mt-1">
                Try a different title or check your spelling
            </p>
        </div>
    {/if}
</div>

<style>
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        line-clamp: 2;
        overflow: hidden;
    }
</style>
