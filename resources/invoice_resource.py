from attrs import define
from ..client import AuthenticatedClient
from ..models.generic import GenericModel
from ..base_resource import BaseResource

@define
class Invoices(BaseResource[GenericModel]):
    """Operations on Stateset Invoices."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, GenericModel, "/invoices")
