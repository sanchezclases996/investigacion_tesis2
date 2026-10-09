"""EDA preliminar del corpus UMA y del banco piloto.

Bloques (gpt2): inventario, calidad, texto, cobertura, vacíos;
más distribución del banco de consultas. No inventa resultados experimentales.
"""

from __future__ import annotations

import json
import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

LOGGER = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[3]
INV = ROOT / "data" / "processed" / "corpus" / "inventario_documental.csv"
TEXT_DIR = ROOT / "data" / "interim" / "extracted_text"
QB = ROOT / "data" / "processed" / "question_bank" / "consultas_piloto.csv"
FIG_DIR = ROOT / "reports" / "figures"
REPORT_DOC = ROOT / "reports" / "eda" / "document_eda.md"
REPORT_QB = ROOT / "reports" / "eda" / "question_bank_eda.md"
SUMMARY_JSON = ROOT / "reports" / "eda" / "eda_summary.json"

# Temas orientativos para cobertura (no afirman vigencia jurídica)
THEME_PATTERNS: dict[str, re.Pattern[str]] = {
    "matricula": re.compile(r"matricul", re.I),
    "asistencia": re.compile(r"inasistenc|asistenc", re.I),
    "evaluacion": re.compile(r"evaluaci[oó]n|examen|parcial|sustitutor", re.I),
    "creditos": re.compile(r"cr[eé]dito", re.I),
    "prerrequisitos": re.compile(r"prerrequis|pre-?requis", re.I),
    "convalidacion": re.compile(r"convalid", re.I),
    "tramites_grados": re.compile(r"bachiller|t[ií]tulo|grado", re.I),
    "becas": re.compile(r"beca", re.I),
    "admision": re.compile(r"admisi[oó]n", re.I),
    "tarifas": re.compile(r"tarif|pension|pago", re.I),
    "malla_plan": re.compile(r"plan de estudi|malla|curricul", re.I),
    "calendario": re.compile(r"calendario acad[eé]mico|periodo acad[eé]mico", re.I),
}


def _load_inventory() -> pd.DataFrame:
    """Load the documental inventory CSV."""
    df = pd.read_csv(INV)
    df["n_pages"] = pd.to_numeric(df["n_pages"], errors="coerce").fillna(0).astype(int)
    df["chars"] = pd.to_numeric(df["chars"], errors="coerce").fillna(0).astype(int)
    df["words"] = pd.to_numeric(df["words"], errors="coerce").fillna(0).astype(int)
    return df


def _theme_hits(text: str) -> dict[str, int]:
    """Count theme keyword hits in one document text."""
    return {theme: len(pat.findall(text)) for theme, pat in THEME_PATTERNS.items()}


def _coverage_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Build theme × document presence matrix (Sí / Parcial / No)."""
    rows: list[dict[str, str]] = []
    for theme in THEME_PATTERNS:
        row: dict[str, str] = {"tema": theme}
        for _, doc in df.iterrows():
            path = TEXT_DIR / f"{doc['doc_id']}.txt"
            if not path.exists():
                row[doc["doc_id"]] = "No"
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            hits = len(THEME_PATTERNS[theme].findall(text))
            if hits >= 8:
                row[doc["doc_id"]] = "Sí"
            elif hits >= 1:
                row[doc["doc_id"]] = "Parcial"
            else:
                row[doc["doc_id"]] = "No"
        rows.append(row)
    return pd.DataFrame(rows)


def _plot_bar(series: pd.Series, title: str, xlabel: str, out: Path) -> None:
    """Save a simple horizontal-friendly bar chart."""
    fig, ax = plt.subplots(figsize=(8, 4.2))
    series.plot(kind="bar", ax=ax, color="#4C72B0", edgecolor="black", linewidth=0.4)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("cantidad")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)


def run_document_eda(df: pd.DataFrame) -> dict[str, Any]:
    """Produce figures and stats for the documental corpus."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    by_dom = df["dominio"].value_counts().sort_index()
    by_status = df["estado_extraccion"].value_counts()
    _plot_bar(by_dom, "Documentos por dominio", "dominio", FIG_DIR / "eda_docs_por_dominio.png")
    _plot_bar(by_status, "Calidad de extracción", "estado", FIG_DIR / "eda_calidad_extraccion.png")

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.bar(df["doc_id"], df["words"], color="#55A868", edgecolor="black", linewidth=0.4)
    ax.set_title("Palabras extraídas por documento")
    ax.set_xlabel("doc_id")
    ax.set_ylabel("palabras")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "eda_palabras_por_doc.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.scatter(df["n_pages"], df["words"], s=60, c="#C44E52")
    for _, r in df.iterrows():
        ax.annotate(r["doc_id"], (r["n_pages"], r["words"]), fontsize=8, xytext=(4, 4), textcoords="offset points")
    ax.set_title("Páginas vs palabras extraídas")
    ax.set_xlabel("páginas")
    ax.set_ylabel("palabras")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "eda_paginas_vs_palabras.png", dpi=140)
    plt.close(fig)

    cov = _coverage_matrix(df)
    cov.to_csv(FIG_DIR / "eda_matriz_cobertura.csv", index=False)

    # Heat-like table as image via text counts
    score = (
        cov.set_index("tema")
        .replace({"Sí": 2, "Parcial": 1, "No": 0})
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
    )
    fig, ax = plt.subplots(figsize=(10, 5.5))
    im = ax.imshow(score.to_numpy(dtype=float), aspect="auto", cmap="YlGn")
    ax.set_xticks(range(len(score.columns)))
    ax.set_xticklabels(score.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(score.index)))
    ax.set_yticklabels(score.index)
    ax.set_title("Cobertura temática (0=No, 1=Parcial, 2=Sí)")
    fig.colorbar(im, ax=ax, fraction=0.03)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "eda_matriz_cobertura.png", dpi=140)
    plt.close(fig)

    weak = df[df["estado_extraccion"] != "ok"]["doc_id"].tolist()
    theme_totals: Counter[str] = Counter()
    for path in TEXT_DIR.glob("D*.txt"):
        hits = _theme_hits(path.read_text(encoding="utf-8", errors="replace"))
        theme_totals.update({k: (1 if v > 0 else 0) for k, v in hits.items()})

    return {
        "n_docs": int(len(df)),
        "n_ok": int((df["estado_extraccion"] == "ok").sum()),
        "n_weak": int(len(weak)),
        "weak_ids": weak,
        "total_words": int(df["words"].sum()),
        "total_pages": int(df["n_pages"].sum()),
        "by_dominio": by_dom.to_dict(),
        "docs_con_tema": dict(theme_totals),
        "coverage_csv": str(FIG_DIR / "eda_matriz_cobertura.csv"),
    }


