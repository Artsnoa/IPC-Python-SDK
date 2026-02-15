"""Common request handling utilities"""

from typing import Any
from requests import Session
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError

from ..exceptions import IPCAPIError, IPCConnectionError, IPCTimeoutError


def make_request(
    session: Session,
    url: str,
    timeout: float
) -> dict[str, Any]:
    """
    Make a GET request and handle common errors

    Args:
        session: Requests session object
        url: URL to request
        timeout: Request timeout in seconds

    Returns:
        dict containing API response

    Raises:
        IPCAPIError: When API returns an error response
        IPCConnectionError: When connection fails
        IPCTimeoutError: When request times out
    """
    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Timeout as e:
        raise IPCTimeoutError(f'Request timed out after {timeout}s') from e
    except ConnectionError as e:
        raise IPCConnectionError(f'Failed to connect to {url}') from e
    except HTTPError as e:
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
