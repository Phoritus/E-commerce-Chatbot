from app.core.config import groq_config

from langchain_groq import ChatGroq

from langchain_core.messages import SystemMessage, HumanMessage

class SmallTalkService:
    def __init__(self):
        self._client_groq = ChatGroq(
            api_key=groq_config.GROQ_API_KEY,
            model="openai/gpt-oss-20b",
            temperature=0.7,
            max_tokens=512,
            model_kwargs={"stream": False}
        )

    def get_response(self, user_query: str, history: list = []) -> str:
        prompt = f"""
        You are a friendly and helpful customer support assistant for an e-commerce platform. 
        Engage in small talk with users while subtly promoting our products and services. 
        Keep the conversation light-hearted and enjoyable.

        User: {user_query}
        Assistant:"""

        # Use SystemMessage object
        messages = [
            SystemMessage(content="You are a friendly and helpful customer support assistant for an e-commerce platform. Engage in small talk with users while subtly promoting our products and services. Keep the conversation light-hearted and enjoyable.")
        ]
        
        # Add history (already BaseMessages)
        messages.extend(history)
        
        # Add current user prompt as HumanMessage
        messages.append(HumanMessage(content=prompt))
        
        response = self._client_groq.invoke(messages)

        return response.content

# if __name__ == "__main__":
#     small_talk_service = SmallTalkService()
#     user_input = "Hi there! How's it going?"
#     response = small_talk_service.get_response(user_input)
#     print(response)