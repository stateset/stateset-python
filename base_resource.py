"""
Enhanced base resource class with improved pagination, filtering, and modern Python features.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, AsyncIterator, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from .client import AuthenticatedClient
from .stateset_types import PaginatedList, PaginationParams
from .errors import StatesetError, StatesetInvalidRequestError

logger = logging.getLogger(__name__)

T = TypeVar("T")


class FilterOperator(str, Enum):
    """Filter operators for advanced querying."""
    EQUALS = "eq"
    NOT_EQUALS = "ne"
    GREATER_THAN = "gt"
    GREATER_THAN_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_EQUAL = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


@dataclass
class FilterExpression:
    """Represents a filter expression with field, operator, and value."""
    field: str
    operator: FilterOperator
    value: Any
    
    def to_query_param(self) -> tuple[str, Any]:
        """Convert to query parameter format."""
        if self.operator == FilterOperator.EQUALS:
            return (self.field, self.value)
        else:
            return (f"{self.field}__{self.operator.value}", self.value)


@dataclass
class FilterParams:
    """Enhanced parameters for filtering API requests."""
    
    # Common filter parameters
    created_after: Optional[str] = None
    created_before: Optional[str] = None
    updated_after: Optional[str] = None
    updated_before: Optional[str] = None
    status: Optional[str] = None
    
    # Advanced filtering expressions
    expressions: List[FilterExpression] = field(default_factory=list)
    
    # Custom filters (can be extended by subclasses)
    custom_filters: Dict[str, Any] = field(default_factory=dict)
    
    # Search functionality
    search_query: Optional[str] = None
    search_fields: List[str] = field(default_factory=list)
    
    def add_filter(self, field: str, operator: FilterOperator, value: Any) -> "FilterParams":
        """Add a filter expression."""
        self.expressions.append(FilterExpression(field, operator, value))
        return self
    
    def search(self, query: str, fields: List[str] = None) -> "FilterParams":
        """Add search query."""
        self.search_query = query
        if fields:
            self.search_fields = fields
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert filter parameters to dictionary for API requests."""
        params = {}
        
        if self.created_after:
            params["created[gte]"] = self.created_after
        if self.created_before:
            params["created[lte]"] = self.created_before
        if self.updated_after:
            params["updated[gte]"] = self.updated_after
        if self.updated_before:
            params["updated[lte]"] = self.updated_before
        if self.status:
            params["status"] = self.status
            
        # Add filter expressions
        for expr in self.expressions:
            key, value = expr.to_query_param()
            params[key] = value
            
        # Add search parameters
        if self.search_query:
            params["q"] = self.search_query
            if self.search_fields:
                params["search_fields"] = ",".join(self.search_fields)
        
        # Add custom filters
        params.update(self.custom_filters)
        
        # Remove None values
        return {k: v for k, v in params.items() if v is not None}


@dataclass
class RequestOptions:
    """Enhanced options for customizing API requests."""
    
    timeout: Optional[float] = None
    headers: Optional[Dict[str, str]] = None
    idempotency_key: Optional[str] = None
    
    # Performance options
    include_fields: Optional[List[str]] = None
    exclude_fields: Optional[List[str]] = None
    
    # Caching options
    cache_ttl: Optional[int] = None
    force_refresh: bool = False
    
    def to_kwargs(self) -> Dict[str, Any]:
        """Convert options to httpx request kwargs."""
        kwargs = {}
        
        if self.timeout:
            kwargs["timeout"] = self.timeout
            
        headers = dict(self.headers or {})
        if self.idempotency_key:
            headers["Idempotency-Key"] = self.idempotency_key
            
        # Field selection headers
        if self.include_fields:
            headers["X-Include-Fields"] = ",".join(self.include_fields)
        if self.exclude_fields:
            headers["X-Exclude-Fields"] = ",".join(self.exclude_fields)
            
        # Cache control headers
        if self.force_refresh:
            headers["Cache-Control"] = "no-cache"
        elif self.cache_ttl:
            headers["Cache-Control"] = f"max-age={self.cache_ttl}"
            
        if headers:
            kwargs["headers"] = headers
            
        return kwargs


