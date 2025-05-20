"""
Example implementation of a specific Stateset resource (Orders).
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from attrs import define, field

from ..base_resource import BaseResource
from ..stateset_types import StatesetObject, StatesetID, OrderStatus, Metadata


@define
class OrderItem:
    """Represents an item in an order."""

    product_id: StatesetID
    quantity: int
    price: float
    currency: str = field(default="USD")
    metadata: Metadata = field(factory=dict)


@define
class Order(StatesetObject):
    """Represents a Stateset Order."""

    customer_id: StatesetID
    status: OrderStatus
    items: List[OrderItem]
    total_amount: float
    currency: str = field(default="USD")
    shipping_address: Optional[Dict[str, str]] = None
    tracking_number: Optional[str] = None

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        # Convert item dictionaries to OrderItem objects
        if self.items and isinstance(self.items[0], dict):
            self.items = [OrderItem(**item) for item in self.items]


class Orders(BaseResource[Order]):
    """Operations on Stateset Orders."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, Order, "/orders")

    async def cancel(self, id: str, reason: Optional[str] = None) -> Order:
        """Cancel an order."""
        data = {"reason": reason} if reason else {}
        response = await self.client.post(f"{self.base_path}/{id}/cancel", json=data)
        return Order(**response)

    async def mark_as_shipped(
        self,
        id: str,
        tracking_number: str,
        carrier: str,
        shipped_at: Optional[datetime] = None,
    ) -> Order:
        """Mark an order as shipped."""
        data = {
            "tracking_number": tracking_number,
            "carrier": carrier,
            "shipped_at": shipped_at.isoformat() if shipped_at else None,
        }
        response = await self.client.post(f"{self.base_path}/{id}/ship", json=data)
        return Order(**response)

    async def add_items(self, id: str, items: List[Dict[str, Any]]) -> Order:
        """Add items to an existing order."""
        response = await self.client.post(
            f"{self.base_path}/{id}/items", json={"items": items}
        )
        return Order(**response)
