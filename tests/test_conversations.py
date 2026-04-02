from unittest.mock import MagicMock

from bass.models.conversation import Message, Role
from bass.services.conversation import ConversationService
from bass.storage.conversations import ConversationsStorage


def test_send_message_uses_rag_pipeline() -> None:
    storage = ConversationsStorage()
    retrieval = MagicMock()
    retrieval.search.return_value = []
    rag = MagicMock()
    rag.answer.return_value = Message(role=Role.ASSISTANT, content="fallback")

    service = ConversationService(storage, retrieval, rag)
    conversation = service.create()
    response = service.send_message(conversation.id, "hello")

    assert response.role == Role.ASSISTANT
    retrieval.search.assert_called_once_with("hello")
    rag.answer.assert_called_once()
