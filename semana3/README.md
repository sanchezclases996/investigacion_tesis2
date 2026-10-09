# tesis-routing-universitario

Repositorio reproducible del plan de tesis: asistente de consultas académicas-administrativas con enrutamiento predictivo.

**Caso:** Facultad de Ingeniería y Negocios, UMA (San Juan de Lurigancho).

**Pregunta:** ¿el routing predictivo de estrategias de IA mejora la relación calidad–latencia–costo frente a una estrategia fija?

## Estrategias (A0–A5)

| Código | Configuración |
|--------|----------------|
| A0 | Modelo base |
| A1 | RAG |
| A2 | Fine-tuning (si es viable) |
| A3 | RAG + herramientas (malla) |
| A4 | Estrategia compuesta fija |
| A5 | Routing predictivo |

## Inicio rápido

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

make eda
make prepare
# make experiment EXP=baseline   # cuando haya datos y API
```

## Layout

| Ruta | Rol |
|------|-----|
| `configs/` | Parámetros versionados (datos, retrieval, router, experimentos) |
| `data/` | Raw → interim → processed (sin secretos ni PII en git) |
| `src/thesis_routing/` | Código del pipeline |
| `experiments/` | Matriz, corridas y resultados |
| `reports/` | EDA, figuras y resúmenes |
| `docs/` | Protocolo, gobernanza y decisiones |
| `tests/` | Pytest por módulo |
| `scripts/` | Entradas shell reproducibles |

Detalle del flujo experimental: ver `docs/experimental_protocol.md` y el entregable de semana 2.

## Datos

No subir documentación autorizada ni consultas con PII. Ver `data/README.md` y `docs/data_governance.md`.
