"""검색 품질 평가: 질문마다 정답 문서가 Top-k 안에 들어오는지(hit rate)와 MRR을 계산.

사용: python -m eval.run_eval [--k 3]
questions.jsonl 한 줄 형식: {"q": "질문", "source": "정답 파일명.md"}
LLM을 부르지 않으므로 API 비용 없이 청크 크기·임베딩 모델을 비교할 수 있다.
"""
import argparse
import json
from pathlib import Path

from app.store import search

QFILE = Path(__file__).parent / "questions.jsonl"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--k", type=int, default=3)
    k = p.parse_args().k

    rows = [json.loads(l) for l in QFILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    hits, rr = 0, 0.0
    for r in rows:
        sources = [h["metadata"]["source"] for h in search(r["q"], k)]
        rank = sources.index(r["source"]) + 1 if r["source"] in sources else None
        hits += rank is not None
        rr += 1 / rank if rank else 0
        print(f"{'✅' if rank else '❌'} rank={rank or '-':<2} {r['q']}")

    n = len(rows)
    print(f"\nHit@{k}: {hits}/{n} = {hits / n:.0%}   MRR: {rr / n:.3f}")


if __name__ == "__main__":
    main()
