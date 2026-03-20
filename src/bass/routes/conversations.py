from fastapi import APIRouter, HTTPException

from bass.models.conversation import Conversation, Message, SendMessageRequest
from bass.services.conversation import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


def create_router(service: ConversationService) -> APIRouter:
    @router.post("", response_model=Conversation)
    def create() -> Conversation:
        return service.create()

    @router.get("", response_model=list[Conversation])
    def get_all() -> list[Conversation]:
        return service.get_all()

    @router.get("/{conversation_id}", response_model=Conversation)
    def get(conversation_id: str) -> Conversation:
        conversation = service.get(conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation

    @router.post("/{conversation_id}/messages", response_model=Message)
    def send_message(conversation_id: str, request: SendMessageRequest) -> Message:
        conversation = service.get(conversation_id)
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return service.send_message(conversation_id, request.content)

    @router.delete("/{conversation_id}", status_code=204)
    def delete(conversation_id: str) -> None:
        if not service.delete(conversation_id):
            raise HTTPException(status_code=404, detail="Conversation not found")

    return router
