from attrs import define

from ..base_resource import BaseResource
from ..client import AuthenticatedClient
from ..models.attribute import Attribute


@define
class Attributes(BaseResource[Attribute]):
    """Operations on Stateset Attributes."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, Attribute, "/attributes")
