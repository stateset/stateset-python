from attrs import define
from .client import AuthenticatedClient
from .models.generic import GenericModel
from .base_resource import BaseResource


@define
class FulfillmentOrders(BaseResource[GenericModel]):
    """Operations on Stateset Fulfillment Orders."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, GenericModel, "/fulfillment_orders")
