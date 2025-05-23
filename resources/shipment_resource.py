from typing import Any, Dict

from attrs import define

from ..client import AuthenticatedClient
from ..models.generic import GenericModel
from ..models.shipping_label import ShippingLabel
from ..base_resource import BaseResource


@define
class Shipments(BaseResource[GenericModel]):
    """Operations on Stateset Shipments."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, GenericModel, "/shipments")

    async def create_label(self, id: str, data: Dict[str, Any]) -> ShippingLabel:
        """Generate a shipping label for the given shipment."""
        response = await self.client.post(f"{self.base_path}/{id}/label", json=data)
        return ShippingLabel.from_dict(response)
