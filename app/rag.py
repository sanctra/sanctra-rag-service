import os
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

PROJECT = os.getenv("GCP_PROJECT","sanctra-prod")
LOCATION = os.getenv("GCP_LOCATION","us-central1")
EMBED_MODEL = os.getenv("VERTEX_EMBED_MODEL","textembedding-gecko@003")
INDEX_ID = os.getenv("VERTEX_INDEX_ID","changeme")

router = APIRouter()

class UpsertItem(BaseModel):
  id: str
  person_id: str
  text: str
  title: str | None = None
  tags: List[str] = []

class SearchReq(BaseModel):
  person_id: str
  query: str
  k: int = 8

# NOTE: In production, use the official client to embed and upsert to Vertex Vector Search.
# Below keeps API shape stable until the index is ready.

@router.post("/index")
def upsert(items: List[UpsertItem]):
  # TODO: call embeddings for each text -> vectors, then upsert to index
  return {"upserted": len(items)}

@router.post("/search")
def search(req: SearchReq):
  # TODO: call index.query with embedded query
  fake = [{"id":"demo","text":"Placeholder memory", "score":0.42, "title":"Demo"}]
  return {"hits": fake[: req.k]}
