from pydantic import BaseModel

class ChatBotRequest(BaseModel):
    question: str

class ChatBotResponse(BaseModel):
    answer: str