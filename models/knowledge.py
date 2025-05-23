from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="Knowledge")


@define
class Knowledge:
    """Represents a knowledge base entry for an Agent."""

    id: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    content: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        title = self.title
        content = self.content

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if title is not UNSET:
            field_dict["title"] = title
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)
        title = d.pop("title", UNSET)
        content = d.pop("content", UNSET)

        knowledge = cls(
            id=id,
            title=title,
            content=content,
        )

        knowledge.additional_properties = d
        return knowledge

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
