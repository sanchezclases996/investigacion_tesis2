# Contribuir

## Reglas

1. Trabajar en una rama; no subir `.env`, docs autorizados ni PII.
2. Tipado en Python 3.11+; docstrings NumPy/Google en módulos de `src/`.
3. Cada módulo nuevo en `src/` lleva test en `tests/`.
4. Sin `print()` de secretos; usar `logging`.
5. Decisiones de diseño relevantes van en `docs/decisions/`.

## Flujo local

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
```

## Commits

Mensajes cortos en español o inglés, enfocados en el *por qué*.
