from attrs import define

from ..client import AuthenticatedClient
from ..models.return_ import Return as ReturnModel
from ..base_resource import BaseResource


@define
class Returns(BaseResource[ReturnModel]):
    """Operations on Stateset Returns."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, ReturnModel, "/returns")

