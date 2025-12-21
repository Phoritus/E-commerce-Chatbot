from app.services.chat_bot_route import chat_bot_route
from app.models.chat_bot_model import ChatBotRequest, ChatBotResponse

from fastapi import APIRouter
router = APIRouter()


@router.post("/chat", response_model=ChatBotResponse)
async def chat_bot_endpoint(request: ChatBotRequest):
    answer = chat_bot_route(request.question)
    return ChatBotResponse(answer=answer)