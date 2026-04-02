import logging

from bass.services.embedding import EmbeddingService
from bass.storage.vector_store import SearchResult, VectorStore

logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(
        self,
        store: VectorStore,
        embedder: EmbeddingService,
        threshold: float = 0.7,
    ) -> None:
        self._store = store
        self._embedder = embedder
        self._threshold = threshold

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        logger.info("Searching for: %r (threshold=%.2f)", query, self._threshold)
        query_embedding = self._embedder.embed(query)
        results = self._store.search(query_embedding, top_k=top_k)
        for r in results:
            logger.debug(
                "  chunk %s (score=%.4f): %s", r.id, r.score, r.content[:80]
            )
        filtered = [r for r in results if r.score >= self._threshold]
        logger.info(
            "Found %d/%d chunks above threshold", len(filtered), len(results)
        )
        return filtered
