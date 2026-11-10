"""환경 변수 기반 설정. .env 파일을 읽어 옵니다."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# 데이터·DB 경로
POSTS_DIR = Path(os.getenv("POSTS_DIR", ROOT / "data" / "posts"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", ROOT / ".chroma"))
COLLECTION = os.getenv("COLLECTION", "sonia_wiki")

# 임베딩: "local"(bge-m3) 또는 "openai"
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local")
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "BAAI/bge-m3")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# LLM
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# 청크·검색 파라미터
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))      # 글자 수
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
TOP_K = int(os.getenv("TOP_K", 4))
