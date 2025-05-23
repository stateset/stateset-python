from attrs import define

from ..base_resource import BaseResource
from ..client import AuthenticatedClient
from ..models.agent_response import AgentResponse


@define
class Responses(BaseResource[AgentResponse]):
    """Operations on Agent responses."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, AgentResponse, "/responses")
