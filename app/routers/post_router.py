from fastapi import APIRouter, HTTPException

from app.schemes.post_scheme import Post_Create, Post_Response, Post_Update
from app.services.post_service import (
    create_post,
    delete_post,
    get_post,
    get_posts,
    update_post,
)


post_router = APIRouter(prefix="/posts", tags=["posts"])


# 게시글 생성
@post_router.post("", response_model=Post_Response, status_code=201)
def post_create(post: Post_Create):
    return create_post(post)



# 게시글 조회
@post_router.get("/{post_id}", response_model=Post_Response)
def post_get(post_id: int):
    post = get_post(post_id)

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


# 게시글 수정
@post_router.put("/{post_id}", response_model=Post_Response)
def post_update(post_id: int, update_data: Post_Update):
    post = update_post(post_id, update_data)

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


# 게시글 삭제
@post_router.delete("/{post_id}", response_model=Post_Response)
def post_delete(post_id: int):
    post = delete_post(post_id)

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post
