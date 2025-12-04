"""
Stateless REST API endpoints for anime recommendations.

Author: Runkai Zhang
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.limiter import limiter
from app.schemas import (
    ErrorResponse,
    RecommendRequest,
    RecommendResponse,
)
from app.services import RecommendationEngine, get_mal_client, get_openai_client
from app.services.mal_client import MALClient
from app.services.openai_client import OpenAIRecommendationClient

router = APIRouter(prefix="/api", tags=["recommendations"])


def get_recommendation_engine(
    mal_client: MALClient = Depends(get_mal_client),
    openai_client: OpenAIRecommendationClient = Depends(get_openai_client),
) -> RecommendationEngine:
    """Dependency to get recommendation engine instance."""
    return RecommendationEngine(mal_client, openai_client)


@router.post(
    "/recommend",
    response_model=RecommendResponse,
    status_code=status.HTTP_200_OK,
    summary="Get anime recommendation (stateless)",
    description=(
        "Get a personalized anime recommendation based on your watch history. "
        "This is completely stateless - send your entire anime history from your "
        "JSON save file (ordered, with your favorite anime first), and receive a "
        "recommendation with extracted preferences."
    ),
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Anime not found or no candidates available",
        },
        422: {
            "model": ErrorResponse,
            "description": "anime_history is required and must contain at least one anime",
        },
        429: {
            "model": ErrorResponse,
            "description": "Rate limit exceeded - please try again later",
        },
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
@limiter.limit("100/hour")
async def recommend_anime(
    request: Request,
    body: RecommendRequest,
    engine: RecommendationEngine = Depends(get_recommendation_engine),
):
    """
    Get personalized anime recommendation (stateless).

    **Modes:**
    - `similar`: Find anime similar to what you already love (comfort zone)
    - `explore`: Discover new genres and expand horizons (default)

    **How it works:**
    1. Send your anime history (from your JSON save file) with ratings
    2. Choose your mode: similar or explore
    3. API finds candidates and uses AI to select the best match
    4. Save the recommendation to your JSON file and rate it
    5. Include the updated history in your next request

    **Example - Explore Mode (default):**
    ```json
    {
      "anime_history": [
        {
          "mal_id": 1,
          "title": "Cowboy Bebop",
          "genres": ["Action", "Sci-Fi"],
          "has_seen": true,
          "rating": "positive"
        }
      ],
      "mode": "explore"
    }
    ```

    **Example - Similar Mode:**
    ```json
    {
      "anime_history": [...],
      "mode": "similar"
    }
    ```

    **Optional Controls:**
    - `exclude_ids`: MAL IDs to skip (useful when a user dismisses a recommendation without rating it)

    **Note:** Minimum required fields per anime are `mal_id`, `title`, `has_seen`, and optionally `rating`.
    More complete metadata improves recommendation quality.

    **Rate Limits:** 20 recommendations per hour per IP address to prevent API abuse.
    """
    try:
        result = await engine.get_recommendation(
            anime_history=body.anime_history,
            mode=body.mode,
            exclude_ids=body.exclude_ids,
        )

        return RecommendResponse(recommendation=result["recommendation"])

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendation: {str(e)}",
        )


@router.get(
    "/search",
    summary="Search anime by title",
    description="Search for anime by title to bootstrap your history or find a specific anime.",
)
async def search_anime(
    query: str,
    limit: int = 5,
    mal_client: MALClient = Depends(get_mal_client),
):
    """
    Search for anime by title.

    **Parameters:**
    - query: Anime title to search for
    - limit: Maximum number of results (default: 5)

    **Returns:** List of anime search results with basic information.
    """
    try:
        results = await mal_client.search_anime(query, limit=limit)
        enriched_results = [mal_client.extract_metadata(result) for result in results]
        return {"results": enriched_results}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search anime: {str(e)}",
        )


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running and responsive.",
)
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "Anime Recommendation API (Stateless)",
        "version": "2.0",
    }
