from attrs import define

from ..client import AuthenticatedClient
from ..models.return_item import ReturnItem
from ..base_resource import BaseResource


@define
class ReturnLines(BaseResource[ReturnItem]):
    """Operations on Stateset Return line items."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, ReturnItem, "/returnitems")
