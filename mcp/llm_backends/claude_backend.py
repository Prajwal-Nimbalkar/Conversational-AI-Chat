import httpx
from typing import List, Dict
import logging
import traceback
import anthropic

logger = logging.getLogger("uvicorn.error")

class ClaudeBackend:
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.api_key = api_key
        self.model = model

    async def generate(self, prompt: str, history: List[Dict[str, str]]) -> str:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        # Convert OpenAI-style history into Claude format (Claude uses 'messages' as a single string prompt)
        formatted_history = ""
        for msg in history:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                formatted_history += f"\n\nHuman: {content}"
            elif role == "assistant":
                formatted_history += f"\n\nAssistant: {content}"

        # Add current prompt
        formatted_history += f"\n\nHuman: {prompt}\n\nAssistant:"

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "temperature": 0.7,
            "messages": [],  # required field, but using `prompt` below
            "system": None,
            "stop_sequences": ["\n\nHuman:"],
            "stream": False,
            "prompt": formatted_history
        }

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    logger.error(f"Claude returned error: {response.text}")
                response.raise_for_status()
                data = response.json()
                return data.get("content", "").strip()
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            logger.error(f"Payload: {payload}")
            logger.error(traceback.format_exc())
            raise e
