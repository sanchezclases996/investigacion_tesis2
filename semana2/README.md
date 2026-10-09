# Semana 2 — Pipeline experimental reproducible

Diseño del flujo para el plan: asistente de consultas académicas-administrativas con enrutamiento predictivo (caso UMA–SJL, Facultad de Ingeniería y Negocios). Doce fases: definición → informe.

| Archivo | Rol |
|---------|-----|
| `flujo-reproducible-semana2.tex` | Fuente editable |
| `flujo-reproducible-semana2.pdf` | Entregable |

Alineado con `3_Sustentacion/2_plan_tesis/4_informe/Plan-tesis-nuevo/ppt/ppt_eleccion_tema.tex` (estrategias A0–A5, tipos N/R/M/A).

```bash
cd semana2
latexmk -xelatex -interaction=nonstopmode flujo-reproducible-semana2.tex
latexmk -c -xelatex flujo-reproducible-semana2.tex
```
