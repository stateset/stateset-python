import os
import logging
from typing import Any, Dict, Mapping, Optional, Union, Callable, List
import time
import asyncio
from datetime import datetime, timedelta

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


@define
class PerformanceMetrics:
    """Track performance metrics for requests."""
    
    total_requests: int = field(default=0)
    successful_requests: int = field(default=0)
    failed_requests: int = field(default=0)
    total_response_time: float = field(default=0.0)
    cache_hits: int = field(default=0)
    cache_misses: int = field(default=0)
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests
    
    @property
    def average_response_time(self) -> float:
        if self.successful_requests == 0:
            return 0.0
        return self.total_response_time / self.successful_requests
    
    @property
    def cache_hit_rate(self) -> float:
        total_cache_requests = self.cache_hits + self.cache_misses
        if total_cache_requests == 0:
            return 0.0
        return self.cache_hits / total_cache_requests
    
    def record_request(self, success: bool, response_time: float) -> None:
        """Record a request's performance metrics."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
            self.total_response_time += response_time
        else:
            self.failed_requests += 1
    
    def record_cache_hit(self) -> None:
        """Record a cache hit."""
        self.cache_hits += 1
    
    def record_cache_miss(self) -> None:
        """Record a cache miss."""
        self.cache_misses += 1


@define
class RequestContext:
    """Context information for a request."""
    
    method: str
    url: str
    headers: Dict[str, str] = field(factory=dict)
    started_at: datetime = field(factory=datetime.now)
    attempt: int = field(default=1)
    metadata: Dict[str, Any] = field(factory=dict)
    
    @property
    def duration(self) -> timedelta:
        return datetime.now() - self.started_at


# Type aliases for event hooks
RequestHook = Callable[[RequestContext], None]
ResponseHook = Callable[[RequestContext, httpx.Response], None]
ErrorHook = Callable[[RequestContext, Exception], None]


class Client:
    """Enhanced HTTP client wrapper with advanced features."""

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
        enable_metrics: bool = True,
        debug: bool = False,
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
        self.enable_metrics = enable_metrics
        self.debug = debug
        
        # Performance tracking
        self.metrics = PerformanceMetrics() if enable_metrics else None
        
        # Event hooks
        self.request_hooks: List[RequestHook] = []
        self.response_hooks: List[ResponseHook] = []
        self.error_hooks: List[ErrorHook] = []
        
        # Client instances
        self._client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None
        
        # Rate limiting
        self._rate_limit_remaining: Optional[int] = None
        self._rate_limit_reset: Optional[datetime] = None
        
        if debug:
            self._setup_debug_logging()

    def _setup_debug_logging(self) -> None:
        """Setup debug logging for HTTP requests."""
        debug_logger = logging.getLogger("stateset.client.debug")
        debug_logger.setLevel(logging.DEBUG)
        
        def log_request(ctx: RequestContext) -> None:
            debug_logger.debug(f"→ {ctx.method} {ctx.url}")
            if ctx.headers:
                for key, value in ctx.headers.items():
                    # Mask sensitive headers
                    if "authorization" in key.lower() or "token" in key.lower():
                        value = f"{value[:8]}..." if len(value) > 8 else "***"
                    debug_logger.debug(f"  {key}: {value}")
        
        def log_response(ctx: RequestContext, response: httpx.Response) -> None:
            duration_ms = ctx.duration.total_seconds() * 1000
            debug_logger.debug(
                f"← {response.status_code} {ctx.method} {ctx.url} "
                f"({duration_ms:.1f}ms)"
            )
        
        def log_error(ctx: RequestContext, error: Exception) -> None:
            duration_ms = ctx.duration.total_seconds() * 1000
            debug_logger.debug(
                f"✗ {ctx.method} {ctx.url} failed after {duration_ms:.1f}ms: {error}"
            )
        
        self.add_request_hook(log_request)
        self.add_response_hook(log_response)
        self.add_error_hook(log_error)

    def add_request_hook(self, hook: RequestHook) -> None:
        """Add a request hook."""
        self.request_hooks.append(hook)

    def add_response_hook(self, hook: ResponseHook) -> None:
        """Add a response hook."""
        self.response_hooks.append(hook)

    def add_error_hook(self, hook: ErrorHook) -> None:
        """Add an error hook."""
        self.error_hooks.append(hook)

    def _call_request_hooks(self, ctx: RequestContext) -> None:
        """Call all request hooks."""
        for hook in self.request_hooks:
            try:
                hook(ctx)
            except Exception as e:
                logger.warning(f"Request hook failed: {e}")

    def _call_response_hooks(self, ctx: RequestContext, response: httpx.Response) -> None:
        """Call all response hooks."""
        for hook in self.response_hooks:
            try:
                hook(ctx, response)
            except Exception as e:
                logger.warning(f"Response hook failed: {e}")

    def _call_error_hooks(self, ctx: RequestContext, error: Exception) -> None:
        """Call all error hooks."""
        for hook in self.error_hooks:
            try:
                hook(ctx, error)
            except Exception as e:
                logger.warning(f"Error hook failed: {e}")

    def _update_rate_limit_info(self, response: httpx.Response) -> None:
        """Update rate limit information from response headers."""
        try:
            remaining = response.headers.get("X-RateLimit-Remaining")
            if remaining:
                self._rate_limit_remaining = int(remaining)
            
            reset_timestamp = response.headers.get("X-RateLimit-Reset")
            if reset_timestamp:
                self._rate_limit_reset = datetime.fromtimestamp(int(reset_timestamp))
        except (ValueError, TypeError):
            pass  # Ignore invalid rate limit headers

    @property
    def rate_limit_remaining(self) -> Optional[int]:
        """Get remaining rate limit requests."""
        return self._rate_limit_remaining

    @property
    def rate_limit_reset(self) -> Optional[datetime]:
        """Get rate limit reset time."""
        return self._rate_limit_reset

    def get_performance_metrics(self) -> Optional[PerformanceMetrics]:
        """Get performance metrics."""
        return self.metrics

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

    async def _wait_for_rate_limit(self) -> None:
        """Wait if rate limited."""
        if (self._rate_limit_remaining is not None and 
            self._rate_limit_remaining <= 0 and 
            self._rate_limit_reset is not None):
            
            now = datetime.now()
            if self._rate_limit_reset > now:
                wait_time = (self._rate_limit_reset - now).total_seconds()
                logger.info(f"Rate limited, waiting {wait_time:.1f} seconds")
                await asyncio.sleep(wait_time)

    async def _make_request_with_retries(
        self, method: str, path: str, **kwargs: Any
    ) -> httpx.Response:
        """Make HTTP request with enhanced retry logic and monitoring."""
        client = self.get_async_httpx_client()
        last_exception = None
        full_url = f"{self.base_url.rstrip('/')}{path}" if not path.startswith('http') else path
        
        # Create request context
        ctx = RequestContext(
            method=method,
            url=full_url,
            headers=kwargs.get('headers', {}),
        )
        
        # Call request hooks
        self._call_request_hooks(ctx)
        
        for attempt in range(self.retry_config.max_retries + 1):
            ctx.attempt = attempt + 1
            start_time = time.time()
            
            try:
                # Wait for rate limit if needed
                await self._wait_for_rate_limit()
                
                response = await client.request(method, path, **kwargs)
                response_time = time.time() - start_time
                
                # Update rate limit info
                self._update_rate_limit_info(response)
                
                # Call response hooks
                self._call_response_hooks(ctx, response)
                
                # Record metrics
                if self.metrics:
                    self.metrics.record_request(True, response_time)
                
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
                response_time = time.time() - start_time
                last_exception = e
                
                # Call error hooks
                self._call_error_hooks(ctx, e)
                
                # Record metrics
                if self.metrics:
                    self.metrics.record_request(False, response_time)
                
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
        """Make GET request with enhanced error handling and monitoring."""
        try:
            response = await self._make_request_with_retries("GET", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                raise StatesetRateLimitError(
                    "Rate limit exceeded", 
                    response=e.response,
                    retry_after=int(retry_after) if retry_after else None
                )
            raise_for_status_code(e.response.status_code, e.response.content)
        except httpx.RequestError as e:
            raise StatesetConnectionError(f"Request failed: {e}") from e

    async def post(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make POST request with enhanced error handling and monitoring."""
        try:
            response = await self._make_request_with_retries("POST", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                raise StatesetRateLimitError(
                    "Rate limit exceeded", 
                    response=e.response,
                    retry_after=int(retry_after) if retry_after else None
                )
            raise_for_status_code(e.response.status_code, e.response.content)
        except httpx.RequestError as e:
            raise StatesetConnectionError(f"Request failed: {e}") from e

    async def put(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make PUT request with enhanced error handling and monitoring."""
        try:
            response = await self._make_request_with_retries("PUT", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                raise StatesetRateLimitError(
                    "Rate limit exceeded", 
                    response=e.response,
                    retry_after=int(retry_after) if retry_after else None
                )
            raise_for_status_code(e.response.status_code, e.response.content)
        except httpx.RequestError as e:
            raise StatesetConnectionError(f"Request failed: {e}") from e

    async def delete(self, path: str, **kwargs: Any) -> None:
        """Make DELETE request with enhanced error handling and monitoring."""
        try:
            response = await self._make_request_with_retries("DELETE", path, **kwargs)
            raise_for_status_code(response.status_code, response.content)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                raise StatesetRateLimitError(
                    "Rate limit exceeded", 
                    response=e.response,
                    retry_after=int(retry_after) if retry_after else None
                )
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
    """An HTTP client with authentication support and enhanced features."""

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

    def get_masked_token(self) -> str:
        """Get the API token with masking for security."""
        return f"{self.token[:8]}..." if len(self.token) > 8 else "***"


class Stateset:
    """
    Enhanced high-level Stateset client with environment-based configuration.
    
    This client reads configuration from environment variables and provides
    a convenient interface for interacting with the Stateset API with advanced features.
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
        enable_metrics: bool = True,
        debug: bool = None,
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
        
        # Debug mode
        if debug is None:
            debug = os.getenv("STATESET_DEBUG", "false").lower() == "true"
        
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
            enable_metrics=enable_metrics,
            debug=debug,
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

    def add_request_hook(self, hook: RequestHook) -> None:
        """Add a request hook to monitor requests."""
        self._client.add_request_hook(hook)

    def add_response_hook(self, hook: ResponseHook) -> None:
        """Add a response hook to monitor responses."""
        self._client.add_response_hook(hook)

    def add_error_hook(self, hook: ErrorHook) -> None:
        """Add an error hook to monitor errors."""
        self._client.add_error_hook(hook)

    def get_performance_metrics(self) -> Optional[PerformanceMetrics]:
        """Get performance metrics for this client."""
        return self._client.get_performance_metrics()

    @property
    def rate_limit_remaining(self) -> Optional[int]:
        """Get remaining rate limit requests."""
        return self._client.rate_limit_remaining

    @property
    def rate_limit_reset(self) -> Optional[datetime]:
        """Get rate limit reset time."""
        return self._client.rate_limit_reset

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
        return self._client.get_masked_token()

    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._base_url
