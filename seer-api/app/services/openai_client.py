"""
OpenAI API client for preference extraction and recommendation ranking.
"""

import json
from typing import Any, Dict, List

from openai import AsyncOpenAI

from app.config import get_settings


class OpenAIRecommendationClient:
    """Client for using OpenAI to extract preferences and rank anime recommendations."""

    def __init__(self, api_key: str, model: str = "gpt-5-thinking"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def rank_for_similar(
        self,
        candidates: List[Dict[str, Any]],
        anime_history: List[Dict[str, Any]],
        seen_anime_ids: List[int],
    ) -> Dict[str, Any]:
        """
        Select a recommendation similar to what the user already enjoys.

        This mode stays within the user's comfort zone, finding anime with
        similar themes, genres, and appeal.

        Args:
            candidates: List of candidate anime
            anime_history: User's viewing history with ratings
            seen_anime_ids: List of MAL IDs the user has already seen

        Returns:
            Recommendation that matches user's established preferences
        """
        # Filter out already seen anime
        candidates = [c for c in candidates if c.get("mal_id") not in seen_anime_ids]

        if not candidates:
            return None

        # Get liked anime for pattern matching
        liked_anime = [h for h in anime_history if h.get("user_rating") == "positive"]

        # Format for prompt
        candidates_text = self._format_candidates(
            candidates[:20]
        )  # Increased from 12 to 20
        liked_text = self._build_history_context(
            liked_anime[-8:]
        )  # Increased from 3 to 8

        prompt = f"""You are an anime recommender finding similar anime to what the user loves.

What the User Loved:
{liked_text}

Available Candidates:
{candidates_text}

Your Mission:
Select ONE anime that closely matches what the user already enjoys. Find strong similarities in:
- Genre and themes
- Tone and atmosphere
- Character dynamics
- Story structure

This is "similar" mode - give them more of what they love!

Return JSON with:
- mal_id: Selected anime's MAL ID
- title: Anime title
- reason: 2 sentences explaining the similarities and why they'll love it

Return ONLY the JSON object."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at finding anime similar to what users already love.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,  # Lower temperature for more consistent/safe recommendations
            response_format={"type": "json_object"},
        )

        try:
            result = json.loads(response.choices[0].message.content)
            selected_anime = next(
                (c for c in candidates if c.get("mal_id") == result.get("mal_id")),
                candidates[0] if candidates else None,
            )

            if selected_anime:
                selected_anime["recommendation_reason"] = result.get(
                    "reason", "This anime is similar to what you've enjoyed."
                )
                return selected_anime
            return None
        except (json.JSONDecodeError, StopIteration):
            if candidates:
                candidates[0]["recommendation_reason"] = (
                    "This anime shares similarities with your favorites."
                )
                return candidates[0]
            return None

    async def rank_for_discovery(
        self,
        candidates: List[Dict[str, Any]],
        anime_history: List[Dict[str, Any]],
        seen_anime_ids: List[int],
    ) -> Dict[str, Any]:
        """
        Select a recommendation that encourages discovery and expanding horizons.

        Unlike Netflix-style algorithms that keep users in their comfort zone,
        this prioritizes introducing new perspectives, genres, and styles.

        Args:
            candidates: List of diverse candidate anime
            anime_history: User's viewing history with ratings
            seen_anime_ids: List of MAL IDs the user has already seen

        Returns:
            Recommendation that balances familiarity with discovery
        """
        # Filter out already seen anime
        candidates = [c for c in candidates if c.get("mal_id") not in seen_anime_ids]

        if not candidates:
            return None

        # Format for prompt
        candidates_text = self._format_candidates(
            candidates[:20]
        )  # Increased from 12 to 20
        history_text = self._build_history_context(
            anime_history[-10:]
        )  # Increased from 5 to 10

        prompt = f"""You are an anime curator focused on expanding horizons and discovery.

User's Recent History:
{history_text}

Available Candidates:
{candidates_text}

Your Mission:
Select ONE anime that will expand the user's horizons. This is NOT Netflix - we're not optimizing for retention or comfort zones.

Principles:
1. Introduce new genres/themes they haven't explored much
2. Balance challenge with accessibility (not too jarring)
3. Recommend critically acclaimed works they might have missed
4. Encourage breaking out of patterns

Avoid:
- Safe, predictable choices that match their exact preferences
- Only recommending what they already like
- Echo chamber recommendations

Return JSON with:
- mal_id: Selected anime's MAL ID
- title: Anime title
- reason: 2-3 sentences explaining why this expands their horizons (be specific about what's new/different)

Return ONLY the JSON object."""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a curator helping users discover great anime beyond their comfort zone.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,  # Higher temperature for more creative recommendations
            response_format={"type": "json_object"},
        )

        try:
            result = json.loads(response.choices[0].message.content)
            selected_anime = next(
                (c for c in candidates if c.get("mal_id") == result.get("mal_id")),
                candidates[0] if candidates else None,
            )

            if selected_anime:
                selected_anime["recommendation_reason"] = result.get(
                    "reason", "This anime will introduce you to new perspectives."
                )
                return selected_anime
            return None
        except (json.JSONDecodeError, StopIteration):
            if candidates:
                candidates[0]["recommendation_reason"] = (
                    "This critically acclaimed anime will expand your horizons."
                )
                return candidates[0]
            return None

    def _build_history_context(self, anime_history: List[Dict[str, Any]]) -> str:
        """Build a text summary of anime history for prompts."""
        if not anime_history:
            return "No history yet."

        lines = [
            self._summarize_anime(
                anime,
                prefix="- ",
                include_user_context=True,
                include_synopsis=True,
            )
            for anime in anime_history
        ]

        return "\n".join(lines)

    def _format_candidates(self, candidates: List[Dict[str, Any]]) -> str:
        """Format candidate anime for inclusion in prompts."""
        lines = [
            self._summarize_anime(
                anime,
                prefix=f"{i}. ",
                include_synopsis=True,
            )
            for i, anime in enumerate(candidates, 1)
        ]

        return "\n".join(lines)

    def _summarize_anime(
        self,
        anime: Dict[str, Any],
        prefix: str = "- ",
        include_user_context: bool = False,
        include_synopsis: bool = False,
    ) -> str:
        """Create a rich summary block for an anime entry."""
        title = anime.get("title", "Unknown")
        mal_id = anime.get("mal_id")
        header = f"{prefix}{title}"
        if mal_id:
            header += f" (MAL ID: {mal_id})"

        lines = [header]

        if anime.get("genres"):
            lines.append(f"   Genres: {', '.join(anime['genres'])}")
        if anime.get("studios"):
            lines.append(f"   Studios: {', '.join(anime['studios'])}")

        meta_parts = []
        if anime.get("media_type"):
            meta_parts.append(f"Format: {anime['media_type']}")
        if anime.get("episodes"):
            meta_parts.append(f"Episodes: {anime['episodes']}")
        if anime.get("score"):
            meta_parts.append(f"MAL Score: {anime['score']}")
        if anime.get("source"):
            meta_parts.append(f"Source: {anime['source']}")
        if anime.get("rating"):
            meta_parts.append(f"Content Rating: {anime['rating']}")
        if meta_parts:
            lines.append("   " + " | ".join(meta_parts))

        if include_user_context:
            user_parts = []
            if anime.get("user_seen") is not None:
                user_parts.append("Seen" if anime.get("user_seen") else "Not seen")
            if anime.get("watch_status"):
                user_parts.append(f"Watch Status: {anime['watch_status']}")
            if anime.get("user_rating"):
                user_parts.append(f"User Rating: {anime['user_rating']}")
            if user_parts:
                lines.append("   " + " | ".join(user_parts))

        if include_synopsis and anime.get("synopsis"):
            synopsis = anime["synopsis"].strip().replace("\n", " ")
            lines.append(f"   Synopsis: {synopsis[:200]}...")

        return "\n".join(lines)


def get_openai_client() -> OpenAIRecommendationClient:
    """Get OpenAI client instance with configured credentials."""
    settings = get_settings()
    return OpenAIRecommendationClient(
        api_key=settings.openai_api_key, model=settings.openai_model
    )
