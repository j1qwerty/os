# WorldView Intelligence Platform (Full App Scaffold)

This repository now contains a **backend + frontend application** for a multi-domain OSINT intelligence catalog.

## Features

- FastAPI backend with versioned REST endpoints.
- Browser dashboard frontend served by FastAPI.
- Cross-domain provider registry with auth model + required env var metadata.
- Required API-key checklist endpoint and generated `.env.example`.

## Backend API

- `GET /api/v1/health`
- `GET /api/v1/providers?domain=<domain>&free_tier=<true|false>`
- `GET /api/v1/providers/required-keys`
- `GET /api/v1/domains/summary`

## Frontend

- `GET /` serves a dashboard that:
  - lists providers,
  - supports filtering by domain/free-tier,
  - shows per-domain stats,
  - displays all required env vars.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src uvicorn worldview.main:app --reload
```

Open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## Next implementation step

This full scaffold is ready for adding real ingestion workers (ADS-B, AIS, TLE propagation, GDELT polling) and persistence layers (ClickHouse/PostGIS + Redis).
