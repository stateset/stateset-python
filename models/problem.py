from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="Problem")


@define
class Problem:
    """The Problem Details JSON Object [[RFC7807](https://tools.ietf.org/html/rfc7807)].

    Attributes:
        type (Union[Unset, str]): A URI reference [[RFC3986](https://tools.ietf.org/html/rfc3986)] that identifies the
            problem type. It should provide human-readable documentation for the problem type. When this member is not
            present, its value is assumed to be "about:blank".
        title (Union[Unset, str]): A short, human-readable summary of the problem type. It SHOULD NOT change from
            occurrence to occurrence of the problem, except for purposes of localization.
        status (Union[Unset, int]): The HTTP status code.
        detail (Union[Unset, str]): A human-readable explanation specific to this occurrence of the problem.
        instance (Union[Unset, str]): A URI reference that identifies the specific occurrence of the problem.  It may or
            may not yield further information if dereferenced.
    """

    type: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    detail: Union[Unset, str] = UNSET
    instance: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        title = self.title
        status = self.status
        detail = self.detail
        instance = self.instance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if title is not UNSET:
            field_dict["title"] = title
        if status is not UNSET:
            field_dict["status"] = status
        if detail is not UNSET:
            field_dict["detail"] = detail
        if instance is not UNSET:
            field_dict["instance"] = instance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type", UNSET)

        title = d.pop("title", UNSET)

        status = d.pop("status", UNSET)

        detail = d.pop("detail", UNSET)

        instance = d.pop("instance", UNSET)

        problem = cls(
            type=type,
            title=title,
            status=status,
            detail=detail,
            instance=instance,
        )

        problem.additional_properties = d
        return problem

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
