from typing import Dict, List

MAX_HISTORY = 5  # keep only the last 5 exchanges

class ConversationalAgent:
    def __init__(self, llm_backends: Dict[str, object]):
        self.llm_backends = llm_backends
        self.user_histories: Dict[str, List[Dict[str, str]]] = {}

    async def chat(self, user_id: str, message: str, provider: str = "openai") -> str:
        if provider not in self.llm_backends:
            raise ValueError(f"Unsupported provider: {provider}")

        if user_id not in self.user_histories:
            self.user_histories[user_id] = []

        # Append user message to history
        self.user_histories[user_id].append({"role": "user", "content": message})

        # Keep only the last MAX_HISTORY messages
        if len(self.user_histories[user_id]) > MAX_HISTORY:
            self.user_histories[user_id] = self.user_histories[user_id][-MAX_HISTORY:]

        # Call backend LLM
        llm = self.llm_backends[provider]
        history = self.user_histories[user_id]

        # Generate response
        response = await llm.generate(message, history)

        # Append assistant response to history
        self.user_histories[user_id].append({"role": "assistant", "content": response})

        return response
