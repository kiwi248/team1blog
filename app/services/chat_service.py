# chat_service.py
import os
from app.schemes.chat_scheme import ChatResponse, ChatRequest
from openai import OpenAI
from app.core.chat_config import *

def call_gpt(chat_request:ChatRequest)->ChatResponse:
    api_key = os.getenv("GPT_API_KEY")
    model = os.getenv("GPT_MODEL", "gpt-5.4-mini")

    print(api_key)
    print(model)

    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model = model,
        messages = [{"role": "user", "content": chat_request.prompt}],
    )

    return ChatResponse(
        answer = response.choices[0].message.content
    )