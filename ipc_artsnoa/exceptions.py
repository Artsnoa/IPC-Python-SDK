"""Custom exceptions for ipc_artsnoa SDK."""

from typing import Any, Optional


class IPCError(Exception):
    """Base exception for all IPC SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(IPCError):
    """Raised when API key is invalid or missing."""

    def __init__(
        self,
        message: str = "Authentication failed. Check your API key.",
        status_code: Optional[int] = 401,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class RateLimitError(IPCError):
    """Raised when API rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please try again later.",
        status_code: Optional[int] = 429,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class ValidationError(IPCError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str = "Request validation failed.",
        status_code: Optional[int] = 400,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class APIError(IPCError):
    """Raised when API returns an error response."""

    def __init__(
        self,
        message: str = "API request failed.",
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class NetworkError(IPCError):
    """Raised when network connectivity issues occur."""

    def __init__(
        self,
        message: str = "Network error occurred.",
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class TimeoutError(IPCError):
    """Raised when request timeout occurs."""

    def __init__(
        self,
        message: str = "Request timeout.",
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response)


class ConfigurationError(IPCError):
    """Raised when SDK configuration is invalid."""

    def __init__(
        self,
        message: str = "Invalid configuration.",
        status_code: Optional[int] = None,
        response: Optional[Any] = None,
    ) -> None:
        super().__init__(message, status_code, response)
