from attrs import define
from ..client import AuthenticatedClient
from ..models.work_order import WorkOrder
from ..base_resource import BaseResource

@define
class WorkOrders(BaseResource[WorkOrder]):
    """Operations on Stateset WorkOrders."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, WorkOrder, "/workorders")
