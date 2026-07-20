from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# 1. 생성/조회할 때 공통으로 들어가는 기본 데이터
class PostBase(BaseModel):
    title: str = Field(..., min_length=2, examples=["나의 첫 블로그 글"])
    content: str = Field(..., min_length=5, examples=["오늘 날씨가 너무 좋네요!"])
    author: str = Field(..., examples=["james"])

# 2. 동료분(CU)이 게시글을 '생성'할 때 받을 데이터 양식
class PostCreate(PostBase):
    pass # PostBase의 항목(제목, 내용, 작성자)을 그대로 사용합니다.

# 3. 동료분(CU)이 게시글을 '수정'할 때 받을 데이터 양식
class PostUpdate(BaseModel):
    # 제목과 내용만 수정 가능하도록 설정 (선택적 입력 허용)
    title: Optional[str] = Field(None, min_length=2)
    content: Optional[str] = Field(None, min_length=5)

# 4. 질문자님(RD)이 게시글을 '조회'해서 보여줄 때의 데이터 양식
class PostResponse(PostBase):
    post_id: int           # 서버에서 부여한 글 번호
    created_at: datetime   # 작성된 시간