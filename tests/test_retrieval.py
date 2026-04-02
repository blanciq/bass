"""
Retrieval tests using real LocalEmbeddingService and production knowledge base.

These tests use the actual embedding model to verify that queries match
the correct chunks from our knowledge base.
"""

import json
from pathlib import Path

import pytest

from bass.models.rag import Chunk
from bass.services.local_embedding import LocalEmbeddingService
from bass.services.retrieval import RetrievalService
from bass.storage.vector_store import InMemoryVectorStore

KNOWLEDGE_BASE = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"
THRESHOLD = 0.4


@pytest.fixture(scope="module")
def embedder() -> LocalEmbeddingService:
    return LocalEmbeddingService()


@pytest.fixture(scope="module")
def store(embedder: LocalEmbeddingService) -> InMemoryVectorStore:
    s = InMemoryVectorStore()
    with open(KNOWLEDGE_BASE) as f:
        entries = json.load(f)
    for entry in entries:
        s.add(
            Chunk(
                content=entry["content"],
                embedding=embedder.embed(entry["content"]),
                metadata=entry["metadata"],
            )
        )
    return s


@pytest.fixture(scope="module")
def retrieval(
    store: InMemoryVectorStore, embedder: LocalEmbeddingService
) -> RetrievalService:
    return RetrievalService(store, embedder, threshold=THRESHOLD)


# -- GOOD CASES: banking queries find relevant chunks


class TestGoodCases:
    def test_fraud_query_finds_fraud_chunk(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("How do I report fraud?")
        assert len(results) >= 1
        assert results[0].metadata["source"] == "policies/fraud_reporting"

    def test_savings_query_finds_savings_chunk(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("What is the savings interest rate?")
        assert len(results) >= 1
        assert results[0].metadata["source"] == "products/savings_accounts"

    def test_home_loan_query_finds_home_loan_chunk(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("What are the home loan rates?")
        assert len(results) >= 1
        assert results[0].metadata["source"] == "products/home_loans"

    def test_wire_transfer_query_finds_transfer_chunk(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("How much does a wire transfer cost?")
        assert len(results) >= 1
        assert results[0].metadata["source"] == "products/transfers"

    def test_checking_account_query_finds_checking_chunk(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("What is the monthly fee for checking?")
        assert len(results) >= 1
        assert results[0].metadata["source"] == "products/checking_accounts"

    def test_top_result_has_highest_score(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("How do I report fraud?")
        if len(results) > 1:
            assert results[0].score >= results[1].score


# -- BAD CASES: non-banking queries return nothing


class TestBadCases:
    def test_cooking_query_returns_nothing(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("How do I make pasta carbonara?")
        assert len(results) == 0

    def test_sports_query_returns_nothing(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("What was the football score?")
        assert len(results) == 0

    def test_generic_greeting_returns_nothing(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("Hello")
        assert len(results) == 0

    def test_weather_query_returns_nothing(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("What is the weather like today?")
        assert len(results) == 0

    def test_programming_query_returns_nothing(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("How do I write a Python function?")
        assert len(results) == 0


# -- EDGE CASES


class TestEdgeCases:
    def test_empty_store_returns_nothing(
        self, embedder: LocalEmbeddingService
    ) -> None:
        empty_store = InMemoryVectorStore()
        r = RetrievalService(empty_store, embedder, threshold=THRESHOLD)
        results = r.search("What are the home loan rates?")
        assert len(results) == 0

    def test_top_k_limits_results(
        self, retrieval: RetrievalService
    ) -> None:
        results = retrieval.search("What are the home loan rates?", top_k=1)
        assert len(results) <= 1

    def test_no_threshold_returns_all_chunks(
        self, store: InMemoryVectorStore, embedder: LocalEmbeddingService
    ) -> None:
        lenient = RetrievalService(store, embedder, threshold=-1.0)
        results = lenient.search("How do I make pasta carbonara?", top_k=10)
        assert len(results) == 10
