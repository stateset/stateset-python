import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="WarrantyItem")


@define
class WarrantyItem:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier of the warranty
        status (Union[Unset, str]): The status of the warranty
        order_id (Union[Unset, str]): The unique identifier of the order associated with the warranty
        rma (Union[Unset, str]): The warranty merchandise authorization number
        tracking_number (Union[Unset, str]): The tracking number of the warrantyed item
        description (Union[Unset, str]): A description of the warranty
        customer_email (Union[Unset, str]): The email address of the customer who initiated the warranty
        zendesk_number (Union[Unset, str]): The unique identifier of the Zendesk ticket associated with the warranty
        action_needed (Union[Unset, str]): Any action required to process the warranty
        issue (Union[Unset, str]): The reason for the warranty
        order_date (Union[Unset, datetime.date]): The date the order was placed
        shipped_date (Union[Unset, datetime.date]): The date the order was shipped
        requested_date (Union[Unset, datetime.date]): The date the warranty was requested
        entered_by (Union[Unset, str]): The name of the employee who entered the warranty into the system
        serial_number (Union[Unset, str]): The serial number of the warranty item
        condition (Union[Unset, str]): The condition of the warranty item
        customer_id (Union[Unset, str]): The unique identifier of the customer who initiated the warranty
        amount (Union[Unset, str]): The total amount refunded for the warranty
        reported_condition (Union[Unset, str]): The condition of the item reported by the customer
        tax_refunded (Union[Unset, str]): The amount of tax refunded for the warranty
        total_refunded (Union[Unset, str]): The total amount refunded for the warranty, including tax
        created_date (Union[Unset, datetime.date]): The date
    """

    id: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    order_id: Union[Unset, str] = UNSET
    rma: Union[Unset, str] = UNSET
    tracking_number: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    customer_email: Union[Unset, str] = UNSET
    zendesk_number: Union[Unset, str] = UNSET
    action_needed: Union[Unset, str] = UNSET
    issue: Union[Unset, str] = UNSET
    order_date: Union[Unset, datetime.date] = UNSET
    shipped_date: Union[Unset, datetime.date] = UNSET
    requested_date: Union[Unset, datetime.date] = UNSET
    entered_by: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    condition: Union[Unset, str] = UNSET
    customer_id: Union[Unset, str] = UNSET
    amount: Union[Unset, str] = UNSET
    reported_condition: Union[Unset, str] = UNSET
    tax_refunded: Union[Unset, str] = UNSET
    total_refunded: Union[Unset, str] = UNSET
    created_date: Union[Unset, datetime.date] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        status = self.status
        order_id = self.order_id
        rma = self.rma
        tracking_number = self.tracking_number
        description = self.description
        customer_email = self.customer_email
        zendesk_number = self.zendesk_number
        action_needed = self.action_needed
        issue = self.issue
        order_date: Union[Unset, str] = UNSET
        if not isinstance(self.order_date, Unset):
            order_date = self.order_date.isoformat()

        shipped_date: Union[Unset, str] = UNSET
        if not isinstance(self.shipped_date, Unset):
            shipped_date = self.shipped_date.isoformat()

        requested_date: Union[Unset, str] = UNSET
        if not isinstance(self.requested_date, Unset):
            requested_date = self.requested_date.isoformat()

        entered_by = self.entered_by
        serial_number = self.serial_number
        condition = self.condition
        customer_id = self.customer_id
        amount = self.amount
        reported_condition = self.reported_condition
        tax_refunded = self.tax_refunded
        total_refunded = self.total_refunded
        created_date: Union[Unset, str] = UNSET
        if not isinstance(self.created_date, Unset):
            created_date = self.created_date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if order_id is not UNSET:
            field_dict["order_id"] = order_id
        if rma is not UNSET:
            field_dict["rma"] = rma
        if tracking_number is not UNSET:
            field_dict["tracking_number"] = tracking_number
        if description is not UNSET:
            field_dict["description"] = description
        if customer_email is not UNSET:
            field_dict["customerEmail"] = customer_email
        if zendesk_number is not UNSET:
            field_dict["zendesk_number"] = zendesk_number
        if action_needed is not UNSET:
            field_dict["action_needed"] = action_needed
        if issue is not UNSET:
            field_dict["issue"] = issue
        if order_date is not UNSET:
            field_dict["order_date"] = order_date
        if shipped_date is not UNSET:
            field_dict["shipped_date"] = shipped_date
        if requested_date is not UNSET:
            field_dict["requested_date"] = requested_date
        if entered_by is not UNSET:
            field_dict["enteredBy"] = entered_by
        if serial_number is not UNSET:
            field_dict["serial_number"] = serial_number
        if condition is not UNSET:
            field_dict["condition"] = condition
        if customer_id is not UNSET:
            field_dict["customer_id"] = customer_id
        if amount is not UNSET:
            field_dict["amount"] = amount
        if reported_condition is not UNSET:
            field_dict["reported_condition"] = reported_condition
        if tax_refunded is not UNSET:
            field_dict["tax_refunded"] = tax_refunded
        if total_refunded is not UNSET:
            field_dict["total_refunded"] = total_refunded
        if created_date is not UNSET:
            field_dict["created_date"] = created_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        status = d.pop("status", UNSET)

        order_id = d.pop("order_id", UNSET)

        rma = d.pop("rma", UNSET)

        tracking_number = d.pop("tracking_number", UNSET)

        description = d.pop("description", UNSET)

        customer_email = d.pop("customerEmail", UNSET)

        zendesk_number = d.pop("zendesk_number", UNSET)

        action_needed = d.pop("action_needed", UNSET)

        issue = d.pop("issue", UNSET)

        _order_date = d.pop("order_date", UNSET)
        order_date: Union[Unset, datetime.date]
        if isinstance(_order_date, Unset):
            order_date = UNSET
        else:
            order_date = isoparse(_order_date).date()

        _shipped_date = d.pop("shipped_date", UNSET)
        shipped_date: Union[Unset, datetime.date]
        if isinstance(_shipped_date, Unset):
            shipped_date = UNSET
        else:
            shipped_date = isoparse(_shipped_date).date()

        _requested_date = d.pop("requested_date", UNSET)
        requested_date: Union[Unset, datetime.date]
        if isinstance(_requested_date, Unset):
            requested_date = UNSET
        else:
            requested_date = isoparse(_requested_date).date()

        entered_by = d.pop("enteredBy", UNSET)

        serial_number = d.pop("serial_number", UNSET)

        condition = d.pop("condition", UNSET)

        customer_id = d.pop("customer_id", UNSET)

        amount = d.pop("amount", UNSET)

        reported_condition = d.pop("reported_condition", UNSET)

        tax_refunded = d.pop("tax_refunded", UNSET)

        total_refunded = d.pop("total_refunded", UNSET)

        _created_date = d.pop("created_date", UNSET)
        created_date: Union[Unset, datetime.date]
        if isinstance(_created_date, Unset):
            created_date = UNSET
        else:
            created_date = isoparse(_created_date).date()

        warranty_item = cls(
            id=id,
            status=status,
            order_id=order_id,
            rma=rma,
            tracking_number=tracking_number,
            description=description,
            customer_email=customer_email,
            zendesk_number=zendesk_number,
            action_needed=action_needed,
            issue=issue,
            order_date=order_date,
            shipped_date=shipped_date,
            requested_date=requested_date,
            entered_by=entered_by,
            serial_number=serial_number,
            condition=condition,
            customer_id=customer_id,
            amount=amount,
            reported_condition=reported_condition,
            tax_refunded=tax_refunded,
            total_refunded=total_refunded,
            created_date=created_date,
        )

        warranty_item.additional_properties = d
        return warranty_item

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
