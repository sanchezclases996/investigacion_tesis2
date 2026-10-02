# Conclusiones del EDA

1. **Chunking:** varios fragmentos superan el tamaño útil para BM25; conviene acotar por sección y caracteres antes de indexar de nuevo.
2. **Anclas en el prompt:** títulos y secciones en la consulta pueden inflar el retrieval; conviene una corrida ciega para medir el efecto.
3. **Top-k:** Recall@5 y Recall@20 difieren en el baseline; el k operativo debe fijarse según ese trade-off en `logs/metrics_baseline.txt`.
