"""FastAPI 서버. 실행: uvicorn app.main:app --reload"""
import html
import json
import re
import time
from collections import defaultdict, deque

import openai
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, Response
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


# shortcut: 질문별 답을 파일에 영구 캐시하고 글이 바뀌어도 지우지 않음, 답이 낡으면 .cache/cards.json을 지울 것
CARDS = config.ROOT / ".cache" / "cards.json"


def _card_svg(q: str, a: str, sources: list[str]) -> str:
    a = re.sub(r"[*`#>]|\[\d+\]", "", a).strip()  # 마크다운·인용 번호는 이미지에서 읽기 어려워 뺀다
    a = re.sub(r"\n\s*\n+", "\n", re.sub(r"(?m)^\s*[-*]\s+", "• ", a))
    e = html.escape
    src = " · ".join(dict.fromkeys(sources)) or "-"
    # foreignObject로 HTML을 넣어 줄바꿈·말줄임을 브라우저에 맡긴다 (SVG text는 자동 줄바꿈이 없음)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="250" viewBox="0 0 800 250">
<style>
.c{{box-sizing:border-box;width:800px;height:250px;padding:20px 24px;border:1px solid #d0d7de;border-radius:12px;
background:#fff;color:#1f2328;font:14px/1.6 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Segoe UI","Noto Sans KR",sans-serif}}
.q{{font-weight:700;font-size:16px;margin-bottom:8px}}
.a{{display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden;white-space:pre-line}}
.s{{margin-top:10px;font-size:12px;color:#59636e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
@media (prefers-color-scheme:dark){{.c{{background:#0d1117;color:#e6edf3;border-color:#30363d}}.s{{color:#9198a1}}}}
</style>
<foreignObject width="800" height="250"><div xmlns="http://www.w3.org/1999/xhtml" class="c">
<div class="q">💬 {e(q)}</div><div class="a">{e(a)}</div><div class="s">출처: {e(src)} — sonia-wiki</div>
</div></foreignObject></svg>"""


@app.get("/card.svg")
def card(request: Request, q: str = Query(..., min_length=1, max_length=200)):
    """README에 이미지로 넣는 답변 카드. GitHub 이미지 프록시는 몇 초 안에 끊으므로 캐시된 답만 빠르게 준다."""
    cache = json.loads(CARDS.read_text()) if CARDS.exists() else {}
    if q not in cache:
        # 캐시에 없으면 LLM을 부르므로 /ask와 같은 전체 한도를 건다
        ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[-1].strip()
        if not _allow("*", config.RATE_LIMIT_TOTAL) or not _allow(ip, config.RATE_LIMIT_PER_IP):
            raise HTTPException(429, "too many requests")
        r = answer(q)
        cache[q] = {"answer": r["answer"], "sources": [s.get("title", "") for s in r["sources"]]}
        CARDS.parent.mkdir(exist_ok=True)
        CARDS.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
    c = cache[q]
    return Response(_card_svg(q, c["answer"], c["sources"]), media_type="image/svg+xml",
                    headers={"Cache-Control": "no-cache, max-age=0"})
