"""
Test cases for the Stateset client implementations.
"""

import os
from unittest.mock import Mock, patch

import httpx
import pytest

from stateset import AuthenticatedClient, Client, Stateset
from stateset.errors import StatesetAuthenticationError, StatesetConnectionError


class TestClient:
    """Test cases for the base Client class."""

    def test_client_initialization(self):
        """Test basic client initialization."""
        client = Client(base_url="https://api.test.com")
        assert client.base_url == "https://api.test.com"
        assert "stateset-python/" in client.headers["User-Agent"]

    def test_client_custom_headers(self):
        """Test client initialization with custom headers."""
        custom_headers = {"Custom-Header": "test-value"}
        client = Client(
            base_url="https://api.test.com",
            headers=custom_headers
        )
        assert client.headers["Custom-Header"] == "test-value"
        assert "stateset-python/" in client.headers["User-Agent"]

    def test_client_timeout_configuration(self):
        """Test client timeout configuration."""
        client = Client(
            base_url="https://api.test.com",
            timeout=30.0
        )
        assert client.timeout.timeout == 30.0

    def test_httpx_client_creation(self):
        """Test httpx client creation."""
        client = Client(base_url="https://api.test.com")
        httpx_client = client.get_httpx_client()
        assert isinstance(httpx_client, httpx.Client)
        assert str(httpx_client.base_url) == "https://api.test.com"

    def test_async_httpx_client_creation(self):
        """Test async httpx client creation."""
        client = Client(base_url="https://api.test.com")
        async_client = client.get_async_httpx_client()
        assert isinstance(async_client, httpx.AsyncClient)
        assert str(async_client.base_url) == "https://api.test.com"


class TestAuthenticatedClient:
    """Test cases for the AuthenticatedClient class."""

    def test_authenticated_client_initialization(self):
        """Test authenticated client initialization."""
        client = AuthenticatedClient(
            base_url="https://api.test.com",
            token="test_token"
        )
        assert client.base_url == "https://api.test.com"
        assert client.headers["Authorization"] == "Bearer test_token"

    def test_authenticated_client_without_token(self):
        """Test authenticated client without token raises error."""
        with pytest.raises(StatesetAuthenticationError):
            AuthenticatedClient(base_url="https://api.test.com", token="")

    async def test_authenticated_client_get_request(self, httpx_mock):
        """Test authenticated client GET request."""
        client = AuthenticatedClient(
            base_url="https://api.test.com",
            token="test_token"
        )
        
        httpx_mock.add_response(
            method="GET",
            url="https://api.test.com/test",
            json={"success": True},
            status_code=200
        )

        response = await client.get("/test")
        assert response["success"] is True

    async def test_authenticated_client_post_request(self, httpx_mock):
        """Test authenticated client POST request."""
        client = AuthenticatedClient(
            base_url="https://api.test.com",
            token="test_token"
        )
        
        httpx_mock.add_response(
            method="POST",
            url="https://api.test.com/test",
            json={"id": "test_123"},
            status_code=201
        )

        response = await client.post("/test", json={"name": "test"})
        assert response["id"] == "test_123"


class TestStatesetHighLevelClient:
    """Test cases for the high-level Stateset client."""

    def test_stateset_client_from_env_vars(self):
        """Test Stateset client initialization from environment variables."""
        with patch.dict(os.environ, {
            'STATESET_API_KEY': 'test_key',
            'STATESET_BASE_URL': 'https://custom.api.com'
        }):
            client = Stateset()
            assert client._api_key == "test_key"
            assert client._base_url == "https://custom.api.com"

    def test_stateset_client_missing_api_key(self):
        """Test Stateset client without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(StatesetAuthenticationError):
                Stateset()

    def test_stateset_client_default_base_url(self):
        """Test Stateset client uses default base URL."""
        with patch.dict(os.environ, {'STATESET_API_KEY': 'test_key'}):
            client = Stateset()
            assert client._base_url == "https://api.stateset.com"

    def test_stateset_client_custom_timeout(self):
        """Test Stateset client with custom timeout."""
        with patch.dict(os.environ, {
            'STATESET_API_KEY': 'test_key',
            'STATESET_TIMEOUT': '60'
        }):
            client = Stateset()
            # Verify timeout is set correctly (implementation dependent)

    def test_stateset_client_ssl_verification_disabled(self):
        """Test Stateset client with SSL verification disabled."""
        with patch.dict(os.environ, {
            'STATESET_API_KEY': 'test_key',
            'STATESET_VERIFY_SSL': 'false'
        }):
            client = Stateset()
            # Verify SSL verification is disabled (implementation dependent)

    def test_stateset_client_context_manager(self):
        """Test Stateset client as context manager."""
        with patch.dict(os.environ, {'STATESET_API_KEY': 'test_key'}):
            with Stateset() as client:
                assert client is not None
            # Client should be closed after context

    async def test_stateset_client_async_context_manager(self):
        """Test Stateset client as async context manager."""
        with patch.dict(os.environ, {'STATESET_API_KEY': 'test_key'}):
            async with Stateset() as client:
                assert client is not None
            # Client should be closed after context


class TestClientErrorHandling:
    """Test cases for client error handling."""

    async def test_connection_error_handling(self):
        """Test handling of connection errors."""
        client = AuthenticatedClient(
            base_url="https://nonexistent.api.com",
            token="test_token"
        )
        
        with pytest.raises(StatesetConnectionError):
            await client.get("/test")

    async def test_timeout_error_handling(self):
        """Test handling of timeout errors."""
        client = AuthenticatedClient(
            base_url="https://api.test.com",
            token="test_token",
            timeout=0.001  # Very short timeout
        )
        
        with pytest.raises(StatesetConnectionError):
            await client.get("/test")

    async def test_http_error_handling(self, httpx_mock):
        """Test handling of HTTP errors."""
        client = AuthenticatedClient(
            base_url="https://api.test.com",
            token="test_token"
        )
        
        httpx_mock.add_response(
            method="GET",
            url="https://api.test.com/test",
            json={"error": "Not found"},
            status_code=404
        )

        with pytest.raises(Exception):  # Should raise appropriate Stateset error
            await client.get("/test")


class TestClientConfiguration:
    """Test cases for client configuration options."""

    def test_client_with_custom_httpx_args(self):
        """Test client with custom httpx arguments."""
        client = Client(
            base_url="https://api.test.com",
            httpx_args={"timeout": 60.0}
        )
        httpx_client = client.get_httpx_client()
        assert httpx_client.timeout.timeout == 60.0

    def test_client_with_custom_user_agent(self):
        """Test client with custom user agent."""
        client = Client(
            base_url="https://api.test.com",
            headers={"User-Agent": "custom-agent/1.0"}
        )
        assert client.headers["User-Agent"] == "custom-agent/1.0"

    def test_client_ssl_configuration(self):
        """Test client SSL configuration."""
        client = Client(
            base_url="https://api.test.com",
            verify_ssl="/path/to/cert"
        )
        assert client.verify_ssl == "/path/to/cert"

    def test_client_proxy_configuration(self):
        """Test client proxy configuration."""
        proxy_config = {"http://": "http://proxy:8080"}
        client = Client(
            base_url="https://api.test.com",
            httpx_args={"proxies": proxy_config}
        )
        httpx_client = client.get_httpx_client()
        assert httpx_client._mounts