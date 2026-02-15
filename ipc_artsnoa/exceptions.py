class IPCError(Exception):
    """Base exception for IPC SDK"""
    pass


class IPCAPIError(IPCError):
    """Raised when API returns an error response"""
    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class IPCConnectionError(IPCError):
    """Raised when connection to API fails"""
    pass


class IPCTimeoutError(IPCError):
    """Raised when request times out"""
    pass
