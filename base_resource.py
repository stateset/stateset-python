"""
Enhanced base resource class with improved pagination, filtering, and modern Python features.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, AsyncIterator, Union
from dataclasses import dataclass, field

from .client import AuthenticatedClient
from .stateset_types import PaginatedList, PaginationParams
from .errors import StatesetError, StatesetInvalidRequestError

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class FilterParams:
    """Parameters for filtering API requests."""
    
    # Common filter parameters
    created_after: Optional[str] = None
    created_before: Optional[str] = None
    updated_after: Optional[str] = None
    updated_before: Optional[str] = None
    status: Optional[str] = None
    
    # Custom filters (can be extended by subclasses)
    custom_filters: Dict[str, Any] = field(default_factory=dict)
    
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
            
        # Add custom filters
        params.update(self.custom_filters)
        
        # Remove None values
        return {k: v for k, v in params.items() if v is not None}


@dataclass
class RequestOptions:
    """Options for customizing API requests."""
    
    timeout: Optional[float] = None
    headers: Optional[Dict[str, str]] = None
    idempotency_key: Optional[str] = None
    
    def to_kwargs(self) -> Dict[str, Any]:
        """Convert options to httpx request kwargs."""
        kwargs = {}
        
        if self.timeout:
            kwargs["timeout"] = self.timeout
            
        headers = dict(self.headers or {})
        if self.idempotency_key:
            headers["Idempotency-Key"] = self.idempotency_key
            
        if headers:
            kwargs["headers"] = headers
            
        return kwargs


class BaseResource(Generic[T]):
    """Enhanced base class for all Stateset API resources."""

    def __init__(
        self, 
        client: AuthenticatedClient, 
        object_class: Type[T], 
        base_path: str,
        default_limit: int = 50,
        max_limit: int = 1000
    ) -> None:
        self.client = client
        self.object_class = object_class
        self.base_path = base_path.rstrip("/")
        self.default_limit = default_limit
        self.max_limit = max_limit

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
                return PaginatedList(
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
                return PaginatedList(
                    data=data,
                    total=response.get("total", len(data)),
                    page=response.get("page", 1),
                    per_page=response.get("per_page", len(data)),
                    total_pages=response.get("total_pages", 1),
                    has_next=response.get("has_next", False),
                    has_prev=response.get("has_prev", False),
                )

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
            
        request_kwargs = options.to_kwargs() if options else {}
        if kwargs:
            request_kwargs["params"] = kwargs

        try:
            response = await self.client.get(
                f"{self.base_path}/{id}",
                **request_kwargs
            )
            return self.object_class(**response)

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
            return self.object_class(**response)

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
            return self.object_class(**response)

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

        except Exception as e:
            logger.error(f"Failed to delete {self.object_class.__name__} {id}: {e}")
            raise

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
        # Get first page to access total count
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


class ResourceQuery(Generic[T]):
    """Query builder for resource operations with method chaining."""
    
    def __init__(self, resource: BaseResource[T], filters: FilterParams):
        self.resource = resource
        self.filters = filters
        self.pagination = PaginationParams()
        self.options = RequestOptions()
    
    def where(self, **filters: Any) -> "ResourceQuery[T]":
        """Add filter conditions."""
        self.filters.custom_filters.update(filters)
        return self
    
    def created_after(self, date: str) -> "ResourceQuery[T]":
        """Filter by creation date (after)."""
        self.filters.created_after = date
        return self
    
    def created_before(self, date: str) -> "ResourceQuery[T]":
        """Filter by creation date (before)."""
        self.filters.created_before = date
        return self
    
    def status(self, status: str) -> "ResourceQuery[T]":
        """Filter by status."""
        self.filters.status = status
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
    
    def timeout(self, seconds: float) -> "ResourceQuery[T]":
        """Set request timeout."""
        self.options.timeout = seconds
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
    
    async def count(self) -> int:
        """Execute query and return count."""
        return await self.resource.count(
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
