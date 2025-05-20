import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="CaseTicket")


@define
class CaseTicket:
    """Represents a customer service case ticket."""

    id: Union[Unset, str] = UNSET
    customer_id: Union[Unset, str] = UNSET
    subject: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    priority: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        customer_id = self.customer_id
        subject = self.subject
        description = self.description
        status = self.status
        priority = self.priority
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()
        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if customer_id is not UNSET:
            field_dict["customer_id"] = customer_id
        if subject is not UNSET:
            field_dict["subject"] = subject
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)
        customer_id = d.pop("customer_id", UNSET)
        subject = d.pop("subject", UNSET)
        description = d.pop("description", UNSET)
        status = d.pop("status", UNSET)
        priority = d.pop("priority", UNSET)
        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)
        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)
        case_ticket = cls(
            id=id,
            customer_id=customer_id,
            subject=subject,
            description=description,
            status=status,
            priority=priority,
            created_at=created_at,
            updated_at=updated_at,
        )

        case_ticket.additional_properties = d
        return case_ticket

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
