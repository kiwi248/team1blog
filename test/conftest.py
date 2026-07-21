"""댓글 테스트에서 공통으로 사용하는 pytest 설정."""

import pytest
from fastapi.testclient import TestClient

from app.port import app
from app.services.comment_service import clear_comments


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_fake_db():
    clear_comments()
    yield
    clear_comments()

