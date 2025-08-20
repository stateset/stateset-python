from attrs import define

from ..client import AuthenticatedClient
from ..models.warranty import Warranty as WarrantyModel
from ..base_resource import BaseResource


@define
class Warranties(BaseResource[WarrantyModel]):
    """Operations on Stateset Warranties."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, WarrantyModel, "/warranties")

