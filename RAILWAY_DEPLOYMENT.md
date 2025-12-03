# Railway Deployment Guide

**Author:** Runkai Zhang  
**Project:** Seer - Anime Recommendation System

This guide provides step-by-step instructions for deploying the Seer application to Railway.

## What is Railway?

Railway is a modern deployment platform that simplifies deploying web applications. This project is configured for a **monorepo deployment** - both the frontend (SvelteKit) and backend (FastAPI) are deployed as a single service.

## Prerequisites

1. A GitHub account
2. A Railway account ([Sign up here](https://railway.app))
3. Your code pushed to a GitHub repository
4. API keys:
   - OpenAI API Key ([Get one](https://platform.openai.com/api-keys))
   - MyAnimeList Client ID ([Get one](https://myanimelist.net/apiconfig))

## Deployment Steps

### Step 1: Push Your Code to GitHub

```bash
# If you haven't already initialized git
git init
git add .
git commit -m "Initial commit"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main
```

### Step 2: Create a Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"Login"** and sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Authorize Railway to access your GitHub repositories
6. Select your repository from the list

### Step 3: Configure the Deployment

Railway should automatically detect the Python project and use the configuration from `railway.json` and `Procfile`.

**Verify the settings:**
- **Root Directory:** Should be `/` (the repository root)
- **Build Command:** Should use the command from `railway.json`:
  ```bash
  cd seer && pnpm install && pnpm run build && cd ../seer-api && pip install -r requirements.txt
  ```
- **Start Command:** Should use the command from `Procfile`:
  ```bash
  cd seer-api && uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

### Step 4: Add Environment Variables

In your Railway project dashboard:

1. Click on your service
2. Go to the **"Variables"** tab
3. Click **"New Variable"** and add:

```
OPENAI_API_KEY=your_actual_openai_key
MAL_CLIENT_ID=your_actual_mal_client_id
```

Optional variables (with defaults):
```
DEBUG=False
OPENAI_MODEL=gpt-4-turbo-preview
MAX_CANDIDATES=10
```

**Important:** Don't include quotes around the values.

### Step 5: Deploy

1. Railway will automatically trigger a deployment after you add the environment variables
2. Watch the **"Deployments"** tab for build progress
3. The build process will:
   - Install Node.js dependencies
   - Build the SvelteKit frontend
   - Install Python dependencies
   - Start the FastAPI server

### Step 6: Get Your URL

1. Once deployed, go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"** if not already generated
4. Your app will be available at: `https://your-app-name.up.railway.app`

### Step 7: Test Your Deployment

Visit your Railway URL and test:
1. ✅ Frontend loads correctly
2. ✅ Anime search works (tests MAL API)
3. ✅ Recommendations work (tests OpenAI API)
4. ✅ Watchlist functionality works (local storage)

### Step 8: Update README

Update the README.md with your deployed URL:

```markdown
**Live Demo:** https://your-app-name.up.railway.app
```

## How It Works

### Monorepo Deployment Architecture

```
Railway Build Process:
1. Install pnpm and Node.js dependencies
2. Build SvelteKit frontend → creates seer/build/
3. Install Python dependencies
4. Start FastAPI server

Runtime:
- FastAPI serves at 0.0.0.0:$PORT
- API endpoints available at /api/*
- Built frontend served at / (root)
- Single URL for everything!
```

### File Structure

```
.
├── Procfile              # Tells Railway how to start the app
├── railway.json          # Build and deploy configuration
├── .dockerignore         # Files to ignore during deployment
├── seer/                 # Frontend
│   └── build/           # Generated during deployment
└── seer-api/            # Backend
    └── app/
        └── main.py      # Serves both API and frontend
```

## Troubleshooting

### Build Fails

**Problem:** `pnpm: command not found`
- Railway should auto-detect and install pnpm
- Check that `railway.json` is in the repository root

**Problem:** `No module named 'app'`
- Ensure the start command includes `cd seer-api`
- Check that `requirements.txt` is in `seer-api/`

### Runtime Errors

**Problem:** API endpoints return 404
- Verify environment variables are set
- Check Railway logs in the **"Deployments"** tab

**Problem:** Frontend shows blank page
- Ensure frontend built successfully (check build logs)
- Verify `seer/build/` directory exists after build

**Problem:** Recommendations don't work
- Check that `OPENAI_API_KEY` is set correctly
- Verify you have credits in your OpenAI account
- Check Railway logs for error messages

### Environment Variables

**Problem:** Variables not loading
- Don't use quotes around values in Railway dashboard
- Redeploy after adding variables (click **"Redeploy"**)

## Updating Your Deployment

To deploy changes:

```bash
# Make your changes locally
git add .
git commit -m "Description of changes"
git push

# Railway will automatically detect and redeploy
```

## Cost Considerations

- **Railway Free Tier:** $5 of usage credit per month
- This project is lightweight and should fit within free tier limits
- Monitor usage in Railway dashboard
- Consider pausing the service when not in use (for development/testing)

## Local Testing (Production Mode)

Before deploying, test the production build locally:

```bash
# Build frontend
cd seer
pnpm install
pnpm run build

# Run backend (serves built frontend)
cd ../seer-api
source venv/bin/activate
python run.py
```

Visit `http://localhost:8000` - this simulates the Railway deployment.

## API Documentation

Your FastAPI documentation is available at:
- **Local:** `http://localhost:8000/docs`
- **Railway:** `https://your-app-name.up.railway.app/docs`

## Support

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **Project Issues:** [Your GitHub repo]/issues

---

**Note for TAs/Professors:** The live Railway deployment is the easiest way to test this project - just visit the URL, no local setup required!
