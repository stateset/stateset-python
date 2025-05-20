import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="ManufactureOrderLineItem")


@define
class ManufactureOrderLineItem:
    """
    Attributes:
        id (Union[Unset, str]): Unique identifier for the Manufacture Order Line Item.
        line_type (Union[Unset, str]): The type of the manufacture order line item.
        output_type (Union[Unset, str]): The type of output of the manufacture order line item.
        line_status (Union[Unset, str]): The status of the manufacture order line item.
        part_number (Union[Unset, str]): The part number of the manufacture order line item.
        part_name (Union[Unset, str]): The name of the part of the manufacture order line item.
        expected_date (Union[Unset, datetime.date]): The expected completion date of the manufacture order line item.
        quantity (Union[Unset, int]): The quantity of the manufacture order line item.
        work_order_number (Union[Unset, int]): The work order number of the manufacture order line item.
        site (Union[Unset, str]): The site where the manufacture order line item is to be produced.
        yield_location (Union[Unset, str]): The location where the yield of the manufacture order line item is to be
            produced.
        bom_number (Union[Unset, int]): The Bill of Materials (BOM) number of the manufacture order line item.
        bom_name (Union[Unset, str]): The Bill of Materials (BOM) name of the manufacture order line item.
        priority (Union[Unset, str]): The priority of the manufacture order line item.
        manufacture_order_number (Union[Unset, int]): The number of the manufacture order for which the manufacture
            order line item belongs to.
    """

    id: Union[Unset, str] = UNSET
    line_type: Union[Unset, str] = UNSET
    output_type: Union[Unset, str] = UNSET
    line_status: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    part_name: Union[Unset, str] = UNSET
    expected_date: Union[Unset, datetime.date] = UNSET
    quantity: Union[Unset, int] = UNSET
    work_order_number: Union[Unset, int] = UNSET
    site: Union[Unset, str] = UNSET
    yield_location: Union[Unset, str] = UNSET
    bom_number: Union[Unset, int] = UNSET
    bom_name: Union[Unset, str] = UNSET
    priority: Union[Unset, str] = UNSET
    manufacture_order_number: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        line_type = self.line_type
        output_type = self.output_type
        line_status = self.line_status
        part_number = self.part_number
        part_name = self.part_name
        expected_date: Union[Unset, str] = UNSET
        if not isinstance(self.expected_date, Unset):
            expected_date = self.expected_date.isoformat()

        quantity = self.quantity
        work_order_number = self.work_order_number
        site = self.site
        yield_location = self.yield_location
        bom_number = self.bom_number
        bom_name = self.bom_name
        priority = self.priority
        manufacture_order_number = self.manufacture_order_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if line_type is not UNSET:
            field_dict["line_type"] = line_type
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if line_status is not UNSET:
            field_dict["line_status"] = line_status
        if part_number is not UNSET:
            field_dict["part_number"] = part_number
        if part_name is not UNSET:
            field_dict["part_name"] = part_name
        if expected_date is not UNSET:
            field_dict["expected_date"] = expected_date
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if work_order_number is not UNSET:
            field_dict["work_order_number"] = work_order_number
        if site is not UNSET:
            field_dict["site"] = site
        if yield_location is not UNSET:
            field_dict["yield_location"] = yield_location
        if bom_number is not UNSET:
            field_dict["bom_number"] = bom_number
        if bom_name is not UNSET:
            field_dict["bom_name"] = bom_name
        if priority is not UNSET:
            field_dict["priority"] = priority
        if manufacture_order_number is not UNSET:
            field_dict["manufacture_order_number"] = manufacture_order_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        line_type = d.pop("line_type", UNSET)

        output_type = d.pop("output_type", UNSET)

        line_status = d.pop("line_status", UNSET)

        part_number = d.pop("part_number", UNSET)

        part_name = d.pop("part_name", UNSET)

        _expected_date = d.pop("expected_date", UNSET)
        expected_date: Union[Unset, datetime.date]
        if isinstance(_expected_date, Unset):
            expected_date = UNSET
        else:
            expected_date = isoparse(_expected_date).date()

        quantity = d.pop("quantity", UNSET)

        work_order_number = d.pop("work_order_number", UNSET)

        site = d.pop("site", UNSET)

        yield_location = d.pop("yield_location", UNSET)

        bom_number = d.pop("bom_number", UNSET)

        bom_name = d.pop("bom_name", UNSET)

        priority = d.pop("priority", UNSET)

        manufacture_order_number = d.pop("manufacture_order_number", UNSET)

        manufacture_order_line_item = cls(
            id=id,
            line_type=line_type,
            output_type=output_type,
            line_status=line_status,
            part_number=part_number,
            part_name=part_name,
            expected_date=expected_date,
            quantity=quantity,
            work_order_number=work_order_number,
            site=site,
            yield_location=yield_location,
            bom_number=bom_number,
            bom_name=bom_name,
            priority=priority,
            manufacture_order_number=manufacture_order_number,
        )

        manufacture_order_line_item.additional_properties = d
        return manufacture_order_line_item

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
