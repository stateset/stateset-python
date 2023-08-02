import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BillOfMaterials")


@define
class BillOfMaterials:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier for the bill of materials.
        number (Union[Unset, int]): The number of the bill of materials.
        name (Union[Unset, str]): The name of the bill of materials.
        valid (Union[Unset, str]): Whether or not the bill of materials is valid.
        groups (Union[Unset, str]): The groups associated with the bill of materials.
        created_at (Union[Unset, datetime.datetime]): The date and time the bill of materials was created.
        updated_at (Union[Unset, datetime.datetime]): The date and time the bill of materials was last updated.
        description (Union[Unset, str]): A description of the bill of materials.
    """

    id: Union[Unset, str] = UNSET
    number: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    valid: Union[Unset, str] = UNSET
    groups: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        number = self.number
        name = self.name
        valid = self.valid
        groups = self.groups
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if number is not UNSET:
            field_dict["number"] = number
        if name is not UNSET:
            field_dict["name"] = name
        if valid is not UNSET:
            field_dict["valid"] = valid
        if groups is not UNSET:
            field_dict["groups"] = groups
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        number = d.pop("number", UNSET)

        name = d.pop("name", UNSET)

        valid = d.pop("valid", UNSET)

        groups = d.pop("groups", UNSET)

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

        description = d.pop("description", UNSET)

        bill_of_materials = cls(
            id=id,
            number=number,
            name=name,
            valid=valid,
            groups=groups,
            created_at=created_at,
            updated_at=updated_at,
            description=description,
        )

        bill_of_materials.additional_properties = d
        return bill_of_materials

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
