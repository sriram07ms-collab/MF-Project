# Facts-Only MF Assistant – Backend

FastAPI microservice that powers the Nippon Paint branded FAQ chatbot. It ingests official AMC web pages, stores embeddings locally, and exposes a `/query` endpoint that returns concise, citation-backed answers.

## Prerequisites

- Python 3.11+
- pip

## Setup

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate  # PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file (optional) to override defaults in `app/config.py`.

## Ingestion

```bash
cd backend
python -m app.ingest
```

This fetches the three Nippon India AMC scheme pages, extracts factual snippets, builds embeddings, and stores them under `data/`.

## Run API

```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /health`
- `POST /query { "question": "What is the exit load on Nippon India Large Cap Fund?" }`
- `POST /admin/reindex` (no auth in prototype; wire auth before production)


