"""Error response helpers for Flask JSON APIs."""
from __future__ import annotations

from flask import jsonify
from utils.exceptions import SparkRepoException
import logging

logger = logging.getLogger(__name__)


def json_error(message: str, status_code: int = 400, error_code: str = None):
    """
    Return a standardized JSON error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        error_code: Optional error code for client-side handling
    
    Returns:
        Tuple of (JSON response, status code)
    """
    response = {"error": message}
    if error_code:
        response["error_code"] = error_code
    return jsonify(response), status_code


def handle_exception(exc: Exception, status_code: int = 500):
    """
    Handle an exception and return appropriate JSON response.
    
    Args:
        exc: The exception to handle
        status_code: Default HTTP status code
        
    Returns:
        Tuple of (JSON response, status code)
    """
    if isinstance(exc, SparkRepoException):
        logger.warning(f"{exc.__class__.__name__}: {exc.message}")
        return json_error(exc.message, exc.status_code)
    
    # Log unexpected exceptions
    logger.error(f"Unexpected exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    return json_error(str(exc), status_code)
