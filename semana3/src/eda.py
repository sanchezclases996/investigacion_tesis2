"""EDA accionable del corpus y del banco de evaluación (Semana 3)."""

from __future__ import annotations

import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt

from datautil import gold_text, load_chunks, load_eval, repo_semana3

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger("eda")


def main() -> None:
    """Genera figuras, resumen JSON y conclusiones accionables."""
    root = repo_semana3()
    corpus_dir = root / "data" / "corpus"
    eval_path = root / "data" / "eval" / "eval_sample.jsonl"
    fig_dir = root / "reports" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    rows = load_eval(eval_path)
    chunks = load_chunks(corpus_dir)

    bloque = Counter(r["bloque"] for r in rows)
    vendor = Counter(r["vendor"] for r in rows)
    prompt_lens = [len(r.get("prompt") or "") for r in rows]
    gold_lens = [len(gold_text(r)) for r in rows]
    chunk_lens = [len(c.text) for c in chunks]
    docs = sorted({c.doc_id for c in chunks})

    # Fig 1: balance de bloques
    fig, ax = plt.subplots(figsize=(5, 3.2))
    labels = list(bloque.keys())
    vals = [bloque[k] for k in labels]
    ax.bar(labels, vals, color=["#4C78A8", "#F58518", "#54A24B"][: len(labels)])
    ax.set_title("Balance del banco de evaluación (bloques)")
    ax.set_ylabel("N ítems")
    fig.tight_layout()
    fig.savefig(fig_dir / "eda_balance_bloques.png", dpi=140)
    plt.close(fig)

    # Fig 2: longitudes
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.2))
    axes[0].hist(prompt_lens, bins=20, color="#4C78A8", edgecolor="white")
    axes[0].set_title("Longitud de prompts")
    axes[0].set_xlabel("caracteres")
    axes[1].hist(chunk_lens, bins=20, color="#F58518", edgecolor="white")
    axes[1].set_title("Longitud de chunks indexados")
    axes[1].set_xlabel("caracteres")
    fig.tight_layout()
    fig.savefig(fig_dir / "eda_longitudes.png", dpi=140)
    plt.close(fig)

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "n_eval": len(rows),
        "bloques": dict(bloque),
        "vendors": dict(vendor),
        "n_docs": len(docs),
        "n_chunks": len(chunks),
        "prompt_len_mean": round(sum(prompt_lens) / max(len(prompt_lens), 1), 1),
        "gold_len_mean": round(sum(gold_lens) / max(len(gold_lens), 1), 1),
        "chunk_len_mean": round(sum(chunk_lens) / max(len(chunk_lens), 1), 1),
        "chunk_len_max": max(chunk_lens) if chunk_lens else 0,
        "prompts_unicos": len({r["prompt"] for r in rows}),
        "golds_unicos": len({gold_text(r) for r in rows}),
        "riesgos": [
            "Prompts con ancla de página/sección pueden inflar retrieval frente a usuario real.",
            "Corpus bilingüe (docs EN, prompts ES): el BM25 léxico puede degradarse sin normalización.",
            "Muestra N=120; las métricas son de laboratorio, no el N=1000 definitivo.",
        ],
    }
    (reports / "eda_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    conclusiones = """# Conclusiones accionables del EDA (Semana 3)

1. **Ajustar chunking por sección** y tope de caracteres: hay chunks largos que diluyen BM25; recortar/partir mejora Recall@k medible en el baseline.
2. **Separar evaluación ciega**: correr una variante de prompts sin título/sección para medir dependencia de anclas verbales (riesgo de leakage de retrieval).
3. **Comparar top-k=5 vs top-k=20** en BM25 esta misma semana y elegir k para el siguiente sprint según Recall@k / MRR en `logs/metrics_baseline.txt`.
"""
    (reports / "eda_conclusiones.md").write_text(conclusiones, encoding="utf-8")
    LOG.info(
        "EDA listo: %s docs, %s chunks, %s ítems → reports/",
        len(docs),
        len(chunks),
        len(rows),
    )


if __name__ == "__main__":
    main()
