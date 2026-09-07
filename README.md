# BrewMatch

Coffee recommender with a quiz, journal, and personalized drink suggestions.

## Repo layout

- `frontend/` — Next.js app (TypeScript, Tailwind). Deployed on Vercel.
- `backend/` — FastAPI API + PostgreSQL. Deployed on Render.
- `.github/workflows/` — CI, then deploy on push to `main`.

## Local setup

**API** (from `backend/`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit DATABASE_URL if needed
uvicorn main:app --reload --port 8000
```

Postgres should be running locally (`DATABASE_URL` in `backend/.env`).

**Web app** (from `frontend/`):

```bash
npm ci
cp .env.example .env.local
npm run dev
```

Open http://localhost:3000. The frontend expects the API at http://localhost:8000 unless you change `NEXT_PUBLIC_API_URL`.
