<script lang="ts">
    import type { AnimeHistoryItem, UserRating, WatchStatus } from "$lib/types";

    interface Props {
        history: AnimeHistoryItem[];
        onBack: () => void;
        onClear: () => void;
        onUpdateStatus: (index: number, status: WatchStatus) => void;
        onUpdateRating: (index: number, rating: UserRating) => void;
    }

    let { history, onBack, onClear, onUpdateStatus, onUpdateRating }: Props =
        $props();

    function getRatingEmoji(rating: string | null): string {
        if (rating === "positive") return "👍";
        if (rating === "neutral") return "🤔";
        if (rating === "negative") return "👎";
        return "—";
    }

    function getRatingColor(rating: string | null): string {
        if (rating === "positive") return "text-green-600 dark:text-green-400";
        if (rating === "neutral") return "text-slate-600 dark:text-slate-400";
        if (rating === "negative") return "text-red-600 dark:text-red-400";
        return "text-slate-400";
    }

    // Reverse history for display (newest first) with original indices
    let displayHistory = $derived(
        history.map((item, index) => ({ item, originalIndex: index })).reverse()
    );

    let stats = $derived({
        total: history.length,
        positive: history.filter((a) => a.rating === "positive").length,
        neutral: history.filter((a) => a.rating === "neutral").length,
        negative: history.filter((a) => a.rating === "negative").length,
    });

    const statusOptions: {
        label: string;
        value: WatchStatus;
        description: string;
    }[] = [
        { label: "Watching", value: "watching", description: "In progress" },
        { label: "Completed", value: "completed", description: "Finished" },
        { label: "Backlog", value: "backlog", description: "Saved for later" },
        { label: "Ignore", value: "ignored", description: "Not for me" },
    ];

    const statusBadges: Record<WatchStatus, string> = {
        watching:
            "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-200",
        completed:
            "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-200",
        backlog:
            "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-200",
        ignored:
            "bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
    };

    const ratingOptions: { value: UserRating; emoji: string; label: string }[] =
        [
            { value: "positive", emoji: "🙂", label: "Loved it" },
            { value: "neutral", emoji: "😐", label: "It was fine" },
            { value: "negative", emoji: "🤮", label: "Hard pass" },
        ];
</script>

