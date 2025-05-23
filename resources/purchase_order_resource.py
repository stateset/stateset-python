from attrs import define
from ..client import AuthenticatedClient
from ..models.generic import GenericModel
from ..base_resource import BaseResource

@define
class PurchaseOrders(BaseResource[GenericModel]):
    """Operations on Stateset PurchaseOrders."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, GenericModel, "/purchaseorders")
