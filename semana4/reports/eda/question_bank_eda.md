# EDA del banco piloto de consultas

- Consultas en el piloto: **196**, con `validacion_experta=draft`.
- Por categoría N/R/M/A: `{'A': 44, 'M': 11, 'N': 125, 'R': 16}`.
- Por complejidad: `{'baja': 107, 'media': 65, 'alta': 24}`.
- Requieren herramienta (malla/tools): **16**.
- Requieren múltiples fuentes: **11**.
- Marcadas como respondibles con la evidencia actual: **193** / 196.
- Estrategia candidata (etiqueta de diseño): `{'A1': 125, 'A5': 44, 'A3': 27}`.

Figuras: `eda_qb_categoria.png`, `eda_qb_complejidad.png`.

## Observaciones (para decisión)

1. El piloto ya cubre N/R/M/A, pero está **sesgado a N**. Evaluar A0–A5 por estrato, no solo con un promedio global.
2. Muchas preguntas anclan en D012 (FAQ). Mantener un bloque anclado a reglamentos para no sobreajustar a la FAQ.
3. Todo está en `draft`. Validar primero un subconjunto (40–50) antes de crecer a 300–500.
4. `es_respondible` ≈ ancla en corpus usable (193/196); completar `respuesta_esperada` sigue pendiente en muchas filas.
5. R y M son pocas a propósito: faltan malla oficial y evidencia multi-fuente. No inflar con preguntas inventadas.

## Limitación

Este banco no se presenta como muestra estadísticamente representativa.
