from attrs import define

from ..base_resource import BaseResource
from ..client import AuthenticatedClient
from ..models.rule import Rule


@define
class Rules(BaseResource[Rule]):
    """Operations on Stateset Rules."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, Rule, "/rules")
