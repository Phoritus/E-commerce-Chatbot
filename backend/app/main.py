from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.components.html_content import HTML_CONTENT

from app.api.v1 import chat_bot_api
from app.core.config import config


origin = [
    "http://localhost:5173"
]

app = FastAPI(title=config.app_name)

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