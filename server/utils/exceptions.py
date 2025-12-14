"""Custom exception classes for SparkRepo API."""


class SparkRepoException(Exception):
    """Base exception for SparkRepo application."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(SparkRepoException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message, 400)


class AuthenticationError(SparkRepoException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(SparkRepoException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


class NotFoundError(SparkRepoException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", 404)


class ConflictError(SparkRepoException):
    """Raised when a resource conflict occurs (e.g., duplicate)."""
    
    def __init__(self, message: str):
        super().__init__(message, 409)


class DatabaseError(SparkRepoException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, 500)


class ConfigurationError(SparkRepoException):
    """Raised when configuration is missing or invalid."""
    
    def __init__(self, message: str):
        super().__init__(message, 500)
