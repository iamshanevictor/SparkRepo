"""Validation and parsing utilities for API request handling."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable


def validate_required_fields(data: dict, required: Iterable[str]) -> tuple[bool, list[str]]:
    missing = [f for f in required if f not in data or data.get(f) in (None, "")]
    return (len(missing) == 0, missing)


def parse_iso8601(value: str | None) -> datetime | None:
    if not value:
        return None
    # Allow a trailing 'Z' and convert to offset-aware string acceptable by fromisoformat
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)
