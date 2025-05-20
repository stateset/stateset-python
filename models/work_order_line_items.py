from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="WorkOrderLineItems")


@define
class WorkOrderLineItems:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier for the work order line item.
        part_number (Union[Unset, str]): The part number for the line item.
        part_name (Union[Unset, str]): The name of the part for the line item.
        line_type (Union[Unset, str]): The type of line item.
        line_status (Union[Unset, str]): The status of the line item.
        unit_quantity (Union[Unset, int]): The quantity per unit of the line item.
        total_quantity (Union[Unset, int]): The total quantity of the line item.
        work_order_number (Union[Unset, int]): The work order number associated with the line item.
    """

    id: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    part_name: Union[Unset, str] = UNSET
    line_type: Union[Unset, str] = UNSET
    line_status: Union[Unset, str] = UNSET
    unit_quantity: Union[Unset, int] = UNSET
    total_quantity: Union[Unset, int] = UNSET
    work_order_number: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        part_number = self.part_number
        part_name = self.part_name
        line_type = self.line_type
        line_status = self.line_status
        unit_quantity = self.unit_quantity
        total_quantity = self.total_quantity
        work_order_number = self.work_order_number

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if part_number is not UNSET:
            field_dict["part_number"] = part_number
        if part_name is not UNSET:
            field_dict["part_name"] = part_name
        if line_type is not UNSET:
            field_dict["line_type"] = line_type
        if line_status is not UNSET:
            field_dict["line_status"] = line_status
        if unit_quantity is not UNSET:
            field_dict["unit_quantity"] = unit_quantity
        if total_quantity is not UNSET:
            field_dict["total_quantity"] = total_quantity
        if work_order_number is not UNSET:
            field_dict["work_order_number"] = work_order_number

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        part_number = d.pop("part_number", UNSET)

        part_name = d.pop("part_name", UNSET)

        line_type = d.pop("line_type", UNSET)

        line_status = d.pop("line_status", UNSET)

        unit_quantity = d.pop("unit_quantity", UNSET)

        total_quantity = d.pop("total_quantity", UNSET)

        work_order_number = d.pop("work_order_number", UNSET)

        work_order_line_items = cls(
            id=id,
            part_number=part_number,
            part_name=part_name,
            line_type=line_type,
            line_status=line_status,
            unit_quantity=unit_quantity,
            total_quantity=total_quantity,
            work_order_number=work_order_number,
        )

        work_order_line_items.additional_properties = d
        return work_order_line_items

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
