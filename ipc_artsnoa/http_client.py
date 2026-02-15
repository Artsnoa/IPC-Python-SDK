"""HTTP client wrapper for ipc_artsnoa SDK."""

import json
import time
from typing import Any, Dict, Optional
from urllib import request
from urllib.error import HTTPError, URLError

from .config import Config
from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)


class HTTPClient:
    """HTTP client for making API requests with retry logic."""

    def __init__(self, config: Config) -> None:
        """
        Initialize HTTP client.

        Args:
            config: SDK configuration
        """
        self.config = config

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data as dictionary

        Raises:
            Various IPCError subclasses based on error type
        """
        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query_string}"

        request_headers = self.config.get_default_headers()
        if headers:
            request_headers.update(headers)

        body = None
        if data:
            body = json.dumps(data).encode("utf-8")

        for attempt in range(self.config.max_retries):
            try:
                req = request.Request(
                    url,
                    data=body,
                    headers=request_headers,
                    method=method,
                )

                with request.urlopen(req, timeout=self.config.timeout) as response:
                    response_data = response.read().decode("utf-8")
                    return json.loads(response_data) if response_data else {}

            except HTTPError as e:
                status_code = e.code
                try:
                    error_data = json.loads(e.read().decode("utf-8"))
                    error_message = error_data.get("error", str(e))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    error_message = str(e)

                if status_code == 401:
                    raise AuthenticationError(error_message, status_code, error_data)
                elif status_code == 429:
                    if attempt < self.config.max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise RateLimitError(error_message, status_code, error_data)
                elif status_code == 400:
                    raise ValidationError(error_message, status_code, error_data)
                elif status_code >= 500:
                    if attempt < self.config.max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise APIError(error_message, status_code, error_data)
                else:
                    raise APIError(error_message, status_code, error_data)

            except URLError as e:
                if "timed out" in str(e).lower():
                    if attempt < self.config.max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise TimeoutError(f"Request timeout after {self.config.timeout}s")
                raise NetworkError(f"Network error: {e}")

            except Exception as e:
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise NetworkError(f"Unexpected error: {e}")

        raise NetworkError("Max retries exceeded")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data
        """
        return self._make_request("GET", endpoint, params=params, headers=headers)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make POST request.

        Args:
            endpoint: API endpoint
            data: Request body
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data
        """
        return self._make_request("POST", endpoint, data=data, params=params, headers=headers)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make PUT request.

        Args:
            endpoint: API endpoint
            data: Request body
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data
        """
        return self._make_request("PUT", endpoint, data=data, params=params, headers=headers)

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Make DELETE request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data
        """
        return self._make_request("DELETE", endpoint, params=params, headers=headers)
