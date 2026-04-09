# SignalRoom

SignalRoom ingests culture signals from Reddit + RSS, clusters conversations into emerging “signals,” tracks momentum over time, and generates concise insight briefs + campaign ideas using LLMs.

**Live demo** (may take 30=60s to wake up on free tier)

- Frontend: 'signal-room.vercel.app'
- Backend API: '<https://signal-room.onrender.com>'

---

## Features

- **Reddit + RSS ingestion** – Hot posts from subreddits and    entries from RSS feeds.

- **Automatic clustering** – Groups related posts using TF‑IDF + KMeans.

- **Momentum scoring** – Trending strength based on recency and engagement.

- **AI briefs** – Generates summaries and marketing insights using OpenAI gpt-4o-mini.

- **Minimal dashboard** – Clean Next.js UI to explore signals and trigger ingestion.

---

## Tech Stack

| Layer       | Technology                                                                 |
|-------------|----------------------------------------------------------------------------|
| Backend     | FastAPI, SQLAlchemy, SQLite, PRAW, feedparser, scikit‑learn, OpenAI API    |
| Frontend    | Next.js 14 (App Router), TypeScript, Tailwind CSS, Axios                   |
| Deployment  | **Render** (backend), **Vercel** (frontend)                                |

---

## Deployment on Render + Vercel

### 1. Backend (Render)

1. Push your code to a GitHub repository.
2. On [Render](https://render.com), create a new **Web Service**.
3. Connect your repo and set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add the following environment variables (see table below).
5. Click **Create Web Service** – Render will automatically deploy.

### 2. Frontend (Vercel)

1. On [Vercel](https://vercel.com), import the same GitHub repository.
2. Set **Root Directory** to `frontend` (if your repo has both backend and frontend in one).
3. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = your Render backend URL (e.g., `https://signal-room.onrender.com/api`)
4. Deploy – Vercel will build and host the frontend.

> **Note**: Because both services run on free tiers, the backend may take 30‑60 seconds to wake up after inactivity. The frontend will load instantly, but the first API call will be slow.

---

## Environment Variables

### Backend (on Render)

| Variable               | Description                                         | Example / Default                        |
|------------------------|-----------------------------------------------------|------------------------------------------|
| `APP_NAME`             | Application name                                    | `SignalRoom`                             |
| `DEBUG`                | FastAPI debug mode                                  | `False`                                  |
| `DATABASE_URL`         | SQLite or PostgreSQL URL                            | `sqlite:///./signalroom.db`              |
| `OPENAI_API_KEY`       | Your OpenAI API key                                 | `sk-...`                                 |
| `OPENAI_MODEL`         | Model for brief generation                          | `gpt-4o-mini`                            |
| `AI_MODE`              | `live` or `mock` (mock for testing)                 | `live`                                   |
| `EMBEDDINGS_MODE`      | (optional) Embedding mode                           | `openai` or `mock`                       |
| `REDDIT_CLIENT_ID`     | Reddit app client ID                                | from reddit.com/prefs/apps               |
| `REDDIT_CLIENT_SECRET` | Reddit app secret                                   | from reddit.com/prefs/apps               |
| `REDDIT_USER_AGENT`    | User agent string for Reddit API                    | `SignalRoom/1.0`                         |
| `RSS_FEEDS`            | Comma‑separated RSS feed URLs                       | `https://feeds.npr.org/1001/rss.xml`     |
| `PORT`                 | Render sets this automatically – do not change      | (Render manages)                         |

### Frontend (on Vercel)

| Variable                  | Description                          | Example                                      |
|---------------------------|--------------------------------------|----------------------------------------------|
| `NEXT_PUBLIC_API_URL`     | Backend API base URL (with `/api`)   | `https://signal-room.onrender.com/api`       |

---

## 📡 API Endpoints (available after deployment)

| Method | Endpoint                     | Description                          |
|--------|------------------------------|--------------------------------------|
| POST   | `/api/ingest/run`            | Trigger ingestion + clustering       |
| GET    | `/api/clusters/`             | List all clusters (by momentum)      |
| GET    | `/api/clusters/{id}`         | Get cluster details + its items      |
| POST   | `/api/clusters/{id}/brief`   | Generate AI brief for a cluster      |

> You can test the API directly via the interactive docs at `https://signal-room.onrender.com/docs`.

---

## 🧠 AI Brief Generation

- Uses **OpenAI `gpt-4o-mini`** (as configured in `OPENAI_MODEL`).
- Prompt asks for a 2‑3 sentence summary and three bullet points with actionable marketing insights.
- If `AI_MODE=mock`, it returns placeholder text without calling OpenAI (useful for testing).

---

## 📁 Local Development (optional)

If you want to run the project locally instead of deploying:

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -c "from app.db.database import init_db; init_db()"
python run.py

# Frontend (new terminal)
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
npm run dev
