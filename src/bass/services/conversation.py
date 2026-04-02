import logging

from bass.models.conversation import Conversation, Message, Role
from bass.services.rag_service import RagService
from bass.services.retrieval import RetrievalService
from bass.storage.conversations import ConversationsStorage

logger = logging.getLogger(__name__)


class ConversationService:
    def __init__(
        self,
        storage: ConversationsStorage,
        retrieval: RetrievalService,
        rag: RagService,
    ) -> None:
        self._storage = storage
        self._retrieval = retrieval
        self._rag = rag

    def create(self) -> Conversation:
        conversation = Conversation()
        self._storage.save(conversation)
        return conversation

    def get(self, conversation_id: str) -> Conversation | None:
        return self._storage.get(conversation_id)

    def get_all(self) -> list[Conversation]:
        return self._storage.get_all()

    def delete(self, conversation_id: str) -> bool:
        return self._storage.delete(conversation_id)

    def send_message(self, conversation_id: str, content: str) -> Message:
        logger.info(
            "Processing message in conversation %s: %r", conversation_id, content
        )
        self._storage.add_message(
            conversation_id, Message(role=Role.USER, content=content)
        )
        chunks = self._retrieval.search(content)
        response = self._rag.answer(content, chunks)
        self._storage.add_message(conversation_id, response)
        return response
