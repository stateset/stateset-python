from attrs import define
from ..client import AuthenticatedClient
from ..models.manufacture_order_line_item import ManufactureOrderLineItem
from ..base_resource import BaseResource

@define
class ManufactureOrderLines(BaseResource[ManufactureOrderLineItem]):
    """Operations on Stateset ManufactureOrderLines."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, ManufactureOrderLineItem, "/manufactureorderitems")
