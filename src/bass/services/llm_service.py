from bass.models.conversation import Message, Role

class LlmService:
    def generate_response(self, chat: list[Message]) -> Message:
        return Message(role=Role.ASSISTANT, content="echo " + chat[-1].content)