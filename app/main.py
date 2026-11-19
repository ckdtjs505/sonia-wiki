"""FastAPI 서버. 실행: uvicorn app.main:app --reload"""
import time
from collections import defaultdict, deque

import openai
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from google.genai import errors
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


# shortcut: 메모리에만 두고 IP 키를 지우지 않음, 방문자가 아주 많아지면 Redis 등으로 옮길 것
_hits: dict[str, deque] = defaultdict(deque)


def _allow(key: str, limit: int, window: float = 60) -> bool:
    now, q = time.monotonic(), _hits[key]
    while q and now - q[0] > window:
        q.popleft()
    if len(q) >= limit:
        return False
    q.append(now)
    return True


@app.post("/ask")
def ask(req: AskRequest, request: Request):
    # 서버는 127.0.0.1에만 열려 있어 Funnel을 거친 요청뿐이다. 프록시가 덧붙인 맨 뒤 IP가 실제 방문자
    ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[-1].strip()
    if not _allow("*", config.RATE_LIMIT_TOTAL):
        raise HTTPException(429, "지금 질문이 몰려 있어요. 1분 뒤에 다시 시도해 주세요.")
    if not _allow(ip, config.RATE_LIMIT_PER_IP):
        raise HTTPException(429, f"1분에 {config.RATE_LIMIT_PER_IP}번까지 물어볼 수 있어요. 잠시 뒤에 다시 시도해 주세요.")
    try:
        return answer(req.question, req.k)
    except errors.APIError as e:  # 키·크레딧·모델 이름 문제를 화면에 그대로 보여 준다
        raise HTTPException(502, f"Gemini 오류 {e.code}: {e.message}")
    except openai.APIError as e:  # Ollama가 꺼져 있거나 모델을 안 받았을 때
        raise HTTPException(502, f"로컬 LLM 오류: {e.message}")


@app.get("/search")
def search_only(q: str, k: int = config.TOP_K):
    """LLM 없이 검색 결과만 확인 (디버깅·평가용)."""
    return search(q, k)


@app.get("/health")
def health():
    return {"ok": True, "embedding": config.EMBEDDING_PROVIDER}
