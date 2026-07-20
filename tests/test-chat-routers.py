from fastapi.testclient import TestClient

from app.ykw import app
from app.routers import chat_router
from app.services.chat_service import call_gpt
from app.schemes.chat_scheme import ChatResponse


client = TestClient(app)


def test_chat_gemini_returns_service_response(monkeypatch):
    def fake_call_gpt(request):
        assert request.user_id == "user-1"
        assert request.prompt == "Hello"
        return ChatResponse(answer="Mocked GPT answer")

    monkeypatch.setattr(chat_router, "call_gpt", fake_call_gpt)

    response = client.post(
        "/chat/gpt-5.4 mini",
        json={"user_id": "user-1", "prompt": "Hello"},
    )

    assert response.status_code == 200
    assert response.json() == {"answer": "Mocked GPT answer"}


def test_chat_gemini_rejects_empty_prompt():
    response = client.post(
        "/chat/gpt-5.4 mini",
        json={"user_id": "user-1", "prompt": ""},
    )

    assert response.status_code == 422
