from attrs import define
from ..client import AuthenticatedClient
from ..models.bill_of_materials import BillOfMaterials
from ..base_resource import BaseResource

@define
class BillOfMaterials(BaseResource[BillOfMaterials]):
    """Operations on Stateset BillOfMaterials."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, BillOfMaterials, "/billofmaterials")
