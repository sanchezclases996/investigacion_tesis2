# Semana 3 — EDA y baseline BM25

Pipeline de tipo LLM + RAG. En esta etapa se documenta el estado de los datos y un baseline léxico de recuperación.

## Layout

- `data/` — muestra del corpus e ítems de evaluación (`DATA_MANIFEST.json` con hash por archivo)
- `src/` — EDA y baseline BM25
- `config/baseline.json` — seed y valores de top-k
- `logs/` — métricas del baseline
- `reports/` — figuras y conclusiones del EDA

## Dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
PYTHONPATH=src python src/eda.py
PYTHONPATH=src python src/baseline_bm25.py
```

## Baseline

- Recuperación: BM25
- Comparación: top-k ∈ {5, 20}
- Métricas: Recall@k, MRR (acierto si el gold aparece en el contexto recuperado)
- Muestra: N = 120 (50 S1 / 50 S2 / 20 PII), seed 42
