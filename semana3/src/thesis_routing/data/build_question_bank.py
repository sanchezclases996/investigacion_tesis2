"""Construye el banco de consultas con campos mínimos."""

from __future__ import annotations

import logging
from typing import Literal

from pydantic import BaseModel, Field

LOGGER = logging.getLogger(__name__)

QueryType = Literal["N", "R", "M", "A"]
ValidationStatus = Literal["draft", "validated", "rejected", "no_verifiable_answer"]


class QuestionRecord(BaseModel):
    """Minimum schema for the evaluation bank (fase 5)."""

    id: str
    question: str
    category: QueryType
    source_ref: str
    reference_answer: str | None = None
    validation_status: ValidationStatus = "draft"
    complexity: int | None = Field(default=None, ge=1, le=5)
    n_sources_required: int | None = None
    candidate_strategy: str | None = None
    answerable_with_corpus: bool | None = None


def validate_record(record: QuestionRecord) -> QuestionRecord:
    """Validate a question record against the schema."""
    LOGGER.debug("validate_record: %s", record.id)
    return record
