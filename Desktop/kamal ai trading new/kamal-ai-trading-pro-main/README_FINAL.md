
# Kamal AI Trading — Ready-to-Launch (Ultimate)

## What's included
- Full application code (strategies, backtesting, order execution, risk, AI agent)
- AI extension (models, LLM adapter, decision maker, AutoTradeAgent)
- In-process EventBus and typed events
- Paper broker adapter for safe testing
- FastAPI control service (kill-switch + metrics)
- Dockerfile and docker-compose (includes Prometheus and Grafana)
- .env.example for required env vars
- CI workflow (lint + tests)
- LICENSE (MIT)

## Quick start (local, docker)
1. Copy `.env.example` to `.env` and fill secrets.
2. Build & run with docker-compose:
    docker-compose up --build -d
3. App will be available at http://localhost:8000
   Prometheus at http://localhost:9090
   Grafana at http://localhost:3000  (admin/admin)

## Kill switch (fast action)
- To disable trading:
    curl -X POST -H "X-Token: <KILL_SWITCH_TOKEN>" http://localhost:8000/kill
- To enable:
    curl -X POST -H "X-Token: <KILL_SWITCH_TOKEN>" http://localhost:8000/revive

## Notes
- Always run in paper mode until you are confident. Do not use real keys in the repo.
- Add monitoring dashboards and alerts in Grafana.
