from attrs import define
from ..client import AuthenticatedClient
from ..models.generic import GenericModel
from ..base_resource import BaseResource

@define
class Settlements(BaseResource[GenericModel]):
    """Operations on Stateset Settlements."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, GenericModel, "/settlements")
