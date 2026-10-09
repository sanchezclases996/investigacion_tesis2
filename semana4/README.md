# tesis-routing-universitario (semana 4 — foco data)

Asistente de consultas académicas-administrativas con enrutamiento predictivo.

**Caso:** Facultad de Ingeniería y Negocios, UMA (SJL).

## Semana 4: data antes del EDA

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m thesis_routing.pipeline.prepare_data
```

Salidas principales:

| Artefacto | Ruta |
|-----------|------|
| Catálogo URL | `data/sources/catalog_sources.yaml` |
| PDFs/HTML | `data/raw/public_documents/` |
| Texto extraído | `data/interim/extracted_text/` |
| Inventario | `data/processed/corpus/inventario_documental.csv` |
| Banco piloto | `data/processed/question_bank/consultas_piloto.csv` |
| Perfiles demo | `data/synthetic/synthetic_profiles/perfiles_demo.json` |

Detalle: [`data/README.md`](data/README.md).

## Estrategias A0–A5

A0 base · A1 RAG · A2 FT (si viable) · A3 RAG+tools · A4 compuesta fija · A5 routing.
