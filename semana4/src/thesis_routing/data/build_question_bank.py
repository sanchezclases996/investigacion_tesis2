"""Construye banco piloto de consultas a partir de FAQ y plantillas documentales."""

from __future__ import annotations

import csv
import logging
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

LOGGER = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[3]
FAQ_HTML = ROOT / "data" / "raw" / "public_documents" / "D012__faq.html"
OUT_CSV = ROOT / "data" / "processed" / "question_bank" / "consultas_piloto.csv"
OUT_SYN = ROOT / "data" / "synthetic" / "generated_questions" / "consultas_desde_faq.csv"

QueryType = Literal["N", "R", "M", "A"]
ValidationStatus = Literal["draft", "validated", "rejected", "no_verifiable_answer"]


class QuestionRecord(BaseModel):
    """Minimum schema for the evaluation bank (fase 5)."""

    query_id: str
    pregunta: str
    categoria: str
    complejidad: str = "media"
    doc_referencia: str = "D012"
    seccion_referencia: str = ""
    respuesta_esperada: str = ""
    requiere_herramienta: bool = False
    requiere_multiples_fuentes: bool = False
    es_respondible: bool = True
    validacion_experta: ValidationStatus = "draft"
    candidate_strategy: str | None = Field(default="A1")


SEED_FROM_FAQ: list[dict[str, str]] = [
    {
        "pregunta": "¿Qué modalidades de estudio tiene la UMA?",
        "respuesta": "Presencial, Semipresencial y A Distancia; varían según la carrera.",
        "categoria": "N",
        "complejidad": "baja",
    },
    {
        "pregunta": "¿Pueden deshabilitarme por inasistencias?",
        "respuesta": "Sí: hasta 30% de inasistencias a sesiones con horas lectivas implica desaprobación del curso (según FAQ/reglamento).",
        "categoria": "N",
        "complejidad": "media",
    },
    {
        "pregunta": "¿Qué es el examen sustitutorio y quiénes pueden acceder?",
        "respuesta": "Evaluación extraordinaria opcional que reemplaza la menor nota de parcial o final; se programa en la semana 17.",
        "categoria": "N",
        "complejidad": "media",
    },
    {
        "pregunta": "¿En qué consiste el curso o examen de aplazados?",
        "respuesta": "Trámite para recuperar asignaturas desaprobadas en el periodo regular inmediato anterior, con condiciones (no por inasistencias).",
        "categoria": "N",
        "complejidad": "alta",
    },
    {
        "pregunta": "¿Dónde reviso mis horarios de clase actualizados?",
        "respuesta": "En SIGU, opción matrícula (www.sigu.uma.edu.pe/alumno/entrar).",
        "categoria": "A",
        "complejidad": "baja",
        "candidate_strategy": "A5",
    },
    {
        "pregunta": "¿Qué hago si tengo cruce de horario o un curso no aparece en mi matrícula?",
        "respuesta": "Escribir a Coordinación Académica (coacademica@uma.edu.pe) con código y detalle.",
        "categoria": "A",
        "complejidad": "media",
        "candidate_strategy": "A5",
    },
    {
        "pregunta": "¿Cuánto cuesta el carné universitario y cómo lo solicito?",
        "respuesta": "S/30.00; registrar pedido en SIGU UMA.",
        "categoria": "A",
        "complejidad": "baja",
    },
    {
        "pregunta": "Perdí mi carné, ¿puedo solicitar otro?",
        "respuesta": "Sí, duplicado por SIGU adjuntando denuncia policial de pérdida/robo.",
        "categoria": "A",
        "complejidad": "media",
    },
    {
        "pregunta": "¿Cómo visualizo mi avance curricular?",
        "respuesta": "SIGU → Académica / Avance curricular.",
        "categoria": "R",
        "complejidad": "baja",
        "candidate_strategy": "A3",
    },
    {
        "pregunta": "¿Cuáles son los requisitos para tramitar el diploma de bachiller o título?",
        "respuesta": "Ver FAQ y Reglamento de grados y títulos (D005); validar lista vigente con fuente oficial.",
        "categoria": "M",
        "complejidad": "alta",
        "candidate_strategy": "A3",
        "doc_referencia": "D005",
    },
    {
        "pregunta": "¿Qué condiciones establece el reglamento de matrícula para matricularme?",
        "respuesta": "Pendiente: citar artículos del Reglamento general de matrícula (D002) tras revisión humana.",
        "categoria": "N",
        "complejidad": "media",
        "doc_referencia": "D002",
    },
    {
        "pregunta": "¿Qué dice el reglamento académico sobre evaluación y asistencia?",
        "respuesta": "Pendiente: contrastar D001 (reglamento académico) y FAQ D012; no inventar umbrales.",
        "categoria": "M",
        "complejidad": "alta",
        "doc_referencia": "D001",
        "candidate_strategy": "A1",
    },
    {
        "pregunta": "¿Cuáles son los prerrequisitos del curso C103 en la malla demo?",
        "respuesta": "Usar herramienta sobre grafo demo (no es la malla oficial UMA).",
        "categoria": "R",
        "complejidad": "media",
        "doc_referencia": "malla_demo_grafo",
        "candidate_strategy": "A3",
    },
    {
        "pregunta": "¿Puedo convalidar un curso cursado en otra universidad?",
        "respuesta": "Consultar Reglamento de convalidaciones (D009); respuesta gold pendiente de validación.",
        "categoria": "N",
        "complejidad": "alta",
        "doc_referencia": "D009",
    },
    {
        "pregunta": "¿Cómo solicito una beca y qué requisitos aplica el reglamento?",
        "respuesta": "Pendiente: D007 + canal institucional; posible derivación a persona.",
        "categoria": "A",
        "complejidad": "alta",
        "doc_referencia": "D007",
        "candidate_strategy": "A5",
    },
]