def run_question_eda() -> dict[str, Any]:
    """Produce figures and stats for the pilot question bank."""
    if not QB.exists():
        return {"n_queries": 0}
    qb = pd.read_csv(QB)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    by_cat = qb["categoria"].value_counts().sort_index()
    by_comp = qb["complejidad"].value_counts()
    _plot_bar(by_cat, "Consultas piloto por categoría (N/R/M/A)", "categoria", FIG_DIR / "eda_qb_categoria.png")
    _plot_bar(by_comp, "Consultas piloto por complejidad", "complejidad", FIG_DIR / "eda_qb_complejidad.png")

    tools = int(qb["requiere_herramienta"].astype(str).str.lower().isin(["true", "1"]).sum())
    multi = int(qb["requiere_multiples_fuentes"].astype(str).str.lower().isin(["true", "1"]).sum())
    respondible = int(qb["es_respondible"].astype(str).str.lower().isin(["true", "1"]).sum())

    return {
        "n_queries": int(len(qb)),
        "by_categoria": by_cat.to_dict(),
        "by_complejidad": by_comp.to_dict(),
        "requiere_herramienta": tools,
        "requiere_multiples_fuentes": multi,
        "es_respondible": respondible,
        "validacion": qb["validacion_experta"].value_counts().to_dict(),
        "by_strategy": qb["candidate_strategy"].value_counts().to_dict(),
    }


def write_document_report(df: pd.DataFrame, stats: dict[str, Any]) -> None:
    """Write the documental EDA markdown report."""
    REPORT_DOC.parent.mkdir(parents=True, exist_ok=True)
    weak = stats["weak_ids"] or ["ninguno"]
    lines = [
        "# EDA documental (UMA)",
        "",
        "**Caso:** Facultad de Ingeniería y Negocios / UMA–SJL.  ",
        "**Fuentes:** documentación pública (reglamentos, tarifario y FAQ).  ",
        "**Alcance:** análisis del corpus; no incluye resultados de las configuraciones A0–A5.",
        "",
        "## 1. Inventario y cobertura",
        "",
        f"- Documentos en inventario: **{stats['n_docs']}**.",
        f"- Páginas totales (metadato): **{stats['total_pages']}**.",
        f"- Palabras extraídas: **{stats['total_words']:,}**.".replace(",", " "),
        f"- Distribución por dominio: `{stats['by_dominio']}`.",
        "",
        "Figuras: `reports/figures/eda_docs_por_dominio.png`, `eda_palabras_por_doc.png`.",
        "",
        "## 2. Calidad de extracción",
        "",
        f"- Extracción OK: **{stats['n_ok']}** / {stats['n_docs']}.",
        f"- Extracción débil o posible documento escaneado: **{weak}**.",
        "",
        "D010 (guía de proceso de matrícula) aporta poco texto seleccionable.",
        "En el índice de recuperación se deja fuera o se trata aparte hasta disponer de OCR",
        "o de una versión textual usable.",
        "",
        "Figuras: `eda_calidad_extraccion.png`, `eda_paginas_vs_palabras.png`.",
        "",
        "## 3. Cobertura temática (aproximada por términos)",
        "",
        "Matriz: `reports/figures/eda_matriz_cobertura.csv` y `eda_matriz_cobertura.png`.",
        "La presencia de términos indica cobertura lexical, no la vigencia de un artículo concreto.",
        "",
        "| Tema | Docs con al menos 1 mención |",
        "|------|-----------------------------|",
    ]
    for theme, n in sorted(stats["docs_con_tema"].items()):
        lines.append(f"| {theme} | {n} / {stats['n_docs']} |")

    lines.extend(
        [
            "",
            "## 4. Implicaciones para el diseño experimental",
            "",
            "1. **Recuperación documental (A1):** D001–D009, D011 y D012 tienen texto extraíble",
            "   suficiente para un índice RAG normativo y administrativo.",
            "2. **Malla y prerrequisitos (A3):** el corpus público cubre poco la estructura operativa",
            "   de prerrequisitos; las consultas tipo R requieren malla oficial o grafo autorizado.",
            "   El grafo actual es de demostración.",
            "3. **Calendario académico:** no hay documento dedicado en este piloto;",
            "   las consultas centradas en fechas del ciclo tienen cobertura limitada.",
            "4. **FAQ (D012):** concentra preguntas frecuentes; ante divergencia, la referencia son los reglamentos.",
            "5. **Derivación a persona (tipo A):** la FAQ menciona SIGU, correo y ventanilla.",
            "",
            "## 5. Limitaciones del corpus",
            "",
            "| Limitación | Efecto en la evaluación | Tratamiento |",
            "|------------|-------------------------|-------------|",
            "| Sin malla oficial de la facultad | Consultas tipo R incompletas | Incorporar plan/grafo institucional |",
            "| Sin calendario dedicado | Preguntas de fechas frágiles | Añadir calendario del ciclo |",
            "| D010 con poco texto | Bajo valor en retrieval | OCR o fuente alternativa |",
            "| Banco en estado draft | Sin gold institucional | Revisión por personal de la facultad |",
            "| Sin consultas reales anonimizadas | Menor validez ecológica | Incorporarlas si hay autorización |",
            "",
            "## 6. Preparación del corpus para etapas siguientes",
            "",
            "- Incluir en el índice RAG: D001–D009, D011, D012.",
            "- Excluir o aislar: D010 mientras la extracción sea débil.",
            "- Mantener la malla en herramientas o grafo, separada del índice de texto normativo.",
            "- Ampliar y validar el banco de consultas antes de las corridas A0–A5.",
            "",
        ]
    )
    REPORT_DOC.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("wrote %s", REPORT_DOC)


def write_question_report(stats: dict[str, Any]) -> None:
    """Write the question-bank EDA markdown report."""
    REPORT_QB.parent.mkdir(parents=True, exist_ok=True)
    if stats.get("n_queries", 0) == 0:
        REPORT_QB.write_text("# EDA del banco de consultas\n\nSin archivo de piloto.\n", encoding="utf-8")
        return

    lines = [
        "# EDA del banco piloto de consultas",
        "",
        f"- Consultas en el piloto: **{stats['n_queries']}**, con `validacion_experta=draft`.",
        f"- Por categoría N/R/M/A: `{stats['by_categoria']}`.",
        f"- Por complejidad: `{stats['by_complejidad']}`.",
        f"- Requieren herramienta (malla/tools): **{stats['requiere_herramienta']}**.",
        f"- Requieren múltiples fuentes: **{stats['requiere_multiples_fuentes']}**.",
        f"- Marcadas como respondibles con la evidencia actual: **{stats['es_respondible']}** / {stats['n_queries']}.",
        f"- Estrategia candidata (etiqueta de diseño): `{stats['by_strategy']}`.",
        "",
        "Figuras: `eda_qb_categoria.png`, `eda_qb_complejidad.png`.",
        "",
        "## Observaciones",
        "",
        "1. El piloto incluye tipos N, R, M y A, lo que permite plantear la comparación entre",
        "   recuperación documental, herramientas y derivación a persona.",
        "2. Las respuestas de referencia están en borrador; no hay gold validado por la facultad.",
        "3. Las consultas tipo R usan el grafo de demostración o referencias a SIGU.",
        "4. El tamaño actual es un piloto de trabajo; la ampliación queda sujeta a evidencia",
        "   documental y a validación posterior.",
        "",
        "## Limitación",
        "",
        "Este banco no se presenta como muestra estadísticamente representativa.",
        "",
    ]
    REPORT_QB.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("wrote %s", REPORT_QB)


def main() -> None:
    """Run documental + question-bank EDA and write reports."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    df = _load_inventory()
    doc_stats = run_document_eda(df)
    qb_stats = run_question_eda()
    write_document_report(df, doc_stats)
    write_question_report(qb_stats)
    SUMMARY_JSON.write_text(
        json.dumps({"documental": doc_stats, "consultas": qb_stats}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    LOGGER.info("summary -> %s", SUMMARY_JSON)
    LOGGER.info("EDA completado")


if __name__ == "__main__":
    main()
