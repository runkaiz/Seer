# Seer - Anime Recommendation System

**Author:** Runkai (Nico) Zhang  
**Course:** HCDE 310

A minimalistic anime recommendation system that encourages users to explore beyond their comfort zone. Seer combines MyAnimeList data with AI-powered personalization to help you discover anime you wouldn't normally find.

## Philosophy

Rather than reinforcing existing preferences, Seer bridges your comfort zone with unexplored territory by actively promoting genre diversity. It uses simple ratings to build nuanced understanding while keeping your data local and private.

## Architecture

- **Frontend:** SvelteKit 5 + TypeScript + TailwindCSS
- **Backend:** FastAPI (Python) - Stateless, no database
- **APIs:** MyAnimeList API, OpenAI API

## Local Setup

### Prerequisites

- Node.js 18+ (with pnpm: `npm install -g pnpm`)
- Python 3.10+
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [MyAnimeList Client ID](https://myanimelist.net/apiconfig)

### Installation

```bash
# Backend
cd seer-api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: add OPENAI_API_KEY and MAL_CLIENT_ID

# Frontend (new terminal)
cd seer
pnpm install
```

### Run

```bash
# Terminal 1: Backend
cd seer-api && source venv/bin/activate && python run.py

# Terminal 2: Frontend  
cd seer && pnpm run dev
```

Open `http://localhost:5173`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.
