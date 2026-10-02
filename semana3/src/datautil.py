"""Utilidades compartidas: carga de corpus/eval y chunking simple por sección."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

SECTION_SPLIT = re.compile(r"(?m)^(#{1,3}\s+.+)$")


@dataclass(frozen=True)
class Chunk:
    """Fragmento indexable del corpus."""

    doc_id: str
    chunk_id: str
    text: str


def repo_semana3() -> Path:
    """Raíz de ``semana3/`` (padre de ``src/``)."""
    return Path(__file__).resolve().parents[1]


def load_eval(path: Path) -> list[dict]:
    """Lee un JSONL de evaluación."""
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def clean_markdown(text: str) -> str:
    """Limpieza ligera de Markdown/HTML para indexar."""
    text = re.sub(r"(?s)```.*?```", " ", text)
    text = re.sub(r"`[^`]+`", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def chunk_document(doc_id: str, text: str, max_chars: int = 1200) -> list[Chunk]:
    """Parte por encabezados Markdown; si un bloque es largo, corta por tamaño."""
    text = clean_markdown(text)
    parts = SECTION_SPLIT.split(text)
    blocks: list[str] = []
    buf = ""
    for part in parts:
        if SECTION_SPLIT.match(part or ""):
            if buf.strip():
                blocks.append(buf.strip())
            buf = part
        else:
            buf += "\n" + (part or "")
    if buf.strip():
        blocks.append(buf.strip())
    if not blocks:
        blocks = [text]

    chunks: list[Chunk] = []
    n = 0
    for block in blocks:
        if len(block) <= max_chars:
            pieces = [block]
        else:
            pieces = [
                block[i : i + max_chars] for i in range(0, len(block), max_chars)
            ]
        for piece in pieces:
            if len(piece.strip()) < 40:
                continue
            chunks.append(Chunk(doc_id=doc_id, chunk_id=f"{doc_id}#c{n}", text=piece))
            n += 1
    return chunks


def load_chunks(corpus_dir: Path) -> list[Chunk]:
    """Carga todos los ``.md``/``.html`` bajo ``corpus_dir`` como chunks."""
    chunks: list[Chunk] = []
    for path in sorted(corpus_dir.rglob("*")):
        if path.suffix.lower() not in {".md", ".html", ".htm", ".txt"}:
            continue
        if path.name.startswith("README"):
            continue
        rel = path.relative_to(corpus_dir).as_posix()
        raw = path.read_text(encoding="utf-8", errors="ignore")
        chunks.extend(chunk_document(rel, raw))
    return chunks


def gold_text(row: dict) -> str:
    """Gold verbatim (oración o rúbrica unida)."""
    if row.get("gold_quote"):
        return str(row["gold_quote"])
    rubric = row.get("gold_rubric") or []
    if isinstance(rubric, list):
        return " ".join(str(x) for x in rubric)
    return str(rubric)
