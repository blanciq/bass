from bass.models.conversation import Conversation, Message


class ConversationsStorage:
    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def save(self, conversation: Conversation) -> None:
        self._conversations[conversation.id] = conversation

    def get(self, conversation_id: str) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def get_all(self) -> list[Conversation]:
        return list(self._conversations.values())

    def delete(self, conversation_id: str) -> bool:
        if conversation_id in self._conversations:
            del self._conversations[conversation_id]
            return True
        return False

    def add_message(self, conversation_id: str, message: Message) -> list[Message]:
        conversation = self._conversations.get(conversation_id)
        if conversation is None:
            raise ValueError(f"Conversation {conversation_id} not found")
        conversation.messages.append(message)
        return conversation.messages