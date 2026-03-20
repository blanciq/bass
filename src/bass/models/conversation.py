from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    role: Role
    content: str
    created_at: datetime = Field(default_factory=datetime.now)


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = ""
    messages: list[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)


class SendMessageRequest(BaseModel):
    content: str