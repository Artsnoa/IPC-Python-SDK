from typing import Any
import requests

from . import modules
from .exceptions import IPCConnectionError, IPCTimeoutError, IPCAPIError


class IPCClient:
    """Client for IPC API"""

    DEFAULT_BASE_URL = "https://ipc.artsnoa.com"
    BACKUP_BASE_URL = "https://ipc.makedns.net"
    DEFAULT_TIMEOUT = 10.0

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT
    ):
        """
        Initialize IPC client

        Args:
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds (default: 10.0)
        """
        self.api_key = api_key
        self.timeout = timeout
        self._session = requests.Session()

        if self.api_key:
            self._session.headers['Authorization'] = f'Bearer {self.api_key}'

    def get_ip(self) -> dict[str, Any]:
        """
        Get current IP information

        Returns:
            dict containing IP information (ip, country, etc.)

        Raises:
            IPCAPIError: When API returns an error response
            IPCConnectionError: When connection fails
            IPCTimeoutError: When request times out
        """
        try:
            return modules.get_ip(self._session, self.DEFAULT_BASE_URL, self.timeout)
        except (IPCConnectionError, IPCTimeoutError, IPCAPIError):
            return modules.get_ip(self._session, self.BACKUP_BASE_URL, self.timeout)

    def get_ip_details(self) -> dict[str, Any]:
        """
        Get detailed IP information

        Returns:
            dict containing detailed IP information (ip, userAgent, asn, country, currency, languages, timestamp, version)

        Raises:
            IPCAPIError: When API returns an error response
            IPCConnectionError: When connection fails
            IPCTimeoutError: When request times out
        """
        try:
            return modules.get_ip_details(self._session, self.DEFAULT_BASE_URL, self.timeout)
        except (IPCConnectionError, IPCTimeoutError, IPCAPIError):
            return modules.get_ip_details(self._session, self.BACKUP_BASE_URL, self.timeout)

    def get_sdk_versions(self) -> dict[str, Any]:
        """
        Get SDK versions

        Returns:
            dict containing SDK versions (javascript, python, etc.)

        Raises:
            IPCAPIError: When API returns an error response
            IPCConnectionError: When connection fails
            IPCTimeoutError: When request times out
        """
        try:
            return modules.get_sdk_versions(self._session, self.DEFAULT_BASE_URL, self.timeout)
        except (IPCConnectionError, IPCTimeoutError, IPCAPIError):
            return modules.get_sdk_versions(self._session, self.BACKUP_BASE_URL, self.timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the session"""
        self._session.close()
