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

## 🚀 Getting Started

### Prerequisites

- **Node.js 18+** or **pnpm** (for frontend)
- **Python 3.10+** (for backend)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **MyAnimeList Client ID** ([Register here](https://myanimelist.net/apiconfig))

### Quick Setup

#### 1. Clone the Repository

```bash
git clone [your-repo-url]
cd "HCDE 310 Final"
```

#### 2. Backend Setup

```bash
cd seer-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# OPENAI_API_KEY=your_key_here
# MAL_CLIENT_ID=your_client_id_here

# Start the backend
python run.py
```

The API will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
cd seer

# Install dependencies
pnpm install

# Start development server
pnpm run dev
```

The app will be available at `http://localhost:5173`

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

### Frontend Development

```bash
cd seer

# Test with a live server
pnpm dev
```

### Backend Development

```bash
cd seer-api

# Run with auto-reload
python run.py

# View API docs
# Visit http://localhost:8000/docs
```

## 📜 License

This project is created for educational purposes as part of HCDE 310.

## 🙏 Acknowledgments

- [MyAnimeList](https://myanimelist.net/)
- [OpenAI](https://openai.com/)
- [Svelte](https://svelte.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [TailwindCSS](https://tailwindcss.com/)
