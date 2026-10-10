# investigacion2

Proyecto de Investigación II — Maestría en Ciencias con mención en Inteligencia Artificial (FIIS–UNI).

Tema: asistente de consultas académicas-administrativas con enrutamiento predictivo (caso UMA–SJL).

## Carpetas

| Ruta | Contenido |
|------|-----------|
| `semana2/` | Diseño del pipeline experimental (doce fases, A0–A5) |
| `semana3/` | Esqueleto previo / baseline BM25 |
| `semana4/` | Corpus UMA, banco piloto y EDA preliminar |

## Semana 4

```bash
cd semana4
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make eda
```

Documentación de partida: `semana4/README.md` y `semana4/reports/eda/`.
