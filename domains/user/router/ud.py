
from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel


# 데이터 모양 정의
class User(BaseModel):
    id: str
    name: str
    age: int


class UserUpdate(BaseModel):
    name: str
    age: int


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: User | None = None


# FastAPI 서버와 유저 라우터 생성
app = FastAPI()
router_ud = APIRouter(prefix="/users", tags=["users"])


# 임시 유저 데이터
users: dict[str, User] = {
    "id01": User(id="id01", name="김철수", age=20),
    "id02": User(id="id02", name="이영희", age=25),
}


@router_ud.put("/{user_id}", response_model=ApiResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
) -> ApiResponse:
    """아이디에 해당하는 유저의 이름과 나이를 수정합니다."""

    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 아이디입니다.",
        )

    updated_user = User(
        id=user_id,
        name=user_update.name,
        age=user_update.age,
    )
    users[user_id] = updated_user

    return ApiResponse(
        success=True,
        message=f"{user_id} 유저 정보 수정 완료",
        data=updated_user,
    )


@router_ud.delete("/{user_id}", response_model=ApiResponse)
async def delete_user(user_id: str) -> ApiResponse:
    """아이디에 해당하는 유저를 삭제합니다."""

    if user_id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 아이디입니다.",
        )

    deleted_user = users.pop(user_id)

    return ApiResponse(
        success=True,
        message=f"{user_id} 유저 삭제 완료",
        data=deleted_user,
    )


# 위에서 만든 유저 API를 FastAPI 서버에 연결
app.include_router(router_ud)