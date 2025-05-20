from attrs import define

from ..client import AuthenticatedClient
from ..models.messages import Messages as MessageModel
from ..base_resource import BaseResource


@define
class Messages(BaseResource[MessageModel]):
    """Operations on Stateset Messages."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, MessageModel, "/messages")
