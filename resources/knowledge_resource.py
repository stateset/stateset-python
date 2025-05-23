from attrs import define

from ..base_resource import BaseResource
from ..client import AuthenticatedClient
from ..models.knowledge import Knowledge


@define
class KnowledgeBase(BaseResource[Knowledge]):
    """Operations on knowledge entries."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, Knowledge, "/knowledge")
