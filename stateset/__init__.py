"""
Stateset Python SDK - Enhanced version with advanced features.

A comprehensive Python client library for the Stateset API with:
- Full async/await support
- Advanced query building and filtering  
- Intelligent caching and performance optimization
- Comprehensive error handling with debugging context
- Bulk operations and batch processing
- Request/response monitoring and metrics
- Developer-friendly utilities and tools

Basic Usage:
    >>> from stateset import Stateset
    >>> async with Stateset() as client:
    ...     orders = await client.orders.list()
    ...     order = await client.orders.create({
    ...         "customer_id": "cust_123",
    ...         "total_amount": 99.99
    ...     })

Advanced Usage:
    >>> # Query building with advanced filtering
    >>> high_value_orders = await client.orders.high_value(1000).recent(30).all()
    >>> 
    >>> # Bulk operations
    >>> result = await client.orders.bulk_create([...])
    >>> 
    >>> # Performance monitoring
    >>> metrics = client.get_performance_metrics()
    >>> print(f"Success rate: {metrics.success_rate:.2%}")

Environment Variables:
    - STATESET_API_KEY: Your API key (required)
    - STATESET_BASE_URL: API base URL (default: https://api.stateset.com)
    - STATESET_TIMEOUT: Request timeout in seconds (default: 30)
    - STATESET_DEBUG: Enable debug logging (default: false)
    - STATESET_VERIFY_SSL: SSL verification (default: true)

For detailed documentation, visit: https://docs.stateset.com/python-sdk
"""

from typing import TYPE_CHECKING

# Core client classes
from .client import (
    Stateset,
    AuthenticatedClient,
    Client,
    RetryConfig,
    PerformanceMetrics,
    RequestContext,
)

# Base resource system with enhanced features
from .base_resource import (
    BaseResource,
    ResourceQuery,
    FilterParams,
    FilterOperator,
    FilterExpression,
    RequestOptions,
    BulkOperationResult,
)

# Comprehensive error handling
from .errors import (
    StatesetError,
    StatesetValidationError,
    StatesetInvalidRequestError,
    StatesetAPIError,
    StatesetAuthenticationError,
    StatesetPermissionError,
    StatesetNotFoundError,
    StatesetConnectionError,
    StatesetTimeoutError,
    StatesetRateLimitError,
    StatesetMaintenanceError,
    StatesetDeprecationWarning,
    raise_for_status_code,
)

# Type definitions and utilities
from .stateset_types import (
    PaginatedList,
    PaginationParams,
    StatesetObject,
    OrderStatus,
    ReturnStatus,
    WarrantyStatus,
    UNSET,
    UnsetType,
)

# Version information
from .version import __version__

if TYPE_CHECKING:
    # Resource imports for type checking only
    from .resources.order_resource import Orders
    from .resources.return_resource import Returns
    from .resources.warranty_resource import Warranties
    from .resources.customer_resource import Customers

# Package metadata
__title__ = "stateset"
__description__ = "Enhanced Python client for the Stateset API"
__url__ = "https://github.com/stateset/stateset-python"
__author__ = "Stateset Team"
__author_email__ = "support@stateset.com"
__license__ = "MIT"
__copyright__ = "Copyright 2024 Stateset"

# Convenience aliases for common use cases
StatesetClient = Stateset  # Alternative name for the main client

# Default configuration values
DEFAULT_BASE_URL = "https://api.stateset.com"
DEFAULT_TIMEOUT = 30.0
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_PAGINATION_LIMIT = 50
MAX_PAGINATION_LIMIT = 1000

# Feature flags for experimental features
EXPERIMENTAL_FEATURES = {
    "enhanced_caching": True,
    "bulk_operations": True,
    "performance_metrics": True,
    "request_hooks": True,
}

# SDK information for debugging and support
SDK_INFO = {
    "name": __title__,
    "version": __version__,
    "description": __description__,
    "url": __url__,
    "author": __author__,
    "license": __license__,
}


def get_sdk_info() -> dict:
    """Get SDK information for debugging and support."""
    return SDK_INFO.copy()


def enable_debug_logging():
    """Enable debug logging for the SDK."""
    import logging
    
    # Set up comprehensive logging
    logger = logging.getLogger("stateset")
    logger.setLevel(logging.DEBUG)
    
    # Create console handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    print("✓ Stateset SDK debug logging enabled")


