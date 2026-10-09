# AgriWater AI

AgriWater AI is a responsive agricultural decision-support application that combines a public-facing evaporation prediction workflow with specialist and administrator workspaces.

## Stack

- Frontend: React + Vite + TypeScript + Tailwind CSS
- Backend: FastAPI + SQLAlchemy + Pydantic
- Database: SQLite by default for local development, configurable MySQL for production
- Auth: JWT + secure password hashing
- ML: mock provider by default with a replaceable sklearn adapter interface

## Local setup

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m pytest
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Default admin bootstrap

```bash
curl -X POST "http://localhost:8000/api/v1/auth/bootstrap-admin?email=admin@example.com&password=StrongPass!123&full_name=Admin+User"
```

## Features

- Public evaporation prediction form
- Crop recommendation and crop-water calculator
- Mock provider architecture ready for real sklearn inference
- Specialist and admin protected routes
- SQLite default for local development, MySQL configuration supported via env vars

## Important note

The mock evaporation provider is intentionally labeled as demo output. Real model integration requires configuring `EVAPORATION_PROVIDER=sklearn`, setting `EVAPORATION_MODEL_PATH`, and ensuring the artifact matches the preprocessing and feature ordering used during training.
