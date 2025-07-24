"""
Developer tools and utilities for the Stateset Python SDK.

This module provides helpful utilities for debugging, testing, and development
with the Stateset SDK, including request logging, performance profiling,
and API exploration tools.
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union, AsyncGenerator
from contextlib import asynccontextmanager
import logging

from .client import Stateset, PerformanceMetrics, RequestContext
from .errors import StatesetError


class SDKProfiler:
    """Profiler for SDK operations to help identify performance bottlenecks."""
    
    def __init__(self):
        self.operations: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start(self):
        """Start profiling session."""
        self.operations.clear()
        self.start_time = datetime.now()
        print("🔍 SDK Profiler started")
    
    def stop(self):
        """Stop profiling session."""
        self.end_time = datetime.now()
        print("🔍 SDK Profiler stopped")
    
    def record_operation(self, operation: str, duration: float, success: bool, **metadata):
        """Record an operation for profiling."""
        self.operations.append({
            "operation": operation,
            "duration": duration,
            "success": success,
            "timestamp": datetime.now(),
            "metadata": metadata
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get profiling summary."""
        if not self.operations:
            return {"message": "No operations recorded"}
        
        total_time = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        successful_ops = [op for op in self.operations if op["success"]]
        failed_ops = [op for op in self.operations if not op["success"]]
        
        return {
            "session_duration": total_time,
            "total_operations": len(self.operations),
            "successful_operations": len(successful_ops),
            "failed_operations": len(failed_ops),
            "success_rate": len(successful_ops) / len(self.operations) if self.operations else 0,
            "average_operation_time": sum(op["duration"] for op in successful_ops) / len(successful_ops) if successful_ops else 0,
            "slowest_operation": max(self.operations, key=lambda x: x["duration"]) if self.operations else None,
            "fastest_operation": min(self.operations, key=lambda x: x["duration"]) if self.operations else None,
        }
    
    def print_summary(self):
        """Print a formatted profiling summary."""
        summary = self.get_summary()
        
        if "message" in summary:
            print(summary["message"])
            return
        
        print("\n" + "="*60)
        print("🔍 SDK Profiler Summary")
        print("="*60)
        print(f"Session Duration: {summary['session_duration']:.2f}s")
        print(f"Total Operations: {summary['total_operations']}")
        print(f"Successful: {summary['successful_operations']}")
        print(f"Failed: {summary['failed_operations']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Average Operation Time: {summary['average_operation_time']:.3f}s")
        
        if summary['slowest_operation']:
            slowest = summary['slowest_operation']
            print(f"\nSlowest Operation:")
            print(f"  {slowest['operation']}: {slowest['duration']:.3f}s")
        
        if summary['fastest_operation']:
            fastest = summary['fastest_operation']
            print(f"\nFastest Operation:")
            print(f"  {fastest['operation']}: {fastest['duration']:.3f}s")
        
        print("="*60)


