"""Get SDK versions module"""

from typing import Any
from requests import Session

from ._request_handler import make_request


def get_sdk_versions(
    session: Session,
    base_url: str,
    timeout: float
) -> dict[str, Any]:
    """
    Get SDK versions

    Args:
        session: Requests session object
        base_url: Base URL for the API
        timeout: Request timeout in seconds

    Returns:
        dict containing SDK versions (javascript, python, etc.)

    Raises:
        IPCAPIError: When API returns an error response
        IPCConnectionError: When connection fails
        IPCTimeoutError: When request times out
    """
    url = f'{base_url}/api/v1/sdk/version'
    return make_request(session, url, timeout)
