# Seer - Anime Recommendation System

**Author:** Runkai (Nico) Zhang  
**Course:** HCDE 310

A minimalistic anime recommendation system that encourages users to explore beyond their comfort zone. Seer combines MyAnimeList data with AI-powered personalization to help you discover anime you wouldn't normally find.

## 📺 Demo Video

[Link to demo video - 1-2 minutes]

### Philosophy

Seer is built on the principle that the best discoveries happen outside your comfort zone. Rather than reinforcing existing preferences, the system:
- Bridges your comfort zone with unexplored territory
- Actively promotes genre diversity
- Uses simple ratings to build nuanced understanding
- Keeps your data local and private

See the Philosophy page in the app for a detailed explanation of the recommendation approach.

## 🏗️ Architecture

This project consists of two main components:

### Frontend (`seer/`)
- **Framework:** SvelteKit 2.47 with Svelte 5
- **Language:** TypeScript 5.9
- **Styling:** TailwindCSS 4.1
- **Features:**
  - Anime search interface
  - AI-powered recommendation display
  - Watch history management
  - Philosophy page explaining the system
  - Local storage for privacy
  - Import/export functionality
  - Dark mode support

### Backend (`seer-api/`)
- **Framework:** FastAPI (Python)
- **APIs:** MyAnimeList API, OpenAI API
- **Architecture:** Completely stateless - no database
- **Features:**
  - Preference extraction from ratings
  - AI-powered candidate ranking
  - Recommendation explanations
  - Genre diversity encouragement

## 🚀 Quick Start Options

### Option 1: Railway Deployment

**Live Demo:** [Your Railway URL will be here after deployment]

The easiest way to test this application is via the deployed Railway instance. Simply visit the URL above - no setup required!

If you'd like to deploy your own instance:

1. **Fork/Clone this repository**

2. **Create a Railway account** at [railway.app](https://railway.app)

3. **Deploy to Railway:**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select this repository
   - Railway will automatically detect the configuration

4. **Set Environment Variables** in Railway dashboard:
   ```
   OPENAI_API_KEY=your_openai_api_key
   MAL_CLIENT_ID=your_mal_client_id
   ```

5. **Deploy!** Railway will:
   - Build the SvelteKit frontend
   - Install Python dependencies
   - Serve everything from a single URL

**Note:** The monorepo deployment serves both frontend and backend from one service. The backend serves the built SvelteKit app at the root path, and API endpoints are available at `/api/*`.

---

### Option 2: Local Development Setup

For local development and testing:

#### Prerequisites

- **Node.js 18+** (install pnpm: `npm install -g pnpm`)
- **Python 3.10+**
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **MyAnimeList Client ID** ([Register here](https://myanimelist.net/apiconfig))

#### Setup

```bash
# 1. Backend setup
cd seer-api
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and MAL_CLIENT_ID

# 2. Frontend setup (in a new terminal)
cd seer
pnpm install
```

#### Run Locally (Development Mode)

Start both servers in separate terminals:

```bash
# Terminal 1: Backend
cd seer-api && source venv/bin/activate && python run.py

# Terminal 2: Frontend
cd seer && pnpm run dev
```

Open `http://localhost:5173` in your browser.

#### Run Locally (Production Mode - Test Railway Build)

To test how the application will run on Railway:

```bash
# 1. Build the frontend
cd seer
pnpm install
pnpm run build

# 2. Start the backend (which serves the built frontend)
cd ../seer-api
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open `http://localhost:8000` in your browser.

### Getting API Keys

#### OpenAI API Key
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key to your `.env` file

**Note:** You'll need credits on your OpenAI account. The API uses GPT-5-Thinking.

#### MyAnimeList Client ID
1. Visit [MAL API Config](https://myanimelist.net/apiconfig)
2. Sign in to your MyAnimeList account
3. Click "Create ID"
4. Fill in:
   - App Name: "Seer Anime Recommendation"
   - App Type: "web"
   - Description: "Personal anime recommendation system"
   - Homepage URL: "http://localhost:8000"
   - Redirect URL: "http://localhost:8000/callback"
5. Copy your Client ID to your `.env` file


## 🔧 Configuration

### Backend Configuration (`.env`)

```env
# Required
OPENAI_API_KEY=your_openai_api_key
MAL_CLIENT_ID=your_mal_client_id

# Optional
OPENAI_MODEL=gpt-4-turbo-preview
MAX_CANDIDATES=10
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=False
```

### Frontend Configuration

If your backend runs on a different port, update `src/lib/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000/api';
```

## 🧪 Development

### API Documentation

- **Local Development:** `http://localhost:8000/docs`
- **Railway Deployment:** `https://your-railway-url.up.railway.app/docs`

## 📜 License

This project is created for educational purposes as part of HCDE 310.

## 🙏 Acknowledgments

- [MyAnimeList](https://myanimelist.net/)
- [OpenAI](https://openai.com/)
- [Svelte](https://svelte.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [TailwindCSS](https://tailwindcss.com/)
