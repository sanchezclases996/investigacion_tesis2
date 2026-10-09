# Estado de datos (semana 4) — para exposición

Fecha de corrida: 2026-10-09. Caso: UMA–SJL.

## Orden aplicado (antes del EDA)

1. Catálogo con URLs → `sources/catalog_sources.yaml`
2. Descarga pública → `raw/public_documents/` (D001–D012)
3. Extracción → `interim/extracted_text/`
4. Inventario → `processed/corpus/inventario_documental.csv`
5. Banco piloto + drafts FAQ → `processed/question_bank/` y `synthetic/`
6. Perfiles + grafo malla **demo** → `synthetic/synthetic_profiles/` (no es malla oficial)

**EDA:** siguiente paso, cuando el inventario y el banco estén revisados.

## Corpus documental (12 fuentes)

| ID | Documento | Extracción |
|----|-----------|------------|
| D001 | Reglamento académico | ok (~16 p.) |
| D002 | Reglamento de matrícula | ok |
| D003 | Reglamento general UMA 2025 | ok |
| D004 | Reglamento económico | ok |
| D005 | Grados y títulos | ok |
| D006 | Admisión pregrado | ok |
| D007 | Becas | ok |
| D008 | Tutoría | ok |
| D009 | Convalidaciones | ok |
| D010 | Proceso matrícula (guía) | **weak_or_scanned** (poco texto) |
| D011 | Tarifario 2025 | ok |
| D012 | FAQ HTML | ok |

Portales: [reglamentos](https://uma.edu.pe/resolucion-reglamentos/), [FAQ](https://uma.edu.pe/preguntas-frecuentes/), [transparencia](https://uma.edu.pe/transparencia2026/).

## Banco de consultas

| Archivo | N | Estado |
|---------|---|--------|
| `processed/question_bank/consultas_piloto.csv` | 15 | `validacion_experta=draft` |
| `synthetic/generated_questions/consultas_desde_faq.csv` | ~40 | solo preguntas FAQ, sin gold |

No atribuir representatividad estadística a preguntas sintéticas/draft.

## Pendiente institucional

- Malla vigente Facultad de Ingeniería y Negocios
- Calendario académico actual
- Validadores (académico + administrativo)
- Consultas reales anonimizadas (autorización)
- Reemplazar grafo demo por malla oficial estructurada

## Cómo regenerar

```bash
cd tesis-routing-universitario
source .venv/bin/activate
python -m thesis_routing.pipeline.prepare_data
```
