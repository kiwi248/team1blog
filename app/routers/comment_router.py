"""댓글 CRUD API 경로."""

from fastapi import APIRouter, status

from app.schemes.comment_scheme import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)
from app.services.comment_service import (
    create_comment,
    delete_comment,
    get_all_comments,
    get_comment,
    get_comments_by_post,
    update_comment,
)


comment_router = APIRouter(tags=["comments"])


@comment_router.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(post_id: int, comment: CommentCreate) -> CommentResponse:
    return create_comment(post_id, comment)


@comment_router.get("/comments", response_model=list[CommentResponse])
def get_all() -> list[CommentResponse]:
    return get_all_comments()


@comment_router.get(
    "/posts/{post_id}/comments",
    response_model=list[CommentResponse],
)
def get_by_post(post_id: int) -> list[CommentResponse]:
    return get_comments_by_post(post_id)


@comment_router.get(
    "/comments/{comment_id}",
    response_model=CommentResponse,
)
def get(comment_id: int) -> CommentResponse:
    return get_comment(comment_id)


@comment_router.put(
    "/comments/{comment_id}",
    response_model=CommentResponse,
)
def update(comment_id: int, comment: CommentUpdate) -> CommentResponse:
    return update_comment(comment_id, comment)


@comment_router.delete(
    "/comments/{comment_id}",
    response_model=CommentResponse,
)
def delete(comment_id: int) -> CommentResponse:
    return delete_comment(comment_id)
