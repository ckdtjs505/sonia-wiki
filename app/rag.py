"""검색 결과로 프롬프트를 조립하고 Gemini에게 답변을 받는다."""
from google import genai
from google.genai import types

from app import config
from app.store import search

SYSTEM_PROMPT = """당신은 개발자 '소니아'의 개인 위키 도우미입니다.
반드시 아래 <context>에 있는 내용만 근거로 한국어로 답하세요.
근거로 쓴 문단은 [1], [2]처럼 번호로 인용하세요.
마크다운(**굵게**, # 제목 등) 없이 평문으로 답하세요. 화면이 마크다운을 그리지 않습니다.
<context>에 답이 없으면 지어내지 말고 "위키에서 찾지 못했어요."라고 답하세요."""


def build_context(hits: list[dict]) -> str:
    return "\n\n".join(f"[{i + 1}] {h['text']}" for i, h in enumerate(hits))


def answer(question: str, k: int = config.TOP_K) -> dict:
    hits = search(question, k)
    if not hits:
        return {"answer": "위키가 비어 있어요. 먼저 ingest를 실행하세요.", "sources": []}

    client = genai.Client()  # GEMINI_API_KEY 환경 변수를 읽음
    resp = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=f"<context>\n{build_context(hits)}\n</context>\n\n질문: {question}",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    text = resp.text or "답변을 받지 못했어요."
    sources = [
        {"n": i + 1, "score": h["score"], **h["metadata"], "snippet": h["text"][:200]}
        for i, h in enumerate(hits)
    ]
    return {"answer": text, "sources": sources}
