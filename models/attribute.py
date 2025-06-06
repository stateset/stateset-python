from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="Attribute")


@define
class Attribute:
    """Represents a key/value attribute for an Agent."""

    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        key = self.key
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)
        key = d.pop("key", UNSET)
        value = d.pop("value", UNSET)

        attribute = cls(
            id=id,
            key=key,
            value=value,
        )

        attribute.additional_properties = d
        return attribute

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
