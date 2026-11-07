"""FastAPI 서버. 실행: uvicorn app.main:app --reload"""
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app import config
from app.rag import answer
from app.store import search

app = FastAPI(title="Sonia Wiki", description="RAG 기반 개인 위키 Q&A")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    k: int = Field(config.TOP_K, ge=1, le=10)


@app.get("/")
def index():
    return FileResponse(config.ROOT / "web" / "index.html")


@app.post("/ask")
def ask(req: AskRequest):
    return answer(req.question, req.k)


@app.get("/search")
def search_only(q: str, k: int = config.TOP_K):
    """LLM 없이 검색 결과만 확인 (디버깅·평가용)."""
    return search(q, k)


@app.get("/health")
def health():
    return {"ok": True, "embedding": config.EMBEDDING_PROVIDER}
