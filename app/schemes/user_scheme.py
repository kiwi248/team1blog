from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    bio: str | None = None


class UserUpdate(BaseModel):
    username: str
    email: str
    password: str
    bio: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    email: str
    bio: str | None = None
