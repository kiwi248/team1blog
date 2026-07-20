from fastapi import APIRouter, HTTPException, status

from app.schemes.user_scheme import UserCreate, UserResponse, UserUpdate
from app.services import user_service


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> dict:
    return user_service.create_user(user)


@user_router.get("", response_model=list[UserResponse])
def get_users() -> list[dict]:
    return user_service.get_users()


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> dict:
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate) -> dict:
    user = user_service.update_user(user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int) -> dict:
    user = user_service.delete_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
