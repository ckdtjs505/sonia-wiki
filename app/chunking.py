"""마크다운 → 청크 분할.

전략: ① 프론트매터에서 제목·URL 추출 → ② '#' 헤딩 단위로 섹션 분리
→ ③ 섹션이 길면 CHUNK_SIZE 글자로 자르되 CHUNK_OVERLAP만큼 겹치게.
헤딩 기준으로 먼저 자르는 이유: 한 청크에 한 주제만 담겨야 검색 정확도가 올라가기 때문.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    """--- key: value --- 형태의 간단한 프론트매터만 지원."""
    if not raw.startswith("---"):
        return {}, raw
    end = raw.find("\n---", 3)
    if end == -1:
        return {}, raw
    meta = {}
    for line in raw[3:end].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("\"'")
    return meta, raw[end + 4 :].lstrip()


def split_sections(body: str) -> list[tuple[str, str]]:
    """(헤딩, 본문) 목록. 첫 헤딩 앞의 글은 헤딩 ''으로."""
    matches = list(HEADING_RE.finditer(body))
    if not matches:
        return [("", body.strip())]
    sections = []
    if matches[0].start() > 0:
        sections.append(("", body[: matches[0].start()].strip()))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections.append((m.group(2).strip(), body[m.end() : end].strip()))
    return [(h, t) for h, t in sections if t]


def split_long(text: str, size: int, overlap: int) -> list[str]:
    if len(text) <= size:
        return [text]
    parts, start = [], 0
    while start < len(text):
        parts.append(text[start : start + size])
        if start + size >= len(text):
            break
        start += size - overlap
    return parts


def chunk_file(path: Path, size: int, overlap: int) -> list[Chunk]:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    title = meta.get("title", path.stem)
    url = meta.get("url", "")
    chunks = []
    for s_idx, (heading, text) in enumerate(split_sections(body)):
        for p_idx, piece in enumerate(split_long(text, size, overlap)):
            # 헤딩·제목을 본문 앞에 붙여 임베딩에 문맥을 준다
            context = f"[{title}] {heading}\n{piece}" if heading else f"[{title}]\n{piece}"
            chunks.append(
                Chunk(
                    id=f"{path.stem}-{s_idx}-{p_idx}",
                    text=context,
                    metadata={"title": title, "url": url, "heading": heading, "source": path.name},
                )
            )
    return chunks
