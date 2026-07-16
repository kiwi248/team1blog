# app/domains/comment/router.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/comments", tags=["comments"])


class Comment(BaseModel):
    content: str


# CREATE - 댓글 작성
@router.post("")
def create_comment(comment: Comment):
    return {"message": "댓글이 작성되었습니다.", "content": comment.content}


# READ - 댓글 조회
@router.get("/{comment_id}")
def get_comment(comment_id: int):
    return {"message": "댓글 조회", "comment_id": comment_id}


# UPDATE - 댓글 수정
@router.put("/{comment_id}")
def update_comment(comment_id: int, comment: Comment):
    return {"message": "댓글이 수정되었습니다.", "comment_id": comment_id, "content": comment.content}


# DELETE - 댓글 삭제
@router.delete("/{comment_id}")
def delete_comment(comment_id: int):
    return {"message": "댓글이 삭제되었습니다.", "comment_id": comment_id}