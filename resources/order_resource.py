"""
Example implementation of a specific Stateset resource (Orders).
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from attrs import define

from ..client import AuthenticatedClient
from ..base_resource import BaseResource
from ..models.order import Order


@define
class Orders(BaseResource[Order]):
    """Operations on Stateset Orders."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, Order, "/orders")

    async def cancel(self, id: str, reason: Optional[str] = None) -> Order:
        """Cancel an order."""
        data = {"reason": reason} if reason else {}
        response = await self.client.post(f"{self.base_path}/{id}/cancel", json=data)
        return Order.from_dict(response)

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
        return Order.from_dict(response)

    async def add_items(self, id: str, items: List[Dict[str, Any]]) -> Order:
        """Add items to an existing order."""
        response = await self.client.post(
            f"{self.base_path}/{id}/items", json={"items": items}
        )
        return Order.from_dict(response)
