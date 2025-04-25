# Conversational AI MCP Agent

This is a multi-provider Conversational AI system that integrates with OpenAI (ChatGPT), Claude (Anthropic), and Gemini (Google) using a FastAPI-powered MCP (Model Context Protocol) server. It supports dynamic backend selection, handles conversation history, and includes a Gradio-based frontend for chatting.

## Features

- Supports OpenAI, Claude, and Gemini models.
- Unified interface via FastAPI.
- Gradio web UI for seamless chat experience.
- Pluggable backends with LLM abstraction.
- Lightweight, clean, and async-compatible.

## Setup Instructions

### 1. Create a Virtual Environment
- python3 -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate

### 2. Install Dependencies
1) pip install -r setup.txt
2) pip install google-generativeai

### 3. API Key Setup
Create a .env file or export the following environment variables:
- OPENAI_API_KEY=your-openai-key
- ANTHROPIC_API_KEY=your-claude-key
- GEMINI_API_KEY=your-gemini-key

## Running the Project
### 1. Start the FastAPI MCP Server
If you are present in root directory then use this command: uvicorn mcp.main:app --reload
If you are present in mcp directory then use this command: uvicorn main:app --reload
This will start the server at http://127.0.0.1:8000.

### 2. Launch the Gradio Frontend
If you are present in root directory then use this command: python ui/gradio_ui.py
If you are present in mcp directory then use this command: python gradio_ui.py

## Providers Info
1) OpenAI
    - Requires OpenAI API key
    - Endpoint: https://api.openai.com/v1/chat/completions

2) Claude
    - Requires Anthropic API key
    - Endpoint: https://api.anthropic.com/v1/messages
    - Ensure your Anthropic account has credit or trial access

3) Gemini
    - Requires Gemini API key
    - Uses google-generativeai Python SDK
    - Choose from gemini-1.5-pro-latest, gemini-1.5-flash-latest, etc.

## Notes
- Make sure your keys are valid and your billing is active or trial-enabled.
- Claude error: Your credit balance is too low means your Anthropic trial quota is exhausted.

## Author
- Prajwal Nimbalkar
- prajwalnimbalkar11@gmail.com