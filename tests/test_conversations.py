from bass.services.conversation import ConversationService
from bass.services.llm_service import LlmService
from bass.storage.conversations import ConversationsStorage


def test_send_message_returns_echo() -> None:
    storage = ConversationsStorage()
    llm_service = LlmService()
    service = ConversationService(storage, llm_service)

    conversation = service.create()
    response = service.send_message(conversation.id, "hello")

    assert response.role == "assistant"
    assert response.content == "echo hello"