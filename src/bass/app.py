from fastapi import FastAPI

from bass.services.conversation import ConversationService
from bass.services.llm_service import LlmService
from bass.storage.conversations import ConversationsStorage
from bass.routes.conversations import create_router


def create_app() -> FastAPI:
    app = FastAPI(title="Bass")

    storage = ConversationsStorage()
    llm_service = LlmService()
    service = ConversationService(storage, llm_service)
    app.include_router(create_router(service))

    return app


app = create_app()