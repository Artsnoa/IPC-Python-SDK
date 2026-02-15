"""Get detailed IP information module"""

from typing import Any
from requests import Session

from ._request_handler import make_request


def get_ip_details(
    session: Session,
    base_url: str,
    timeout: float
) -> dict[str, Any]:
    """
    Get detailed IP information

    Args:
        session: Requests session object
        base_url: Base URL for the API
        timeout: Request timeout in seconds

    Returns:
        dict containing detailed IP information (ip, userAgent, asn, country, currency, languages, timestamp, version)

    Raises:
        IPCAPIError: When API returns an error response
        IPCConnectionError: When connection fails
        IPCTimeoutError: When request times out
    """
    url = f'{base_url}/api/v1/ip/details'
    return make_request(session, url, timeout)
