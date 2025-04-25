import google.generativeai as genai
from typing import List, Dict
import logging

logger = logging.getLogger("uvicorn.error")

class GeminiBackend:
    def __init__(self, api_key: str, model: str = "models/gemini-1.5-pro-latest"):
        self.api_key = api_key
        self.model_name = model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    async def generate(self, prompt: str, history: List[Dict[str, str]]) -> str:
        try:
            # Construct the prompt with history
            full_prompt = ""
            for turn in history:
                role = turn["role"].capitalize()
                content = turn["content"]
                full_prompt += f"{role}: {content}\n"
            full_prompt += f"User: {prompt}\nAssistant:"

            # Gemini requires sync calls – use thread executor in FastAPI if needed
            response = self.model.generate_content(full_prompt)

            if hasattr(response, "text"):
                return response.text.strip()
            else:
                logger.error("Gemini response has no text.")
                return "I'm sorry, I couldn't generate a response."

        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise e
