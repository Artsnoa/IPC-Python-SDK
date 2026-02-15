"""Main client class for ipc_artsnoa SDK."""

from typing import Dict, Optional

from .config import Config
from .http_client import HTTPClient
from .models import IPResponse


class IPCClient:
    """
    Main client for interacting with IPC Artsnoa API.

    Example:
        >>> from ipc_artsnoa import IPCClient
        >>> client = IPCClient(api_key='YOUR_API_KEY')
        >>> data = client.get_ip()
        >>> print(f'Your IP: {data["ip"]}, Country: {data["country"]}')
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        verify_ssl: bool = True,
        user_agent: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Initialize IPC client.

        Args:
            api_key: API key for authentication
            base_url: Optional custom base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            verify_ssl: Whether to verify SSL certificates
            user_agent: Optional custom user agent
            headers: Optional custom headers

        Example:
            >>> client = IPCClient(api_key='your-api-key')
            >>> client = IPCClient(
            ...     api_key='your-api-key',
            ...     timeout=60,
            ...     max_retries=5
            ... )
        """
        config_params = {
            "api_key": api_key,
            "timeout": timeout,
            "max_retries": max_retries,
            "verify_ssl": verify_ssl,
        }

        if base_url:
            config_params["base_url"] = base_url
        if user_agent:
            config_params["user_agent"] = user_agent
        if headers:
            config_params["headers"] = headers

        self.config = Config(**config_params)
        self.http_client = HTTPClient(self.config)

    @classmethod
    def from_env(cls, api_key: Optional[str] = None) -> "IPCClient":
        """
        Create client from environment variables.

        Args:
            api_key: Optional API key. If not provided, reads from IPC_API_KEY env var.

        Returns:
            IPCClient instance

        Example:
            >>> import os
            >>> os.environ['IPC_API_KEY'] = 'your-api-key'
            >>> client = IPCClient.from_env()
        """
        config = Config.from_env(api_key)
        instance = cls.__new__(cls)
        instance.config = config
        instance.http_client = HTTPClient(config)
        return instance

    def get_ip(self, ip: Optional[str] = None) -> Dict:
        """
        Get IP information.

        Args:
            ip: Optional specific IP address to query. If not provided, returns caller's IP.

        Returns:
            Dictionary containing IP information with keys: ip, country, region, city, etc.

        Raises:
            AuthenticationError: If API key is invalid
            RateLimitError: If rate limit is exceeded
            APIError: If API request fails

        Example:
            >>> client = IPCClient(api_key='your-api-key')
            >>> data = client.get_ip()
            >>> print(f"IP: {data['ip']}, Country: {data['country']}")

            >>> data = client.get_ip(ip='8.8.8.8')
            >>> print(f"Google DNS: {data['ip']}, Country: {data['country']}")
        """
        params = {}
        if ip:
            params["ip"] = ip

        response_data = self.http_client.get("v1/ip", params=params)
        ip_response = IPResponse.from_dict(response_data)
        return ip_response.to_dict()

    def get_ip_detailed(self, ip: Optional[str] = None) -> IPResponse:
        """
        Get detailed IP information as IPResponse object.

        Args:
            ip: Optional specific IP address to query

        Returns:
            IPResponse object with detailed information

        Example:
            >>> client = IPCClient(api_key='your-api-key')
            >>> response = client.get_ip_detailed()
            >>> print(f"IP: {response.ip}")
            >>> print(f"Country: {response.country}")
            >>> print(f"City: {response.city}")
            >>> print(f"ISP: {response.isp}")
        """
        params = {}
        if ip:
            params["ip"] = ip

        response_data = self.http_client.get("v1/ip", params=params)
        return IPResponse.from_dict(response_data)

    def get_location(self, ip: Optional[str] = None) -> Dict:
        """
        Get geographic location information for an IP.

        Args:
            ip: Optional specific IP address

        Returns:
            Dictionary with location data (country, region, city, coordinates)

        Example:
            >>> client = IPCClient(api_key='your-api-key')
            >>> location = client.get_location()
            >>> print(f"Location: {location['city']}, {location['country']}")
        """
        params = {}
        if ip:
            params["ip"] = ip

        response_data = self.http_client.get("v1/location", params=params)
        return response_data

    def get_isp(self, ip: Optional[str] = None) -> Dict:
        """
        Get ISP information for an IP.

        Args:
            ip: Optional specific IP address

        Returns:
            Dictionary with ISP information

        Example:
            >>> client = IPCClient(api_key='your-api-key')
            >>> isp = client.get_isp()
            >>> print(f"ISP: {isp['isp']}")
        """
        params = {}
        if ip:
            params["ip"] = ip

        response_data = self.http_client.get("v1/isp", params=params)
        return response_data

    def batch_lookup(self, ips: list[str]) -> Dict:
        """
        Look up multiple IP addresses in a single request.

        Args:
            ips: List of IP addresses to look up

        Returns:
            Dictionary with results for each IP

        Example:
            >>> client = IPCClient(api_key='your-api-key')
            >>> results = client.batch_lookup(['8.8.8.8', '1.1.1.1'])
            >>> for ip, data in results.items():
            ...     print(f"{ip}: {data['country']}")
        """
        response_data = self.http_client.post("v1/batch", data={"ips": ips})
        return response_data

    def __repr__(self) -> str:
        """String representation of client."""
        return f"IPCClient(base_url='{self.config.base_url}')"
