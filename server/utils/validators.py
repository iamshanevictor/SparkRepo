"""Validation and parsing utilities for API request handling."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable, Tuple, List
import re
from utils.exceptions import ValidationError


def validate_required_fields(data: dict, required: Iterable[str]) -> tuple[bool, list[str]]:
    """
    Validate that required fields are present and not empty.
    
    Args:
        data: Dictionary to validate
        required: Iterable of required field names
        
    Returns:
        Tuple of (is_valid, missing_fields)
    """
    missing = [f for f in required if f not in data or data.get(f) in (None, "")]
    return (len(missing) == 0, missing)


def validate_fields_strict(data: dict, required: Iterable[str]) -> None:
    """
    Validate required fields or raise ValidationError.
    
    Args:
        data: Dictionary to validate
        required: Iterable of required field names
        
    Raises:
        ValidationError: If validation fails
    """
    is_valid, missing = validate_required_fields(data, required)
    if not is_valid:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """
    Validate username format (alphanumeric, underscores, hyphens, 3-50 chars).
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not username or not isinstance(username, str):
        return False
    
    if len(username) < 3 or len(username) > 50:
        return False
    
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, username))


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:[/?#][^\s]*)?$'
    return bool(re.match(pattern, url))


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.
    Requirements: min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not password or not isinstance(password, str):
        return False, "Password cannot be empty"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain an uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain a lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain a digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain a special character"
    
    return True, "Password is strong"


def parse_iso8601(value: str | None) -> datetime | None:
    """
    Parse ISO 8601 datetime string.
    
    Args:
        value: ISO 8601 formatted string
        
    Returns:
        Datetime object or None
        
    Raises:
        ValidationError: If format is invalid
    """
    if not value:
        return None
    
    try:
        # Allow a trailing 'Z' and convert to offset-aware string acceptable by fromisoformat
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Invalid date format: {value}. Expected ISO 8601 format.")


def sanitize_string(value: str, max_length: int = None) -> str:
    """
    Sanitize string input.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length (truncates if exceeded)
        
    Returns:
        Sanitized string
    """
    if not isinstance(value, str):
        return ""
    
    # Strip whitespace
    value = value.strip()
    
    # Remove null bytes
    value = value.replace('\x00', '')
    
    # Truncate if needed
    if max_length and len(value) > max_length:
        value = value[:max_length]
    
    return value


def validate_project_type(project_type: str) -> bool:
    """
    Validate project type.
    
    Args:
        project_type: Project type to validate
        
    Returns:
        True if valid
    """
    valid_types = {'scratch', 'canva'}
    return project_type.lower() in valid_types if project_type else False


def validate_status(status: str) -> bool:
    """
    Validate submission status.
    
    Args:
        status: Status to validate
        
    Returns:
        True if valid
    """
    valid_statuses = {'submitted', 'approved', 'rejected', 'pending'}
    return status.lower() in valid_statuses if status else False
