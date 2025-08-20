from attrs import define

from ..client import AuthenticatedClient
from ..models.customers import Customers as CustomerModel
from ..base_resource import BaseResource


@define
class Customers(BaseResource[CustomerModel]):
    """Operations on Stateset Customers."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, CustomerModel, "/customers")

