import os
import logging
from typing import Any, Dict, Mapping, Optional, Union
import time

import httpx
from attrs import define, field
from httpx import Timeout

from . import __version__
from .errors import (
    raise_for_status_code,
    StatesetAPIError,
    StatesetConnectionError,
    StatesetRateLimitError,
    StatesetAuthenticationError
)

logger = logging.getLogger(__name__)


@define
class RetryConfig:
    """Configuration for request retries."""
    
    max_retries: int = field(default=3)
    backoff_factor: float = field(default=0.5)
    retry_status_codes: tuple = field(default=(429, 500, 502, 503, 504))
    
    def calculate_delay(self, attempt: int) -> float:
        """Calculate delay for exponential backoff."""
        return self.backoff_factor * (2 ** attempt)


class Client:
    """HTTP client wrapper with enhanced error handling and retry logic."""

    def __init__(
        self,
        *,
        base_url: str,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Union[Timeout, float, None] = None,
        follow_redirects: bool = True,
        verify_ssl: Union[bool, str] = True,
        raise_on_unexpected_status: bool = False,
        httpx_args: Optional[Dict[str, Any]] = None,
        retry_config: Optional[RetryConfig] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})
        self.headers.setdefault("User-Agent", f"stateset-python/{__version__}")
        self.timeout = (
            timeout if isinstance(timeout, Timeout) else Timeout(timeout or 30.0)
        )
        self.follow_redirects = follow_redirects
        self.verify_ssl = verify_ssl
        self.raise_on_unexpected_status = raise_on_unexpected_status
        self.httpx_args = dict(httpx_args or {})
        self.retry_config = retry_config or RetryConfig()
        self._client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

    # Synchronous httpx client -------------------------------------------------
    def get_httpx_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=self.follow_redirects,
                verify=self.verify_ssl,
                **self.httpx_args,
            )
        return self._client

    def set_httpx_client(self, client: httpx.Client) -> None:
        """Use a custom :class:`httpx.Client` instance."""
        # Close any previously created client
        if self._client is not None and not self._client.is_closed:
            self._client.close()
        self._client = client
        # Keep configuration in sync with the new client
        self.base_url = str(client.base_url).rstrip("/")
        self.headers = dict(client.headers)
        self.timeout = client.timeout
        self.follow_redirects = client.follow_redirects
        self.verify_ssl = client.verify

    # Async httpx client -------------------------------------------------------
    def get_async_httpx_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=self.follow_redirects,
                verify=self.verify_ssl,
                **self.httpx_args,
            )
        return self._async_client

    def set_async_httpx_client(self, client: httpx.AsyncClient) -> None:
        """Use a custom :class:`httpx.AsyncClient` instance."""
        if self._async_client is not None and not self._async_client.is_closed:
            try:
                import asyncio

                asyncio.get_event_loop().run_until_complete(self._async_client.aclose())
            except Exception:
                pass
        self._async_client = client
        self.base_url = str(client.base_url).rstrip("/")
        self.headers = dict(client.headers)
        self.timeout = client.timeout
        self.follow_redirects = client.follow_redirects
        self.verify_ssl = client.verify

    def _should_retry(self, response: httpx.Response, attempt: int) -> bool:
        """Determine if request should be retried."""
        if attempt >= self.retry_config.max_retries:
            return False
        
        return response.status_code in self.retry_config.retry_status_codes

    async def _make_request_with_retries(
        self, method: str, path: str, **kwargs: Any
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        client = self.get_async_httpx_client()
        last_exception = None
        
        for attempt in range(self.retry_config.max_retries + 1):
            try:
                response = await client.request(method, path, **kwargs)
                
                if self._should_retry(response, attempt):
                    delay = self.retry_config.calculate_delay(attempt)
                    logger.warning(
                        f"Request failed with status {response.status_code}, "
                        f"retrying in {delay}s (attempt {attempt + 1})"
                    )
                    await asyncio.sleep(delay)
                    continue
                
                return response
                
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt < self.retry_config.max_retries:
                    delay = self.retry_config.calculate_delay(attempt)
                    logger.warning(
                        f"Connection error: {e}, retrying in {delay}s "
                        f"(attempt {attempt + 1})"
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise StatesetConnectionError(f"Connection failed: {e}") from e
        
        # If we get here, all retries failed
        if last_exception:
            raise StatesetConnectionError(f"Connection failed: {last_exception}") from last_exception

    # Enhanced async request helpers with retry logic -------------------------
    async def get(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make GET request with retry logic and error handling."""
        try:
            response = await self._make_request_with_retries("GET", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise StatesetRateLimitError("Rate limit exceeded", response=e.response)
            raise_for_status_code(e.response.status_code, e.response.content)
        except httpx.RequestError as e:
            raise StatesetConnectionError(f"Request failed: {e}") from e

    async def post(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make POST request with retry logic and error handling."""
        try:
            response = await self._make_request_with_retries("POST", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise StatesetRateLimitError("Rate limit exceeded", response=e.response)
            raise_for_status_code(e.response.status_code, e.response.content)
        except httpx.RequestError as e:
            raise StatesetConnectionError(f"Request failed: {e}") from e

    async def put(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make PUT request with retry logic and error handling."""
        try:
            response = await self._make_request_with_retries("PUT", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise StatesetRateLimitError("Rate limit exceeded", response=e.response)
            raise_for_status_code(e.response.status_code, e.response.content)
        except httpx.RequestError as e:
            raise StatesetConnectionError(f"Request failed: {e}") from e

    async def delete(self, path: str, **kwargs: Any) -> None:
        """Make DELETE request with retry logic and error handling."""
        try:
            response = await self._make_request_with_retries("DELETE", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise StatesetRateLimitError("Rate limit exceeded", response=e.response)
            raise_for_status_code(e.response.status_code, e.response.content)
        except httpx.RequestError as e:
            raise StatesetConnectionError(f"Request failed: {e}") from e

    # Context manager support
    def __enter__(self) -> "Client":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()

    def close(self) -> None:
        """Close the synchronous HTTP client."""
        if self._client is not None and not self._client.is_closed:
            self._client.close()

    async def aclose(self) -> None:
        """Close the asynchronous HTTP client."""
        if self._async_client is not None and not self._async_client.is_closed:
            await self._async_client.aclose()


class AuthenticatedClient(Client):
    """An HTTP client with authentication support."""

    def __init__(
        self,
        *,
        base_url: str,
        token: str,
        headers: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        if not token:
            raise StatesetAuthenticationError("API token is required")
        
        auth_headers = dict(headers or {})
        auth_headers["Authorization"] = f"Bearer {token}"
        
        super().__init__(base_url=base_url, headers=auth_headers, **kwargs)
        self.token = token


class Stateset:
    """
    High-level Stateset client with environment-based configuration.
    
    This client reads configuration from environment variables and provides
    a convenient interface for interacting with the Stateset API.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        follow_redirects: Optional[bool] = None,
        verify_ssl: Optional[Union[bool, str]] = None,
        httpx_args: Optional[Dict[str, Any]] = None,
        retry_config: Optional[RetryConfig] = None,
    ) -> None:
        # Read configuration from environment variables
        self._api_key = api_key or os.getenv("STATESET_API_KEY")
        if not self._api_key:
            raise StatesetAuthenticationError(
                "API key is required. Set STATESET_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self._base_url = base_url or os.getenv("STATESET_BASE_URL", "https://api.stateset.com")
        
        # Parse environment variables with defaults
        timeout = timeout or float(os.getenv("STATESET_TIMEOUT", "30"))
        follow_redirects = (
            follow_redirects 
            if follow_redirects is not None 
            else os.getenv("STATESET_FOLLOW_REDIRECTS", "true").lower() == "true"
        )
        
        # SSL verification handling
        ssl_env = os.getenv("STATESET_VERIFY_SSL", "true").lower()
        if verify_ssl is None:
            if ssl_env == "false":
                verify_ssl = False
            elif ssl_env == "true":
                verify_ssl = True
            else:
                verify_ssl = ssl_env  # Path to certificate bundle

        # Proxy configuration
        proxy_env = os.getenv("STATESET_HTTPX_PROXIES")
        if proxy_env and httpx_args is None:
            httpx_args = {"proxies": proxy_env}

        self._client = AuthenticatedClient(
            base_url=self._base_url,
            token=self._api_key,
            timeout=timeout,
            follow_redirects=follow_redirects,
            verify_ssl=verify_ssl,
            httpx_args=httpx_args,
            retry_config=retry_config,
        )

        # Initialize resource managers
        self._init_resources()

    def _init_resources(self) -> None:
        """Initialize resource managers."""
        # Import here to avoid circular imports
        from .resources.order_resource import Orders
        from .resources.return_resource import Returns
        from .resources.warranty_resource import Warranties
        from .resources.customer_resource import Customers
        # Add other resource imports as needed

        self.orders = Orders(self._client)
        self.returns = Returns(self._client)
        self.warranties = Warranties(self._client)
        self.customers = Customers(self._client)
        # Add other resource initializations as needed

    # Context manager support
    def __enter__(self) -> "Stateset":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def __aenter__(self) -> "Stateset":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    async def aclose(self) -> None:
        """Close the HTTP client asynchronously."""
        await self._client.aclose()

    @property
    def api_key(self) -> str:
        """Get the API key (masked for security)."""
        return f"{self._api_key[:8]}..." if len(self._api_key) > 8 else "***"

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._base_url
