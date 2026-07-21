"""댓글 Service의 CRUD 처리 테스트."""

import pytest
from fastapi import HTTPException

from app.schemes.comment_scheme import CommentCreate, CommentUpdate
from app.services.comment_service import (
    create_comment,
    delete_comment,
    get_all_comments,
    get_comment,
    get_comments_by_post,
    update_comment,
)


def make_comment(post_id: int = 1, user_id: int = 1, content: str = "댓글"):
    return create_comment(
        post_id,
        CommentCreate(user_id=user_id, content=content),
    )


def test_create_comment_assigns_id_and_saves_comment():
    created = make_comment(post_id=10, user_id=2, content="좋은 글입니다.")

    assert created.comment_id == 1
    assert created.post_id == 10
    assert created.user_id == 2
    assert created.content == "좋은 글입니다."
    assert get_all_comments() == [created]


def test_comment_id_is_not_reused_after_delete():
    first = make_comment()
    second = make_comment()
    delete_comment(second.comment_id)

    third = make_comment()

    assert first.comment_id == 1
    assert second.comment_id == 2
    assert third.comment_id == 3


def test_get_all_comments_returns_empty_list():
    assert get_all_comments() == []


def test_get_comment_returns_matching_comment():
    created = make_comment()

    assert get_comment(created.comment_id) == created


def test_get_comments_by_post_filters_other_posts():
    expected = make_comment(post_id=1, content="첫 번째 게시글 댓글")
    make_comment(post_id=2, content="두 번째 게시글 댓글")

    assert get_comments_by_post(1) == [expected]


def test_update_comment_changes_only_content():
    created = make_comment(post_id=10, user_id=2)

    updated = update_comment(
        created.comment_id,
        CommentUpdate(content="수정된 댓글"),
    )

    assert updated.comment_id == created.comment_id
    assert updated.post_id == created.post_id
    assert updated.user_id == created.user_id
    assert updated.content == "수정된 댓글"
    assert get_comment(created.comment_id) == updated


def test_delete_comment_removes_and_returns_comment():
    created = make_comment()

    deleted = delete_comment(created.comment_id)

    assert deleted == created
    assert get_all_comments() == []


@pytest.mark.parametrize("operation", ["get", "update", "delete"])
def test_missing_comment_raises_404(operation):
    with pytest.raises(HTTPException) as error:
        if operation == "get":
            get_comment(999)
        elif operation == "update":
            update_comment(999, CommentUpdate(content="수정"))
        else:
            delete_comment(999)

    assert error.value.status_code == 404
    assert error.value.detail == "Comment not found"

