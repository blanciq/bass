from bass.models.conversation import Conversation, Message, Role
from bass.services.llm_service import LlmService
from bass.storage.conversations import ConversationsStorage


class ConversationService:
    def __init__(self, storage: ConversationsStorage, llm_service: LlmService) -> None:
        self._storage = storage
        self._llm_service = llm_service

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
        chat = self._storage.add_message(
            conversation_id, Message(role=Role.USER, content=content)
        )
        response = self._llm_service.generate_response(chat)
        self._storage.add_message(conversation_id, response)
        return response
