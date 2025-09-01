# Kamal AI Trading — Pro Setup (Intraday + Delivery)

**Goal:** user-friendly, high-clarity trading toolkit with AI-assisted flows.

## Quick Start
```
python -m venv .venv
. .venv/Scripts/activate      # PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env        # then edit .env
uvicorn app.main:app --reload
```

## Structure
- `app/` — FastAPI service (friend-like chat endpoint)
- `trading_strategies/` — `intraday.py`, `delivery.py`
- `config/settings.yaml` — central config; `.env.example` for secrets
- other modules from your project are preserved
- `STRUCTURE-TREE.txt` — full file list
