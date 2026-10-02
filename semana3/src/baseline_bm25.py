"""Baseline BM25 de retrieval: Recall@k y MRR (k=5 vs k=20)."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from bm25 import BM25, tokenize
from datautil import gold_text, load_chunks, load_eval, repo_semana3

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger("baseline")


def mean(xs: list[float]) -> float:
    return sum(xs) / max(len(xs), 1)


def evaluate(rows: list[dict], chunks: list, ks: list[int]) -> dict:
    """Evalúa BM25: un hit si el gold aparece en algún chunk del top-k."""
    docs_tok = [tokenize(c.text) for c in chunks]
    index = BM25(docs_tok)
    per_k = {k: {"hits": 0, "rr": []} for k in ks}
    max_k = max(ks)

    for row in rows:
        q = tokenize(row.get("prompt") or "")
        gold = gold_text(row).strip()
        ranked = index.top_k(q, max_k)
        texts = [chunks[i].text for i, _ in ranked]
        # rango del primer chunk que contiene el gold (1-based); 0 si no aparece
        rank = 0
        for rnk, txt in enumerate(texts, start=1):
            if gold and gold in txt:
                rank = rnk
                break
        for k in ks:
            if 0 < rank <= k:
                per_k[k]["hits"] += 1
                per_k[k]["rr"].append(1.0 / rank)
            else:
                per_k[k]["rr"].append(0.0)

    n = len(rows)
    out = {"n": n, "n_chunks": len(chunks), "by_k": {}}
    for k in ks:
        out["by_k"][str(k)] = {
            "recall_at_k": round(per_k[k]["hits"] / max(n, 1), 4),
            "mrr": round(mean(per_k[k]["rr"]), 4),
            "hits": per_k[k]["hits"],
        }
    return out


def main() -> None:
    """Corre baseline, escribe log y JSON de métricas."""
    root = repo_semana3()
    cfg = json.loads((root / "config" / "baseline.json").read_text(encoding="utf-8"))
    rows = load_eval(root / "data" / "eval" / "eval_sample.jsonl")
    chunks = load_chunks(root / "data" / "corpus")
    ks = list(cfg.get("ks", [5, 20]))
    seed = cfg.get("seed", 42)

    metrics = evaluate(rows, chunks, ks)
    metrics["seed"] = seed
    metrics["baseline"] = "BM25"
    metrics["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    metrics["config"] = cfg

    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "metrics_baseline.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    lines = [
        f"timestamp_utc={metrics['timestamp_utc']}",
        f"baseline=BM25",
        f"seed={seed}",
        f"n_eval={metrics['n']}",
        f"n_chunks={metrics['n_chunks']}",
    ]
    for k, vals in metrics["by_k"].items():
        lines.append(
            f"k={k} recall@{k}={vals['recall_at_k']} mrr={vals['mrr']} hits={vals['hits']}"
        )
    text = "\n".join(lines) + "\n"
    (logs / "metrics_baseline.txt").write_text(text, encoding="utf-8")
    LOG.info("Baseline listo:\n%s", text)


if __name__ == "__main__":
    main()
