from typing import Any, Dict, List, Type, TypeVar, Union
from datetime import datetime
from attrs import define, field
from dateutil.parser import isoparse

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="ShippingLabel")


@define
class ShippingLabel:
    """Represents a shipping label created for a shipment."""

    id: Union[Unset, str] = UNSET
    shipment_id: Union[Unset, str] = UNSET
    carrier: Union[Unset, str] = UNSET
    tracking_number: Union[Unset, str] = UNSET
    label_url: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        shipment_id = self.shipment_id
        carrier = self.carrier
        tracking_number = self.tracking_number
        label_url = self.label_url
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if shipment_id is not UNSET:
            field_dict["shipment_id"] = shipment_id
        if carrier is not UNSET:
            field_dict["carrier"] = carrier
        if tracking_number is not UNSET:
            field_dict["tracking_number"] = tracking_number
        if label_url is not UNSET:
            field_dict["label_url"] = label_url
        if created_at is not UNSET:
            field_dict["created_at"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)
        shipment_id = d.pop("shipment_id", UNSET)
        carrier = d.pop("carrier", UNSET)
        tracking_number = d.pop("tracking_number", UNSET)
        label_url = d.pop("label_url", UNSET)
        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        shipping_label = cls(
            id=id,
            shipment_id=shipment_id,
            carrier=carrier,
            tracking_number=tracking_number,
            label_url=label_url,
            created_at=created_at,
        )

        shipping_label.additional_properties = d
        return shipping_label

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
