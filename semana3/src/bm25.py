"""BM25 Okapi mínimo (sin dependencias externas) para baseline de retrieval."""

from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN = re.compile(r"[a-z0-9_\.]+")
_STOP = {
    "the", "a", "an", "of", "to", "and", "or", "in", "on", "for", "is", "are", "with", "by",
    "de", "la", "el", "en", "y", "o", "que", "del", "los", "las", "un", "una", "se", "al",
    "según", "documentación", "documento", "sección", "cita", "oración", "exacta", "texto",
    "responde", "citando", "qué", "cómo", "indica", "sobre", "con", "para", "es", "su",
}


def tokenize(text: str) -> list[str]:
    """Tokeniza en minúsculas y elimina stopwords cortas."""
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 1]


class BM25:
    """Índice BM25 Okapi sobre documentos ya tokenizados."""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.n = len(docs)
        self.doc_len = [len(d) for d in docs]
        self.avg_len = sum(self.doc_len) / max(self.n, 1)
        self.tf: list[Counter[str]] = [Counter(d) for d in docs]
        df: Counter[str] = Counter()
        postings: dict[str, list[int]] = {}
        for i, d in enumerate(docs):
            uniq = set(d)
            df.update(uniq)
            for t in uniq:
                postings.setdefault(t, []).append(i)
        self.postings = postings
        self.idf = {
            t: math.log(1 + (self.n - f + 0.5) / (f + 0.5)) for t, f in df.items()
        }

    def score(self, query: list[str], i: int) -> float:
        s = 0.0
        tf, dl = self.tf[i], self.doc_len[i]
        for t in query:
            if t not in tf:
                continue
            f = tf[t]
            denom = f + self.k1 * (1 - self.b + self.b * dl / self.avg_len)
            s += self.idf.get(t, 0.0) * f * (self.k1 + 1) / denom
        return s

    def top_k(self, query: list[str], k: int) -> list[tuple[int, float]]:
        cand: set[int] = set()
        for t in set(query):
            cand.update(self.postings.get(t, ()))
        scored = sorted(
            ((i, self.score(query, i)) for i in cand), key=lambda x: -x[1]
        )
        return scored[:k]