class RequestLogger:
    """Enhanced request logger with filtering and formatting options."""
    
    def __init__(self, 
                 log_requests: bool = True,
                 log_responses: bool = True,
                 log_errors: bool = True,
                 mask_sensitive: bool = True,
                 max_body_length: int = 1000):
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_errors = log_errors
        self.mask_sensitive = mask_sensitive
        self.max_body_length = max_body_length
        self.logger = logging.getLogger("stateset.request_logger")
        
        # Set up colored logging if available
        try:
            import colorama
            colorama.init()
            self.colors = {
                'request': '\033[36m',    # Cyan
                'response': '\033[32m',   # Green
                'error': '\033[31m',      # Red
                'reset': '\033[0m'        # Reset
            }
        except ImportError:
            self.colors = {k: '' for k in ['request', 'response', 'error', 'reset']}
    
    def log_request(self, ctx: RequestContext):
        """Log outgoing request."""
        if not self.log_requests:
            return
        
        message = f"{self.colors['request']}→ {ctx.method} {ctx.url}{self.colors['reset']}"
        
        if ctx.headers:
            filtered_headers = self._filter_headers(ctx.headers)
            for key, value in filtered_headers.items():
                message += f"\n  {key}: {value}"
        
        self.logger.info(message)
    
    def log_response(self, ctx: RequestContext, response):
        """Log incoming response."""
        if not self.log_responses:
            return
        
        duration_ms = ctx.duration.total_seconds() * 1000
        status_code = getattr(response, 'status_code', 'Unknown')
        
        message = (f"{self.colors['response']}← {status_code} {ctx.method} {ctx.url} "
                  f"({duration_ms:.1f}ms){self.colors['reset']}")
        
        self.logger.info(message)
    
    def log_error(self, ctx: RequestContext, error: Exception):
        """Log request error."""
        if not self.log_errors:
            return
        
        duration_ms = ctx.duration.total_seconds() * 1000
        message = (f"{self.colors['error']}✗ {ctx.method} {ctx.url} failed "
                  f"after {duration_ms:.1f}ms: {error}{self.colors['reset']}")
        
        self.logger.error(message)
    
    def _filter_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Filter and mask sensitive headers."""
        if not self.mask_sensitive:
            return headers
        
        filtered = {}
        sensitive_keys = ['authorization', 'api-key', 'token', 'secret']
        
        for key, value in headers.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                filtered[key] = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                filtered[key] = value
        
        return filtered


class APIExplorer:
    """Interactive API explorer for discovering and testing endpoints."""
    
    def __init__(self, client: Stateset):
        self.client = client
    
    async def ping(self) -> Dict[str, Any]:
        """Ping the API to check connectivity."""
        try:
            start_time = time.time()
            # Try a simple API call
            await self.client.get("/health")
            duration = time.time() - start_time
            return {
                "status": "healthy",
                "response_time": f"{duration*1000:.1f}ms",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def explore_endpoints(self) -> Dict[str, List[str]]:
        """Discover available endpoints (if supported by the API)."""
        try:
            response = await self.client._client.get("/")
            # Parse API documentation or endpoint list
            return response
        except Exception:
            # Return known endpoints
            return {
                "resources": [
                    "/orders", "/returns", "/warranties", "/customers",
                    "/inventory", "/products", "/shipments"
                ],
                "note": "This is a predefined list. API discovery not available."
            }
    
    async def test_endpoint(self, path: str, method: str = "GET", 
                           data: Optional[Dict] = None) -> Dict[str, Any]:
        """Test a specific endpoint."""
        try:
            start_time = time.time()
            
            if method.upper() == "GET":
                response = await self.client._client.get(path)
            elif method.upper() == "POST":
                response = await self.client._client.post(path, json=data or {})
            elif method.upper() == "PUT":
                response = await self.client._client.put(path, json=data or {})
            elif method.upper() == "DELETE":
                await self.client._client.delete(path)
                response = {"message": "Deleted successfully"}
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            duration = time.time() - start_time
            
            return {
                "status": "success",
                "method": method.upper(),
                "path": path,
                "response_time": f"{duration*1000:.1f}ms",
                "response": response
            }
        except Exception as e:
            return {
                "status": "error",
                "method": method.upper(), 
                "path": path,
                "error": str(e)
            }


class MockDataGenerator:
    """Generate mock data for testing purposes."""
    
    @staticmethod
    def generate_order(customer_id: str = None, **overrides) -> Dict[str, Any]:
        """Generate mock order data."""
        import random
        
        base_order = {
            "customer_id": customer_id or f"cust_{random.randint(1000, 9999)}",
            "status": random.choice(["pending", "processing", "completed"]),
            "total_amount": round(random.uniform(10.0, 1000.0), 2),
            "items": [
                {
                    "product_id": f"prod_{random.randint(100, 999)}",
                    "quantity": random.randint(1, 5),
                    "price": round(random.uniform(5.0, 200.0), 2)
                }
            ],
            "shipping_address": {
                "street": f"{random.randint(100, 9999)} Test St",
                "city": "Test City",
                "state": "TS",
                "zip_code": f"{random.randint(10000, 99999)}",
                "country": "US"
            }
        }
        
        base_order.update(overrides)
        return base_order
    
    @staticmethod
    def generate_customer(**overrides) -> Dict[str, Any]:
        """Generate mock customer data."""
        import random
        
        first_names = ["John", "Jane", "Alice", "Bob", "Carol", "David"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        base_customer = {
            "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
            "name": f"{first_name} {last_name}",
            "phone": f"+1{random.randint(2000000000, 9999999999)}",
            "address": {
                "street": f"{random.randint(100, 9999)} Main St",
                "city": "Testville",
                "state": "TS", 
                "zip_code": f"{random.randint(10000, 99999)}",
                "country": "US"
            }
        }
        
        base_customer.update(overrides)
        return base_customer
    
    @staticmethod
    def generate_return(order_id: str = None, **overrides) -> Dict[str, Any]:
        """Generate mock return data."""
        import random
        
        base_return = {
            "order_id": order_id or f"order_{random.randint(1000, 9999)}",
            "reason": random.choice(["defective", "wrong_item", "not_needed", "damaged"]),
            "status": random.choice(["requested", "approved", "received"]),
            "items": [
                {
                    "product_id": f"prod_{random.randint(100, 999)}",
                    "quantity": random.randint(1, 3),
                    "reason": "Item damaged during shipping"
                }
            ]
        }
        
        base_return.update(overrides)
        return base_return


@asynccontextmanager
async def profiled_client(**client_kwargs) -> AsyncGenerator[tuple[Stateset, SDKProfiler], None]:
    """Context manager that provides a client with automatic profiling."""
    profiler = SDKProfiler()
    client = Stateset(**client_kwargs)
    
    # Add profiling hooks
    def profile_request(ctx: RequestContext):
        profiler.record_operation(
            f"{ctx.method} {ctx.url}",
            0,  # Will be updated in response hook
            True,
            method=ctx.method,
            url=ctx.url
        )
    
    def profile_response(ctx: RequestContext, response):
        duration = ctx.duration.total_seconds()
        # Update the last recorded operation
        if profiler.operations:
            profiler.operations[-1]["duration"] = duration
    
    def profile_error(ctx: RequestContext, error: Exception):
        duration = ctx.duration.total_seconds()
        profiler.record_operation(
            f"{ctx.method} {ctx.url}",
            duration,
            False,
            method=ctx.method,
            url=ctx.url,
            error=str(error)
        )
    
    client.add_request_hook(profile_request)
    client.add_response_hook(profile_response) 
    client.add_error_hook(profile_error)
    
    profiler.start()
    
    try:
        async with client:
            yield client, profiler
    finally:
        profiler.stop()


@asynccontextmanager
async def logged_client(log_level: str = "INFO", **client_kwargs) -> AsyncGenerator[Stateset, None]:
    """Context manager that provides a client with request logging."""
    # Set up logging
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    
    client = Stateset(debug=True, **client_kwargs)
    logger = RequestLogger()
    
    client.add_request_hook(logger.log_request)
    client.add_response_hook(logger.log_response)
    client.add_error_hook(logger.log_error)
    
    try:
        async with client:
            yield client
    finally:
        pass


def create_test_suite(client: Stateset) -> Dict[str, Any]:
    """Create a basic test suite for the client."""
    
    async def test_connectivity():
        """Test basic API connectivity."""
        explorer = APIExplorer(client)
        return await explorer.ping()
    
    async def test_authentication():
        """Test API authentication."""
        try:
            # Try to access a protected endpoint
            await client.orders.count()
            return {"status": "authenticated", "message": "API key is valid"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    async def test_basic_operations():
        """Test basic CRUD operations."""
        results = {}
        
        # Test listing
        try:
            orders = await client.orders.list()
            results["list"] = {"status": "success", "count": len(orders.data)}
        except Exception as e:
            results["list"] = {"status": "failed", "error": str(e)}
        
        # Test counting
        try:
            count = await client.orders.count()
            results["count"] = {"status": "success", "total": count}
        except Exception as e:
            results["count"] = {"status": "failed", "error": str(e)}
        
        return results
    
    return {
        "connectivity": test_connectivity,
        "authentication": test_authentication,
        "basic_operations": test_basic_operations
    }


async def run_diagnostics(client: Stateset) -> Dict[str, Any]:
    """Run comprehensive diagnostics on the client."""
    print("🔧 Running Stateset SDK Diagnostics...")
    
    results = {}
    test_suite = create_test_suite(client)
    
    for test_name, test_func in test_suite.items():
        print(f"  Running {test_name} test...")
        try:
            result = await test_func()
            results[test_name] = result
            status = result.get("status", "unknown")
            if status == "success" or status == "authenticated" or status == "healthy":
                print(f"    ✓ {test_name}: {status}")
            else:
                print(f"    ✗ {test_name}: {status}")
        except Exception as e:
            results[test_name] = {"status": "error", "error": str(e)}
            print(f"    ✗ {test_name}: error")
    
    # Get performance metrics if available
    metrics = client.get_performance_metrics()
    if metrics:
        results["performance"] = {
            "total_requests": metrics.total_requests,
            "success_rate": metrics.success_rate,
            "average_response_time": metrics.average_response_time,
            "cache_hit_rate": metrics.cache_hit_rate if hasattr(metrics, 'cache_hit_rate') else 0
        }
    
    print("🔧 Diagnostics complete")
    return results


# Convenience functions for quick testing
async def quick_test():
    """Quick test of the SDK with sample operations."""
    print("🚀 Quick SDK Test")
    print("-" * 40)
    
    async with logged_client() as client:
        # Test basic connectivity
        explorer = APIExplorer(client)
        ping_result = await explorer.ping()
        print(f"API Status: {ping_result['status']}")
        
        # Test listing orders
        try:
            orders = await client.orders.list()
            print(f"Orders: {len(orders.data)} found")
        except Exception as e:
            print(f"Orders: Error - {e}")
        
        # Show performance metrics
        metrics = client.get_performance_metrics()
        if metrics:
            print(f"Performance: {metrics.success_rate:.1%} success rate")


if __name__ == "__main__":
    # Run quick test if this module is executed directly
    asyncio.run(quick_test())