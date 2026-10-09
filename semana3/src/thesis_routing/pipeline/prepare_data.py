"""Pipeline step: prepare_data."""

from __future__ import annotations

import logging

LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Entry point for `python -m thesis_routing.pipeline.prepare_data`."""
    LOGGER.info("prepare_data: stub (implementar según docs/experimental_protocol.md)")
    raise SystemExit("NotImplemented: prepare_data")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
