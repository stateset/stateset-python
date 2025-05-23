from attrs import define
from ..client import AuthenticatedClient
from ..models.inventory_items import InventoryItems
from ..base_resource import BaseResource

@define
class Inventory(BaseResource[InventoryItems]):
    """Operations on Stateset Inventory."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, InventoryItems, "/inventoryitems")
