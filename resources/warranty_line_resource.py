from attrs import define

from ..client import AuthenticatedClient
from ..models.warranty_item import WarrantyItem
from ..base_resource import BaseResource


@define
class WarrantyLines(BaseResource[WarrantyItem]):
    """Operations on Stateset Warranty line items."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, WarrantyItem, "/warrantyitems")
