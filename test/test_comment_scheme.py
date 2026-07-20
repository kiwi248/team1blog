"""댓글 Pydantic 모델의 입력값 검증 테스트."""

import pytest
from pydantic import ValidationError

from app.schemes.comment_scheme import CommentCreate, CommentUpdate


def test_comment_create_accepts_valid_data():
    comment = CommentCreate(user_id=1, content="좋은 글입니다.")

    assert comment.user_id == 1
    assert comment.content == "좋은 글입니다."


def test_comment_update_accepts_valid_data():
    comment = CommentUpdate(content="수정된 댓글입니다.")

    assert comment.content == "수정된 댓글입니다."


@pytest.mark.parametrize(
    "payload",
    [
        {"content": "작성자가 없습니다."},
        {"user_id": "not-a-number", "content": "잘못된 ID입니다."},
        {"user_id": 0, "content": "0은 사용할 수 없습니다."},
        {"user_id": -1, "content": "음수는 사용할 수 없습니다."},
        {"user_id": 1},
        {"user_id": 1, "content": ""},
        {"user_id": 1, "content": "   "},
    ],
)
def test_comment_create_rejects_invalid_data(payload):
    with pytest.raises(ValidationError):
        CommentCreate(**payload)


@pytest.mark.parametrize("content", ["", "   "])
def test_comment_update_rejects_empty_content(content):
    with pytest.raises(ValidationError):
        CommentUpdate(content=content)


def test_comment_content_removes_surrounding_spaces():
    comment = CommentCreate(user_id=1, content="  좋은 글입니다.  ")

    assert comment.content == "좋은 글입니다."

