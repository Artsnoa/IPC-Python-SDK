"""Configuration management for ipc_artsnoa SDK."""

import os
from dataclasses import dataclass, field
from typing import Optional

from .exceptions import ConfigurationError


@dataclass
class Config:
    """SDK configuration container."""

    api_key: str
    base_url: str = "https://ipc.artsnoa.com/api"
    timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = True
    user_agent: Optional[str] = None
    headers: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.api_key:
            raise ConfigurationError("API key is required")

        if not isinstance(self.timeout, int) or self.timeout <= 0:
            raise ConfigurationError("Timeout must be a positive integer")

        if not isinstance(self.max_retries, int) or self.max_retries < 0:
            raise ConfigurationError("Max retries must be a non-negative integer")

    @classmethod
    def from_env(cls, api_key: Optional[str] = None) -> "Config":
        """
        Create configuration from environment variables.

        Args:
            api_key: Optional API key. If not provided, reads from IPC_API_KEY env var.

        Returns:
            Config instance

        Raises:
            ConfigurationError: If API key is not provided or found in environment
        """
        key = api_key or os.getenv("IPC_API_KEY")
        if not key:
            raise ConfigurationError(
                "API key must be provided or set as IPC_API_KEY environment variable"
            )

        return cls(
            api_key=key,
            base_url=os.getenv("IPC_BASE_URL", cls.__dataclass_fields__["base_url"].default),
            timeout=int(os.getenv("IPC_TIMEOUT", cls.__dataclass_fields__["timeout"].default)),
            max_retries=int(
                os.getenv("IPC_MAX_RETRIES", cls.__dataclass_fields__["max_retries"].default)
            ),
            verify_ssl=os.getenv("IPC_VERIFY_SSL", "true").lower() == "true",
        )

    def get_auth_header(self) -> dict:
        """
        Get authorization header for API requests.

        Returns:
            Dictionary with authorization header
        """
        return {"Authorization": f"Bearer {self.api_key}"}

    def get_default_headers(self) -> dict:
        """
        Get all default headers including auth and custom headers.

        Returns:
            Dictionary with all headers
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            **self.get_auth_header(),
        }

        if self.user_agent:
            headers["User-Agent"] = self.user_agent

        headers.update(self.headers)
        return headers
