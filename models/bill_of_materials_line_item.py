from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="BillOfMaterialsLineItem")


@define
class BillOfMaterialsLineItem:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier of the line item. Example: 3fa85f64-5717-4562-b3fc-2c963f66afa6.
        part_number (Union[Unset, str]): The part number of the item. Example: 12345.
        part_name (Union[Unset, str]): The name of the item. Example: Screw.
        quantity (Union[Unset, int]): The quantity of the item required in the bill of materials. Example: 50.
        purchase_supply_type (Union[Unset, str]): The type of purchase/supply for the item. Example: Vendor.
        line_type (Union[Unset, str]): The type of line item in the bill of materials. Example: Raw Material.
        bill_of_materials_number (Union[Unset, int]): The bill of materials number that this line item belongs to.
            Example: 1.
        status (Union[Unset, str]): The status of the line item. Example: Pending.
    """

    id: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    part_name: Union[Unset, str] = UNSET
    quantity: Union[Unset, int] = UNSET
    purchase_supply_type: Union[Unset, str] = UNSET
    line_type: Union[Unset, str] = UNSET
    bill_of_materials_number: Union[Unset, int] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        part_number = self.part_number
        part_name = self.part_name
        quantity = self.quantity
        purchase_supply_type = self.purchase_supply_type
        line_type = self.line_type
        bill_of_materials_number = self.bill_of_materials_number
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if part_number is not UNSET:
            field_dict["part_number"] = part_number
        if part_name is not UNSET:
            field_dict["part_name"] = part_name
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if purchase_supply_type is not UNSET:
            field_dict["purchase_supply_type"] = purchase_supply_type
        if line_type is not UNSET:
            field_dict["line_type"] = line_type
        if bill_of_materials_number is not UNSET:
            field_dict["bill_of_materials_number"] = bill_of_materials_number
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        part_number = d.pop("part_number", UNSET)

        part_name = d.pop("part_name", UNSET)

        quantity = d.pop("quantity", UNSET)

        purchase_supply_type = d.pop("purchase_supply_type", UNSET)

        line_type = d.pop("line_type", UNSET)

        bill_of_materials_number = d.pop("bill_of_materials_number", UNSET)

        status = d.pop("status", UNSET)

        bill_of_materials_line_item = cls(
            id=id,
            part_number=part_number,
            part_name=part_name,
            quantity=quantity,
            purchase_supply_type=purchase_supply_type,
            line_type=line_type,
            bill_of_materials_number=bill_of_materials_number,
            status=status,
        )

        bill_of_materials_line_item.additional_properties = d
        return bill_of_materials_line_item

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
