<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { getRateLimitInfo, type RateLimitInfo } from "$lib/api";

    let rateLimitInfo = $state<RateLimitInfo | null>(null);
    let timeUntilReset = $state<string>("");
    let interval: ReturnType<typeof setInterval> | null = null;
    const showResetTimer = $derived(
        !!rateLimitInfo && rateLimitInfo.remaining < rateLimitInfo.limit,
    );
    const statusText = $derived(
        rateLimitInfo
            ? `${rateLimitInfo.remaining}/${rateLimitInfo.limit} requests`
            : "API status: no response",
    );
    const statusTitle = $derived(
        rateLimitInfo
            ? "API rate limit status"
            : "No API response detected; service may be offline",
    );
    const statusIcon = $derived(rateLimitInfo ? getStatusIcon() : "⚠");

    function updateRateLimitInfo() {
        rateLimitInfo = getRateLimitInfo();
        if (rateLimitInfo) {
            updateTimeUntilReset();
        }
    }

    function updateTimeUntilReset() {
        if (!rateLimitInfo) return;

        const now = Math.floor(Date.now() / 1000);
        const secondsLeft = rateLimitInfo.reset - now;

        if (secondsLeft <= 0) {
            timeUntilReset = "Reset available";
        } else if (secondsLeft < 60) {
            timeUntilReset = `${secondsLeft}s`;
        } else {
            const minutes = Math.floor(secondsLeft / 60);
            timeUntilReset = `${minutes}m`;
        }
    }

    onMount(() => {
        updateRateLimitInfo();
        // Update every 10 seconds
        interval = setInterval(() => {
            updateRateLimitInfo();
        }, 10000);
    });

    onDestroy(() => {
        if (interval) {
            clearInterval(interval);
        }
    });

    $effect(() => {
        // Update immediately when rate limit info changes
        updateRateLimitInfo();
    });

    function getStatusColor() {
        if (!rateLimitInfo)
            return "bg-slate-100 text-slate-600 dark:bg-slate-800/70 dark:text-slate-200";
        const percentage =
            (rateLimitInfo.remaining / rateLimitInfo.limit) * 100;

        if (percentage > 50) {
            return "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300";
        } else if (percentage > 25) {
            return "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300";
        } else {
            return "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300";
        }
    }

    function getStatusIcon() {
        if (!rateLimitInfo) return "ⓘ";
        const percentage =
            (rateLimitInfo.remaining / rateLimitInfo.limit) * 100;

        if (percentage > 50) {
            return "✓";
        } else if (percentage > 25) {
            return "⚠";
        } else {
            return "⚠";
        }
    }
</script>

<div
    class={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${getStatusColor()}`}
    title={statusTitle}
>
    <span>{statusIcon}</span>
    <span>{statusText}</span>
    {#if showResetTimer}
        <span class="opacity-75">• {timeUntilReset}</span>
    {/if}
</div>