def _parse_faq_headings(html: str) -> list[str]:
    """Collect question-like headings from FAQ HTML."""
    # Prefer explicit FAQ questions already curated; HTML parse is best-effort.
    found = re.findall(r"¿[^?<]{8,160}\?", html)
    # Deduplicate preserving order
    seen: set[str] = set()
    out: list[str] = []
    for q in found:
        qn = re.sub(r"\s+", " ", q).strip()
        if qn not in seen:
            seen.add(qn)
            out.append(qn)
    return out


def build_pilot_bank() -> Path:
    """Write curated pilot CSV (+ optional FAQ-derived drafts)."""
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_SYN.parent.mkdir(parents=True, exist_ok=True)

    rows: list[QuestionRecord] = []
    for i, item in enumerate(SEED_FROM_FAQ, start=1):
        rows.append(
            QuestionRecord(
                query_id=f"Q{i:03d}",
                pregunta=item["pregunta"],
                categoria=item["categoria"],
                complejidad=item.get("complejidad", "media"),
                doc_referencia=item.get("doc_referencia", "D012"),
                respuesta_esperada=item.get("respuesta", ""),
                requiere_herramienta=item["categoria"] == "R",
                requiere_multiples_fuentes=item["categoria"] == "M",
                es_respondible="Pendiente" not in item.get("respuesta", ""),
                validacion_experta="draft",
                candidate_strategy=item.get("candidate_strategy", "A1"),
            )
        )

    fieldnames = list(QuestionRecord.model_fields.keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.model_dump())

    # Extra drafts from HTML if present (unverified answers)
    if FAQ_HTML.exists():
        html = FAQ_HTML.read_text(encoding="utf-8", errors="replace")
        extras = _parse_faq_headings(html)[:40]
        with OUT_SYN.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["query_id", "pregunta", "doc_referencia", "validacion_experta", "nota"],
            )
            writer.writeheader()
            for i, q in enumerate(extras, start=1):
                writer.writerow(
                    {
                        "query_id": f"S{i:03d}",
                        "pregunta": q,
                        "doc_referencia": "D012",
                        "validacion_experta": "draft",
                        "nota": "Extraída de FAQ HTML; sin respuesta gold verificada aún.",
                    }
                )
        LOGGER.info("synthetic FAQ drafts -> %s (%d)", OUT_SYN, len(extras))

    LOGGER.info("pilot bank -> %s (%d)", OUT_CSV, len(rows))
    return OUT_CSV


def main() -> None:
    """CLI entry."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    build_pilot_bank()


if __name__ == "__main__":
    main()
