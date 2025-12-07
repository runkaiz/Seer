<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import {
        getApiStatus,
        getRateLimitInfo,
        subscribeToApiStatus,
        subscribeToRateLimitInfo,
        type ApiStatus,
        type RateLimitInfo,
    } from "$lib/api";

    let rateLimitInfo = $state<RateLimitInfo | null>(null);
    let apiStatus = $state<ApiStatus | null>(null);
    let timeUntilReset = $state<string>("");
    let resetTimerInterval: ReturnType<typeof setInterval> | null = null;
    let unsubscribeApiStatus: (() => void) | null = null;
    let unsubscribeRateLimitInfo: (() => void) | null = null;
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
    const rateLimitPercentage = $derived(
        rateLimitInfo
            ? (rateLimitInfo.remaining / rateLimitInfo.limit) * 100
            : null,
    );
    const statusIcon = $derived(
        (() => {
            if (rateLimitPercentage !== null) {
                return rateLimitPercentage > 50 ? "✓" : "⚠";
            }
            if (apiStatus?.status === "ok") return "✓";
            if (apiStatus?.status === "error") return "⚠";
            return "";
        })(),
    );
    const statusColor = $derived(
        (() => {
            if (rateLimitPercentage !== null) {
                if (rateLimitPercentage > 50) {
                    return "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300";
                } else if (rateLimitPercentage > 25) {
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
        if (!rateLimitInfo) {
            timeUntilReset = "";
            return;
        }

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

        unsubscribeApiStatus = subscribeToApiStatus((status) => {
            apiStatus = status;
        });

        unsubscribeRateLimitInfo = subscribeToRateLimitInfo((info) => {
            rateLimitInfo = info;
            updateTimeUntilReset();
        });

        // Keep the reset timer display fresh
        resetTimerInterval = setInterval(() => {
            updateTimeUntilReset();
        }, 1000);
    });

    onDestroy(() => {
        if (resetTimerInterval) {
            clearInterval(resetTimerInterval);
        }
        if (unsubscribeApiStatus) unsubscribeApiStatus();
        if (unsubscribeRateLimitInfo) unsubscribeRateLimitInfo();
    });
</script>

{#if hasStatus}
    <div
        class={`hidden sm:inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium ${statusColor}`}
        title={statusTitle}
    >
        <span>{statusIcon}</span>
        <span>{statusText}</span>
        {#if showResetTimer}
            <span class="opacity-75">• {timeUntilReset}</span>
        {/if}
    </div>
{/if}
