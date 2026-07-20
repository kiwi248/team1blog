#각자성함으로 파일명 바꿔서 깃헙에 올려주세요. ex)ykw.py
# app/main.py
from fastapi import FastAPI
from app.routers.chat_router import chat_router

app = FastAPI()
app.include_router(chat_router)