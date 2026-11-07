"""data/posts/*.md 를 청크로 잘라 임베딩 후 ChromaDB에 저장.

사용: python -m app.ingest
"""
from app import config
from app.chunking import chunk_file
from app.embeddings import get_embedder
from app.store import get_collection

BATCH = 32


def main():
    files = sorted(config.POSTS_DIR.glob("**/*.md"))
    if not files:
        raise SystemExit(f"마크다운 파일이 없습니다: {config.POSTS_DIR}")

    chunks = [c for f in files for c in chunk_file(f, config.CHUNK_SIZE, config.CHUNK_OVERLAP)]
    print(f"파일 {len(files)}개 → 청크 {len(chunks)}개")

    col = get_collection(reset=True)
    embedder = get_embedder()
    for i in range(0, len(chunks), BATCH):
        batch = chunks[i : i + BATCH]
        col.add(
            ids=[c.id for c in batch],
            documents=[c.text for c in batch],
            embeddings=embedder.embed([c.text for c in batch]),
            metadatas=[c.metadata for c in batch],
        )
        print(f"  저장 {min(i + BATCH, len(chunks))}/{len(chunks)}")
    print(f"완료: {config.CHROMA_DIR}")


if __name__ == "__main__":
    main()
