"""
IPC Artsnoa Python SDK

Official Python SDK for ipc.artsnoa.com API.

Example:
    >>> from ipc_artsnoa import IPCClient
    >>> client = IPCClient(api_key='YOUR_API_KEY')
    >>> data = client.get_ip()
    >>> print(f'Your IP: {data["ip"]}, Country: {data["country"]}')
"""

from .client import IPCClient
from .config import Config
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    IPCError,
    NetworkError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)
from .models import APIResponse, IPResponse
from .version import __author__, __email__, __version__

__all__ = [
    # Main client
    "IPCClient",
    # Configuration
    "Config",
    # Models
    "IPResponse",
    "APIResponse",
    # Exceptions
    "IPCError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "APIError",
    "NetworkError",
    "TimeoutError",
    "ConfigurationError",
    # Version info
    "__version__",
    "__author__",
    "__email__",
]
