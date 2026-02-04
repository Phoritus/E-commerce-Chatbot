from fastapi import APIRouter, Request # Import Request
from app.services.chat_bot_route import chat_bot_route
from app.models.chat_bot_model import ChatBotRequest, ChatBotResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

# This assumes you want a local limiter or import it from your main app
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/chat", response_model=ChatBotResponse)
# 1. Add the @limiter.limit decorator ("5 per minute", etc)
@limiter.limit("5/minute")
# 2. Ensure 'request: Request' is an argument
async def chat_bot_endpoint(request: Request, chat_request: ChatBotRequest):
    answer = chat_bot_route(chat_request)
    return ChatBotResponse(answer=answer)