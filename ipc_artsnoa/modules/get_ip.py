"""Get IP information module"""

from typing import Any
from requests import Session

from ._request_handler import make_request


def get_ip(
    session: Session,
    base_url: str,
    timeout: float
) -> dict[str, Any]:
    """
    Get current IP information

    Args:
        session: Requests session object
        base_url: Base URL for the API
        timeout: Request timeout in seconds

    Returns:
        dict containing IP information (ip, country, etc.)

    Raises:
        IPCAPIError: When API returns an error response
        IPCConnectionError: When connection fails
        IPCTimeoutError: When request times out
    """
    url = f'{base_url}/api/v1/ip'
    return make_request(session, url, timeout)
