"""
A2E Protocol Exceptions
"""


class A2EError(Exception):
    """Base exception for A2E errors."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"A2E Error [{code}]: {message}")


class AuthenticationError(A2EError):
    """Authentication failed."""
    pass


class PermissionDeniedError(A2EError):
    """Permission denied."""
    pass


class ServiceNotFoundError(A2EError):
    """Service not found."""
    pass


class ExecutionError(A2EError):
    """Execution failed."""
    pass
