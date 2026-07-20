from fastapi import APIRouter, HTTPException
from typing import List
from ..schema import PostResponse  # 스키마 파일 불러오기

# 태그와 주소 세팅 (도메인 주소가 /posts 로 시작하도록)
router = APIRouter(prefix="/posts", tags=["Post 조회/삭제"])

# (임시) 데이터베이스 역할을 할 리스트 - 실제로는 진짜 DB(MySQL 등)를 연결해야 합니다.
fake_db = [
    {"post_id": 1, "title": "첫 글", "content": "안녕하세요", "author": "user1", "created_at": "2026-07-16T10:00:00"},
    {"post_id": 2, "title": "두 번째 글", "content": "반갑습니다", "author": "user2", "created_at": "2026-07-16T11:00:00"}
]

# 1. 게시글 목록 전체 조회 (Read All)
@router.get("/", response_model=List[PostResponse])
async def get_all_posts():
    return fake_db

# 2. 특정 게시글 하나만 상세 조회 (Read One)
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    for post in fake_db:
        if post["post_id"] == post_id:
            return post
    # 글 번호가 없으면 404 에러 발생
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

# 3. 특정 게시글 삭제 (Delete)
@router.delete("/{post_id}")
async def delete_post(post_id: int):
    for i, post in enumerate(fake_db):
        if post["post_id"] == post_id:
            del fake_db[i]
            return {"success": True, "message": f"{post_id}번 게시글이 삭제되었습니다."}
    # 삭제하려는 글이 없으면 404 에러 발생
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")