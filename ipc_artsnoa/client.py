from typing import Any
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from .exceptions import IPCAPIError, IPCConnectionError, IPCTimeoutError


class IPCClient:
    """Client for IPC API"""

    DEFAULT_BASE_URL = "https://ipc.artsnoa.com"
    DEFAULT_TIMEOUT = 10.0

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT
    ):
        """
        Initialize IPC client

        Args:
            api_key: Optional API key for authentication
            base_url: Optional base URL (default: https://ipc.artsnoa.com)
            timeout: Request timeout in seconds (default: 10.0)
        """
        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip('/')
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
        url = f'{self.base_url}/api/v1/ip'

        try:
            response = self._session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Timeout as e:
            raise IPCTimeoutError(f'Request timed out after {self.timeout}s') from e
        except ConnectionError as e:
            raise IPCConnectionError(f'Failed to connect to {url}') from e
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            error_msg = f'API request failed with status {status_code}'
            try:
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = error_data['error']
            except Exception:
                pass
            raise IPCAPIError(error_msg, status_code) from e
        except RequestException as e:
            raise IPCConnectionError(f'Request failed: {str(e)}') from e

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
        url = f'{self.base_url}/api/v1/ip/details'

        try:
            response = self._session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Timeout as e:
            raise IPCTimeoutError(f'Request timed out after {self.timeout}s') from e
        except ConnectionError as e:
            raise IPCConnectionError(f'Failed to connect to {url}') from e
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            error_msg = f'API request failed with status {status_code}'
            try:
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = error_data['error']
            except Exception:
                pass
            raise IPCAPIError(error_msg, status_code) from e
        except RequestException as e:
            raise IPCConnectionError(f'Request failed: {str(e)}') from e

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the session"""
        self._session.close()
