import anthropic

from bass.models.conversation import Message, Role


class LlmService:
    def __init__(self, api_key: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)

    def generate_response(self, chat: list[Message]) -> Message:
        messages = [{"role": msg.role.value, "content": msg.content} for msg in chat]
        response = self._client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=messages,
        )
        content = response.content[0].text
        return Message(role=Role.ASSISTANT, content=content)