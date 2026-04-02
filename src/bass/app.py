import json
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from bass.models.rag import Chunk
from bass.routes.conversations import create_router
from bass.services.conversation import ConversationService
from bass.services.llm_service import LlmService
from bass.services.local_embedding import LocalEmbeddingService
from bass.services.rag_service import RagService
from bass.services.retrieval import RetrievalService
from bass.settings import Settings
from bass.storage.conversations import ConversationsStorage
from bass.storage.vector_store import InMemoryVectorStore

logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"
KNOWLEDGE_BASE = Path(__file__).resolve().parent.parent.parent / "data" / "knowledge_base.json"


def load_knowledge_base(
    path: Path, store: InMemoryVectorStore, embedder: LocalEmbeddingService
) -> None:
    logger.info("Loading knowledge base from %s", path)
    with open(path) as f:
        entries = json.load(f)
    for entry in entries:
        chunk = Chunk(
            content=entry["content"],
            embedding=embedder.embed(entry["content"]),
            metadata=entry["metadata"],
        )
        store.add(chunk)
    logger.info("Loaded %d chunks into vector store", len(entries))


def create_app() -> FastAPI:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    )
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    app = FastAPI(title="Bass")

    settings = Settings()  # type: ignore[call-arg]

    embedder = LocalEmbeddingService()
    store = InMemoryVectorStore()
    load_knowledge_base(KNOWLEDGE_BASE, store, embedder)

    retrieval = RetrievalService(store, embedder, threshold=0.4)
    llm = LlmService(api_key=settings.anthropic_api_key)
    rag = RagService(llm)

    storage = ConversationsStorage()
    service = ConversationService(storage, retrieval, rag)

    app.include_router(create_router(service))
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

    return app


app = create_app()
