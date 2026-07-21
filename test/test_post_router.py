"""
실행 방법

1. 프로젝트 루트로 이동합니다.
   cd C:\과제\team1blog

2. pytest와 httpx가 없다면 설치합니다.
   python -m pip install pytest httpx

3. Post Router 테스트를 실행합니다.
   python -m pytest test/test_post_router.py -v
"""

from fastapi.testclient import TestClient

from app import sym
from app.services import post_service


client = TestClient(sym.app)


def setup_function():
    """각 테스트를 시작하기 전에 게시글 데이터를 초기화합니다."""
    post_service.post_list.clear()
    post_service.post_id = 1


def create_test_post():
    """여러 테스트에서 사용할 게시글 하나를 생성합니다."""
    return client.post(
        "/posts",
        json={
            "user_id": 1,
            "title": "첫 번째 게시글",
            "content": "게시글 내용입니다.",
        },
    )


def test_create_post():
    response = create_test_post()

    assert response.status_code == 201
    assert response.json()["title"] == "첫 번째 게시글"
    assert response.json()["content"] == "게시글 내용입니다."


def test_get_post():
    create_test_post()

    response = client.get("/posts/1")

    assert response.status_code == 200
    assert response.json()["title"] == "첫 번째 게시글"


def test_update_post():
    create_test_post()

    response = client.put(
        "/posts/1",
        json={
            "title": "수정된 게시글",
            "content": "수정된 내용입니다.",
        },
    )

    assert response.status_code == 200
    assert response.json()["title"] == "수정된 게시글"
    assert response.json()["content"] == "수정된 내용입니다."


def test_delete_post():
    create_test_post()

    response = client.delete("/posts/1")

    assert response.status_code == 200
    assert response.json()["title"] == "첫 번째 게시글"

    get_response = client.get("/posts/1")
    assert get_response.status_code == 404


def test_get_post_not_found():
    response = client.get("/posts/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_update_post_not_found():
    response = client.put(
        "/posts/999",
        json={
            "title": "수정된 게시글",
            "content": "수정된 내용입니다.",
        },
    )

    assert response.status_code == 404


def test_delete_post_not_found():
    response = client.delete("/posts/999")

    assert response.status_code == 404


def test_create_post_without_user_id():
    response = client.post(
        "/posts",
        json={
            "title": "작성자 없는 게시글",
            "content": "게시글 내용입니다.",
        },
    )

    assert response.status_code == 422


def test_create_post_without_title():
    response = client.post(
        "/posts",
        json={
            "user_id": 1,
            "content": "게시글 내용입니다.",
        },
    )

    assert response.status_code == 422


def test_create_post_without_content():
    response = client.post(
        "/posts",
        json={
            "user_id": 1,
            "title": "내용 없는 게시글",
        },
    )

    assert response.status_code == 422
