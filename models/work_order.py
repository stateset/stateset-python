import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkOrder")


@define
class WorkOrder:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier for the work order.
        number (Union[Unset, int]): The work order number.
        site (Union[Unset, str]): The site where the work order is located.
        work_order_type (Union[Unset, str]): The type of work order.
        location (Union[Unset, str]): The location where the work order is taking place.
        part (Union[Unset, str]): The part being worked on in the work order.
        order_number (Union[Unset, str]): The order number associated with the work order.
        manufacture_order (Union[Unset, str]): The manufacture order associated with the work order.
        status (Union[Unset, str]): The current status of the work order.
        created_by (Union[Unset, str]): The user who created the work order.
        created_at (Union[Unset, datetime.datetime]): The date and time the work order was created.
        updated_at (Union[Unset, datetime.datetime]): The date and time the work order was last updated.
        issue_date (Union[Unset, datetime.date]): The date the work order was issued.
        expected_completion_date (Union[Unset, datetime.date]): The expected completion date for the work order.
        priority (Union[Unset, str]): The priority level of the work order.
        memo (Union[Unset, str]): Any additional notes or comments about the work order.
        bill_of_materials_number (Union[Unset, int]): The bill of materials number associated with the work order.
    """

    id: Union[Unset, str] = UNSET
    number: Union[Unset, int] = UNSET
    site: Union[Unset, str] = UNSET
    work_order_type: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    part: Union[Unset, str] = UNSET
    order_number: Union[Unset, str] = UNSET
    manufacture_order: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    issue_date: Union[Unset, datetime.date] = UNSET
    expected_completion_date: Union[Unset, datetime.date] = UNSET
    priority: Union[Unset, str] = UNSET
    memo: Union[Unset, str] = UNSET
    bill_of_materials_number: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        number = self.number
        site = self.site
        work_order_type = self.work_order_type
        location = self.location
        part = self.part
        order_number = self.order_number
        manufacture_order = self.manufacture_order
        status = self.status
        created_by = self.created_by
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        issue_date: Union[Unset, str] = UNSET
        if not isinstance(self.issue_date, Unset):
            issue_date = self.issue_date.isoformat()

        expected_completion_date: Union[Unset, str] = UNSET
        if not isinstance(self.expected_completion_date, Unset):
            expected_completion_date = self.expected_completion_date.isoformat()

        priority = self.priority
        memo = self.memo
        bill_of_materials_number = self.bill_of_materials_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if number is not UNSET:
            field_dict["number"] = number
        if site is not UNSET:
            field_dict["site"] = site
        if work_order_type is not UNSET:
            field_dict["work_order_type"] = work_order_type
        if location is not UNSET:
            field_dict["location"] = location
        if part is not UNSET:
            field_dict["part"] = part
        if order_number is not UNSET:
            field_dict["order_number"] = order_number
        if manufacture_order is not UNSET:
            field_dict["manufacture_order"] = manufacture_order
        if status is not UNSET:
            field_dict["status"] = status
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if issue_date is not UNSET:
            field_dict["issue_date"] = issue_date
        if expected_completion_date is not UNSET:
            field_dict["expected_completion_date"] = expected_completion_date
        if priority is not UNSET:
            field_dict["priority"] = priority
        if memo is not UNSET:
            field_dict["memo"] = memo
        if bill_of_materials_number is not UNSET:
            field_dict["bill_of_materials_number"] = bill_of_materials_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        number = d.pop("number", UNSET)

        site = d.pop("site", UNSET)

        work_order_type = d.pop("work_order_type", UNSET)

        location = d.pop("location", UNSET)

        part = d.pop("part", UNSET)

        order_number = d.pop("order_number", UNSET)

        manufacture_order = d.pop("manufacture_order", UNSET)

        status = d.pop("status", UNSET)

        created_by = d.pop("created_by", UNSET)

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

        _issue_date = d.pop("issue_date", UNSET)
        issue_date: Union[Unset, datetime.date]
        if isinstance(_issue_date, Unset):
            issue_date = UNSET
        else:
            issue_date = isoparse(_issue_date).date()

        _expected_completion_date = d.pop("expected_completion_date", UNSET)
        expected_completion_date: Union[Unset, datetime.date]
        if isinstance(_expected_completion_date, Unset):
            expected_completion_date = UNSET
        else:
            expected_completion_date = isoparse(_expected_completion_date).date()

        priority = d.pop("priority", UNSET)

        memo = d.pop("memo", UNSET)

        bill_of_materials_number = d.pop("bill_of_materials_number", UNSET)

        work_order = cls(
            id=id,
            number=number,
            site=site,
            work_order_type=work_order_type,
            location=location,
            part=part,
            order_number=order_number,
            manufacture_order=manufacture_order,
            status=status,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
            issue_date=issue_date,
            expected_completion_date=expected_completion_date,
            priority=priority,
            memo=memo,
            bill_of_materials_number=bill_of_materials_number,
        )

        work_order.additional_properties = d
        return work_order

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
