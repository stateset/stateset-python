import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..stateset_types import UNSET, Unset, OrderStatus

T = TypeVar("T", bound="Order")
TI = TypeVar("TI", bound="OrderItem")


@define
class OrderItem:
    product_id: Union[Unset, str] = UNSET
    quantity: Union[Unset, int] = UNSET
    price: Union[Unset, float] = UNSET
    currency: Union[Unset, str] = UNSET
    metadata: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        product_id = self.product_id
        quantity = self.quantity
        price = self.price
        currency = self.currency

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.metadata)
        if product_id is not UNSET:
            field_dict["product_id"] = product_id
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if price is not UNSET:
            field_dict["price"] = price
        if currency is not UNSET:
            field_dict["currency"] = currency

        return field_dict

    @classmethod
    def from_dict(cls: Type[TI], src_dict: Dict[str, Any]) -> TI:
        d = src_dict.copy()
        product_id = d.pop("product_id", UNSET)
        quantity = d.pop("quantity", UNSET)
        price = d.pop("price", UNSET)
        currency = d.pop("currency", UNSET)

        order_item = cls(
            product_id=product_id,
            quantity=quantity,
            price=price,
            currency=currency,
        )

        order_item.metadata = d
        return order_item


@define
class Order:
    id: Union[Unset, str] = UNSET
    customer_id: Union[Unset, str] = UNSET
    status: Union[Unset, OrderStatus] = UNSET
    items: Union[Unset, List[OrderItem]] = UNSET
    total_amount: Union[Unset, float] = UNSET
    currency: Union[Unset, str] = UNSET
    shipping_address: Union[Unset, Dict[str, str]] = UNSET
    tracking_number: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        customer_id = self.customer_id
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value
        items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = [item.to_dict() for item in self.items]
        total_amount = self.total_amount
        currency = self.currency
        shipping_address = self.shipping_address
        tracking_number = self.tracking_number
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()
        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if customer_id is not UNSET:
            field_dict["customer_id"] = customer_id
        if status is not UNSET:
            field_dict["status"] = status
        if items is not UNSET:
            field_dict["items"] = items
        if total_amount is not UNSET:
            field_dict["total_amount"] = total_amount
        if currency is not UNSET:
            field_dict["currency"] = currency
        if shipping_address is not UNSET:
            field_dict["shipping_address"] = shipping_address
        if tracking_number is not UNSET:
            field_dict["tracking_number"] = tracking_number
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)
        customer_id = d.pop("customer_id", UNSET)
        _status = d.pop("status", UNSET)
        status: Union[Unset, OrderStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = OrderStatus(_status)
        _items = d.pop("items", UNSET)
        items: Union[Unset, List[OrderItem]] = UNSET
        if not isinstance(_items, Unset):
            items = [OrderItem.from_dict(item) for item in _items]
        total_amount = d.pop("total_amount", UNSET)
        currency = d.pop("currency", UNSET)
        shipping_address = d.pop("shipping_address", UNSET)
        tracking_number = d.pop("tracking_number", UNSET)
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

        order = cls(
            id=id,
            customer_id=customer_id,
            status=status,
            items=items,
            total_amount=total_amount,
            currency=currency,
            shipping_address=shipping_address,
            tracking_number=tracking_number,
            created_at=created_at,
            updated_at=updated_at,
        )

        order.additional_properties = d
        return order

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
