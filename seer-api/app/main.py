"""
Main FastAPI application entry point.

Author: Runkai Zhang
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

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


@app.get("/api", tags=["root"])
async def root():
    """API root endpoint with information."""
    return {
        "message": "Welcome to the Anime Recommendation API (Stateless)",
        "version": "2.0.0",
        "description": "No accounts needed - manage your recommendations with a local JSON file!",
        "docs": "/docs",
        "health": "/api/health",
        "main_endpoint": "/api/recommend",
    }


# Serve SvelteKit frontend (built files)
# In production, the frontend should be built and available in ../seer/build
frontend_build_dir = Path(__file__).parent.parent.parent / "seer" / "build"

if frontend_build_dir.exists():
    # Mount static files for assets
    app.mount(
        "/", StaticFiles(directory=str(frontend_build_dir), html=True), name="frontend"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)
