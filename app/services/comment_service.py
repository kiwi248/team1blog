"""리스트 기반의 댓글 CRUD 처리 로직."""

from fastapi import HTTPException, status

from app.schemes.comment_scheme import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)


fake_db: list[CommentResponse] = []
_next_comment_id = 1


def _find_comment_index(comment_id: int) -> int:
    for index, comment in enumerate(fake_db):
        if comment.comment_id == comment_id:
            return index

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Comment not found",
    )


def create_comment(post_id: int, comment: CommentCreate) -> CommentResponse:
    """새 댓글을 저장하고 생성된 댓글을 반환한다."""
    global _next_comment_id

    created_comment = CommentResponse(
        comment_id=_next_comment_id,
        post_id=post_id,
        user_id=comment.user_id,
        content=comment.content,
    )
    fake_db.append(created_comment)
    _next_comment_id += 1
    return created_comment


def get_all_comments() -> list[CommentResponse]:
    """저장된 모든 댓글을 반환한다."""
    return list(fake_db)


def get_comments_by_post(post_id: int) -> list[CommentResponse]:
    """특정 게시글에 작성된 댓글만 반환한다."""
    return [comment for comment in fake_db if comment.post_id == post_id]


def get_comment(comment_id: int) -> CommentResponse:
    """댓글 한 개를 조회한다."""
    return fake_db[_find_comment_index(comment_id)]


def update_comment(
    comment_id: int,
    comment: CommentUpdate,
) -> CommentResponse:
    """댓글 내용을 수정한다."""
    index = _find_comment_index(comment_id)
    saved_comment = fake_db[index]
    updated_comment = CommentResponse(
        comment_id=saved_comment.comment_id,
        post_id=saved_comment.post_id,
        user_id=saved_comment.user_id,
        content=comment.content,
    )
    fake_db[index] = updated_comment
    return updated_comment


def delete_comment(comment_id: int) -> CommentResponse:
    """댓글을 삭제하고 삭제된 댓글을 반환한다."""
    return fake_db.pop(_find_comment_index(comment_id))


def clear_comments() -> None:
    """테스트가 서로 영향을 주지 않도록 댓글 저장소를 초기화한다."""
    global _next_comment_id

    fake_db.clear()
    _next_comment_id = 1
