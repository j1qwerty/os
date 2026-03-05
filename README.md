# WorldView Intelligence Platform (Full-Stack Feature Build)

This app now includes a backend + frontend foundation implementing core pieces of a multi-domain situational awareness workflow.

## Implemented capabilities

- Provider catalog and key management checklist (140-source catalog + env var contract).
- Live mode telemetry stream via WebSocket.
- Recorded mode telemetry playback API with time-window + bbox + domain filters.
- Layer toggles and feature configuration endpoint.
- Intelligence records feed.
- News synthesis endpoint (rule-based placeholder for LLM orchestration).
- MGRS-style coordinate endpoint (placeholder conversion).
- Tactical HUD-style dashboard inspired by WorldView mockups, including live/playback pills, side control panels, globe-stage telemetry pings, timeline controls, and synthesis form.

## API endpoints
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
- `POST /api/v1/telemetry/playback`
- `GET /api/v1/telemetry/live`
- `GET /api/v1/telemetry/default-window`
- `GET /api/v1/intelligence/records`
- `POST /api/v1/intelligence/synthesize`
- `GET /api/v1/features`
- `GET /api/v1/geo/mgrs?lat=<>&lon=<>`
- `WS /api/v1/ws/live`

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
- Dashboard: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## Important production notes

Current implementation uses mock in-memory telemetry/intelligence data and rule-based synthesis. Replace with:
- ingestion workers for OpenSky/ADSBExchange/AISStream/Space-Track/GDELT,
- ClickHouse or PostGIS persistence,
- OpenRouter/OpenAI orchestration for synthesis,
- robust MGRS conversion library,
- authentication/RBAC/auditing.
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## Next implementation step

This full scaffold is ready for adding real ingestion workers (ADS-B, AIS, TLE propagation, GDELT polling) and persistence layers (ClickHouse/PostGIS + Redis).
