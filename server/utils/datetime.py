"""Datetime utilities for parsing and formatting.

Provides safe helpers for working with ISO 8601 strings coming from the client.
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional


def parse_iso_datetime(value: str | None) -> Optional[datetime]:
    """Parse an ISO 8601-ish datetime string to a datetime or return None.

    - Accepts strings like "2025-06-15T23:59:59" or ones ending with "Z".
    - Returns None if the input is falsy.
    - Raises ValueError if the format is invalid.
    """
    if not value:
        return None
    # Allow trailing Z by converting to +00:00
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)
