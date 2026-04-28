from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class RagItem(BaseModel):
    id: str
    person_id: str
    title: str = ""
    text: str
    tags: List[str] = Field(default_factory=list)


class RagSearchResult(BaseModel):
    id: str
    text: str
    score: float
    title: str = ""
    tags: List[str] = Field(default_factory=list)


class RagClient:
    """Small runtime-safe RAG adapter.

    This preserves the service contract while Vertex Vector Search wiring is
    completed. Items indexed during the current process are scoped by person_id
    and searched with simple lexical overlap so local/runtime smoke can pass.
    """

    def __init__(
        self,
        project: str = "",
        location: str = "us-central1",
        index_id: str = "",
        embedding_model: str = "textembedding-gecko@003",
        sa_json_b64: str | None = None,
    ):
        self.project = project
        self.location = location
        self.index_id = index_id
        self.embedding_model = embedding_model
        self.sa_json_b64 = sa_json_b64
        self._items: dict[str, RagItem] = {}

    def upsert(self, items: List[RagItem]) -> None:
        for item in items:
            self._items[item.id] = item

    def search(
        self,
        person_id: str,
        query: str,
        k: int = 5,
        lambda_mult: float = 0.5,
    ) -> List[RagSearchResult]:
        del lambda_mult  # Reserved for the Vertex/MMR implementation.
        terms = {part.lower() for part in query.split() if part.strip()}
        candidates: list[RagSearchResult] = []

        for item in self._items.values():
            if item.person_id != person_id:
                continue
            haystack = f"{item.title} {item.text} {' '.join(item.tags)}".lower()
            overlap = sum(1 for term in terms if term in haystack)
            score = float(overlap) if terms else 0.0
            if score > 0 or not terms:
                candidates.append(
                    RagSearchResult(
                        id=item.id,
                        text=item.text,
                        score=score,
                        title=item.title,
                        tags=item.tags,
                    )
                )

        candidates.sort(key=lambda result: result.score, reverse=True)
        return candidates[:k]
