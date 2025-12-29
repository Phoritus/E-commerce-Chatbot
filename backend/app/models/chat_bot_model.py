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

from typing import Literal
from pydantic import Field

class RouterDecision(BaseModel):
    """Decide the most appropriate route for the user's question."""
    route: Literal["faq", "product_inquiry", "small_talk", "default"] = Field(
        description="Select 'faq' for general questions, 'product_inquiry' for product searches, and 'small_talk' for greetings."
    )