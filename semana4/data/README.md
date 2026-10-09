# Datos — orden correcto (antes del EDA)

**No empezar por el EDA.** Primero hay que conseguir, extraer y organizar. El EDA valida que lo colocado esté bien.

```text
1. Catálogo de fuentes   data/sources/catalog_sources.yaml
2. Descarga pública      data/raw/public_documents/
3. Extracción            data/interim/extracted_text/
4. Inventario            data/processed/corpus/inventario_documental.csv
5. Banco piloto          data/processed/question_bank/consultas_piloto.csv
6. Sintéticos            data/synthetic/…
7. EDA (después)         notebooks/02_… y reports/eda/
```

## Portales UMA

| Portal | URL |
|--------|-----|
| Reglamentos | https://uma.edu.pe/resolucion-reglamentos/ |
| FAQ | https://uma.edu.pe/preguntas-frecuentes/ |
| Transparencia | https://uma.edu.pe/transparencia2026/ |

## Tres datasets de la tesis

| Dataset | Qué es | Dónde |
|---------|--------|-------|
| Documental | Reglamentos, calendarios, mallas | `raw/` → `interim/` → `processed/corpus/` |
| Consultas | Preguntas + gold | `processed/question_bank/` (+ drafts en `synthetic/`) |
| Experimental | Resultados A0–A5 | `../experiments/results/` (aún vacío) |

## Cómo llenar `data/`

```bash
cd tesis-routing-universitario
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m thesis_routing.pipeline.prepare_data
```

Eso:

1. Lee `sources/catalog_sources.yaml` (IDs D001… + URLs reales).
2. Descarga PDFs/HTML públicos a `raw/public_documents/`.
3. Extrae texto a `interim/extracted_text/`.
4. Escribe `processed/corpus/inventario_documental.csv`.
5. Arma piloto `consultas_piloto.csv` (FAQ curada) + drafts sintéticos.
6. Genera perfiles demo y grafo de malla **placeholder** (no es la malla oficial).

## Qué falta (institucional)

- Malla vigente Facultad de Ingeniería y Negocios.
- Calendario académico actual.
- Validación experta del banco (draft → validated).
- Consultas reales anonimizadas (solo con autorización).
- Docs autorizados no públicos → `raw/authorized_documents/` (**no versionar**).

## Reglas

- No inventar metadatos: si no hay año/páginas, medir del archivo.
- Preguntas sintéticas ≠ representatividad estadística; marcar `validacion_experta=draft`.
- Gold verificable contra documento o grafo.
- Separar público vs autorizado.
