# Semana 4 — Datos primero (UMA)

Copia de `semana3/tesis-routing-universitario` centrada en **llenar y organizar `data/`** antes del EDA (como indica GPT en `temppp/`).

## Orden

1. Catálogo + URLs → `data/sources/catalog_sources.yaml`
2. Descarga → `data/raw/public_documents/` (12 fuentes UMA)
3. Extracción → `data/interim/`
4. Inventario + banco piloto + sintéticos → `data/processed/` y `data/synthetic/`
5. **Después** EDA (cuando el inventario esté bien)

Estado listo para exponer: `data/STATUS.md`

```bash
source .venv/bin/activate   # o: python3.11 -m venv .venv && pip install -e ".[dev]"
make data
```
