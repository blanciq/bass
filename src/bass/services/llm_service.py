from anthropic import Anthropic
from anthropic.types import MessageParam, TextBlock

from bass.models.conversation import Message, Role


class LlmService:
    def __init__(self, api_key: str) -> None:
        self._client = Anthropic(api_key=api_key)

    def generate_response(
        self, chat: list[Message], system: str | None = None
    ) -> Message:
        messages: list[MessageParam] = [
            {"role": msg.role.value, "content": msg.content} for msg in chat
        ]
        response = self._client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=messages,
            system=system or "",
        )
        first_block = response.content[0]
        if isinstance(first_block, TextBlock):
            content = first_block.text
        else:
            raise ValueError(f"Unexpected content block type: {type(first_block)}")
        return Message(role=Role.ASSISTANT, content=content)