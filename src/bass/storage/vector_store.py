from typing import Protocol

from sentence_transformers import util

from bass.models.rag import Chunk


class SearchResult(Chunk):
    score: float = 0.0


class VectorStore(Protocol):
    def add(self, chunk: Chunk) -> None: ...
    def search(self, embedding: list[float], top_k: int = 5) -> list[SearchResult]: ...


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: list[Chunk] = []

    def add(self, chunk: Chunk) -> None:
        self._chunks.append(chunk)

    def search(self, embedding: list[float], top_k: int = 5) -> list[SearchResult]:
        scored = []
        for chunk in self._chunks:
            score: float = util.cos_sim(embedding, chunk.embedding).item()
            scored.append(
                SearchResult(
                    id=chunk.id,
                    content=chunk.content,
                    embedding=chunk.embedding,
                    metadata=chunk.metadata,
                    score=score,
                )
            )
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:top_k]
