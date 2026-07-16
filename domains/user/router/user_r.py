from fastapi import FastAPI, HTTPException
from scheme.model_common import ApiResponse

app = FastAPI()

users = {
    "id01": {"id": "id01", "name": "name1", "age": 10},
    "id02": {"id": "id02", "name": "name2", "age": 20},
    "id03": {"id": "id03", "name": "name3", "age": 30},
}


@app.get("/users/{user_id}")
async def get_user(user_id: str):

    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="해당 아이디가 없습니다."
        )

    response = ApiResponse(
        success=True,
        message="정상조회",
        data=users[user_id]
    )

    return response