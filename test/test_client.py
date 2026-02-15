import pytest
from unittest.mock import Mock, patch
import requests

from ipc_artsnoa import (
    IPCClient,
    IPCAPIError,
    IPCConnectionError,
    IPCTimeoutError,
)


class TestIPCClientInit:
    """Test IPCClient initialization"""

    def test_init_with_defaults(self):
        client = IPCClient()
        assert client.api_key is None
        assert client.base_url == "https://ipc.artsnoa.com"
        assert client.timeout == 10.0

    def test_init_with_api_key(self):
        client = IPCClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client._session.headers['Authorization'] == 'Bearer test_key'

    def test_init_with_custom_base_url(self):
        client = IPCClient(base_url="https://custom.example.com")
        assert client.base_url == "https://custom.example.com"

    def test_init_with_trailing_slash_in_url(self):
        client = IPCClient(base_url="https://custom.example.com/")
        assert client.base_url == "https://custom.example.com"

    def test_init_with_custom_timeout(self):
        client = IPCClient(timeout=30.0)
        assert client.timeout == 30.0


class TestIPCClientGetIP:
    """Test get_ip method"""

    def test_get_ip_success(self):
        """Test successful get_ip call with mocked response"""
        mock_response = {
            "ip": "1.2.3.4",
            "country": "US",
            "city": "New York"
        }

        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = mock_response
            mock_resp.status_code = 200
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp

            client = IPCClient()
            result = client.get_ip()

            assert result == mock_response
            mock_get.assert_called_once_with(
                'https://ipc.artsnoa.com/api/v1/ip',
                timeout=10.0
            )

    def test_get_ip_with_api_key(self):
        """Test get_ip with API key"""
        mock_response = {"ip": "1.2.3.4", "country": "US"}

        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = mock_response
            mock_resp.status_code = 200
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp

            client = IPCClient(api_key="test_api_key")
            result = client.get_ip()

            assert result == mock_response
            assert client._session.headers['Authorization'] == 'Bearer test_api_key'

    def test_get_ip_with_custom_url(self):
        """Test get_ip with custom base URL"""
        mock_response = {"ip": "5.6.7.8", "country": "KR"}
        custom_url = "https://test.example.com"

        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = mock_response
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp

            client = IPCClient(base_url=custom_url)
            result = client.get_ip()

            assert result == mock_response
            mock_get.assert_called_once_with(
                f'{custom_url}/api/v1/ip',
                timeout=10.0
            )

    def test_get_ip_timeout_error(self):
        """Test timeout handling"""
        with patch.object(requests.Session, 'get') as mock_get:
            mock_get.side_effect = requests.Timeout("Connection timeout")

            client = IPCClient()
            with pytest.raises(IPCTimeoutError) as exc_info:
                client.get_ip()

            assert "timed out after 10.0s" in str(exc_info.value)

    def test_get_ip_connection_error(self):
        """Test connection error handling"""
        with patch.object(requests.Session, 'get') as mock_get:
            mock_get.side_effect = requests.ConnectionError("Failed to connect")

            client = IPCClient()
            with pytest.raises(IPCConnectionError) as exc_info:
                client.get_ip()

            assert "Failed to connect" in str(exc_info.value)

    def test_get_ip_http_error_404(self):
        """Test HTTP 404 error handling"""
        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.status_code = 404
            mock_resp.json.return_value = {"error": "Not found"}
            mock_resp.raise_for_status.side_effect = requests.HTTPError(response=mock_resp)
            mock_get.return_value = mock_resp

            client = IPCClient()
            with pytest.raises(IPCAPIError) as exc_info:
                client.get_ip()

            assert exc_info.value.status_code == 404
            assert "Not found" in str(exc_info.value)

    def test_get_ip_http_error_401(self):
        """Test HTTP 401 unauthorized error"""
        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.status_code = 401
            mock_resp.json.return_value = {"error": "Unauthorized"}
            mock_resp.raise_for_status.side_effect = requests.HTTPError(response=mock_resp)
            mock_get.return_value = mock_resp

            client = IPCClient(api_key="invalid_key")
            with pytest.raises(IPCAPIError) as exc_info:
                client.get_ip()

            assert exc_info.value.status_code == 401

    def test_get_ip_http_error_500(self):
        """Test HTTP 500 server error"""
        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.status_code = 500
            mock_resp.json.side_effect = ValueError("Invalid JSON")
            mock_resp.raise_for_status.side_effect = requests.HTTPError(response=mock_resp)
            mock_get.return_value = mock_resp

            client = IPCClient()
            with pytest.raises(IPCAPIError) as exc_info:
                client.get_ip()

            assert exc_info.value.status_code == 500


class TestIPCClientContextManager:
    """Test context manager functionality"""

    def test_context_manager(self):
        """Test using client as context manager"""
        mock_response = {"ip": "1.2.3.4", "country": "US"}

        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = mock_response
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp

            with patch.object(requests.Session, 'close') as mock_close:
                with IPCClient() as client:
                    result = client.get_ip()
                    assert result == mock_response

                mock_close.assert_called_once()

    def test_close_method(self):
        """Test explicit close method"""
        with patch.object(requests.Session, 'close') as mock_close:
            client = IPCClient()
            client.close()
            mock_close.assert_called_once()


class TestIPCClientRealAPI:
    """Test with real API calls - these tests require actual network access"""

    @pytest.mark.skipif(
        True,  # Set to False to run real API tests
        reason="Skipping real API tests by default"
    )
    def test_get_ip_real_api_without_key(self):
        """Test real API call without authentication"""
        client = IPCClient()
        result = client.get_ip()

        assert "ip" in result
        assert isinstance(result["ip"], str)
        print(f"Result: {result}")

    @pytest.mark.skipif(
        True,  # Set to False to run real API tests
        reason="Skipping real API tests by default"
    )
    def test_get_ip_real_api_with_key(self):
        """Test real API call with authentication"""
        api_key = "YOUR_API_KEY_HERE"  # Replace with actual key
        client = IPCClient(api_key=api_key)
        result = client.get_ip()

        assert "ip" in result
        assert isinstance(result["ip"], str)
        print(f"Result: {result}")


class TestIPCClientIntegration:
    """Integration tests with different configurations"""

    def test_multiple_clients_with_different_urls(self):
        """Test multiple clients with different base URLs"""
        mock_response_1 = {"ip": "1.1.1.1", "country": "US"}
        mock_response_2 = {"ip": "2.2.2.2", "country": "KR"}

        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp_1 = Mock()
            mock_resp_1.json.return_value = mock_response_1
            mock_resp_1.raise_for_status = Mock()

            mock_resp_2 = Mock()
            mock_resp_2.json.return_value = mock_response_2
            mock_resp_2.raise_for_status = Mock()

            mock_get.side_effect = [mock_resp_1, mock_resp_2]

            client1 = IPCClient(base_url="https://api1.example.com")
            client2 = IPCClient(base_url="https://api2.example.com")

            result1 = client1.get_ip()
            result2 = client2.get_ip()

            assert result1 == mock_response_1
            assert result2 == mock_response_2

    def test_client_reuse(self):
        """Test reusing same client for multiple calls"""
        mock_response = {"ip": "3.3.3.3", "country": "JP"}

        with patch.object(requests.Session, 'get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = mock_response
            mock_resp.raise_for_status = Mock()
            mock_get.return_value = mock_resp

            client = IPCClient()
            result1 = client.get_ip()
            result2 = client.get_ip()

            assert result1 == mock_response
            assert result2 == mock_response
            assert mock_get.call_count == 2
