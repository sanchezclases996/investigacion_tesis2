# investigacion2

Proyecto de Investigación II — Maestría en Ciencias con mención en Inteligencia Artificial (FIIS–UNI).

Arquitectura híbrida *edge–cloud* para un asistente técnico GenAI (LLM + RAG) sobre documentación de Azure AI Foundry y Amazon Bedrock.

## Contenido

| Ruta | Descripción |
|------|-------------|
| `semana2/` | Diseño del pipeline reproducible |
| `semana3/` | Análisis exploratorio y baseline de retrieval (BM25) |

## Reproducibilidad (semana 3)

```bash
cd semana3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python src/eda.py
PYTHONPATH=src python src/baseline_bm25.py
```

Resultados en `semana3/logs/` y `semana3/reports/`. Configuración en `semana3/config/baseline.json` (seed 42).
