# Andela AI — Health App

A minimal healthcare consultation assistant: paste raw consultation notes, get back a structured summary, recommended next steps, and a patient-facing email. Inspired by the Ed Donner "AI in Production Udemy Course".

## Stack

- **Frontend**: Next.js 15 (App Router) + Clerk (auth UI, session tokens)
- **Backend**: FastAPI + `fastapi-clerk-auth` (JWT verification via Clerk JWKS)
- **LLM**: OpenRouter
- **Deployment**: Cloud Run (both services), Artifact Registry for images
- **CI/CD**: GitHub Actions → GCP via Workload Identity Federation

## Layout

```
backend/     FastAPI app, Dockerfile, pytest
frontend/    Next.js app, Dockerfile
.github/workflows/
  deploy-backend.yml
  deploy-frontend.yml
```

## Local development

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env   # then fill in real values
uvicorn app.main:app --reload --port 8080
pytest -q
```

**Frontend**

```bash
cd frontend
npm install
cp .env.local.example .env.local   # then fill in real values
npm run dev
```

Open http://localhost:3000, sign in, go to `/consult`, paste notes, hit Summarise.

## Deployment

Pushes to `main` trigger path-filtered GitHub Actions workflows. See `MANUAL_SETUP.md` for the one-time GCP + Clerk + GitHub setup.
