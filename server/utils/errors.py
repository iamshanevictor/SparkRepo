"""Error response helpers for Flask JSON APIs."""
from __future__ import annotations

from flask import jsonify


def json_error(message: str, status_code: int = 400):
    return jsonify({"error": message}), status_code


def handle_exception(exc: Exception, status_code: int = 500):
    return json_error(str(exc), status_code)
