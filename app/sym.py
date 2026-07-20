from fastapi import FastAPI

from app.routers.post_router import post_router


app = FastAPI(title="Post CRUD")

app.include_router(post_router)
