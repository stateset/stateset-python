from attrs import define

from ..client import AuthenticatedClient
from ..models.case_ticket import CaseTicket
from ..base_resource import BaseResource


@define
class CaseTickets(BaseResource[CaseTicket]):
    """Operations on Stateset Case Tickets."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, CaseTicket, "/case_tickets")
