<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import {
        getApiStatus,
        getRateLimitInfo,
        type ApiStatus,
        type RateLimitInfo,
    } from "$lib/api";

    let rateLimitInfo = $state<RateLimitInfo | null>(null);
    let apiStatus = $state<ApiStatus | null>(null);
    let timeUntilReset = $state<string>("");
    let interval: ReturnType<typeof setInterval> | null = null;
    const showResetTimer = $derived(
        !!rateLimitInfo && rateLimitInfo.remaining < rateLimitInfo.limit,
    );
    const hasStatus = $derived(
        !!rateLimitInfo ||
            apiStatus?.status === "ok" ||
            apiStatus?.status === "error",
    );
    const statusText = $derived(
        (() => {
            if (rateLimitInfo) {
                return `${rateLimitInfo.remaining}/${rateLimitInfo.limit} requests`;
            }
            if (apiStatus?.status === "ok") return "API connected";
            if (apiStatus?.status === "error") return "API error";
            return "";
        })(),
    );
    const statusTitle = $derived(
        (() => {
            if (rateLimitInfo) return "API rate limit status";
            if (apiStatus?.status === "ok")
                return "API responded successfully (no limit data provided)";
            if (apiStatus?.status === "error")
                return "Recent API request failed; check backend";
            return "";
        })(),
    );
    const statusIcon = $derived(
        (() => {
            if (rateLimitInfo) {
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

            if (apiStatus?.status === "ok") return "✓";
            if (apiStatus?.status === "error") return "⚠";
            return "";
        })(),
    );

    function updateIndicatorInfo() {
        rateLimitInfo = getRateLimitInfo();
        apiStatus = getApiStatus();
        if (rateLimitInfo) {
            updateTimeUntilReset();
        } else {
            timeUntilReset = "";
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
        updateIndicatorInfo();
        // Update every 10 seconds
        interval = setInterval(() => {
            updateIndicatorInfo();
        }, 10000);
    });

    onDestroy(() => {
        if (interval) {
            clearInterval(interval);
        }
    });

    $effect(() => {
        // Update immediately when rate limit info changes
        updateIndicatorInfo();
    });

    function getStatusColor() {
        if (rateLimitInfo) {
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

        if (apiStatus?.status === "ok") {
            return "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300";
        }
        if (apiStatus?.status === "error") {
            return "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300";
        }
        return "bg-slate-100 text-slate-600 dark:bg-slate-800/70 dark:text-slate-200";
    }
</script>

{#if hasStatus}
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
{/if}
