"""Registra y descarga fuentes documentales permitidas."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


def register_source(meta: dict[str, Any], inventory_path: Path) -> None:
    """Append a source record to the inventory file.

    Parameters
    ----------
    meta :
        Source metadata (url, date, license, public/authorized).
    inventory_path :
        Path to the inventory JSON/YAML file.
    """
    LOGGER.info("register_source stub: %s -> %s", meta.get("url"), inventory_path)
    raise NotImplementedError("Implementar inventario reproducible (fase 2).")
