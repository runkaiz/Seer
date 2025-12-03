"""
Quick start script for the Anime Recommendation API.
Run this script to start the server with default settings.
"""
import uvicorn
from app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()

    print("=" * 60)
    print("🎌 Anime Recommendation API")
    print("=" * 60)
    print(f"Starting server on http://0.0.0.0:8000")
    print(f"API Documentation: http://localhost:8000/docs")
    print(f"Debug Mode: {settings.debug}")
    print("=" * 60)
    print("\nPress CTRL+C to stop the server\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )
