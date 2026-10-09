"""Extrae texto de PDF, HTML y documentos de texto."""

from __future__ import annotations

import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def extract_file(source_path: Path, out_dir: Path) -> Path:
    """Extract text from one document into ``out_dir``.

    Parameters
    ----------
    source_path :
        Original file path.
    out_dir :
        Directory for extracted text artifacts.

    Returns
    -------
    Path
        Path to the extracted text file.
    """
    LOGGER.info("extract_file stub: %s", source_path)
    raise NotImplementedError("Implementar extracción con trazabilidad (fase 3).")
