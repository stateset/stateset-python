from attrs import define
from ..client import AuthenticatedClient
from ..models.manufacture_order import ManufactureOrder
from ..base_resource import BaseResource

@define
class ManufactureOrders(BaseResource[ManufactureOrder]):
    """Operations on Stateset ManufactureOrders."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, ManufactureOrder, "/manufactureorders")
