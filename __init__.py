"""A Python client library for accessing the Stateset API

This library provides a convenient interface to interact with the Stateset API,
offering support for all Stateset resources including returns, warranties, orders,
inventory management, and more.

Basic usage:
    ```python
    from stateset import Stateset

    # Initialize the client using environment variables
    # STATESET_API_KEY and optional STATESET_BASE_URL
    client = Stateset()

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
from .errors import (
    StatesetAPIError,
    StatesetAuthenticationError,
    StatesetConnectionError,
    StatesetError,
    StatesetInvalidRequestError,
    StatesetNotFoundError,
    StatesetPermissionError,
    StatesetRateLimitError,
)
from .stateset_types import (
    UNSET,
    File,
    FileUploadError,
    Metadata,
    OrderStatus,
    PaginatedList,
    PaginationParams,
    Response,
    ReturnStatus,
    StatesetID,
    StatesetObject,
    Timestamp,
    WarrantyStatus,
)

# Semantic version of the SDK
__version__ = "1.1.0"

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
