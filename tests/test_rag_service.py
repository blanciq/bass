"""
Unit tests for RagService — LLM is mocked.
"""

from unittest.mock import MagicMock

from bass.models.conversation import Message, Role
from bass.models.rag import Chunk
from bass.services.rag_service import FALLBACK_RESPONSE, RagService


def _make_chunk(content: str, source: str = "test.md") -> Chunk:
    return Chunk(
        id="doc-1",
        content=content,
        metadata={"source": source},
    )


class TestRagServiceFallback:
    def test_no_chunks_returns_static_fallback(self) -> None:
        llm = MagicMock()
        service = RagService(llm)

        result = service.answer("How do I make pasta?", chunks=[])

        assert result.role == Role.ASSISTANT
        assert result.content == FALLBACK_RESPONSE
        llm.generate_response.assert_not_called()


class TestRagServiceWithChunks:
    def test_passes_query_and_context_to_llm(self) -> None:
        llm = MagicMock()
        llm.generate_response.return_value = Message(
            role=Role.ASSISTANT, content="The annual fee is $0."
        )
        service = RagService(llm)
        chunks = [_make_chunk("Platinum card has no annual fee.", "credit_cards.md")]

        result = service.answer("What is the annual fee?", chunks=chunks)

        assert result.content == "The annual fee is $0."
        call_args = llm.generate_response.call_args
        assert call_args.kwargs["system"] is not None
        assert "Platinum card has no annual fee." in call_args.kwargs["system"]
        assert "credit_cards.md" in call_args.kwargs["system"]

    def test_multiple_chunks_all_included_in_context(self) -> None:
        llm = MagicMock()
        llm.generate_response.return_value = Message(
            role=Role.ASSISTANT, content="answer"
        )
        service = RagService(llm)
        chunks = [
            _make_chunk("Chunk A", "a.md"),
            _make_chunk("Chunk B", "b.md"),
        ]

        service.answer("question", chunks=chunks)

        system = llm.generate_response.call_args.kwargs["system"]
        assert "Chunk A" in system
        assert "Chunk B" in system

    def test_query_is_passed_as_user_message(self) -> None:
        llm = MagicMock()
        llm.generate_response.return_value = Message(
            role=Role.ASSISTANT, content="answer"
        )
        service = RagService(llm)
        chunks = [_make_chunk("some content")]

        service.answer("What are the fees?", chunks=chunks)

        chat = llm.generate_response.call_args.kwargs["chat"]
        assert len(chat) == 1
        assert chat[0].role == Role.USER
        assert chat[0].content == "What are the fees?"
