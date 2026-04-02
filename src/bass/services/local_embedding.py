from sentence_transformers import SentenceTransformer


class LocalEmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        embedding = self._model.encode(text)
        result: list[float] = embedding.tolist()
        return result
