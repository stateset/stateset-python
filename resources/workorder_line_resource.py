from attrs import define
from ..client import AuthenticatedClient
from ..models.work_order_line_items import WorkOrderLineItems
from ..base_resource import BaseResource

@define
class WorkOrderLines(BaseResource[WorkOrderLineItems]):
    """Operations on Stateset WorkOrderLines."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, WorkOrderLineItems, "/workorderitems")
