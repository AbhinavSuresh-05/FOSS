# Cloud Deployment Guide (Free Tier)

This guide focuses on deploying your application to **Render.com**, which offers a generous free tier for both web services (backend) and static sites (frontend).

## Prerequisites
1.  **GitHub Account**: You must have your project pushed to a GitHub repository.
2.  **Render Account**: Sign up at [render.com](https://render.com).

## Part 1: Deploy Backend (Django)

1.  **Dashboard**: Go to your Render Dashboard and click **New +** -> **Web Service**.
2.  **Connect Repo**: Select your repository (you may need to configure permissions).
3.  **Settings**:
    *   **Name**: `chemical-backend` (or similar)
    *   **Root Directory**: `backend` (Important! This tells Render where your requirements.txt is)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `./build.sh`
    *   **Start Command**: `gunicorn config.wsgi:application`
    *   **Instance Type**: `Free`
4.  **Environment Variables** (Advanced):
    *   Add the following keys:
        *   `PYTHON_VERSION`: `3.11.9` (optional, but good for consistency)
        *   `SECRET_KEY`: (Generate a random string)
        *   `DEBUG`: `False`
        *   `ALLOWED_HOSTS`: `*` (or your Render URL once generated, e.g., `chemical-backend.onrender.com`)
        *   `CORS_ALLOWED_ORIGINS`: You will add your Frontend URL here later. For now, you can put different local hosts or wait.

5.  **Deploy**: Click "Create Web Service". Render will install dependencies and start the server.

## Part 2: Deploy Frontend (React/Vite)

1.  **Dashboard**: Click **New +** -> **Static Site**.
2.  **Connect Repo**: Select the same repository.
3.  **Settings**:
    *   **Name**: `chemical-frontend`
    *   **Root Directory**: `web-frontend`
    *   **Build Command**: `npm install && npm run build`
    *   **Publish Directory**: `dist`
4.  **Environment Variables**:
    *   `VITE_API_BASE_URL`: The URL of your backend from Part 1 (e.g., `https://chemical-backend.onrender.com/api`) **Note: Ensure /api is appended if your backend expects it, but usually the base URL is enough if your code handles the rest.** (Based on your code, it expects the base URL).
5.  **Deploy**: Click "Create Static Site".

## Part 3: Connect Them

1.  Copy your **Frontend URL** (e.g., `https://chemical-frontend.onrender.com`).
2.  Go back to your **Backend Service** settings > Environment Variables.
3.  Add/Update `CORS_ALLOWED_ORIGINS` with your frontend URL (no trailing slash).
    *   Example: `https://chemical-frontend.onrender.com`
4.  **Save Changes**: Render will restart the backend.

## Done!
Your application is now live on the web.
