# sanctra-rag-service

FastAPI wrapper for Vertex AI Vector Search.

Endpoints
- POST /index  -> upsert items {id, person_id, title, text, tags}
- POST /search -> {person_id, query, k} returns top-k using MMR
All results are strictly filtered by person_id.

## Quickstart
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install uv
uv pip compile pyproject.toml -o requirements.txt
uv pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8082 --reload

## Auth
Cloud Run: use Workload Identity.
Local: set GOOGLE_APPLICATION_CREDENTIALS or provide base64 JSON in GCP_SA_JSON_B64.

## Config (env)
- GCP_PROJECT
- GCP_LOCATION               (e.g., us-central1)
- VERTEX_INDEX_ID            (Matching Engine index id)
- VERTEX_EMBED_MODEL         (e.g., textembedding-gecko@003)
- GCP_SA_JSON_B64            (optional; base64-encoded service account JSON for local/dev)
