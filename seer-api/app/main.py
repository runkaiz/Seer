"""
Main FastAPI application entry point.

Author: Runkai Zhang
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import recommendations

settings = get_settings()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=(
        "A stateless anime recommendation API powered by MyAnimeList and OpenAI. "
        "No accounts needed - manage your recommendations with a local JSON file!"
    ),
    version="2.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Anime Recommendation API (Stateless)",
        "version": "2.0.0",
        "description": "No accounts needed - manage your recommendations with a local JSON file!",
        "docs": "/docs",
        "health": "/api/health",
        "main_endpoint": "/api/recommend"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
