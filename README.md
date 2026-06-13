# AI Investment Copilot

AI Investment Copilot is a local-first investment research and portfolio decision-support platform for Indian equities. It implements deterministic scoring, auditable recommendation runs, portfolio analysis, and AI-generated explanations that never decide the investment action.

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs

## Local Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Local Frontend

```bash
cd frontend
npm install
npm run dev
```

## Governance

Recommendations are produced from deterministic agent outputs:

- Fundamentals and quality are the primary drivers.
- Sentiment can influence but cannot override fundamentals.
- LLM output is limited to narrative explanation.
- Recommendation inputs, scores, decisions, model version, prompt version, and timestamps are persisted for auditability.

This platform does not execute trades.
