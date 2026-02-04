import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.v1 import chat_bot_api
from app.core.config import config
from app.db import postgresdb
from app.models.amazon_data_model import Base
from app.components.html_content import HTML_CONTENT


# Create database tables
#Base.metadata.create_all(bind=postgresdb.engine)


origin = [
    "http://localhost:5173",
    "https://e-commerce-chatbot-kappa.vercel.app"
]

# Initialize the limiter (using IP address as the key)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=config.app_name)

# Attach limiter to app state and handle errors
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_CONTENT

# Register API routers
app.include_router(chat_bot_api.router, prefix="/api/v1")