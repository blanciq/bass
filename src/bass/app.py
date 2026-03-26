from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from bass.services.conversation import ConversationService
from bass.services.llm_service import LlmService
from bass.storage.conversations import ConversationsStorage
from bass.routes.conversations import create_router

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"


def create_app() -> FastAPI:
    app = FastAPI(title="Bass")

    storage = ConversationsStorage()
    llm_service = LlmService()
    service = ConversationService(storage, llm_service)
    app.include_router(create_router(service))
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

    return app


app = create_app()