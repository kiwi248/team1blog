"""댓글 API에서 사용하는 요청 및 응답 데이터 형식."""

from pydantic import BaseModel, PositiveInt, constr


CommentContent = constr(strip_whitespace=True, min_length=1)


class CommentCreate(BaseModel):
    """댓글 생성 요청."""

    user_id: PositiveInt
    content: CommentContent


class CommentUpdate(BaseModel):
    """댓글 수정 요청."""

    content: CommentContent


class CommentResponse(BaseModel):
    """댓글 API 응답."""

    comment_id: int
    post_id: int
    user_id: int
    content: str
