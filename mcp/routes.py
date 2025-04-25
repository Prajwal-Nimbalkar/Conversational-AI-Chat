from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agent.agent import ConversationalAgent
from mcp.config import settings
from mcp.llm_backends.openai_backend import OpenAIBackend
from mcp.llm_backends.claude_backend import ClaudeBackend
from mcp.llm_backends.gemini_backend import GeminiBackend
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

# Define input/output format
class ChatRequest(BaseModel):
    user_id: str
    message: str
    provider: str

class ChatResponse(BaseModel):
    response: str

# Initialize agent + LLM backends
llm_backends = {
    "openai": OpenAIBackend(api_key=settings.OPENAI_API_KEY),
    "claude": ClaudeBackend(api_key=settings.CLAUDE_API_KEY),
    "gemini": GeminiBackend(api_key=settings.GEMINI_API_KEY),
}

agent = ConversationalAgent(llm_backends)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info(f"Received message from {request.user_id}: {request.message}")
        reply = await agent.chat(
            user_id=request.user_id,
            message=request.message,
            provider=request.provider
        )
        logger.info(f"Generated reply: {reply}")
        return {"response": reply}
    except Exception as e:
        logger.error(f"Error in /chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
