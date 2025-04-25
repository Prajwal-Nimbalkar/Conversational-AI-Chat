import httpx
from typing import List, Dict
import logging
import traceback

logger = logging.getLogger("uvicorn.error")

class OpenAIBackend:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    async def generate(self, prompt: str, history: List[Dict[str, str]]) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": history,
            "temperature": 0.7
        }

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    logger.error(f"OpenAI returned error: {response.text}")
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            # logger.error(f"Payload: {payload}")
            # logger.error(traceback.format_exc())
            raise e
