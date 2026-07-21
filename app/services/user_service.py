from app.schemes.user_scheme import UserCreate, UserUpdate


fake_db: list[dict] = []
_next_user_id = 1


def create_user(user: UserCreate) -> dict:
    global _next_user_id
    new_user = {"user_id": _next_user_id, **user.model_dump()}
    fake_db.append(new_user)
    _next_user_id += 1
    return new_user


def get_users() -> list[dict]:
    return fake_db


def get_user(user_id: int) -> dict | None:
    return next((user for user in fake_db if user["user_id"] == user_id), None)


def update_user(user_id: int, user: UserUpdate) -> dict | None:
    saved_user = get_user(user_id)
    if saved_user is None:
        return None
    saved_user.update(user.model_dump())
    return saved_user


def delete_user(user_id: int) -> dict | None:
    saved_user = get_user(user_id)
    if saved_user is None:
        return None
    fake_db.remove(saved_user)
    return saved_user


def reset_users() -> None:
    global _next_user_id
    fake_db.clear()
    _next_user_id = 1
