import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="ManufactureOrder")


@define
class ManufactureOrder:
    """
    Attributes:
        id (Union[Unset, str]):
        number (Union[Unset, int]):
        site (Union[Unset, str]):
        yield_location (Union[Unset, str]):
        priority (Union[Unset, str]):
        expected_completion_date (Union[Unset, datetime.date]):
        created_on (Union[Unset, datetime.date]):
        issued_on (Union[Unset, datetime.date]):
        memo (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    number: Union[Unset, int] = UNSET
    site: Union[Unset, str] = UNSET
    yield_location: Union[Unset, str] = UNSET
    priority: Union[Unset, str] = UNSET
    expected_completion_date: Union[Unset, datetime.date] = UNSET
    created_on: Union[Unset, datetime.date] = UNSET
    issued_on: Union[Unset, datetime.date] = UNSET
    memo: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        number = self.number
        site = self.site
        yield_location = self.yield_location
        priority = self.priority
        expected_completion_date: Union[Unset, str] = UNSET
        if not isinstance(self.expected_completion_date, Unset):
            expected_completion_date = self.expected_completion_date.isoformat()

        created_on: Union[Unset, str] = UNSET
        if not isinstance(self.created_on, Unset):
            created_on = self.created_on.isoformat()

        issued_on: Union[Unset, str] = UNSET
        if not isinstance(self.issued_on, Unset):
            issued_on = self.issued_on.isoformat()

        memo = self.memo

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if number is not UNSET:
            field_dict["number"] = number
        if site is not UNSET:
            field_dict["site"] = site
        if yield_location is not UNSET:
            field_dict["yield_location"] = yield_location
        if priority is not UNSET:
            field_dict["priority"] = priority
        if expected_completion_date is not UNSET:
            field_dict["expected_completion_date"] = expected_completion_date
        if created_on is not UNSET:
            field_dict["created_on"] = created_on
        if issued_on is not UNSET:
            field_dict["issued_on"] = issued_on
        if memo is not UNSET:
            field_dict["memo"] = memo

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        number = d.pop("number", UNSET)

        site = d.pop("site", UNSET)

        yield_location = d.pop("yield_location", UNSET)

        priority = d.pop("priority", UNSET)

        _expected_completion_date = d.pop("expected_completion_date", UNSET)
        expected_completion_date: Union[Unset, datetime.date]
        if isinstance(_expected_completion_date, Unset):
            expected_completion_date = UNSET
        else:
            expected_completion_date = isoparse(_expected_completion_date).date()

        _created_on = d.pop("created_on", UNSET)
        created_on: Union[Unset, datetime.date]
        if isinstance(_created_on, Unset):
            created_on = UNSET
        else:
            created_on = isoparse(_created_on).date()

        _issued_on = d.pop("issued_on", UNSET)
        issued_on: Union[Unset, datetime.date]
        if isinstance(_issued_on, Unset):
            issued_on = UNSET
        else:
            issued_on = isoparse(_issued_on).date()

        memo = d.pop("memo", UNSET)

        manufacture_order = cls(
            id=id,
            number=number,
            site=site,
            yield_location=yield_location,
            priority=priority,
            expected_completion_date=expected_completion_date,
            created_on=created_on,
            issued_on=issued_on,
            memo=memo,
        )

        manufacture_order.additional_properties = d
        return manufacture_order

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
