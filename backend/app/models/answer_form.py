from pydantic import BaseModel, Field

class AnswerForm(BaseModel):
    question: str = Field(..., title="User Question", description="The question asked by the user.")
    answer: str = Field(..., title="Chatbot Answer", description="The answer provided by the chatbot.")