# Datos

## Capas

| Capa | Ruta | Contenido |
|------|------|-----------|
| Raw público | `raw/public_documents/` | Reglamentos/calendarios/mallas públicos |
| Raw autorizado | `raw/authorized_documents/` | Solo con permiso; **no versionar** |
| Interim | `interim/` | Texto extraído y metadatos |
| Processed | `processed/` | Corpus, banco, gold, splits |
| Synthetic | `synthetic/` | Preguntas/perfiles demo |

## Reglas

1. Inventario con URL, fecha, hash y restricciones de uso.
2. Separar público vs autorizado no público.
3. No subir PII ni `.env`.
4. Gold verificable contra documento o grafo de malla.
