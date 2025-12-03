"""
MyAnimeList API client for fetching anime data.
Official API documentation: https://myanimelist.net/apiconfig/references/api/v2
"""
import httpx
from typing import Optional, List, Dict, Any
from app.config import get_settings


class MALClient:
    """Client for interacting with the MyAnimeList API."""

    BASE_URL = "https://api.myanimelist.net/v2"

    def __init__(self, client_id: str):
        self.client_id = client_id
        self.headers = {
            "X-MAL-CLIENT-ID": client_id
        }

    async def search_anime(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for anime by title.

        Args:
            query: Search query (anime title)
            limit: Maximum number of results to return

        Returns:
            List of anime search results
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/anime",
                headers=self.headers,
                params={
                    "q": query,
                    "limit": limit,
                    "fields": "id,title,main_picture,alternative_titles"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])

    async def get_anime_details(self, anime_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific anime.

        Args:
            anime_id: MAL anime ID

        Returns:
            Detailed anime information including genres, studios, etc.
        """
        fields = [
            "id",
            "title",
            "main_picture",
            "alternative_titles",
            "synopsis",
            "mean",
            "rank",
            "popularity",
            "num_list_users",
            "num_scoring_users",
            "media_type",
            "status",
            "genres",
            "num_episodes",
            "start_season",
            "source",
            "average_episode_duration",
            "rating",
            "studios",
            "related_anime",
            "recommendations",
            "statistics"
        ]

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/anime/{anime_id}",
                headers=self.headers,
                params={"fields": ",".join(fields)},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    async def get_anime_recommendations(self, anime_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get MAL's recommended anime for a given anime.

        Args:
            anime_id: MAL anime ID
            limit: Maximum number of recommendations

        Returns:
            List of recommended anime
        """
        anime_details = await self.get_anime_details(anime_id)
        if not anime_details:
            return []

        recommendations = anime_details.get("recommendations", [])[:limit]
        return recommendations

    async def search_by_genre(
        self,
        genre_ids: List[int],
        limit: int = 10,
        min_score: float = 7.0
    ) -> List[Dict[str, Any]]:
        """
        Search for anime by genre.
        Note: The MAL API v2 doesn't directly support genre filtering in search,
        so this is a simplified implementation that would need enhancement.

        Args:
            genre_ids: List of genre IDs to filter by
            limit: Maximum number of results
            min_score: Minimum score threshold

        Returns:
            List of anime matching criteria
        """
        # This is a placeholder - MAL API v2 has limited filtering capabilities
        # In a production system, you'd want to fetch ranking lists and filter
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/anime/ranking",
                headers=self.headers,
                params={
                    "ranking_type": "all",
                    "limit": limit * 2,  # Fetch more to filter
                    "fields": "id,title,mean,genres,num_episodes,synopsis,studios"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])[:limit]

    def extract_metadata(self, anime_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and normalize metadata from MAL anime data.

        Args:
            anime_data: Raw anime data from MAL API

        Returns:
            Normalized metadata dictionary
        """
        # Handle both search results and detailed anime objects
        if "node" in anime_data:
            anime_data = anime_data["node"]

        return {
            "mal_id": anime_data.get("id"),
            "title": anime_data.get("title", ""),
            "genres": [g.get("name", "") for g in anime_data.get("genres", [])],
            "studios": [s.get("name", "") for s in anime_data.get("studios", [])],
            "episodes": anime_data.get("num_episodes"),
            "score": str(anime_data.get("mean", "N/A")) if anime_data.get("mean") else "N/A",
            "synopsis": anime_data.get("synopsis", ""),
            "media_type": anime_data.get("media_type", ""),
            "rating": anime_data.get("rating", ""),
            "source": anime_data.get("source", ""),
        }


def get_mal_client() -> MALClient:
    """Get MAL client instance with configured credentials."""
    settings = get_settings()
    return MALClient(client_id=settings.mal_client_id)
