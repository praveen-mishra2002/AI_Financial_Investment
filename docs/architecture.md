# Architecture

```mermaid
flowchart LR
  UI[React Dashboard] --> API[FastAPI API]
  API --> Auth[JWT Auth]
  API --> Portfolio[Portfolio Service]
  API --> Reco[Recommendation Service]
  Reco --> Graph[LangGraph Supervisor]
  Graph --> Market[Market Agent]
  Graph --> Fundamental[Fundamental Agent]
  Graph --> Sentiment[Sentiment Agent]
  Graph --> Risk[Risk Agent]
  Graph --> Decision[Recommendation Agent]
  Graph --> Explain[Explainability Agent]
  API --> DB[(PostgreSQL)]
  Market --> Yahoo[Yahoo Finance]
  Sentiment --> OpenAI[OpenAI]
  Explain --> OpenAI
```

## Principles

- API routes coordinate only; business logic lives in services and agents.
- Recommendations are deterministic and auditable.
- LLMs explain recommendations; they do not choose actions.
- Market and sentiment failures degrade gracefully where possible.

## Data Model

Core tables:

- `users`
- `portfolios`
- `holdings`
- `recommendation_runs`
- `recommendations`
- `market_cache`
- `sentiment_cache`
- `portfolio_analysis_runs`
- `portfolio_analysis_results`
- `audit_logs`
