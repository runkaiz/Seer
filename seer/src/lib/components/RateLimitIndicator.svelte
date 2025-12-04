<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { getRateLimitInfo, type RateLimitInfo } from "$lib/api";

    let rateLimitInfo = $state<RateLimitInfo | null>(null);
    let timeUntilReset = $state<string>("");
    let interval: ReturnType<typeof setInterval> | null = null;

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

{#if rateLimitInfo}
    <div
        class={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${getStatusColor()}`}
        title="API rate limit status"
    >
        <span>{getStatusIcon()}</span>
        <span>
            {rateLimitInfo.remaining}/{rateLimitInfo.limit} requests
        </span>
        {#if rateLimitInfo.remaining < rateLimitInfo.limit}
            <span class="opacity-75">• {timeUntilReset}</span>
        {/if}
    </div>
{/if}
