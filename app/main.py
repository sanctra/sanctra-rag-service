from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os

from app.rag import RagClient, RagItem, RagSearchResult


app = FastAPI(title="Sanctra RAG Service")
app.include_router(rag_router, prefix="/rag", tags=["rag"])

client = RagClient(
    project=os.getenv("GCP_PROJECT", ""),
    location=os.getenv("GCP_LOCATION", "us-central1"),
    index_id=os.getenv("VERTEX_INDEX_ID", ""),
    embedding_model=os.getenv("VERTEX_EMBED_MODEL", "textembedding-gecko@003"),
    sa_json_b64=os.getenv("GCP_SA_JSON_B64"),
)

class IndexItem(BaseModel):
    id: str
    person_id: str
    title: Optional[str] = None
    text: str
    tags: Optional[List[str]] = None

class IndexRequest(BaseModel):
    items: List[IndexItem] = Field(default_factory=list)

class SearchRequest(BaseModel):
    person_id: str
    query: str
    k: int = 5
    lambda_mult: float = 0.5  # for MMR

class SearchResponse(BaseModel):
    results: List[RagSearchResult]

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/index")
def index(req: IndexRequest):
    if not req.items:
        raise HTTPException(status_code=400, detail="No items provided")
    items = [
        RagItem(
            id=i.id,
            person_id=i.person_id,
            title=i.title or "",
            text=i.text,
            tags=i.tags or [],
        )
        for i in req.items
    ]
    client.upsert(items)
    return {"ok": True, "count": len(items)}

@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    results = client.search(person_id=req.person_id, query=req.query, k=req.k, lambda_mult=req.lambda_mult)
    return SearchResponse(results=results)
