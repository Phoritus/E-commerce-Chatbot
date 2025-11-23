from app.core.config import groq_config

from groq import Groq

class SmallTalkService:
    def __init__(self):
        self._client_groq = Groq(
            api_key=groq_config.GROQ_API_KEY,          
        )

    def get_response(self, user_query: str) -> str:
        prompt = f"""
        You are a friendly and helpful customer support assistant for an e-commerce platform. 
        Engage in small talk with users while subtly promoting our products and services. 
        Keep the conversation light-hearted and enjoyable.

        User: {user_query}
        Assistant:"""

        response = self._client_groq.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "  You are a friendly and helpful customer support assistant for an e-commerce platform. Engage in small talk with users while subtly promoting our products and services. Keep the conversation light-hearted and enjoyable.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()
      
# if __name__ == "__main__":
#     small_talk_service = SmallTalkService()
#     user_input = "Hi there! How's it going?"
#     response = small_talk_service.get_response(user_input)
#     print(response)