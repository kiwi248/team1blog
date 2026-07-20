from fastapi import APIRouter
from app.schemes.chat_scheme import ChatRequest, ChatResponse
from app.services.chat_service import call_gpt

chat_router = APIRouter()

@chat_router.post("/chat/gpt-5.4 mini")
def chat_gemini(chat_request:ChatRequest) -> ChatResponse:
    print(chat_request.user_id)
    print(chat_request.prompt)
    return call_gpt(chat_request)