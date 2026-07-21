"""FastAPI TestClient를 이용한 댓글 API 테스트."""


def create_comment(client, post_id=1, user_id=2, content="좋은 글입니다."):
    return client.post(
        f"/posts/{post_id}/comments",
        json={"user_id": user_id, "content": content},
    )


def test_create_comment_api_returns_201(client):
    response = create_comment(client, post_id=10)

    assert response.status_code == 201
    assert response.json() == {
        "comment_id": 1,
        "post_id": 10,
        "user_id": 2,
        "content": "좋은 글입니다.",
    }


def test_get_all_comments_api(client):
    create_comment(client, content="첫 댓글")
    create_comment(client, content="두 번째 댓글")

    response = client.get("/comments")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_comments_by_post_api(client):
    create_comment(client, post_id=1, content="조회할 댓글")
    create_comment(client, post_id=2, content="다른 게시글 댓글")

    response = client.get("/posts/1/comments")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["content"] == "조회할 댓글"


def test_get_comment_api(client):
    created = create_comment(client).json()

    response = client.get(f"/comments/{created['comment_id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_update_comment_api(client):
    created = create_comment(client).json()

    response = client.put(
        f"/comments/{created['comment_id']}",
        json={"content": "수정된 댓글입니다."},
    )

    assert response.status_code == 200
    assert response.json() == {
        **created,
        "content": "수정된 댓글입니다.",
    }


def test_delete_comment_api(client):
    created = create_comment(client).json()

    response = client.delete(f"/comments/{created['comment_id']}")

    assert response.status_code == 200
    assert response.json() == created
    assert client.get(f"/comments/{created['comment_id']}").status_code == 404


def test_missing_comment_apis_return_404(client):
    assert client.get("/comments/999").status_code == 404
    assert client.put("/comments/999", json={"content": "수정"}).status_code == 404
    assert client.delete("/comments/999").status_code == 404


def test_invalid_comment_requests_return_422(client):
    assert client.post("/posts/1/comments", json={"content": "댓글"}).status_code == 422
    assert client.post("/posts/1/comments", json={"user_id": 1}).status_code == 422
    assert create_comment(client, content="   ").status_code == 422
    assert client.get("/comments/not-a-number").status_code == 422

