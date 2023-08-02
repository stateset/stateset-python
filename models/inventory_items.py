import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="InventoryItems")


@define
class InventoryItems:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier of the inventory item.
        sku (Union[Unset, str]): The stock keeping unit of the inventory item.
        description (Union[Unset, str]): The description of the inventory item.
        size (Union[Unset, str]): The size of the inventory item.
        incoming (Union[Unset, int]): The quantity of incoming inventory item.
        color (Union[Unset, str]): The color of the inventory item.
        warehouse (Union[Unset, int]): The identifier of the warehouse where the inventory item is stored.
        arriving (Union[Unset, datetime.date]): The date when the inventory item is expected to arrive.
        purchase_order_id (Union[Unset, str]): The identifier of the purchase order for the inventory item.
        available (Union[Unset, int]): The quantity of available inventory item.
        delivery_date (Union[Unset, datetime.date]): The date when the inventory item is delivered.
        arrival_date (Union[Unset, datetime.date]): The date when the inventory item arrived.
        upc (Union[Unset, str]): The universal product code of the inventory item.
        restock_date (Union[Unset, datetime.date]): The date when the inventory item is scheduled to be restocked.
    """

    id: Union[Unset, str] = UNSET
    sku: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    size: Union[Unset, str] = UNSET
    incoming: Union[Unset, int] = UNSET
    color: Union[Unset, str] = UNSET
    warehouse: Union[Unset, int] = UNSET
    arriving: Union[Unset, datetime.date] = UNSET
    purchase_order_id: Union[Unset, str] = UNSET
    available: Union[Unset, int] = UNSET
    delivery_date: Union[Unset, datetime.date] = UNSET
    arrival_date: Union[Unset, datetime.date] = UNSET
    upc: Union[Unset, str] = UNSET
    restock_date: Union[Unset, datetime.date] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        sku = self.sku
        description = self.description
        size = self.size
        incoming = self.incoming
        color = self.color
        warehouse = self.warehouse
        arriving: Union[Unset, str] = UNSET
        if not isinstance(self.arriving, Unset):
            arriving = self.arriving.isoformat()

        purchase_order_id = self.purchase_order_id
        available = self.available
        delivery_date: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_date, Unset):
            delivery_date = self.delivery_date.isoformat()

        arrival_date: Union[Unset, str] = UNSET
        if not isinstance(self.arrival_date, Unset):
            arrival_date = self.arrival_date.isoformat()

        upc = self.upc
        restock_date: Union[Unset, str] = UNSET
        if not isinstance(self.restock_date, Unset):
            restock_date = self.restock_date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if sku is not UNSET:
            field_dict["sku"] = sku
        if description is not UNSET:
            field_dict["description"] = description
        if size is not UNSET:
            field_dict["size"] = size
        if incoming is not UNSET:
            field_dict["incoming"] = incoming
        if color is not UNSET:
            field_dict["color"] = color
        if warehouse is not UNSET:
            field_dict["warehouse"] = warehouse
        if arriving is not UNSET:
            field_dict["arriving"] = arriving
        if purchase_order_id is not UNSET:
            field_dict["purchase_order_id"] = purchase_order_id
        if available is not UNSET:
            field_dict["available"] = available
        if delivery_date is not UNSET:
            field_dict["deliveryDate"] = delivery_date
        if arrival_date is not UNSET:
            field_dict["arrivalDate"] = arrival_date
        if upc is not UNSET:
            field_dict["upc"] = upc
        if restock_date is not UNSET:
            field_dict["restock_date"] = restock_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        sku = d.pop("sku", UNSET)

        description = d.pop("description", UNSET)

        size = d.pop("size", UNSET)

        incoming = d.pop("incoming", UNSET)

        color = d.pop("color", UNSET)

        warehouse = d.pop("warehouse", UNSET)

        _arriving = d.pop("arriving", UNSET)
        arriving: Union[Unset, datetime.date]
        if isinstance(_arriving, Unset):
            arriving = UNSET
        else:
            arriving = isoparse(_arriving).date()

        purchase_order_id = d.pop("purchase_order_id", UNSET)

        available = d.pop("available", UNSET)

        _delivery_date = d.pop("deliveryDate", UNSET)
        delivery_date: Union[Unset, datetime.date]
        if isinstance(_delivery_date, Unset):
            delivery_date = UNSET
        else:
            delivery_date = isoparse(_delivery_date).date()

        _arrival_date = d.pop("arrivalDate", UNSET)
        arrival_date: Union[Unset, datetime.date]
        if isinstance(_arrival_date, Unset):
            arrival_date = UNSET
        else:
            arrival_date = isoparse(_arrival_date).date()

        upc = d.pop("upc", UNSET)

        _restock_date = d.pop("restock_date", UNSET)
        restock_date: Union[Unset, datetime.date]
        if isinstance(_restock_date, Unset):
            restock_date = UNSET
        else:
            restock_date = isoparse(_restock_date).date()

        inventory_items = cls(
            id=id,
            sku=sku,
            description=description,
            size=size,
            incoming=incoming,
            color=color,
            warehouse=warehouse,
            arriving=arriving,
            purchase_order_id=purchase_order_id,
            available=available,
            delivery_date=delivery_date,
            arrival_date=arrival_date,
            upc=upc,
            restock_date=restock_date,
        )

        inventory_items.additional_properties = d
        return inventory_items

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
