from uuid import uuid4

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    embedding: list[float] = []
    metadata: dict[str, str] = {}
