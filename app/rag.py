"""검색 결과로 프롬프트를 조립하고 Claude에게 답변을 받는다."""
from anthropic import Anthropic

from app import config
from app.store import search

SYSTEM_PROMPT = """당신은 개발자 '소니아'의 개인 위키 도우미입니다.
반드시 아래 <context>에 있는 내용만 근거로 한국어로 답하세요.
근거로 쓴 문단은 [1], [2]처럼 번호로 인용하세요.
<context>에 답이 없으면 지어내지 말고 "위키에서 찾지 못했어요."라고 답하세요."""


def build_context(hits: list[dict]) -> str:
    return "\n\n".join(f"[{i + 1}] {h['text']}" for i, h in enumerate(hits))


def answer(question: str, k: int = config.TOP_K) -> dict:
    hits = search(question, k)
    if not hits:
        return {"answer": "위키가 비어 있어요. 먼저 ingest를 실행하세요.", "sources": []}

    client = Anthropic()
    msg = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"<context>\n{build_context(hits)}\n</context>\n\n질문: {question}",
            }
        ],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    sources = [
        {"n": i + 1, "score": h["score"], **h["metadata"], "snippet": h["text"][:200]}
        for i, h in enumerate(hits)
    ]
    return {"answer": text, "sources": sources}
