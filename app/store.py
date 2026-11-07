"""ChromaDB 래퍼. 임베딩은 직접 계산해서 넣는다(제공자 교체를 쉽게 하기 위해)."""
import chromadb

from app import config
from app.embeddings import get_embedder


def get_collection(reset: bool = False):
    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(config.COLLECTION)
        except Exception:
            pass
    # 코사인 거리 사용 (임베딩을 정규화하므로 내적과 동일)
    return client.get_or_create_collection(config.COLLECTION, metadata={"hnsw:space": "cosine"})


def search(query: str, k: int = config.TOP_K) -> list[dict]:
    col = get_collection()
    q_emb = get_embedder().embed([query])[0]
    res = col.query(query_embeddings=[q_emb], n_results=k)
    hits = []
    for i in range(len(res["ids"][0])):
        hits.append(
            {
                "id": res["ids"][0][i],
                "text": res["documents"][0][i],
                "metadata": res["metadatas"][0][i],
                "score": round(1 - res["distances"][0][i], 4),  # 코사인 유사도
            }
        )
    return hits
