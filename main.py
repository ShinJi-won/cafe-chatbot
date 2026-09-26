from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from rag_engine import CafeRAGBot

app = FastAPI(title="카페 AI 챗봇")

bot = CafeRAGBot()


@app.on_event("startup")
def startup_event():
    # 서버 켜질 때 FAQ 임베딩을 미리 만들어둠 (매 질문마다 다시 만들지 않도록)
    bot.build_index()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = bot.answer(req.message)
    return ChatResponse(reply=reply)


# 정적 파일(간단한 테스트용 채팅 화면) 서빙
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root():
    return FileResponse(os.path.join(static_dir, "index.html"))
