"""임베딩 제공자 추상화. 설정 한 줄로 로컬 모델 ↔ OpenAI를 바꿉니다."""
from functools import lru_cache

from app import config


class Embedder:
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


class LocalEmbedder(Embedder):
    """sentence-transformers로 로컬 다국어 모델(기본 bge-m3)을 사용. 무료, 첫 실행 시 모델 다운로드."""

    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()


class OpenAIEmbedder(Embedder):
    """OpenAI 임베딩 API. OPENAI_API_KEY 필요."""

    def __init__(self, model_name: str):
        from openai import OpenAI

        self.client = OpenAI()
        self.model_name = model_name

    def embed(self, texts):
        res = self.client.embeddings.create(model=self.model_name, input=texts)
        return [d.embedding for d in res.data]


@lru_cache
def get_embedder() -> Embedder:
    if config.EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbedder(config.OPENAI_EMBEDDING_MODEL)
    return LocalEmbedder(config.LOCAL_EMBEDDING_MODEL)