def disable_debug_logging():
    """Disable debug logging for the SDK."""
    import logging
    
    logger = logging.getLogger("stateset")
    logger.setLevel(logging.WARNING)
    
    print("✓ Stateset SDK debug logging disabled")


def check_environment():
    """Check environment configuration and provide recommendations."""
    import os
    
    print("Stateset SDK Environment Check")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv("STATESET_API_KEY")
    if api_key:
        masked_key = f"{api_key[:8]}..." if len(api_key) > 8 else "***"
        print(f"✓ API Key: {masked_key}")
    else:
        print("✗ API Key: Not set (required)")
        print("  Set STATESET_API_KEY environment variable")
    
    # Check base URL
    base_url = os.getenv("STATESET_BASE_URL", DEFAULT_BASE_URL)
    print(f"✓ Base URL: {base_url}")
    
    # Check timeout
    timeout = os.getenv("STATESET_TIMEOUT", str(DEFAULT_TIMEOUT))
    print(f"✓ Timeout: {timeout}s")
    
    # Check debug mode
    debug = os.getenv("STATESET_DEBUG", "false").lower() == "true"
    print(f"✓ Debug Mode: {'Enabled' if debug else 'Disabled'}")
    
    # Check SSL verification
    ssl_verify = os.getenv("STATESET_VERIFY_SSL", "true")
    print(f"✓ SSL Verification: {ssl_verify}")
    
    print()
    print("SDK Information:")
    print(f"  Version: {__version__}")
    print(f"  Documentation: https://docs.stateset.com/python-sdk")
    print(f"  Support: {__author_email__}")


# Export all public symbols
__all__ = [
    # Core client
    "Stateset",
    "StatesetClient",
    "AuthenticatedClient", 
    "Client",
    "RetryConfig",
    "PerformanceMetrics",
    "RequestContext",
    
    # Base resource system
    "BaseResource",
    "ResourceQuery", 
    "FilterParams",
    "FilterOperator",
    "FilterExpression",
    "RequestOptions",
    "BulkOperationResult",
    
    # Error handling
    "StatesetError",
    "StatesetValidationError",
    "StatesetInvalidRequestError",
    "StatesetAPIError", 
    "StatesetAuthenticationError",
    "StatesetPermissionError",
    "StatesetNotFoundError",
    "StatesetConnectionError",
    "StatesetTimeoutError",
    "StatesetRateLimitError",
    "StatesetMaintenanceError",
    "StatesetDeprecationWarning",
    "raise_for_status_code",
    
    # Types and utilities
    "PaginatedList",
    "PaginationParams",
    "StatesetObject",
    "OrderStatus",
    "ReturnStatus", 
    "WarrantyStatus",
    "UNSET",
    "UnsetType",
    
    # Utilities
    "get_sdk_info",
    "enable_debug_logging",
    "disable_debug_logging",
    "check_environment",
    
    # Constants
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "DEFAULT_RETRY_ATTEMPTS",
    "DEFAULT_PAGINATION_LIMIT",
    "MAX_PAGINATION_LIMIT",
    "SDK_INFO",
    "EXPERIMENTAL_FEATURES",
    
    # Version
    "__version__",
    "__title__",
    "__description__",
    "__url__",
    "__author__",
    "__author_email__",
    "__license__",
    "__copyright__",
]

# Set default logging handler to avoid "No handler found" warnings.
import logging

try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


logging.getLogger(__name__).addHandler(NullHandler())

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .resources.agent_resource import Agents
    from .resources.attribute_resource import Attributes
    from .resources.case_ticket_resource import CaseTickets
    from .resources.customer_resource import Customers
    from .resources.eval_resource import Evals
    from .resources.inventory_resource import Inventory
    from .resources.knowledge_resource import KnowledgeBase
    from .resources.message_resource import Messages
    from .resources.note_resource import Notes
    from .resources.order_resource import Orders
    from .resources.fulfillment_order_resource import FulfillmentOrders
    from .resources.item_receipt_resource import ItemReceipts
    from .resources.cash_sale_resource import CashSales
    from .resources.payment_resource import Payments
    from .resources.response_resource import Responses
    from .resources.return_line_resource import ReturnLines
    from .resources.return_resource import Returns
    from .resources.rule_resource import Rules
    from .resources.warranty_line_resource import WarrantyLines
    from .resources.warranty_resource import Warranties

    # Add other resource types as needed