<div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
            <h2 class="text-xl sm:text-2xl font-bold text-slate-900 dark:text-slate-100">
                Your Watchlist
            </h2>
            <p class="text-sm text-slate-600 dark:text-slate-400 mt-1">
                {stats.total} anime tracked
            </p>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 hidden sm:block">
                These statuses help Seer personalize future recommendations.
            </p>
        </div>
        <div class="flex items-center gap-2">
            <button
                onclick={onBack}
                class="px-3 sm:px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-300 text-xs sm:text-sm font-medium"
            >
                Back
            </button>
            <button
                onclick={onClear}
                class="px-3 sm:px-4 py-2 rounded-lg border border-red-300 dark:border-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-red-700 dark:text-red-400 text-xs sm:text-sm font-medium"
            >
                Clear All
            </button>
        </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mb-6">
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-slate-900 dark:text-slate-100">
                {stats.total}
            </div>
            <div class="text-xs text-slate-600 dark:text-slate-400 mt-1">
                Total
            </div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-green-600 dark:text-green-400">
                {stats.positive}
            </div>
            <div class="text-xs text-slate-600 dark:text-slate-400 mt-1">
                Liked
            </div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-slate-600 dark:text-slate-400">
                {stats.neutral}
            </div>
            <div class="text-xs text-slate-600 dark:text-slate-400 mt-1">
                Neutral
            </div>
        </div>
        <div class="bg-white dark:bg-slate-800 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-red-600 dark:text-red-400">
                {stats.negative}
            </div>
            <div class="text-xs text-slate-600 dark:text-slate-400 mt-1">
                Disliked
            </div>
        </div>
    </div>

    <!-- Watchlist -->
    <div class="space-y-4">
        {#each displayHistory as { item: anime, originalIndex } (anime.mal_id)}
            <div
                class="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 transition-colors"
            >
                <div class="flex items-start gap-4">
                    <div
                        class={`flex-shrink-0 text-3xl ${getRatingColor(anime.rating)}`}
                    >
                        {getRatingEmoji(anime.rating)}
                    </div>

                    <div class="flex-1 min-w-0">
                        <h3
                            class="font-semibold text-lg text-slate-900 dark:text-slate-100 mb-2"
                        >
                            {anime.title}
                        </h3>

                        <div
                            class="flex flex-wrap items-center gap-2 mb-3"
                        >
                            <span
                                class={`px-2.5 py-1 text-xs rounded-full font-medium ${statusBadges[anime.watch_status]}`}
                            >
                                {statusOptions.find(
                                    (option) =>
                                        option.value === anime.watch_status,
                                )?.label ?? anime.watch_status}
                            </span>

                            <select
                                class="px-2.5 py-1 text-xs rounded-md border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:border-slate-400 dark:hover:border-slate-500 transition-colors cursor-pointer"
                                value={anime.watch_status}
                                onchange={(event) => {
                                    const select = event.currentTarget as HTMLSelectElement;
                                    onUpdateStatus(originalIndex, select.value as WatchStatus);
                                }}
                            >
                                {#each statusOptions as option}
                                    <option value={option.value}>
                                        {option.label} — {option.description}
                                    </option>
                                {/each}
                            </select>
                        </div>

                        {#if anime.genres.length > 0}
                            <div class="flex flex-wrap gap-1.5 mb-3">
                                {#each anime.genres.slice(0, 5) as genre}
                                    <span
                                        class="px-2 py-0.5 text-xs rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300"
                                    >
                                        {genre}
                                    </span>
                                {/each}
                            </div>
                        {/if}

                        <div
                            class="flex items-center gap-3 mb-3 text-xs text-slate-500 dark:text-slate-500"
                        >
                            {#if anime.score}
                                <span>⭐ {anime.score}</span>
                            {/if}
                            {#if anime.episodes}
                                <span>{anime.episodes} eps</span>
                            {/if}
                            {#if anime.studios.length > 0}
                                <span>{anime.studios[0]}</span>
                            {/if}
                        </div>

                        {#if anime.watch_status === "completed"}
                            <div
                                class="pt-3 border-t border-slate-200 dark:border-slate-700"
                            >
                                <p
                                    class="text-xs font-medium text-slate-600 dark:text-slate-400 mb-2"
                                >
                                    How was it?
                                </p>
                                <div class="flex flex-wrap gap-2">
                                    {#each ratingOptions as option}
                                        <button
                                            type="button"
                                            class={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm border transition-all ${
                                                anime.rating === option.value
                                                    ? "border-indigo-500 bg-indigo-50 text-indigo-700 dark:border-indigo-400 dark:bg-indigo-900/30 dark:text-indigo-200 shadow-sm"
                                                    : "border-slate-200 text-slate-600 hover:border-slate-400 dark:border-slate-700 dark:text-slate-300 dark:hover:border-slate-500"
                                            }`}
                                            onclick={() => onUpdateRating(originalIndex, option.value)}
                                        >
                                            <span class="text-base">{option.emoji}</span>
                                            <span
                                                class="text-xs font-medium"
                                                >{option.label}</span
                                            >
                                        </button>
                                    {/each}
                                </div>
                            </div>
                        {:else}
                            <p
                                class="pt-2 text-xs text-slate-500 dark:text-slate-500"
                            >
                                💡 Mark as completed to rate this anime
                            </p>
                        {/if}
                    </div>
                </div>
            </div>
        {/each}
    </div>

    {#if history.length === 0}
        <div class="text-center py-12">
            <div class="text-6xl mb-4">📚</div>
            <h3
                class="text-xl font-semibold text-slate-900 dark:text-slate-100 mb-2"
            >
                Nothing in your watchlist yet
            </h3>
            <p class="text-slate-600 dark:text-slate-400">
                Start by searching for an anime you've enjoyed!
            </p>
            <button
                onclick={onBack}
                class="mt-4 px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-medium transition-colors"
            >
                Get Started
            </button>
        </div>
    {/if}
</div>
