"""Data models for ipc_artsnoa SDK."""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class IPResponse:
    """Base response model for IP-related data."""

    ip: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    timezone: Optional[str] = None
    isp: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    raw_data: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IPResponse":
        """
        Create IPResponse from dictionary.

        Args:
            data: Response dictionary from API

        Returns:
            IPResponse instance
        """
        return cls(
            ip=data.get("ip", ""),
            country=data.get("country"),
            region=data.get("region"),
            city=data.get("city"),
            timezone=data.get("timezone"),
            isp=data.get("isp"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            raw_data=data,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert response to dictionary.

        Returns:
            Dictionary representation
        """
        result = {
            "ip": self.ip,
        }

        if self.country is not None:
            result["country"] = self.country
        if self.region is not None:
            result["region"] = self.region
        if self.city is not None:
            result["city"] = self.city
        if self.timezone is not None:
            result["timezone"] = self.timezone
        if self.isp is not None:
            result["isp"] = self.isp
        if self.latitude is not None:
            result["latitude"] = self.latitude
        if self.longitude is not None:
            result["longitude"] = self.longitude

        return result

    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-style access for backward compatibility.

        Args:
            key: Attribute name

        Returns:
            Attribute value
        """
        if key in self.__dataclass_fields__:
            return getattr(self, key)
        if self.raw_data and key in self.raw_data:
            return self.raw_data[key]
        raise KeyError(f"Key '{key}' not found")

    def __repr__(self) -> str:
        """String representation of response."""
        return f"IPResponse(ip='{self.ip}', country='{self.country}')"


@dataclass
class APIResponse:
    """Generic API response wrapper."""

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    status_code: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], status_code: int) -> "APIResponse":
        """
        Create APIResponse from dictionary.

        Args:
            data: Response dictionary
            status_code: HTTP status code

        Returns:
            APIResponse instance
        """
        success = 200 <= status_code < 300
        return cls(
            success=success,
            data=data if success else None,
            error=data.get("error") if not success else None,
            status_code=status_code,
        )
