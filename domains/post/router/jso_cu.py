from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..schema import PostCreate, PostUpdate, PostResponse # 스키마 파일 불러오기

router = APIRouter(prefix="/posts", tags=["Post 생성/수정"])

# (임시) 데이터베이스 역할을 할 리스트 - 질문자님 파일과 동일한 원리입니다.
fake_db = []
post_counter = 3 # 임시 글 번호 생성기

# 1. 새 게시글 생성 (Create)
@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate):
    global post_counter
    # 입력받은 데이터에 글 번호와 작성 시간을 추가로 부여합니다.
    new_post = {
        "post_id": post_counter,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "created_at": datetime.now()
    }
    fake_db.append(new_post)
    post_counter += 1
    return new_post

# 2. 기존 게시글 수정 (Update)
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: PostUpdate):
    for post in fake_db:
        if post["post_id"] == post_id:
            # 수정하려는 내용(제목, 내용)이 있을 경우에만 덮어씌웁니다.
            if post_update.title:
                post["title"] = post_update.title
            if post_update.content:
                post["content"] = post_update.content
            return post
    
    # 수정하려는 글 번호가 없으면 404 에러 발생
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")