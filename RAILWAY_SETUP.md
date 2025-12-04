# Railway Deployment Setup - Isolated Monorepo

This project uses Railway's **Isolated Monorepo** pattern with two separate services:
- **Backend** (Python/FastAPI) in `seer-api/`
- **Frontend** (Node.js/SvelteKit) in `seer/`

## Deployment Instructions

### Step 1: Create the Backend Service

1. Go to [railway.app](https://railway.app) and create a new project
2. Click **"Deploy from GitHub repo"** and select your repository
3. Railway will create a service - rename it to **"Backend"**
4. Go to **Settings** → **Root Directory** and set it to: `/seer-api`
5. The `seer-api/railway.json` configuration will be automatically detected
6. Add environment variables in the **Variables** tab:
   ```
   OPENAI_API_KEY=your_openai_api_key
   MAL_CLIENT_ID=your_mal_client_id
   ```
7. Deploy the backend service

### Step 2: Create the Frontend Service

1. In the same Railway project, click **"New Service"**
2. Select **"GitHub Repo"** and choose the same repository
3. Rename this service to **"Frontend"**
4. Go to **Settings** → **Root Directory** and set it to: `/seer`
5. The `seer/railway.json` configuration will be automatically detected
6. Deploy the frontend service

### Step 3: Configure Networking (if needed)

If your frontend needs to call the backend:
1. In the Backend service, go to **Settings** → **Networking**
2. Generate a public domain
3. Copy the domain URL (e.g., `https://backend-production.up.railway.app`)
4. In the Frontend service, add an environment variable:
   ```
   VITE_API_URL=https://backend-production.up.railway.app
   ```

### Step 4: Access Your Applications

- **Backend API**: `https://your-backend.up.railway.app`
- **Frontend**: `https://your-frontend.up.railway.app`
- **API Docs**: `https://your-backend.up.railway.app/docs`

## How It Works

Railway's Railpack builder will:

**For the Backend (`/seer-api`):**
- Detect `requirements.txt` and automatically install Python dependencies
- Use the start command from `railway.json`: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**For the Frontend (`/seer`):**
- Detect `pnpm-lock.yaml` and `packageManager` in `package.json`
- Automatically install dependencies with pnpm
- Build the SvelteKit application
- Serve the built application

## Configuration Files

- **Root `/railway.json`**: Legacy config (can be removed if not needed)
- **`/seer-api/railway.json`**: Backend-specific configuration
- **`/seer/railway.json`**: Frontend-specific configuration

## Why Separate Services?

According to [Railway's Monorepo Documentation](https://docs.railway.com/guides/monorepo), isolated monorepos with different tech stacks (Python + Node.js) should be deployed as separate services with different root directories. This approach:

- ✅ Allows each service to use its appropriate builder
- ✅ Enables independent scaling
- ✅ Provides better resource management
- ✅ Simplifies debugging and logs

## Alternative: Single Service Deployment

If you want to deploy as a single service (FastAPI serving the built frontend):

1. Use only the backend service
2. Set root directory to `/`
3. Add a custom build command:
   ```json
   {
     "build": {
       "buildCommand": "cd seer && pnpm install && pnpm run build && cd ../seer-api && pip install -r requirements.txt"
     }
   }
   ```
4. Make sure your FastAPI app serves the built frontend from `../seer/build/`

However, this approach is more complex and not recommended by Railway for isolated monorepos.

## Resources

- [Deploying a Monorepo | Railway Docs](https://docs.railway.com/guides/monorepo)
- [Deploy a FastAPI App | Railway Docs](https://docs.railway.com/guides/fastapi)
- [Build Configuration | Railway Docs](https://docs.railway.com/guides/build-configuration)
