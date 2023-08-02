import datetime
from typing import TYPE_CHECKING, Any, BinaryIO, Dict, List, Optional, TextIO, Tuple, Type, TypeVar, Union, cast

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Warranty")


@define
class Warranty:
    """ 
        Attributes:
            id (Union[Unset, str]):
            warranty_number (Union[Unset, str]):
            warranty_name (Union[Unset, str]):
            warranty_type (Union[Unset, str]):
            created_date (Union[Unset, datetime.datetime]):
            expiration_date (Union[Unset, datetime.datetime]):
            order_id (Union[Unset, str]):
            description (Union[Unset, str]):
            status (Union[Unset, str]):
            issue (Union[Unset, str]):
            tracking_number (Union[Unset, str]):
            action_needed (Union[Unset, str]):
            customer_email (Union[Unset, str]):
            rma (Union[Unset, str]):
            zendesk_number (Union[Unset, str]):
            entered_by (Union[Unset, str]):
            order_date (Union[Unset, datetime.datetime]):
            shipped_date (Union[Unset, datetime.datetime]):
            requested_date (Union[Unset, datetime.datetime]):
            condition (Union[Unset, str]):
            reported_condition (Union[Unset, str]):
            amount (Union[Unset, str]):
            tax_refunded (Union[Unset, str]):
            total_refunded (Union[Unset, str]):
            created_date (Union[Unset, datetime.datetime]):
            serial_number (Union[Unset, str]):
            reason_category (Union[Unset, str]):
     """

    id: Union[Unset, str] = UNSET
    warranty_number: Union[Unset, str] = UNSET
    warranty_name: Union[Unset, str] = UNSET
    warranty_type: Union[Unset, str] = UNSET
    created_date: Union[Unset, datetime.datetime] = UNSET
    expiration_date: Union[Unset, datetime.datetime] = UNSET
    order_id: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    issue: Union[Unset, str] = UNSET
    tracking_number: Union[Unset, str] = UNSET
    action_needed: Union[Unset, str] = UNSET
    customer_email: Union[Unset, str] = UNSET
    rma: Union[Unset, str] = UNSET
    zendesk_number: Union[Unset, str] = UNSET
    entered_by: Union[Unset, str] = UNSET
    order_date: Union[Unset, datetime.datetime] = UNSET
    shipped_date: Union[Unset, datetime.datetime] = UNSET
    requested_date: Union[Unset, datetime.datetime] = UNSET
    condition: Union[Unset, str] = UNSET
    reported_condition: Union[Unset, str] = UNSET
    amount: Union[Unset, str] = UNSET
    tax_refunded: Union[Unset, str] = UNSET
    total_refunded: Union[Unset, str] = UNSET
    created_date: Union[Unset, datetime.datetime] = UNSET
    serial_number: Union[Unset, str] = UNSET
    reason_category: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        warranty_number = self.warranty_number
        warranty_name = self.warranty_name
        warranty_type = self.warranty_type
        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        expiration_date: Union[Unset, str] = UNSET
        if not isinstance(self.expiration_date, Unset):
            expiration_date = self.expiration_date.isoformat()

        order_id = self.order_id
        description = self.description
        status = self.status
        issue = self.issue
        tracking_number = self.tracking_number
        action_needed = self.action_needed
        customer_email = self.customer_email
        rma = self.rma
        zendesk_number = self.zendesk_number
        entered_by = self.entered_by
        order_date: Union[Unset, str] = UNSET
        if not isinstance(self.order_date, Unset):
            order_date = self.order_date.isoformat()

        shipped_date: Union[Unset, str] = UNSET
        if not isinstance(self.shipped_date, Unset):
            shipped_date = self.shipped_date.isoformat()

        requested_date: Union[Unset, str] = UNSET
        if not isinstance(self.requested_date, Unset):
            requested_date = self.requested_date.isoformat()

        condition = self.condition
        reported_condition = self.reported_condition
        amount = self.amount
        tax_refunded = self.tax_refunded
        total_refunded = self.total_refunded
        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        serial_number = self.serial_number
        reason_category = self.reason_category

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if warranty_number is not UNSET:
            field_dict["warrantyNumber"] = warranty_number
        if warranty_name is not UNSET:
            field_dict["warrantyName"] = warranty_name
        if warranty_type is not UNSET:
            field_dict["warrantyType"] = warranty_type
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if expiration_date is not UNSET:
            field_dict["expirationDate"] = expiration_date
        if order_id is not UNSET:
            field_dict["order_id"] = order_id
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if issue is not UNSET:
            field_dict["issue"] = issue
        if tracking_number is not UNSET:
            field_dict["tracking_number"] = tracking_number
        if action_needed is not UNSET:
            field_dict["action_needed"] = action_needed
        if customer_email is not UNSET:
            field_dict["customerEmail"] = customer_email
        if rma is not UNSET:
            field_dict["rma"] = rma
        if zendesk_number is not UNSET:
            field_dict["zendesk_number"] = zendesk_number
        if entered_by is not UNSET:
            field_dict["enteredBy"] = entered_by
        if order_date is not UNSET:
            field_dict["order_date"] = order_date
        if shipped_date is not UNSET:
            field_dict["shipped_date"] = shipped_date
        if requested_date is not UNSET:
            field_dict["requested_date"] = requested_date
        if condition is not UNSET:
            field_dict["condition"] = condition
        if reported_condition is not UNSET:
            field_dict["reported_condition"] = reported_condition
        if amount is not UNSET:
            field_dict["amount"] = amount
        if tax_refunded is not UNSET:
            field_dict["tax_refunded"] = tax_refunded
        if total_refunded is not UNSET:
            field_dict["total_refunded"] = total_refunded
        if created_date is not UNSET:
            field_dict["created_date"] = created_date
        if serial_number is not UNSET:
            field_dict["serial_number"] = serial_number
        if reason_category is not UNSET:
            field_dict["reason_category"] = reason_category

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        warranty_number = d.pop("warrantyNumber", UNSET)

        warranty_name = d.pop("warrantyName", UNSET)

        warranty_type = d.pop("warrantyType", UNSET)

        _created_date = d.pop("createdDate", UNSET)
        created_date: Union[Unset, datetime.datetime]
        if isinstance(_created_date,  Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date)




        _expiration_date = d.pop("expirationDate", UNSET)
        expiration_date: Union[Unset, datetime.datetime]
        if isinstance(_expiration_date,  Unset):
            expiration_date = UNSET
        else:
            expiration_date = isoparse(_expiration_date)




        order_id = d.pop("order_id", UNSET)

        description = d.pop("description", UNSET)

        status = d.pop("status", UNSET)

        issue = d.pop("issue", UNSET)

        tracking_number = d.pop("tracking_number", UNSET)

        action_needed = d.pop("action_needed", UNSET)

        customer_email = d.pop("customerEmail", UNSET)

        rma = d.pop("rma", UNSET)

        zendesk_number = d.pop("zendesk_number", UNSET)

        entered_by = d.pop("enteredBy", UNSET)

        _order_date = d.pop("order_date", UNSET)
        order_date: Union[Unset, datetime.datetime]
        if isinstance(_order_date,  Unset):
            order_date = UNSET
        else:
            order_date = isoparse(_order_date)




        _shipped_date = d.pop("shipped_date", UNSET)
        shipped_date: Union[Unset, datetime.datetime]
        if isinstance(_shipped_date,  Unset):
            shipped_date = UNSET
        else:
            shipped_date = isoparse(_shipped_date)




        _requested_date = d.pop("requested_date", UNSET)
        requested_date: Union[Unset, datetime.datetime]
        if isinstance(_requested_date,  Unset):
            requested_date = UNSET
        else:
            requested_date = isoparse(_requested_date)




        condition = d.pop("condition", UNSET)

        reported_condition = d.pop("reported_condition", UNSET)

        amount = d.pop("amount", UNSET)

        tax_refunded = d.pop("tax_refunded", UNSET)

        total_refunded = d.pop("total_refunded", UNSET)

        _created_date = d.pop("created_date", UNSET)
        created_date: Union[Unset, datetime.datetime]
        if isinstance(_created_date,  Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date)




        serial_number = d.pop("serial_number", UNSET)

        reason_category = d.pop("reason_category", UNSET)

        warranty = cls(
            id=id,
            warranty_number=warranty_number,
            warranty_name=warranty_name,
            warranty_type=warranty_type,
            created_date=created_date,
            expiration_date=expiration_date,
            order_id=order_id,
            description=description,
            status=status,
            issue=issue,
            tracking_number=tracking_number,
            action_needed=action_needed,
            customer_email=customer_email,
            rma=rma,
            zendesk_number=zendesk_number,
            entered_by=entered_by,
            order_date=order_date,
            shipped_date=shipped_date,
            requested_date=requested_date,
            condition=condition,
            reported_condition=reported_condition,
            amount=amount,
            tax_refunded=tax_refunded,
            total_refunded=total_refunded,
            created_date=created_date,
            serial_number=serial_number,
            reason_category=reason_category,
        )

        warranty.additional_properties = d
        return warranty

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
