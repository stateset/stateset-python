# Stateset Python SDK

[![PyPI version](https://badge.fury.io/py/stateset.svg)](https://badge.fury.io/py/stateset)
[![Python versions](https://img.shields.io/pypi/pyversions/stateset.svg)](https://pypi.org/project/stateset/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/stateset/stateset-python/branch/main/graph/badge.svg)](https://codecov.io/gh/stateset/stateset-python)
[![Tests](https://github.com/stateset/stateset-python/workflows/Test/badge.svg)](https://github.com/stateset/stateset-python/actions)

The official Python client library for the [Stateset API](https://docs.stateset.com). Simplify e-commerce operations with powerful tools for returns, warranties, orders, and inventory management.

## 🚀 Features

- ✅ **Full API Coverage** - Support for all Stateset API endpoints
- ✅ **Type Safety** - Complete type hints and validation with Pydantic
- ✅ **Async/Await Support** - Built for modern Python applications
- ✅ **Automatic Retries** - Intelligent retry logic with exponential backoff
- ✅ **Rate Limiting** - Built-in rate limit handling
- ✅ **Pagination** - Seamless iteration through large datasets
- ✅ **Error Handling** - Comprehensive error types and debugging info
- ✅ **Environment Configuration** - Easy setup via environment variables
- ✅ **Context Managers** - Proper resource management
- ✅ **Query Builder** - Fluent interface for complex queries

## 📦 Installation

```bash
pip install stateset
```

### Requirements

- Python 3.8+
- httpx >= 0.24.0
- pydantic >= 2.0.0

## 🔧 Quick Start

### Environment Setup

Set your API credentials as environment variables:

```bash
export STATESET_API_KEY="your_api_key_here"
export STATESET_BASE_URL="https://api.stateset.com"  # optional
```

### Basic Usage

```python
from stateset import Stateset

# Initialize the client (reads from environment variables)
client = Stateset()

# Create a new order
async with client:
    order = await client.orders.create({
        "customer_id": "cust_123",
        "status": "pending",
        "items": [
            {
                "product_id": "prod_456",
                "quantity": 2,
                "price": 49.99
            }
        ],
        "total_amount": 99.98
    })
    print(f"Created order: {order.id}")
```

### Synchronous Usage

While the SDK is built with async/await in mind, you can use it synchronously:

```python
import asyncio
from stateset import Stateset

def create_order_sync():
    async def _create_order():
        client = Stateset()
        async with client:
            return await client.orders.create({
                "customer_id": "cust_123",
                "status": "pending",
                "total_amount": 99.98
            })
    
    return asyncio.run(_create_order())

order = create_order_sync()
```

## 📚 Core Resources

### Orders

```python
from stateset import Stateset
from stateset.base_resource import FilterParams, PaginationParams

async with Stateset() as client:
    # Create an order
    order = await client.orders.create({
        "customer_id": "cust_123",
        "status": "pending",
        "total_amount": 99.98
    })
    
    # Get an order
    order = await client.orders.get("order_123")
    
    # Update an order
    order = await client.orders.update("order_123", {
        "status": "processing"
    })
    
    # List orders with pagination
    orders = await client.orders.list(
        pagination=PaginationParams(page=1, per_page=20),
        filters=FilterParams(status="pending")
    )
    
    # Query builder approach
    pending_orders = await client.orders.with_filters(
        status="pending"
    ).created_after("2024-01-01").limit(50).all()
    
    # Iterate through all orders
    async for order in client.orders.iter_all():
        print(f"Order {order.id}: {order.status}")
```

### Returns

```python
async with Stateset() as client:
    # Create a return
    return_request = await client.returns.create({
        "order_id": "order_123",
        "reason": "defective",
        "items": [
            {
                "product_id": "prod_456",
                "quantity": 1,
                "reason": "damaged"
            }
        ]
    })
    
    # Process a return
    return_request = await client.returns.update(
        return_request.id,
        {"status": "approved"}
    )
    
    # List returns by status
    approved_returns = await client.returns.with_filters(
        status="approved"
    ).sort_by("created", "desc").all()
```

### Warranties

```python
async with Stateset() as client:
    # Create a warranty
    warranty = await client.warranties.create({
        "product_id": "prod_456",
        "customer_id": "cust_123",
        "start_date": "2024-01-01",
        "end_date": "2025-01-01"
    })
    
    # Check warranty status
    warranty = await client.warranties.get("warranty_123")
    is_active = warranty.status == "active"
    
    # List active warranties
    active_warranties = await client.warranties.with_filters(
        status="active"
    ).all()
```

### Customers

```python
async with Stateset() as client:
    # Create a customer
    customer = await client.customers.create({
        "email": "customer@example.com",
        "name": "John Doe",
        "phone": "+1234567890"
    })
    
    # Get customer with their orders
    customer = await client.customers.get("cust_123")
    
    # Update customer information
    customer = await client.customers.update("cust_123", {
        "name": "John Smith"
    })
```

## 🔍 Advanced Usage

### Query Builder

The SDK provides a fluent query builder for complex operations:

```python
from datetime import datetime, timedelta

async with Stateset() as client:
    # Complex query with method chaining
    recent_high_value_orders = await client.orders.with_filters(
        status="completed"
    ).created_after(
        (datetime.now() - timedelta(days=30)).isoformat()
    ).where(
        total_amount__gte=1000.00
    ).sort_by("total_amount", "desc").limit(100).all()
    
    # Get first matching result
    latest_order = await client.orders.with_filters(
        customer_id="cust_123"
    ).sort_by("created", "desc").first()
    
    # Count results without fetching
    order_count = await client.orders.with_filters(
        status="pending"
    ).count()
```

### Custom Request Options

```python
from stateset.base_resource import RequestOptions

async with Stateset() as client:
    # Custom timeout and headers
    options = RequestOptions(
        timeout=60.0,
        headers={"X-Custom-Header": "value"},
        idempotency_key="unique-key-123"
    )
    
    order = await client.orders.create(
        {"customer_id": "cust_123", "total_amount": 99.98},
        options=options
    )
```

### Error Handling

```python
from stateset.errors import (
    StatesetError,
    StatesetAPIError,
    StatesetAuthenticationError,
    StatesetRateLimitError,
    StatesetConnectionError
)

async with Stateset() as client:
    try:
        order = await client.orders.get("invalid_id")
    except StatesetAPIError as e:
        print(f"API Error: {e.message}")
        print(f"Status Code: {e.status_code}")
        print(f"Error Type: {e.type}")
    except StatesetRateLimitError as e:
        print(f"Rate limited. Retry after: {e.retry_after}")
    except StatesetAuthenticationError as e:
        print(f"Authentication failed: {e.message}")
    except StatesetConnectionError as e:
        print(f"Connection error: {e.message}")
    except StatesetError as e:
        print(f"General Stateset error: {e.message}")
```

### Custom Retry Configuration

```python
from stateset import Stateset
from stateset.client import RetryConfig

# Custom retry configuration
retry_config = RetryConfig(
    max_retries=5,
    backoff_factor=1.0,
    retry_status_codes=(429, 500, 502, 503, 504)
)

client = Stateset(retry_config=retry_config)
```

### Pagination Patterns

```python
async with Stateset() as client:
    # Manual pagination
    page = 1
    per_page = 50
    
    while True:
        orders = await client.orders.list(
            pagination=PaginationParams(page=page, per_page=per_page)
        )
        
        for order in orders.data:
            # Process order
            print(f"Processing order: {order.id}")
        
        if not orders.has_next:
            break
        page += 1
    
    # Automatic iteration (recommended)
    async for order in client.orders.iter_all():
        print(f"Processing order: {order.id}")
    
    # Get all results at once (use carefully for large datasets)
    all_orders = await client.orders.list_all(max_items=1000)
```

## ⚙️ Configuration

### Environment Variables

The SDK supports the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `STATESET_API_KEY` | Your Stateset API key | Required |
| `STATESET_BASE_URL` | API base URL | `https://api.stateset.com` |
| `STATESET_TIMEOUT` | Request timeout in seconds | `30` |
| `STATESET_FOLLOW_REDIRECTS` | Follow HTTP redirects | `true` |
| `STATESET_VERIFY_SSL` | Verify SSL certificates | `true` |
| `STATESET_HTTPX_PROXIES` | Proxy configuration | None |

### Manual Configuration

```python
from stateset import Stateset

client = Stateset(
    api_key="your_api_key",
    base_url="https://api.stateset.com",
    timeout=60.0,
    verify_ssl=True,
    httpx_args={"proxies": {"https://": "https://proxy:8080"}}
)
```

## 🔒 Security

### API Key Management

Never hardcode your API keys. Use environment variables or a secure credential management system:

```python
import os
from stateset import Stateset

# ✅ Good: Use environment variables
client = Stateset()  # Reads STATESET_API_KEY from environment

# ✅ Good: Use a credential manager
api_key = get_secret("stateset_api_key")  # Your credential manager
client = Stateset(api_key=api_key)

# ❌ Bad: Hardcoded API key
client = Stateset(api_key="sk_live_...")  # Never do this!
```

### SSL Configuration

For development or testing with self-signed certificates:

```python
# Disable SSL verification (not recommended for production)
client = Stateset(verify_ssl=False)

# Use custom certificate bundle
client = Stateset(verify_ssl="/path/to/cert/bundle.pem")
```

## 🧪 Testing

The SDK includes comprehensive test coverage and utilities for testing your integration:

### Mock Testing

```python
import pytest
from unittest.mock import AsyncMock, patch
from stateset import Stateset

@pytest.mark.asyncio
async def test_order_creation():
    with patch('stateset.client.AuthenticatedClient') as mock_client:
        mock_client.return_value.post = AsyncMock(return_value={
            "id": "order_123",
            "status": "pending",
            "total_amount": 99.98
        })
        
        client = Stateset()
        order = await client.orders.create({
            "customer_id": "cust_123",
            "total_amount": 99.98
        })
        
        assert order.id == "order_123"
        assert order.status == "pending"
```

### Integration Testing

```python
import pytest
from stateset import Stateset
import os

@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_api_integration():
    # Only run if test API key is available
    if not os.getenv("STATESET_TEST_API_KEY"):
        pytest.skip("Test API key not available")
    
    client = Stateset(api_key=os.getenv("STATESET_TEST_API_KEY"))
    
    async with client:
        # Test creating and retrieving an order
        order = await client.orders.create({
            "customer_id": "test_customer",
            "total_amount": 10.00
        })
        
        retrieved_order = await client.orders.get(order.id)
        assert retrieved_order.id == order.id
```

## 📈 Performance Tips

### Connection Pooling

The SDK automatically manages connection pooling through httpx. For high-throughput applications:

```python
# The client maintains connection pools automatically
async with Stateset() as client:
    # Multiple requests will reuse connections
    for i in range(100):
        order = await client.orders.get(f"order_{i}")
```

### Batch Operations

```python
import asyncio
from stateset import Stateset

async def process_orders_batch(order_ids):
    client = Stateset()
    async with client:
        # Process multiple orders concurrently
        tasks = [client.orders.get(order_id) for order_id in order_ids]
        orders = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle results and exceptions
        for i, result in enumerate(orders):
            if isinstance(result, Exception):
                print(f"Failed to fetch order {order_ids[i]}: {result}")
            else:
                print(f"Order {result.id}: {result.status}")

# Process orders in batches of 10
order_ids = ["order_1", "order_2", "order_3", ...]
for i in range(0, len(order_ids), 10):
    batch = order_ids[i:i+10]
    await process_orders_batch(batch)
```

## 🐛 Debugging

### Enable Debug Logging

```python
import logging
from stateset import Stateset

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("stateset")
logger.setLevel(logging.DEBUG)

client = Stateset()
```

### Request/Response Logging

```python
import httpx
from stateset import Stateset

def log_request(request):
    print(f"Request: {request.method} {request.url}")

def log_response(response):
    print(f"Response: {response.status_code}")

client = Stateset(
    httpx_args={
        "event_hooks": {
            "request": [log_request],
            "response": [log_response]
        }
    }
)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/stateset/stateset-python.git
cd stateset-python

# Install development dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
ruff check .
black --check .
mypy stateset
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Stateset API Documentation](https://docs.stateset.com)
- [SDK Documentation](https://stateset-python.readthedocs.io)
- [PyPI Package](https://pypi.org/project/stateset/)
- [GitHub Repository](https://github.com/stateset/stateset-python)
- [Issue Tracker](https://github.com/stateset/stateset-python/issues)

## 📞 Support

- 📧 Email: [support@stateset.com](mailto:support@stateset.com)
- 💬 Discord: [Stateset Community](https://discord.gg/stateset)
- 📖 Documentation: [docs.stateset.com](https://docs.stateset.com)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/stateset/stateset-python/issues)

---

Made with ❤️ by the [Stateset](https://stateset.com) team.
