import { w as attr, x as ensure_array_like, y as attr_style, z as stringify, F as attr_class } from "../../chunks/index.js";
import { p as public_env } from "../../chunks/shared-server.js";
import { a as ssr_context, e as escape_html } from "../../chunks/context.js";
function onDestroy(fn) {
  /** @type {SSRContext} */
  ssr_context.r.on_destroy(fn);
}
public_env.PUBLIC_API_URL || "http://localhost:8000/api";
function SearchView($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let query = "";
    let results = [];
    const trimmedQuery = query.trim();
    $$renderer2.push(`<div class="max-w-2xl mx-auto"><div class="text-center mb-8"><h2 class="text-3xl font-bold text-slate-900 dark:text-slate-100 mb-3">Welcome to Seer</h2> <p class="text-lg text-slate-600 dark:text-slate-400 mb-2">Start by searching for an anime you recently enjoyed</p> <p class="text-sm text-slate-500 dark:text-slate-500">We'll use this to understand your tastes and recommend something new</p></div> <div class="mb-6"><div class="relative"><input type="text"${attr("value", query)} placeholder="Start typing an anime title... (e.g., 'Cowboy Bebop')" class="w-full px-4 py-3 pr-12 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow" autocomplete="off"/> `);
    {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div> `);
    {
      $$renderer2.push("<!--[!-->");
      if (trimmedQuery.length > 0 && trimmedQuery.length < 3) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<p class="mt-2 text-xs text-slate-500 dark:text-slate-400">Type at least 3 characters to search</p>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--></div> `);
    if (results.length > 0) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="space-y-3 animate-fade-in"><h3 class="text-sm font-medium text-slate-700 dark:text-slate-300">Select the anime you watched:</h3> <!--[-->`);
      const each_array = ensure_array_like(results);
      for (let index = 0, $$length = each_array.length; index < $$length; index++) {
        let anime = each_array[index];
        $$renderer2.push(`<button class="w-full p-4 rounded-xl border text-left transition-all bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:border-indigo-500 dark:hover:border-indigo-400 hover:shadow-lg hover:-translate-y-0.5 animate-slide-in"${attr_style(`animation-delay: ${stringify(index * 50)}ms`)}><div class="flex gap-4">`);
        if (anime.image_url) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<div class="shrink-0 w-20 sm:w-24"><img${attr("src", anime.image_url)}${attr("alt", `${anime.title} poster`)} class="w-full rounded-lg shadow-md object-cover" loading="lazy"/></div>`);
        } else {
          $$renderer2.push("<!--[!-->");
          $$renderer2.push(`<div class="shrink-0 w-20 sm:w-24 h-28 sm:h-32 bg-slate-200 dark:bg-slate-700 rounded-lg flex items-center justify-center"><span class="text-2xl">🎬</span></div>`);
        }
        $$renderer2.push(`<!--]--> <div class="flex-1 min-w-0"><h4 class="font-semibold text-slate-900 dark:text-slate-100 mb-1">${escape_html(anime.title)}</h4> `);
        if (anime.genres.length > 0) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<div class="flex flex-wrap gap-1.5 mb-2"><!--[-->`);
          const each_array_1 = ensure_array_like(anime.genres.slice(0, 4));
          for (let $$index = 0, $$length2 = each_array_1.length; $$index < $$length2; $$index++) {
            let genre = each_array_1[$$index];
            $$renderer2.push(`<span class="px-2 py-0.5 text-xs rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300">${escape_html(genre)}</span>`);
          }
          $$renderer2.push(`<!--]--></div>`);
        } else {
          $$renderer2.push("<!--[!-->");
        }
        $$renderer2.push(`<!--]--> `);
        if (anime.synopsis) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<p class="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 svelte-1e5kcgt">${escape_html(anime.synopsis)}</p>`);
        } else {
          $$renderer2.push("<!--[!-->");
        }
        $$renderer2.push(`<!--]--> <div class="flex items-center gap-3 mt-2 text-xs text-slate-500 dark:text-slate-500">`);
        if (anime.score) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<span>Score: ${escape_html(anime.score)}</span>`);
        } else {
          $$renderer2.push("<!--[!-->");
        }
        $$renderer2.push(`<!--]--> `);
        if (anime.episodes) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<span>${escape_html(anime.episodes)} episodes</span>`);
        } else {
          $$renderer2.push("<!--[!-->");
        }
        $$renderer2.push(`<!--]--></div></div></div></button>`);
      }
      $$renderer2.push(`<!--]--></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      if (trimmedQuery.length >= 2) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="text-center py-12 text-slate-500 dark:text-slate-400"><div class="text-4xl mb-3">🔍</div> <p class="font-medium">No results found for "${escape_html(trimmedQuery)}"</p> <p class="text-sm mt-1">Try a different title or check your spelling</p></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--></div>`);
  });
}
function RateLimitIndicator($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    onDestroy(() => {
    });
    {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]-->`);
  });
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let history = [];
    let isLoading = false;
    let view = "search";
    let recommendationMode = "explore";
    const modeOptions = [
      {
        id: "explore",
        label: "Explore",
        description: "Discover bold picks outside your comfort zone"
      },
      {
        id: "similar",
        label: "Similar",
        description: "Stay close to favorites with familiar vibes"
      }
    ];
    $$renderer2.push(`<main class="min-h-screen bg-linear-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800"><header class="border-b border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-10"><div class="max-w-5xl mx-auto px-4 py-3 sm:py-4"><div class="flex items-center justify-between mb-2 sm:mb-0"><div class="flex items-center gap-2 sm:gap-3"><h1 class="text-xl sm:text-2xl font-bold bg-linear-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Seer</h1> `);
    RateLimitIndicator($$renderer2);
    $$renderer2.push(`<!----></div> <div class="flex items-center gap-1 sm:gap-2"><button${attr_class("px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors", void 0, {
      "bg-slate-100": view === "search",
      "dark:bg-slate-800": view === "search"
    })}>Home</button> <button${attr_class("px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors", void 0, {
      "bg-slate-100": view === "watchlist",
      "dark:bg-slate-800": view === "watchlist"
    })}><span class="hidden sm:inline">Watchlist</span> <span class="sm:hidden">List</span> <span class="ml-1">(${escape_html(history.length)})</span></button> <button${attr_class("px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors", void 0, {
      "bg-slate-100": view === "philosophy",
      "dark:bg-slate-800": view === "philosophy"
    })}>Philosophy</button> <button${attr("disabled", history.length === 0, true)} class="px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">Export</button> <label class="px-2 sm:px-3 py-1.5 text-xs sm:text-sm rounded-lg text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer">Import <input type="file" accept=".json" class="hidden"/></label></div></div></div></header> <div class="max-w-5xl mx-auto px-4 py-8">`);
    {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--> `);
    if (history.length > 0) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="mb-6"><div class="bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 flex flex-col gap-4"><div><p class="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400 font-semibold mb-2">Ready for something new?</p> <p class="text-sm text-slate-600 dark:text-slate-300">Choose your vibe and get a personalized
                            recommendation based on your watchlist.</p></div> <div class="flex flex-col gap-2"><p class="text-xs font-medium text-slate-700 dark:text-slate-300">Recommendation Mode</p> <div class="grid grid-cols-1 sm:grid-cols-2 gap-2"><!--[-->`);
      const each_array = ensure_array_like(modeOptions);
      for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
        let option = each_array[$$index];
        $$renderer2.push(`<button type="button"${attr("disabled", isLoading, true)}${attr_class(`text-left px-4 py-3 rounded-lg border transition-all disabled:opacity-50 disabled:cursor-not-allowed ${stringify(recommendationMode === option.id ? "border-indigo-500 bg-indigo-50/70 dark:bg-indigo-900/20 text-indigo-900 dark:text-indigo-50 shadow-sm" : "border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:border-slate-300 dark:hover:border-slate-500")}`)}><div class="font-semibold text-sm mb-1">${escape_html(option.label)}</div> <div class="text-xs opacity-80">${escape_html(option.description)}</div></button>`);
      }
      $$renderer2.push(`<!--]--></div></div> <div class="flex flex-col gap-2"><button type="button"${attr("disabled", history.length === 0 || isLoading, true)} class="px-5 py-2.5 rounded-lg text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 disabled:text-slate-500 disabled:cursor-not-allowed transition-colors">${escape_html("Get recommendation")}</button> `);
      if (history.length === 0) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<p class="text-xs text-center text-slate-500 dark:text-slate-400">Add a show to your watchlist to enable
                                recommendations.</p>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--></div></div></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[!-->");
      if (history.length === 0) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="animate-fade-in">`);
        SearchView($$renderer2);
        $$renderer2.push(`<!----></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
        {
          $$renderer2.push("<!--[!-->");
          {
            $$renderer2.push("<!--[!-->");
            {
              $$renderer2.push("<!--[!-->");
            }
            $$renderer2.push(`<!--]-->`);
          }
          $$renderer2.push(`<!--]-->`);
        }
        $$renderer2.push(`<!--]-->`);
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--></div></main>`);
  });
}
export {
  _page as default
};
