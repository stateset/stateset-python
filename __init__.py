"""A Python client library for accessing the Stateset API

This library provides a convenient interface to interact with the Stateset API,
offering support for all Stateset resources including returns, warranties, orders,
inventory management, and more.

Basic usage:
    ```python
    from stateset import Stateset
    
    # Initialize the client
    client = Stateset(api_key="your_api_key")
    
    # Make API calls
    async with client:
        # Get a list of returns
        returns = await client.returns.list()
        
        # Create a new order
        order = await client.orders.create({
            "customer_id": "cust_123",
            "items": [{"product_id": "prod_456", "quantity": 1}]
        })
    ```
"""

from .client import AuthenticatedClient, Client, Stateset
from .stateset_types import (
    StatesetID,
    Timestamp,
    Metadata,
    StatesetObject,
    OrderStatus,
    ReturnStatus,
    WarrantyStatus,
    PaginationParams,
    PaginatedList,
    File,
    FileUploadError,
    Response,
    UNSET
)
from .errors import (
    StatesetError,
    StatesetInvalidRequestError,
    StatesetAPIError,
    StatesetAuthenticationError,
    StatesetPermissionError,
    StatesetNotFoundError,
    StatesetConnectionError,
    StatesetRateLimitError
)

# Semantic version of the SDK
__version__ = "1.0.0"

# API version supported by this SDK
__api_version__ = "2024-01"

__all__ = [
    # Main client
    "Stateset",
    
    # Base clients
    "AuthenticatedClient",
    "Client",
    
    # Types
    "StatesetID",
    "Timestamp",
    "Metadata",
    "StatesetObject",
    "OrderStatus",
    "ReturnStatus",
    "WarrantyStatus",
    "PaginationParams",
    "PaginatedList",
    "File",
    "FileUploadError",
    "Response",
    "UNSET",
    
    # Errors
    "StatesetError",
    "StatesetInvalidRequestError",
    "StatesetAPIError",
    "StatesetAuthenticationError",
    "StatesetPermissionError",
    "StatesetNotFoundError",
    "StatesetConnectionError",
    "StatesetRateLimitError",
    
    # Version info
    "__version__",
    "__api_version__",
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

# Type checking
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .resources.return_resource import Returns
    from .resources.warranty_resource import Warranties
    from .resources.order_resource import Orders
    from .resources.inventory_resource import Inventory
    # Add other resource types as needed
