from attrs import define

from ..base_resource import BaseResource
from ..client import AuthenticatedClient
from ..models.eval import Eval


@define
class Evals(BaseResource[Eval]):
    """Operations on evaluation records."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, Eval, "/evals")
