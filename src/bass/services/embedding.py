from typing import Protocol


class EmbeddingService(Protocol):
    def embed(self, text: str) -> list[float]: ...
