# Stateset Python SDK

[![PyPI version](https://badge.fury.io/py/stateset.svg)](https://badge.fury.io/py/stateset)
[![Python versions](https://img.shields.io/pypi/pyversions/stateset.svg)](https://pypi.org/project/stateset/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/stateset/stateset-python/branch/main/graph/badge.svg)](https://codecov.io/gh/stateset/stateset-python)
[![Tests](https://github.com/stateset/stateset-python/workflows/Test/badge.svg)](https://github.com/stateset/stateset-python/actions)

The **official Python client library** for the [Stateset API](https://docs.stateset.com). A world-class, enterprise-ready SDK that simplifies e-commerce operations with powerful tools for returns, warranties, orders, and inventory management.

## 🚀 Features

### Core Functionality
- ✅ **Full API Coverage** - Support for all Stateset API endpoints
- ✅ **Type Safety** - Complete type hints and validation with Pydantic
- ✅ **Async/Await Support** - Built for modern Python applications
- ✅ **Environment Configuration** - Easy setup via environment variables
- ✅ **Context Managers** - Proper resource management

### Advanced Features
- 🎯 **Smart Query Builder** - Fluent interface for complex queries with advanced filtering
- 🚀 **Bulk Operations** - Efficient batch processing with automatic fallbacks
- 📊 **Performance Monitoring** - Built-in metrics and request/response tracking
- 🧠 **Intelligent Caching** - Optional caching with TTL and invalidation strategies
- 🔄 **Enhanced Retry Logic** - Exponential backoff with configurable policies
- ⚡ **Rate Limiting** - Built-in rate limit handling with automatic waiting
- 🎯 **Advanced Pagination** - Seamless iteration through large datasets
- 🐛 **Rich Error Handling** - Comprehensive error types with debugging context
- 🔍 **Request Hooks** - Monitor and debug requests with custom hooks
- 🛠️ **Developer Tools** - Built-in profiling, logging, and diagnostic utilities

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
export STATESET_DEBUG="true"  # optional, for debugging
```

### Basic Usage

```python
from stateset import Stateset

# Initialize the client (reads from environment variables)
async with Stateset() as client:
    # Create a new order
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

### Advanced Query Building

```python
from datetime import datetime, timedelta
from stateset import FilterOperator

async with Stateset() as client:
    # Complex query with method chaining
    high_value_recent_orders = await client.orders.query() \
        .status_in(["completed", "processing"]) \
        .filter("total_amount", FilterOperator.GREATER_THAN_EQUAL, 1000.00) \
        .created_after((datetime.now() - timedelta(days=30)).isoformat()) \
        .sort_desc("total_amount") \
        .limit(100) \
        .all()
    
    # Use convenience methods
    recent_orders = await client.orders.recent(days=7).high_value(500).all()
    
    # Search with full-text search
    product_orders = await client.orders.query() \
        .search("iPhone", fields=["items.product_name"]) \
        .all()
```

### Bulk Operations

```python
# Bulk create orders with automatic error handling
order_data = [
    {"customer_id": "cust_1", "total_amount": 100.00},
    {"customer_id": "cust_2", "total_amount": 200.00},
    # ... more orders
]

result = await client.orders.bulk_create(order_data, batch_size=50)
print(f"Created {result.success_count} orders, {result.error_count} errors")

# Handle errors
for error in result.errors:
    print(f"Error: {error['error']} for item {error['index']}")
```

### Performance Monitoring

```python
# Enable performance tracking
client = Stateset(enable_metrics=True)

async with client:
    # Perform operations
    await client.orders.list()
    await client.customers.create({...})
    
    # Get performance metrics
    metrics = client.get_performance_metrics()
    print(f"Success rate: {metrics.success_rate:.2%}")
    print(f"Average response time: {metrics.average_response_time:.3f}s")
    print(f"Cache hit rate: {metrics.cache_hit_rate:.2%}")
```

## 📚 Core Resources

### Enhanced Orders Operations

```python
async with Stateset() as client:
    # Advanced order operations
    order = await client.orders.create({
        "customer_id": "cust_123",
        "total_amount": 299.99
    })
    
    # Mark as shipped with tracking
    await client.orders.mark_as_shipped(
        order.id,
        tracking_number="1Z999AA1234567890",
        carrier="UPS",
        shipped_at=datetime.now()
    )
    
    # Process refund
    refund = await client.orders.refund(
        order.id,
        amount=50.00,  # Partial refund
        reason="Customer satisfaction"
    )
    
    # Bulk status updates
    await client.orders.bulk_update_status(
        ["order_1", "order_2", "order_3"],
        "processing"
    )
    
    # Get daily statistics
    stats = await client.orders.get_daily_stats("2024-01-15")
```

### Smart Filtering and Search

```python
from stateset import FilterOperator

async with Stateset() as client:
    # Advanced filtering with operators
    expensive_orders = await client.orders.query() \
        .filter("total_amount", FilterOperator.GREATER_THAN, 1000) \
        .filter("status", FilterOperator.IN, ["completed", "processing"]) \
        .created_between("2024-01-01", "2024-12-31") \
        .all()
    
    # Geographic filtering
    us_customers = await client.customers.query() \
        .filter("address.country", FilterOperator.EQUALS, "US") \
        .filter("address.state", FilterOperator.IN, ["CA", "NY", "TX"]) \
        .all()
    
    # Text search across multiple fields
    product_returns = await client.returns.query() \
        .search("defective iPhone", fields=["reason", "notes"]) \
        .status("approved") \
        .all()
```

### Enhanced Error Handling

```python
from stateset import (
    StatesetValidationError,
    StatesetRateLimitError,
    StatesetAuthenticationError
)

try:
    order = await client.orders.create(invalid_data)
except StatesetValidationError as e:
    print(f"Validation failed: {e.message}")
    print("Debugging info:")
    print(e.get_debug_info())
    
    # Check specific field errors
    if e.has_field_error("customer_id"):
        print(f"Customer ID errors: {e.get_field_error('customer_id')}")
        
except StatesetRateLimitError as e:
    print(f"Rate limited. Retry after: {e.retry_after} seconds")
    
except StatesetAuthenticationError as e:
    print(f"Auth error: {e.message}")
    for suggestion in e.suggestions:
        print(f"  • {suggestion}")
```

## 🔍 Advanced Usage

### Request Monitoring and Hooks

```python
from stateset import RequestContext

def log_slow_requests(ctx: RequestContext, response):
    if ctx.duration.total_seconds() > 1.0:
        print(f"Slow request: {ctx.method} {ctx.url} ({ctx.duration.total_seconds():.2f}s)")

def log_errors(ctx: RequestContext, error: Exception):
    print(f"Request failed: {ctx.method} {ctx.url} - {error}")

client = Stateset()
client.add_response_hook(log_slow_requests)
client.add_error_hook(log_errors)
```

### Intelligent Caching

```python
from stateset.base_resource import RequestOptions

# Enable caching for specific resource
orders = Orders(client, enable_caching=True)

# Cache for 5 minutes
options = RequestOptions(cache_ttl=300)
order = await client.orders.get("order_123", options=options)

# Force refresh bypassing cache
fresh_order = await client.orders.query().force_refresh().get("order_123")
```

### Developer Tools and Debugging

```python
from stateset.dev_tools import profiled_client, logged_client, run_diagnostics

# Automatic profiling
async with profiled_client() as (client, profiler):
    await client.orders.list()
    await client.customers.create({...})
    
    profiler.print_summary()

# Enhanced logging
async with logged_client(log_level="DEBUG") as client:
    await client.orders.list()  # All requests logged

# Run diagnostics
async with Stateset() as client:
    results = await run_diagnostics(client)
    print(f"API Health: {results['connectivity']['status']}")
```

### Environment Configuration Utilities

```python
import stateset

# Check your environment setup
stateset.check_environment()

# Enable debug logging
stateset.enable_debug_logging()

# Get SDK information
info = stateset.get_sdk_info()
print(f"SDK Version: {info['version']}")
```

## ⚙️ Configuration

### Environment Variables

The SDK supports comprehensive configuration via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `STATESET_API_KEY` | Your Stateset API key | Required |
| `STATESET_BASE_URL` | API base URL | `https://api.stateset.com` |
| `STATESET_TIMEOUT` | Request timeout in seconds | `30` |
| `STATESET_DEBUG` | Enable debug logging | `false` |
| `STATESET_FOLLOW_REDIRECTS` | Follow HTTP redirects | `true` |
| `STATESET_VERIFY_SSL` | Verify SSL certificates | `true` |
| `STATESET_HTTPX_PROXIES` | Proxy configuration | None |

### Manual Configuration

```python
from stateset import Stateset, RetryConfig

# Custom retry configuration
retry_config = RetryConfig(
    max_retries=5,
    backoff_factor=1.0,
    retry_status_codes=(429, 500, 502, 503, 504)
)

client = Stateset(
    api_key="your_api_key",
    base_url="https://api.stateset.com",
    timeout=60.0,
    enable_metrics=True,
    debug=True,
    retry_config=retry_config
)
```

## 🧪 Testing and Development

### Mock Data Generation

```python
from stateset.dev_tools import MockDataGenerator

# Generate test data
order_data = MockDataGenerator.generate_order(
    customer_id="test_customer",
    total_amount=150.00
)

customer_data = MockDataGenerator.generate_customer(
    email="test@example.com"
)

# Use in tests
test_order = await client.orders.create(order_data)
```

### Testing Utilities

```python
import pytest
from stateset.dev_tools import create_test_suite

@pytest.mark.asyncio
async def test_api_integration():
    async with Stateset() as client:
        test_suite = create_test_suite(client)
        
        # Test connectivity
        connectivity_result = await test_suite["connectivity"]()
        assert connectivity_result["status"] == "healthy"
        
        # Test authentication
        auth_result = await test_suite["authentication"]()
        assert auth_result["status"] == "authenticated"
```

## 📈 Performance Optimization

### Connection Pooling and Caching

```python
# The SDK automatically manages connection pooling
# Enable caching for frequently accessed data
client = Stateset()

# Cache frequently accessed orders
orders_with_cache = Orders(client, enable_caching=True)
```

### Batch Processing Best Practices

```python
# Process large datasets efficiently
async def process_all_orders():
    async with Stateset() as client:
        # Stream through all orders without loading everything into memory
        async for order in client.orders.query().status("pending"):
            await process_order(order)
        
        # Or process in batches
        page = 1
        while True:
            orders = await client.orders.query().page(page).limit(100).paginate()
            if not orders.data:
                break
                
            # Process batch
            await process_order_batch(orders.data)
            page += 1
```

## 🔒 Security Best Practices

### API Key Management

```python
import os
from stateset import Stateset

# ✅ Good: Use environment variables
client = Stateset()  # Reads STATESET_API_KEY from environment

# ✅ Good: Use a credential manager
def get_api_key():
    # Your secure credential retrieval logic
    return retrieve_from_vault("stateset_api_key")

client = Stateset(api_key=get_api_key())

# ❌ Bad: Hardcoded API key
# client = Stateset(api_key="sk_live_...")  # Never do this!
```

### Secure Request Logging

```python
from stateset.dev_tools import RequestLogger

# Automatically mask sensitive information
logger = RequestLogger(mask_sensitive=True)
client.add_request_hook(logger.log_request)
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

# Run with coverage
pytest --cov=stateset --cov-report=html

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

## 🎯 What's New in v1.1.0

### 🚀 Major Enhancements

- **Advanced Query Builder** - Fluent interface with 15+ filter operators
- **Bulk Operations** - Efficient batch processing with automatic fallbacks
- **Performance Monitoring** - Built-in metrics tracking success rates and response times
- **Intelligent Caching** - Optional caching with TTL and smart invalidation
- **Enhanced Error Handling** - Rich error context with debugging information and suggestions
- **Developer Tools** - Profiling, logging, and diagnostic utilities
- **Request Hooks** - Monitor and customize request/response behavior

### 🎯 Improved Developer Experience

- **Better Type Safety** - Comprehensive type hints and validation
- **Rich Error Messages** - Actionable error messages with suggestions
- **Environment Utilities** - Easy environment checking and configuration
- **Mock Data Generators** - Built-in test data generation
- **Comprehensive Documentation** - Examples for every feature

### ⚡ Performance Improvements

- **Smart Rate Limiting** - Automatic rate limit detection and waiting
- **Connection Pooling** - Optimized HTTP connection management
- **Streaming Support** - Memory-efficient iteration over large datasets
- **Concurrent Operations** - Bulk operations with proper error isolation

---

Made with ❤️ by the [Stateset](https://stateset.com) team.
