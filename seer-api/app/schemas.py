"""
Pydantic schemas for stateless API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class UserRatingEnum(str, Enum):
    """User rating options."""

    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class RecommendationMode(str, Enum):
    """Recommendation strategy mode."""

    SIMILAR = "similar"  # Find anime similar to what user likes
    EXPLORE = "explore"  # Discover new genres and expand horizons


class AnimeBase(BaseModel):
    """Base anime information."""

    mal_id: int
    title: str
    genres: List[str] = []
    studios: List[str] = []
    episodes: Optional[int] = None
    score: Optional[str] = None
    synopsis: Optional[str] = None
    media_type: Optional[str] = None
    source: Optional[str] = None
    watch_status: Optional[str] = None
    image_url: Optional[str] = None
    rank: Optional[int] = None
    popularity: Optional[int] = None


class AnimeHistoryItem(AnimeBase):
    """Represents an anime in the user's history with their rating."""

    has_seen: bool = Field(
        default=True, description="Whether the user has seen this anime"
    )
    rating: Optional[UserRatingEnum] = Field(
        None, description="User's rating (POSITIVE/NEUTRAL/NEGATIVE)"
    )


class AnimeRecommendation(AnimeBase):
    """Anime recommendation with explanation."""

    recommendation_reason: str = Field(
        ...,
        description="Why this anime was recommended - focusing on discovery and expanding horizons",
    )


class RecommendRequest(BaseModel):
    """Stateless request for anime recommendation.

    Client sends their full anime history (from their JSON save file).
    The history is ordered, with the first item being the initial/favorite anime.
    """

    anime_history: List[AnimeHistoryItem] = Field(
        ...,
        min_length=1,
        description="Ordered list of anime the user has watched/rated (first item = initial favorite)",
    )
    mode: RecommendationMode = Field(
        default=RecommendationMode.EXPLORE,
        description="Recommendation strategy: 'similar' for comfort zone, 'explore' for discovery (default)",
    )
    exclude_ids: List[int] = Field(
        default_factory=list,
        description="Optional list of MAL IDs to exclude (e.g., recently dismissed recommendations)",
    )


class RecommendResponse(BaseModel):
    """Stateless response containing recommendation.

    Client should save the recommendation to their JSON file and include it
    (with their rating) in the next request's anime_history.
    """

    recommendation: AnimeRecommendation


class ErrorResponse(BaseModel):
    """Error response schema."""

    """Error response schema."""
    error: str
    detail: Optional[str] = None
