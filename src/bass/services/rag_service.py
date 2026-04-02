import logging
from collections.abc import Sequence

from bass.models.conversation import Message, Role
from bass.models.rag import Chunk
from bass.services.llm_service import LlmService

logger = logging.getLogger(__name__)

FALLBACK_RESPONSE = (
    "I can only help with banking-related topics such as "
    "credit cards, savings accounts, and fraud reporting. "
    "Could you rephrase your question?"
)

RAG_SYSTEM_PROMPT = """You are a banking assistant. Answer the user's question using ONLY the provided context.
If the context does not contain enough information to answer, say so honestly.
Keep your response to 1-2 short paragraphs. Do not use markdown, bullet points, or any formatting.
Write in plain conversational language, as if speaking directly to the customer.

Context:
{context}"""


class RagService:
    def __init__(self, llm: LlmService) -> None:
        self._llm = llm

    def answer(self, query: str, chunks: Sequence[Chunk]) -> Message:
        if not chunks:
            logger.info("No chunks found — returning fallback")
            return Message(role=Role.ASSISTANT, content=FALLBACK_RESPONSE)

        logger.info("Generating RAG answer from %d chunks", len(chunks))
        context = "\n\n---\n\n".join(
            f"[Source: {c.metadata.get('source', 'unknown')}]\n{c.content}"
            for c in chunks
        )
        system = RAG_SYSTEM_PROMPT.format(context=context)
        logger.debug("System prompt:\n%s", system)

        response = self._llm.generate_response(
            chat=[Message(role=Role.USER, content=query)],
            system=system,
        )
        logger.info("LLM response: %s", response.content[:120])
        return response
