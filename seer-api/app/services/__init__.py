"""
Services package for anime recommendation system.
"""
from app.services.mal_client import MALClient, get_mal_client
from app.services.openai_client import OpenAIRecommendationClient, get_openai_client
from app.services.recommendation import RecommendationEngine

__all__ = [
    "MALClient",
    "get_mal_client",
    "OpenAIRecommendationClient",
    "get_openai_client",
    "RecommendationEngine",
]
