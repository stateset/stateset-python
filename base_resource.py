"""
Base resource class that implements common functionality for all Stateset API resources.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from .client import AuthenticatedClient
from .stateset_types import PaginatedList, PaginationParams, StatesetObject

T = TypeVar('T', bound=StatesetObject)

class BaseResource(Generic[T]):
    """Base class for all Stateset API resources."""
    
    def __init__(
        self,
        client: AuthenticatedClient,
        object_class: Type[T],
        base_path: str
    ) -> None:
        self.client = client
        self.object_class = object_class
        self.base_path = base_path

    async def list(
        self,
        params: Optional[PaginationParams] = None,
        **kwargs: Any
    ) -> PaginatedList[T]:
        """List all resources with pagination support."""
        params = params or PaginationParams()
        query_params = {
            "page": params.page,
            "per_page": params.per_page,
            **kwargs
        }
        
        if params.sort_by:
            query_params["sort_by"] = params.sort_by
            if params.sort_order:
                query_params["sort_order"] = params.sort_order

        response = await self.client.get(
            path=self.base_path,
            params=query_params
        )
        
        data = [self.object_class(**item) for item in response["data"]]
        return PaginatedList(
            data=data,
            total=response["total"],
            page=response["page"],
            per_page=response["per_page"],
            total_pages=response["total_pages"],
            has_next=response["has_next"],
            has_prev=response["has_prev"]
        )

    async def get(self, id: str) -> T:
        """Retrieve a single resource by ID."""
        response = await self.client.get(f"{self.base_path}/{id}")
        return self.object_class(**response)

    async def create(self, data: Dict[str, Any]) -> T:
        """Create a new resource."""
        response = await self.client.post(self.base_path, json=data)
        return self.object_class(**response)

    async def update(self, id: str, data: Dict[str, Any]) -> T:
        """Update an existing resource."""
        response = await self.client.put(f"{self.base_path}/{id}", json=data)
        return self.object_class(**response)

    async def delete(self, id: str) -> None:
        """Delete a resource."""
        await self.client.delete(f"{self.base_path}/{id}")