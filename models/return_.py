from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="Return")


@define
class Return:
    """
    Attributes:
        id (Union[Unset, str]):
        status (Union[Unset, str]): The status of the return.
        order_id (Union[Unset, str]): The order ID associated with the return.
        rma (Union[Unset, str]): The return merchandise authorization number.
        tracking_number (Union[Unset, str]): The tracking number of the returned item.
        description (Union[Unset, str]): A description of the return.
        customer_email (Union[Unset, str]): The email address of the customer who initiated the return.
        zendesk_number (Union[Unset, str]): The unique identifier of the Zendesk ticket associated with the return.
        action_needed (Union[Unset, str]): Any action required to process the return.
        issue (Union[Unset, str]): The reason for the return.
        order_string (Union[Unset, str]): The string the order was placed.
        shipped_string (Union[Unset, str]): The string the order was shipped.
        requested_string (Union[Unset, str]): The string the return was requested.
        entered_by (Union[Unset, str]): The name of the employee who entered the return into the system.
        customer_id (Union[Unset, str]): The unique identifier of the customer who initiated the return.
        amount (Union[Unset, str]): The amount of the return.
        reported_condition (Union[Unset, str]): The condition of the returned item.
        tax_refunded (Union[Unset, str]): The amount of tax refunded.
        total_refunded (Union[Unset, str]): The total amount refunded.
        created_string (Union[Unset, str]): The string the return was created. Default: 'now()'.
        reason_category (Union[Unset, str]): The category of the reason for the return.
        flat_rate_shipping (Union[Unset, int]): The flat rate shipping amount.
        refunded_string (Union[Unset, str]): The string the return was refunded.
        warehouse_received_string (Union[Unset, str]): The string the return was received at the warehouse.
        warehouse_condition_string (Union[Unset, str]): The string the condition of the return was verified at the
            warehouse.
        fedex_status (Union[Unset, str]): The status of the return in FedEx.
        scanned_serial_number (Union[Unset, str]): The serial number of the returned item.
        match (Union[Unset, str]): Whether or not the serial number matches the order.
        country (Union[Unset, str]): The country of the customer who initiated the return.
        serial_number (Union[Unset, str]): The serial number of the returned item.
        condition (Union[Unset, str]): The condition of the returned item.
        order_refunded (Union[Unset, bool]): Whether or not the order was refunded.
        workflow_id (Union[Unset, str]): The workflow ID associated with the return.
        sso_id (Union[Unset, str]): The unique identifier of the SSO user who initiated the return.
        customer_email_normalized (Union[Unset, str]): The normalized email address of the customer who initiated the
            return.
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
    order_string: Union[Unset, str] = UNSET
    shipped_string: Union[Unset, str] = UNSET
    requested_string: Union[Unset, str] = UNSET
    entered_by: Union[Unset, str] = UNSET
    customer_id: Union[Unset, str] = UNSET
    amount: Union[Unset, str] = UNSET
    reported_condition: Union[Unset, str] = UNSET
    tax_refunded: Union[Unset, str] = UNSET
    total_refunded: Union[Unset, str] = UNSET
    created_string: Union[Unset, str] = "now()"
    reason_category: Union[Unset, str] = UNSET
    flat_rate_shipping: Union[Unset, int] = UNSET
    refunded_string: Union[Unset, str] = UNSET
    warehouse_received_string: Union[Unset, str] = UNSET
    warehouse_condition_string: Union[Unset, str] = UNSET
    fedex_status: Union[Unset, str] = UNSET
    scanned_serial_number: Union[Unset, str] = UNSET
    match: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    condition: Union[Unset, str] = UNSET
    order_refunded: Union[Unset, bool] = False
    workflow_id: Union[Unset, str] = UNSET
    sso_id: Union[Unset, str] = UNSET
    customer_email_normalized: Union[Unset, str] = UNSET
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
        order_string = self.order_string
        shipped_string = self.shipped_string
        requested_string = self.requested_string
        entered_by = self.entered_by
        customer_id = self.customer_id
        amount = self.amount
        reported_condition = self.reported_condition
        tax_refunded = self.tax_refunded
        total_refunded = self.total_refunded
        created_string = self.created_string
        reason_category = self.reason_category
        flat_rate_shipping = self.flat_rate_shipping
        refunded_string = self.refunded_string
        warehouse_received_string = self.warehouse_received_string
        warehouse_condition_string = self.warehouse_condition_string
        fedex_status = self.fedex_status
        scanned_serial_number = self.scanned_serial_number
        match = self.match
        country = self.country
        serial_number = self.serial_number
        condition = self.condition
        order_refunded = self.order_refunded
        workflow_id = self.workflow_id
        sso_id = self.sso_id
        customer_email_normalized = self.customer_email_normalized

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
            field_dict["customer_email"] = customer_email
        if zendesk_number is not UNSET:
            field_dict["zendesk_number"] = zendesk_number
        if action_needed is not UNSET:
            field_dict["action_needed"] = action_needed
        if issue is not UNSET:
            field_dict["issue"] = issue
        if order_string is not UNSET:
            field_dict["order_string"] = order_string
        if shipped_string is not UNSET:
            field_dict["shipped_string"] = shipped_string
        if requested_string is not UNSET:
            field_dict["requested_string"] = requested_string
        if entered_by is not UNSET:
            field_dict["enteredBy"] = entered_by
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
        if created_string is not UNSET:
            field_dict["created_string"] = created_string
        if reason_category is not UNSET:
            field_dict["reason_category"] = reason_category
        if flat_rate_shipping is not UNSET:
            field_dict["flat_rate_shipping"] = flat_rate_shipping
        if refunded_string is not UNSET:
            field_dict["refunded_string"] = refunded_string
        if warehouse_received_string is not UNSET:
            field_dict["warehouse_received_string"] = warehouse_received_string
        if warehouse_condition_string is not UNSET:
            field_dict["warehouse_condition_string"] = warehouse_condition_string
        if fedex_status is not UNSET:
            field_dict["fedex_status"] = fedex_status
        if scanned_serial_number is not UNSET:
            field_dict["scanned_serial_number"] = scanned_serial_number
        if match is not UNSET:
            field_dict["match"] = match
        if country is not UNSET:
            field_dict["country"] = country
        if serial_number is not UNSET:
            field_dict["serial_number"] = serial_number
        if condition is not UNSET:
            field_dict["condition"] = condition
        if order_refunded is not UNSET:
            field_dict["order_refunded"] = order_refunded
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id
        if sso_id is not UNSET:
            field_dict["sso_id"] = sso_id
        if customer_email_normalized is not UNSET:
            field_dict["customer_email_normalized"] = customer_email_normalized

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

        customer_email = d.pop("customer_email", UNSET)

        zendesk_number = d.pop("zendesk_number", UNSET)

        action_needed = d.pop("action_needed", UNSET)

        issue = d.pop("issue", UNSET)

        order_string = d.pop("order_string", UNSET)

        shipped_string = d.pop("shipped_string", UNSET)

        requested_string = d.pop("requested_string", UNSET)

        entered_by = d.pop("enteredBy", UNSET)

        customer_id = d.pop("customer_id", UNSET)

        amount = d.pop("amount", UNSET)

        reported_condition = d.pop("reported_condition", UNSET)

        tax_refunded = d.pop("tax_refunded", UNSET)

        total_refunded = d.pop("total_refunded", UNSET)

        created_string = d.pop("created_string", UNSET)

        reason_category = d.pop("reason_category", UNSET)

        flat_rate_shipping = d.pop("flat_rate_shipping", UNSET)

        refunded_string = d.pop("refunded_string", UNSET)

        warehouse_received_string = d.pop("warehouse_received_string", UNSET)

        warehouse_condition_string = d.pop("warehouse_condition_string", UNSET)

        fedex_status = d.pop("fedex_status", UNSET)

        scanned_serial_number = d.pop("scanned_serial_number", UNSET)

        match = d.pop("match", UNSET)

        country = d.pop("country", UNSET)

        serial_number = d.pop("serial_number", UNSET)

        condition = d.pop("condition", UNSET)

        order_refunded = d.pop("order_refunded", UNSET)

        workflow_id = d.pop("workflow_id", UNSET)

        sso_id = d.pop("sso_id", UNSET)

        customer_email_normalized = d.pop("customer_email_normalized", UNSET)

        return_ = cls(
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
            order_string=order_string,
            shipped_string=shipped_string,
            requested_string=requested_string,
            entered_by=entered_by,
            customer_id=customer_id,
            amount=amount,
            reported_condition=reported_condition,
            tax_refunded=tax_refunded,
            total_refunded=total_refunded,
            created_string=created_string,
            reason_category=reason_category,
            flat_rate_shipping=flat_rate_shipping,
            refunded_string=refunded_string,
            warehouse_received_string=warehouse_received_string,
            warehouse_condition_string=warehouse_condition_string,
            fedex_status=fedex_status,
            scanned_serial_number=scanned_serial_number,
            match=match,
            country=country,
            serial_number=serial_number,
            condition=condition,
            order_refunded=order_refunded,
            workflow_id=workflow_id,
            sso_id=sso_id,
            customer_email_normalized=customer_email_normalized,
        )

        return_.additional_properties = d
        return return_

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
