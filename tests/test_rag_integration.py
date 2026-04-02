"""
Integration tests for RagService — calls real LLM.

Run manually:
    uv run pytest tests/test_rag_integration.py -v -m integration

Reads ANTHROPIC_API_KEY from .env via Settings.
"""

import pytest

from bass.models.rag import Chunk
from bass.services.llm_service import LlmService
from bass.services.rag_service import RagService
from bass.settings import Settings

pytestmark = pytest.mark.integration


def _make_chunk(content: str, source: str) -> Chunk:
    return Chunk(content=content, metadata={"source": source})


@pytest.fixture()
def rag() -> RagService:
    settings = Settings()  # type: ignore[call-arg]
    return RagService(LlmService(api_key=settings.anthropic_api_key))


class TestRagIntegration:
    def test_answers_from_chunk(self, rag: RagService) -> None:
        chunks = [
            _make_chunk(
                "The Platinum credit card has no annual fee and offers 2% cashback "
                "on all purchases. The minimum credit score required is 700.",
                "products/credit_cards.md",
            )
        ]
        result = rag.answer("What is the cashback rate?", chunks=chunks)

        assert "2%" in result.content

    def test_answers_from_multiple_chunks(self, rag: RagService) -> None:
        chunks = [
            _make_chunk(
                "The Premium Savings account offers 4.5% APY with no minimum balance.",
                "products/savings_accounts.md",
            ),
            _make_chunk(
                "The Basic Savings account offers 1.2% APY with a $500 minimum balance.",
                "products/savings_accounts.md",
            ),
        ]
        result = rag.answer(
            "Compare the savings accounts", chunks=chunks
        )

        assert "4.5" in result.content
        assert "1.2" in result.content

    def test_admits_when_context_insufficient(self, rag: RagService) -> None:
        chunks = [
            _make_chunk(
                "The Platinum credit card has no annual fee.",
                "products/credit_cards.md",
            )
        ]
        result = rag.answer(
            "What is the mortgage interest rate?", chunks=chunks
        )

        # Should NOT hallucinate a mortgage rate
        assert "mortgage" in result.content.lower() or "don't" in result.content.lower() or "not" in result.content.lower()
