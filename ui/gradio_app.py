import gradio as gr
import httpx
import uuid

API_URL = "http://localhost:8000/api/chat"

# Store a unique user_id for session context
user_id = str(uuid.uuid4())

async def chat_with_agent(message, chat_history, selected_model):
    payload = {
        "user_id": user_id,
        "message": message,
        "provider": selected_model  # Add the selected model to the payload
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

    chat_history.append((message, data["response"]))
    return "", chat_history

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Conversational AI Chat")
    
    # Add model selection dropdown
    model_dropdown = gr.Dropdown(
        choices=["openai", "claude", "gemini"],
        label="Select AI",
        value="openai"  # Default value
    )
    
    # Increased height for chatbot response area
    chatbot = gr.Chatbot(height=500)
    
    # Increased height for user input box
    msg = gr.Textbox(label="Your Message", lines=4)
    send_btn = gr.Button("Send")

    state = gr.State([])

    send_btn.click(chat_with_agent, inputs=[msg, state, model_dropdown], outputs=[msg, chatbot])
    msg.submit(chat_with_agent, inputs=[msg, state, model_dropdown], outputs=[msg, chatbot])

if __name__ == "__main__":
    demo.queue().launch()