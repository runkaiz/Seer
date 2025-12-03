"""
Stateless recommendation engine that orchestrates MAL and OpenAI services.

Supports two modes:
- similar: Find anime similar to what user loves (comfort zone)
- explore: Discover new genres and expand horizons (default)

Author: Runkai Zhang
"""

from typing import Any, Dict, List, Optional

from app.schemas import AnimeHistoryItem, RecommendationMode
from app.services.mal_client import MALClient
from app.services.openai_client import OpenAIRecommendationClient


class RecommendationEngine:
    """
    Stateless orchestrator for anime recommendations.
    Combines MAL data with OpenAI-powered preference extraction and ranking.

    All state is passed in via anime_history parameter - no database required.
    """

    def __init__(
        self, mal_client: MALClient, openai_client: OpenAIRecommendationClient
    ):
        self.mal_client = mal_client
        self.openai_client = openai_client

    async def get_recommendation(
        self,
        anime_history: List[AnimeHistoryItem],
        mode: RecommendationMode = RecommendationMode.EXPLORE,
        exclude_ids: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a recommendation based on the selected mode.

        Modes:
        - similar: Find anime similar to what user already loves
        - explore: Discover new genres and expand horizons (default)

        This is completely stateless - all user data comes from anime_history parameter.

        Args:
            anime_history: Ordered list of anime the user has watched/rated (first = initial favorite)
            mode: Recommendation strategy (similar or explore)

        Returns:
            Dict containing:
                - recommendation: The recommended anime with explanation

        Raises:
            ValueError: If history is empty
        """
        if not anime_history:
            raise ValueError(
                "anime_history cannot be empty. Please provide at least one anime "
                "(your favorite anime should be the first item)."
            )

        # Convert Pydantic models to dicts for processing
        history_dicts = [self._history_item_to_dict(item) for item in anime_history]
        exclude_ids = exclude_ids or []
        seen_ids = [item.mal_id for item in anime_history]
        blocked_ids = seen_ids + [eid for eid in exclude_ids if eid not in seen_ids]

        # Gather diverse candidates from various sources
        candidates = await self._gather_diverse_candidates(history_dicts, blocked_ids)

        if not candidates:
            raise ValueError(
                "Could not find any new anime to recommend. Try expanding your history!"
            )

        # Use appropriate ranking strategy based on mode
        if mode == RecommendationMode.SIMILAR:
            recommendation = await self.openai_client.rank_for_similar(
                candidates=candidates,
                anime_history=history_dicts,
                seen_anime_ids=blocked_ids,
            )
        else:  # EXPLORE mode
            recommendation = await self.openai_client.rank_for_discovery(
                candidates=candidates,
                anime_history=history_dicts,
                seen_anime_ids=blocked_ids,
            )

        if not recommendation:
            raise ValueError("Could not generate recommendation. Please try again.")

        return {"recommendation": recommendation}

    async def _gather_diverse_candidates(
        self, history_dicts: List[Dict[str, Any]], seen_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """
        Gather diverse candidates prioritizing discovery over comfort zone.

        Mix of familiar (related to liked anime) and exploratory (different genres/themes).

        Args:
            history_dicts: User's anime history as dictionaries
            seen_ids: MAL IDs of anime the user has already seen

        Returns:
            Diverse list of candidate anime (up to 12)
        """
        candidates = []
        seen_ids_set = set(seen_ids)
        liked_anime = [h for h in history_dicts if h.get("user_rating") == "positive"]

        # Strategy 1: Familiar - recommendations from most recent liked anime (33%)
        if liked_anime:
            most_recent = liked_anime[-1]
            recs = await self.mal_client.get_anime_recommendations(
                most_recent["mal_id"], limit=4
            )
            for rec in recs:
                anime_id = rec.get("node", {}).get("id")
                if (
                    anime_id
                    and anime_id not in seen_ids_set
                    and not any(c["mal_id"] == anime_id for c in candidates)
                ):
                    details = await self.mal_client.get_anime_details(anime_id)
                    candidates.append(self.mal_client.extract_metadata(details))
                    if len(candidates) >= 4:
                        break

        # Strategy 2: Exploratory - high-rated anime from MAL rankings (67%)
        ranking = await self.mal_client.search_by_genre([], limit=12)
        for item in ranking:
            anime_id = item.get("node", {}).get("id")
            if (
                anime_id
                and anime_id not in seen_ids_set
                and not any(c["mal_id"] == anime_id for c in candidates)
            ):
                candidates.append(self.mal_client.extract_metadata(item))
                if len(candidates) >= 12:
                    break

        return candidates

    def _history_item_to_dict(self, item: AnimeHistoryItem) -> Dict[str, Any]:
        """
        Convert AnimeHistoryItem Pydantic model to dictionary.

        Args:
            item: AnimeHistoryItem from request

        Returns:
            Dictionary representation
        """
        return {
            "mal_id": item.mal_id,
            "title": item.title,
            "genres": item.genres,
            "studios": item.studios,
            "episodes": item.episodes,
            "score": item.score,
            "synopsis": item.synopsis,
            "media_type": item.media_type,
            "source": item.source,
            "watch_status": item.watch_status,
            "image_url": item.image_url,
            "rank": item.rank,
            "popularity": item.popularity,
            "user_seen": item.has_seen,
            "user_rating": item.rating.value if item.rating else None,
        }
