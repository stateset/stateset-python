from attrs import define

from ..client import AuthenticatedClient
from ..models.notes import Notes as NoteModel
from ..base_resource import BaseResource


@define
class Notes(BaseResource[NoteModel]):
    """Operations on Stateset Notes."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(client, NoteModel, "/notes")
