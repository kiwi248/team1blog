from pydantic import BaseModel, Field


class Post_Create(BaseModel):
    """게시글 생성 요청에 사용하는 데이터 형식입니다."""
    
    user_id: int = Field(gt=0, examples=[1])
    title: str = Field(min_length=1, examples=["FastAPI CRUD 만들기가 프로젝트입니다."])
    content: str = Field(
        min_length=1,
        examples=["FastAPI CRUD 만들어볼까요?"],
    )


class Post_Update(BaseModel):
    """게시글 수정 요청에 사용하는 데이터 형식입니다."""

    title: str = Field(min_length=1, examples=["FastAPI CRUD 만들기"])
    content: str = Field(
        min_length=1,
        examples=["FastAPI CRUD 만들어보겠습니다."],
    )


class Post_Response(BaseModel):
    """게시글 응답에 사용하는 데이터 형식입니다."""

    title: str = Field(min_length=1, examples=["FastAPI CRUD 만들기"])
    content: str = Field(
        min_length=1,
        examples=["FastAPI CRUD 만들어보겠습니다."],
    )
