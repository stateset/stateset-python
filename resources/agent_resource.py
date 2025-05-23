from attrs import define

from ..base_resource import BaseResource
from ..client import AuthenticatedClient
from ..models.agent import Agent


@define
class Agents(BaseResource[Agent]):
    """Operations on Stateset Agents."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, Agent, "/agents")
