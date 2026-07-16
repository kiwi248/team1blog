from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserCreate(BaseModel):
    id: str
    name: str
    age: int


# 임시 데이터 저장소
# 실제 서비스에서는 데이터베이스를 사용합니다.
users: dict[str, UserCreate] = {}


@app.post("/users")
async def create_user(user: UserCreate):
    """새 유저를 등록합니다."""

    if user.id in users:
        raise HTTPException(
            status_code=409,
            detail="이미 존재하는 아이디입니다.",
        )

    users[user.id] = user

    return {
        "message": f"{user.id}의 아이디 생성 완료",
        "user": {
            "id": user.id,
            "name": user.name,
            "age": user.age,
             
        },
    }