@dataclass
class BulkOperationResult:
    """Result of a bulk operation."""
    success_count: int
    error_count: int
    errors: List[Dict[str, Any]] = field(default_factory=list)
    successful_ids: List[str] = field(default_factory=list)
    
    @property
    def total_count(self) -> int:
        return self.success_count + self.error_count
    
    @property
    def success_rate(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.success_count / self.total_count


class BaseResource(Generic[T]):
    """Enhanced base class for all Stateset API resources."""

    def __init__(
        self, 
        client: AuthenticatedClient, 
        object_class: Type[T], 
        base_path: str,
        default_limit: int = 50,
        max_limit: int = 1000,
        enable_caching: bool = False
    ) -> None:
        self.client = client
        self.object_class = object_class
        self.base_path = base_path.rstrip("/")
        self.default_limit = default_limit
        self.max_limit = max_limit
        self.enable_caching = enable_caching
        self._cache: Dict[str, Any] = {}
        self._cache_timestamps: Dict[str, datetime] = {}

    def _validate_pagination_params(self, params: PaginationParams) -> None:
        """Validate pagination parameters."""
        if params.per_page and params.per_page > self.max_limit:
            raise StatesetInvalidRequestError(
                f"per_page cannot exceed {self.max_limit}"
            )
        
        if params.page and params.page < 1:
            raise StatesetInvalidRequestError("page must be >= 1")

    def _build_query_params(
        self,
        pagination: Optional[PaginationParams] = None,
        filters: Optional[FilterParams] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Build query parameters for API requests."""
        params = {}
        
        # Add pagination parameters
        if pagination:
            self._validate_pagination_params(pagination)
            params["page"] = pagination.page or 1
            params["per_page"] = pagination.per_page or self.default_limit
            
            if pagination.sort_by:
                params["sort_by"] = pagination.sort_by
            if pagination.sort_order:
                params["sort_order"] = pagination.sort_order
        else:
            params["page"] = 1
            params["per_page"] = self.default_limit
        
        # Add filter parameters
        if filters:
            params.update(filters.to_dict())
        
        # Add any additional parameters
        params.update(kwargs)
        
        return params

    def _get_cache_key(self, operation: str, **params: Any) -> str:
        """Generate cache key for an operation."""
        key_parts = [operation]
        for k, v in sorted(params.items()):
            key_parts.append(f"{k}={v}")
        return "|".join(key_parts)

    def _is_cache_valid(self, cache_key: str, ttl: int = 300) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self._cache_timestamps:
            return False
        
        age = datetime.now() - self._cache_timestamps[cache_key]
        return age.total_seconds() < ttl

    def _set_cache(self, cache_key: str, data: Any) -> None:
        """Store data in cache."""
        if self.enable_caching:
            self._cache[cache_key] = data
            self._cache_timestamps[cache_key] = datetime.now()

    def _get_cache(self, cache_key: str) -> Optional[Any]:
        """Retrieve data from cache."""
        if self.enable_caching and cache_key in self._cache:
            return self._cache[cache_key]
        return None

    async def list(
        self, 
        pagination: Optional[PaginationParams] = None,
        filters: Optional[FilterParams] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any
    ) -> PaginatedList[T]:
        """
        List all resources with enhanced pagination and filtering support.
        
        Args:
            pagination: Pagination parameters
            filters: Filter parameters  
            options: Request options (timeout, headers, etc.)
            **kwargs: Additional query parameters
            
        Returns:
            Paginated list of resources
        """
        query_params = self._build_query_params(pagination, filters, **kwargs)
        request_kwargs = options.to_kwargs() if options else {}
        
        # Check cache if enabled
        cache_key = self._get_cache_key("list", **query_params)
        if not (options and options.force_refresh):
            cached_data = self._get_cache(cache_key)
            if cached_data and self._is_cache_valid(cache_key):
                return cached_data

        try:
            response = await self.client.get(
                path=self.base_path, 
                params=query_params,
                **request_kwargs
            )

            # Handle both array and object responses
            if isinstance(response, list):
                # Simple array response
                data = [self.object_class(**item) for item in response]
                result = PaginatedList(
                    data=data,
                    total=len(data),
                    page=1,
                    per_page=len(data),
                    total_pages=1,
                    has_next=False,
                    has_prev=False,
                )
            else:
                # Object response with pagination metadata
                data = [self.object_class(**item) for item in response.get("data", [])]
                result = PaginatedList(
                    data=data,
                    total=response.get("total", len(data)),
                    page=response.get("page", 1),
                    per_page=response.get("per_page", len(data)),
                    total_pages=response.get("total_pages", 1),
                    has_next=response.get("has_next", False),
                    has_prev=response.get("has_prev", False),
                )
            
            # Cache result
            self._set_cache(cache_key, result)
            return result

        except Exception as e:
            logger.error(f"Failed to list {self.object_class.__name__}: {e}")
            raise

    async def get(
        self, 
        id: str,
        options: Optional[RequestOptions] = None,
        **kwargs: Any
    ) -> T:
        """
        Retrieve a single resource by ID.
        
        Args:
            id: Resource ID
            options: Request options
            **kwargs: Additional query parameters
            
        Returns:
            The requested resource
        """
        if not id:
            raise StatesetInvalidRequestError("Resource ID is required")
            
        # Check cache if enabled
        cache_key = self._get_cache_key("get", id=id, **kwargs)
        if not (options and options.force_refresh):
            cached_data = self._get_cache(cache_key)
            if cached_data and self._is_cache_valid(cache_key):
                return cached_data
            
        request_kwargs = options.to_kwargs() if options else {}
        if kwargs:
            request_kwargs["params"] = kwargs

        try:
            response = await self.client.get(
                f"{self.base_path}/{id}",
                **request_kwargs
            )
            result = self.object_class(**response)
            
            # Cache result
            self._set_cache(cache_key, result)
            return result

        except Exception as e:
            logger.error(f"Failed to get {self.object_class.__name__} {id}: {e}")
            raise

    async def create(
        self, 
        data: Dict[str, Any],
        options: Optional[RequestOptions] = None
    ) -> T:
        """
        Create a new resource.
        
        Args:
            data: Resource data
            options: Request options
            
        Returns:
            The created resource
        """
        if not data:
            raise StatesetInvalidRequestError("Resource data is required")
            
        request_kwargs = options.to_kwargs() if options else {}

        try:
            response = await self.client.post(
                self.base_path, 
                json=data,
                **request_kwargs
            )
            result = self.object_class(**response)
            
            # Invalidate relevant caches
            self._invalidate_list_caches()
            
            return result

        except Exception as e:
            logger.error(f"Failed to create {self.object_class.__name__}: {e}")
            raise

    async def update(
        self, 
        id: str, 
        data: Dict[str, Any],
        options: Optional[RequestOptions] = None
    ) -> T:
        """
        Update an existing resource.
        
        Args:
            id: Resource ID
            data: Updated resource data
            options: Request options
            
        Returns:
            The updated resource
        """
        if not id:
            raise StatesetInvalidRequestError("Resource ID is required")
        if not data:
            raise StatesetInvalidRequestError("Update data is required")
            
        request_kwargs = options.to_kwargs() if options else {}

        try:
            response = await self.client.put(
                f"{self.base_path}/{id}", 
                json=data,
                **request_kwargs
            )
            result = self.object_class(**response)
            
            # Invalidate caches for this resource
            self._invalidate_resource_caches(id)
            
            return result

        except Exception as e:
            logger.error(f"Failed to update {self.object_class.__name__} {id}: {e}")
            raise

    async def delete(
        self, 
        id: str,
        options: Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a resource.
        
        Args:
            id: Resource ID
            options: Request options
        """
        if not id:
            raise StatesetInvalidRequestError("Resource ID is required")
            
        request_kwargs = options.to_kwargs() if options else {}

        try:
            await self.client.delete(
                f"{self.base_path}/{id}",
                **request_kwargs
            )
            
            # Invalidate caches for this resource
            self._invalidate_resource_caches(id)

        except Exception as e:
            logger.error(f"Failed to delete {self.object_class.__name__} {id}: {e}")
            raise

    async def bulk_create(
        self,
        items: List[Dict[str, Any]],
        options: Optional[RequestOptions] = None,
        batch_size: int = 100
    ) -> BulkOperationResult:
        """
        Create multiple resources in bulk.
        
        Args:
            items: List of resource data dictionaries
            options: Request options
            batch_size: Number of items per batch
            
        Returns:
            BulkOperationResult with success/error counts
        """
        if not items:
            raise StatesetInvalidRequestError("Items list cannot be empty")
        
        total_success = 0
        total_errors = 0
        all_errors = []
        successful_ids = []
        
        # Process in batches
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            try:
                request_kwargs = options.to_kwargs() if options else {}
                response = await self.client.post(
                    f"{self.base_path}/bulk",
                    json={"items": batch},
                    **request_kwargs
                )
                
                # Handle bulk response
                if "results" in response:
                    for result in response["results"]:
                        if result.get("success"):
                            total_success += 1
                            if "id" in result:
                                successful_ids.append(result["id"])
                        else:
                            total_errors += 1
                            all_errors.append(result.get("error", {}))
                else:
                    # Fallback: create items individually
                    batch_results = await self._bulk_create_fallback(batch, options)
                    total_success += batch_results.success_count
                    total_errors += batch_results.error_count
                    all_errors.extend(batch_results.errors)
                    successful_ids.extend(batch_results.successful_ids)
                    
            except Exception as e:
                logger.warning(f"Bulk create batch failed, falling back to individual creates: {e}")
                batch_results = await self._bulk_create_fallback(batch, options)
                total_success += batch_results.success_count
                total_errors += batch_results.error_count
                all_errors.extend(batch_results.errors)
                successful_ids.extend(batch_results.successful_ids)
        
        # Invalidate relevant caches
        self._invalidate_list_caches()
        
        return BulkOperationResult(
            success_count=total_success,
            error_count=total_errors,
            errors=all_errors,
            successful_ids=successful_ids
        )

    async def _bulk_create_fallback(
        self,
        items: List[Dict[str, Any]],
        options: Optional[RequestOptions] = None
    ) -> BulkOperationResult:
        """Fallback method for bulk create using individual API calls."""
        success_count = 0
        error_count = 0
        errors = []
        successful_ids = []
        
        tasks = []
        for item in items:
            tasks.append(self._safe_create(item, options))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_count += 1
                errors.append({
                    "index": i,
                    "error": str(result),
                    "item": items[i]
                })
            else:
                success_count += 1
                if hasattr(result, 'id'):
                    successful_ids.append(result.id)
        
        return BulkOperationResult(
            success_count=success_count,
            error_count=error_count,
            errors=errors,
            successful_ids=successful_ids
        )

    async def _safe_create(
        self, 
        data: Dict[str, Any], 
        options: Optional[RequestOptions] = None
    ) -> Optional[T]:
        """Safely create a resource, returning None on error."""
        try:
            return await self.create(data, options)
        except Exception as e:
            logger.debug(f"Failed to create individual item: {e}")
            raise

    def _invalidate_list_caches(self) -> None:
        """Invalidate all list-related caches."""
        if not self.enable_caching:
            return
            
        keys_to_remove = [k for k in self._cache.keys() if k.startswith("list|")]
        for key in keys_to_remove:
            self._cache.pop(key, None)
            self._cache_timestamps.pop(key, None)

    def _invalidate_resource_caches(self, resource_id: str) -> None:
        """Invalidate caches for a specific resource."""
        if not self.enable_caching:
            return
            
        # Invalidate specific resource cache
        get_key = f"get|id={resource_id}"
        self._cache.pop(get_key, None)
        self._cache_timestamps.pop(get_key, None)
        
        # Invalidate list caches
        self._invalidate_list_caches()

    async def iter_all(
        self,
        pagination: Optional[PaginationParams] = None,
        filters: Optional[FilterParams] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any,
    ) -> AsyncIterator[T]:
        """
        Iterate through all items across paginated results.
        
        Args:
            pagination: Initial pagination parameters
            filters: Filter parameters
            options: Request options
            **kwargs: Additional query parameters
            
        Yields:
            Individual resources
        """
        current_pagination = pagination or PaginationParams()
        
        while True:
            page = await self.list(
                pagination=current_pagination,
                filters=filters,
                options=options,
                **kwargs
            )
            
            for item in page.data:
                yield item
                
            if not page.has_next:
                break
                
            # Move to next page
            current_pagination.page = (current_pagination.page or 1) + 1

    async def list_all(
        self,
        pagination: Optional[PaginationParams] = None,
        filters: Optional[FilterParams] = None,
        options: Optional[RequestOptions] = None,
        max_items: Optional[int] = None,
        **kwargs: Any,
    ) -> List[T]:
        """
        Return a list containing all items from all pages.
        
        Args:
            pagination: Initial pagination parameters
            filters: Filter parameters
            options: Request options
            max_items: Maximum number of items to retrieve
            **kwargs: Additional query parameters
            
        Returns:
            List of all resources
        """
        items: List[T] = []
        count = 0
        
        async for item in self.iter_all(pagination, filters, options, **kwargs):
            items.append(item)
            count += 1
            
            if max_items and count >= max_items:
                break
                
        return items

    async def count(
        self,
        filters: Optional[FilterParams] = None,
        options: Optional[RequestOptions] = None,
        **kwargs: Any
    ) -> int:
        """
        Get the total count of resources matching the filters.
        
        Args:
            filters: Filter parameters
            options: Request options
            **kwargs: Additional query parameters
            
        Returns:
            Total count of matching resources
        """
        # Check if API supports direct count endpoint
        try:
            query_params = self._build_query_params(filters=filters, **kwargs)
            request_kwargs = options.to_kwargs() if options else {}
            
            response = await self.client.get(
                f"{self.base_path}/count",
                params=query_params,
                **request_kwargs
            )
            return response.get("count", 0)
        except Exception:
            # Fallback: Get first page to access total count
            pagination = PaginationParams(page=1, per_page=1)
            page = await self.list(pagination, filters, options, **kwargs)
            return page.total

    async def exists(
        self,
        id: str,
        options: Optional[RequestOptions] = None
    ) -> bool:
        """
        Check if a resource exists.
        
        Args:
            id: Resource ID
            options: Request options
            
        Returns:
            True if resource exists, False otherwise
        """
        try:
            await self.get(id, options)
            return True
        except StatesetError:
            return False

    def with_filters(self, **filters: Any) -> "ResourceQuery[T]":
        """
        Create a query builder for this resource.
        
        Args:
            **filters: Initial filter parameters
            
        Returns:
            ResourceQuery instance for method chaining
        """
        return ResourceQuery(self, FilterParams(custom_filters=filters))

    def query(self) -> "ResourceQuery[T]":
        """
        Create a fresh query builder for this resource.
        
        Returns:
            ResourceQuery instance for method chaining
        """
        return ResourceQuery(self, FilterParams())


class ResourceQuery(Generic[T]):
    """Enhanced query builder for resource operations with method chaining."""
    
    def __init__(self, resource: BaseResource[T], filters: FilterParams):
        self.resource = resource
        self.filters = filters
        self.pagination = PaginationParams()
        self.options = RequestOptions()
    
    def where(self, **filters: Any) -> "ResourceQuery[T]":
        """Add filter conditions using equals operator."""
        self.filters.custom_filters.update(filters)
        return self
    
    def filter(self, field: str, operator: FilterOperator, value: Any) -> "ResourceQuery[T]":
        """Add advanced filter with specific operator."""
        self.filters.add_filter(field, operator, value)
        return self
    
    def search(self, query: str, fields: List[str] = None) -> "ResourceQuery[T]":
        """Add search query."""
        self.filters.search(query, fields)
        return self
    
    def created_after(self, date: str) -> "ResourceQuery[T]":
        """Filter by creation date (after)."""
        self.filters.created_after = date
        return self
    
    def created_before(self, date: str) -> "ResourceQuery[T]":
        """Filter by creation date (before)."""
        self.filters.created_before = date
        return self
    
    def updated_after(self, date: str) -> "ResourceQuery[T]":
        """Filter by update date (after)."""
        self.filters.updated_after = date
        return self
    
    def updated_before(self, date: str) -> "ResourceQuery[T]":
        """Filter by update date (before)."""
        self.filters.updated_before = date
        return self
    
    def created_between(self, start_date: str, end_date: str) -> "ResourceQuery[T]":
        """Filter by creation date range."""
        self.filters.created_after = start_date
        self.filters.created_before = end_date
        return self
    
    def status(self, status: str) -> "ResourceQuery[T]":
        """Filter by status."""
        self.filters.status = status
        return self
    
    def status_in(self, statuses: List[str]) -> "ResourceQuery[T]":
        """Filter by multiple statuses."""
        self.filters.add_filter("status", FilterOperator.IN, statuses)
        return self
    
    def limit(self, count: int) -> "ResourceQuery[T]":
        """Limit number of results."""
        self.pagination.per_page = count
        return self
    
    def page(self, page: int) -> "ResourceQuery[T]":
        """Set page number."""
        self.pagination.page = page
        return self
    
    def sort_by(self, field: str, order: str = "asc") -> "ResourceQuery[T]":
        """Sort results by field."""
        self.pagination.sort_by = field
        self.pagination.sort_order = order
        return self
    
    def sort_desc(self, field: str) -> "ResourceQuery[T]":
        """Sort results by field in descending order."""
        return self.sort_by(field, "desc")
    
    def sort_asc(self, field: str) -> "ResourceQuery[T]":
        """Sort results by field in ascending order."""
        return self.sort_by(field, "asc")
    
    def timeout(self, seconds: float) -> "ResourceQuery[T]":
        """Set request timeout."""
        self.options.timeout = seconds
        return self
    
    def include_fields(self, *fields: str) -> "ResourceQuery[T]":
        """Include only specific fields in response."""
        self.options.include_fields = list(fields)
        return self
    
    def exclude_fields(self, *fields: str) -> "ResourceQuery[T]":
        """Exclude specific fields from response."""
        self.options.exclude_fields = list(fields)
        return self
    
    def force_refresh(self) -> "ResourceQuery[T]":
        """Force refresh from server, bypassing cache."""
        self.options.force_refresh = True
        return self
    
    async def all(self) -> List[T]:
        """Execute query and return all results."""
        return await self.resource.list_all(
            pagination=self.pagination,
            filters=self.filters,
            options=self.options
        )
    
    async def first(self) -> Optional[T]:
        """Execute query and return first result."""
        self.pagination.per_page = 1
        results = await self.resource.list(
            pagination=self.pagination,
            filters=self.filters,
            options=self.options
        )
        return results.data[0] if results.data else None
    
    async def last(self) -> Optional[T]:
        """Execute query and return last result."""
        # First get count to find last page
        total = await self.count()
        if total == 0:
            return None
            
        per_page = self.pagination.per_page or self.resource.default_limit
        last_page = (total - 1) // per_page + 1
        
        self.pagination.page = last_page
        self.pagination.per_page = per_page
        
        results = await self.resource.list(
            pagination=self.pagination,
            filters=self.filters,
            options=self.options
        )
        return results.data[-1] if results.data else None
    
    async def get(self, index: int) -> Optional[T]:
        """Get item at specific index."""
        per_page = self.pagination.per_page or self.resource.default_limit
        page = (index // per_page) + 1
        page_index = index % per_page
        
        self.pagination.page = page
        self.pagination.per_page = per_page
        
        results = await self.resource.list(
            pagination=self.pagination,
            filters=self.filters,
            options=self.options
        )
        
        if page_index < len(results.data):
            return results.data[page_index]
        return None
    
    async def count(self) -> int:
        """Execute query and return count."""
        return await self.resource.count(
            filters=self.filters,
            options=self.options
        )
    
    async def exists(self) -> bool:
        """Check if any results exist for this query."""
        count = await self.count()
        return count > 0
    
    async def paginate(self, page: int = 1, per_page: int = None) -> PaginatedList[T]:
        """Execute query with pagination."""
        self.pagination.page = page
        if per_page:
            self.pagination.per_page = per_page
            
        return await self.resource.list(
            pagination=self.pagination,
            filters=self.filters,
            options=self.options
        )
    
    def __aiter__(self) -> AsyncIterator[T]:
        """Support async iteration."""
        return self.resource.iter_all(
            pagination=self.pagination,
            filters=self.filters,
            options=self.options
        )
