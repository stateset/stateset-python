"""
Pytest configuration and shared fixtures for the Stateset SDK test suite.
"""

import os
from typing import AsyncGenerator, Generator
from unittest.mock import Mock

import httpx
import pytest
import pytest_httpx

from stateset import AuthenticatedClient, Stateset


@pytest.fixture
def api_key() -> str:
    """Return a test API key."""
    return "test_sk_1234567890abcdef"


@pytest.fixture
def base_url() -> str:
    """Return the test base URL."""
    return "https://api.test.stateset.com"


@pytest.fixture
def authenticated_client(base_url: str, api_key: str) -> AuthenticatedClient:
    """Create an authenticated client for testing."""
    return AuthenticatedClient(base_url=base_url, token=api_key)


@pytest.fixture
def stateset_client(api_key: str) -> Stateset:
    """Create a high-level Stateset client for testing."""
    # Use environment variable override for testing
    os.environ["STATESET_API_KEY"] = api_key
    os.environ["STATESET_BASE_URL"] = "https://api.test.stateset.com"
    client = Stateset()
    yield client
    client.close()


@pytest.fixture
async def async_stateset_client(api_key: str) -> AsyncGenerator[Stateset, None]:
    """Create an async Stateset client for testing."""
    os.environ["STATESET_API_KEY"] = api_key
    os.environ["STATESET_BASE_URL"] = "https://api.test.stateset.com"
    client = Stateset()
    yield client
    await client.aclose()


@pytest.fixture
def mock_httpx_client() -> Generator[Mock, None, None]:
    """Create a mock httpx client."""
    mock_client = Mock(spec=httpx.Client)
    yield mock_client


@pytest.fixture
def httpx_mock() -> Generator[pytest_httpx.HTTPXMock, None, None]:
    """Create an httpx mock for testing HTTP requests."""
    with pytest_httpx.HTTPXMock() as mock:
        yield mock


@pytest.fixture
def sample_order_data() -> dict:
    """Return sample order data for testing."""
    return {
        "id": "order_123",
        "customer_id": "cust_456",
        "status": "pending",
        "total_amount": 99.99,
        "items": [
            {
                "product_id": "prod_789",
                "quantity": 2,
                "price": 49.99,
            }
        ],
        "created": "2024-01-15T10:30:00Z",
        "updated": "2024-01-15T10:30:00Z",
    }


@pytest.fixture
def sample_return_data() -> dict:
    """Return sample return data for testing."""
    return {
        "id": "return_123",
        "order_id": "order_456",
        "status": "requested",
        "reason": "defective",
        "items": [
            {
                "product_id": "prod_789",
                "quantity": 1,
                "reason": "damaged",
            }
        ],
        "created": "2024-01-15T10:30:00Z",
        "updated": "2024-01-15T10:30:00Z",
    }


@pytest.fixture
def sample_warranty_data() -> dict:
    """Return sample warranty data for testing."""
    return {
        "id": "warranty_123",
        "product_id": "prod_456",
        "customer_id": "cust_789",
        "status": "active",
        "start_date": "2024-01-01",
        "end_date": "2025-01-01",
        "created": "2024-01-01T00:00:00Z",
        "updated": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_error_response() -> dict:
    """Return a sample error response."""
    return {
        "error": {
            "type": "invalid_request_error",
            "code": "parameter_invalid",
            "message": "The provided parameter is invalid",
            "param": "customer_id",
        }
    }


class TestHTTPResponse:
    """Helper class for creating test HTTP responses."""
    
    def __init__(self, status_code: int, json_data: dict = None, text: str = None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self._text = text or ""
    
    def json(self):
        return self._json_data
    
    @property
    def text(self):
        return self._text
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"HTTP {self.status_code}", 
                request=Mock(), 
                response=self
            )


@pytest.fixture
def test_response_factory():
    """Factory for creating test HTTP responses."""
    return TestHTTPResponse