# Developer Guide

## Backend

The backend follows a service and repository structure:

- `api/routes`: HTTP request and response boundaries.
- `services`: application workflows.
- `repositories`: database persistence.
- `agents`: investment-specific scoring and analysis.
- `graphs`: LangGraph orchestration.
- `models`: SQLAlchemy persistence models.
- `schemas`: Pydantic contracts.

Run tests:

```bash
cd backend
pytest
```

Run migrations:

```bash
cd backend
alembic upgrade head
```

## Frontend

The frontend is a React 18 Vite app using Material UI, React Router, React Query, Axios, and Recharts.

```bash
cd frontend
npm install
npm run dev
```

## Decision Governance

Thresholds:

- `85-100`: Strong Buy
- `70-84`: Buy
- `55-69`: Watch
- `40-54`: Hold
- `<40`: Sell

Score weights:

- Fundamental score: 40%
- Sentiment score: 10%
- Quality score: 35%
- Risk adjustment: 15%
