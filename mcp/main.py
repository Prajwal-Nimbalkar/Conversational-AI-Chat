from fastapi import FastAPI
from mcp.routes import router as chat_router  # updated import

app = FastAPI()

app.include_router(chat_router, prefix="/api")
