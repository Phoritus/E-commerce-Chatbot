from typing import TypedDict, Annotated
from pydantic import BaseModel
from langgraph.graph.message import add_messages

class ChatBotRequest(BaseModel):
    question: str
    thread_id: str

class ChatBotResponse(BaseModel):
    answer: str

class ChatBotState(TypedDict):
    messages: Annotated[list, add_messages]