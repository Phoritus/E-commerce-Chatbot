from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    app_name: str = "E-Commerce Chatbot"
    DATABASE_URL: str | None = None

class ChromaConfig(BaseSettings):
    CHROMA_API_KEY: str | None = None
    CHROMA_TENANT: str | None = None
    database_name: str = "E-Commerce Chatbot"
    

class GroqConfig(BaseSettings):
    GROQ_API_KEY: str | None = None
    project_id: str | None = None

class GoogleConfig(BaseSettings):
    GOOGLE_API_KEY: str | None = None

groq_config = GroqConfig()
google_config = GoogleConfig()
chroma_config = ChromaConfig()
config = Config()