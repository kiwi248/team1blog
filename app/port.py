from fastapi import FastAPI

from app.routers.comment_router import comment_router


app = FastAPI(title="Comment CRUD")

app.include_router(comment_router)
