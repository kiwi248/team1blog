from fastapi import FastAPI

from app.routers.user_router import user_router


app = FastAPI(title="User CRUD")
app.include_router(user_router)
