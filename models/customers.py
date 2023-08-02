import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Customers")


@define
class Customers:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier of the customer.
        sso_id (Union[Unset, str]): The unique identifier of the customer in the SSO system.
        activation_date (Union[Unset, datetime.datetime]): The date and time the customer was activated.
        email (Union[Unset, str]): The email address of the customer.
        first_name (Union[Unset, str]): The first name of the customer.
        last_name (Union[Unset, str]): The last name of the customer.
        phone (Union[Unset, str]): The phone number of the customer.
        stripe_customer_id (Union[Unset, str]): The unique identifier of the customer in the Stripe system.
        timestamp (Union[Unset, datetime.datetime]): The date and time the customer was created.
    """

    id: Union[Unset, str] = UNSET
    sso_id: Union[Unset, str] = UNSET
    activation_date: Union[Unset, datetime.datetime] = UNSET
    email: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    last_name: Union[Unset, str] = UNSET
    phone: Union[Unset, str] = UNSET
    stripe_customer_id: Union[Unset, str] = UNSET
    timestamp: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        sso_id = self.sso_id
        activation_date: Union[Unset, str] = UNSET
        if not isinstance(self.activation_date, Unset):
            activation_date = self.activation_date.isoformat()

        email = self.email
        first_name = self.first_name
        last_name = self.last_name
        phone = self.phone
        stripe_customer_id = self.stripe_customer_id
        timestamp: Union[Unset, str] = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if sso_id is not UNSET:
            field_dict["sso_id"] = sso_id
        if activation_date is not UNSET:
            field_dict["activationDate"] = activation_date
        if email is not UNSET:
            field_dict["email"] = email
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if phone is not UNSET:
            field_dict["phone"] = phone
        if stripe_customer_id is not UNSET:
            field_dict["stripe_customer_id"] = stripe_customer_id
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        sso_id = d.pop("sso_id", UNSET)

        _activation_date = d.pop("activationDate", UNSET)
        activation_date: Union[Unset, datetime.datetime]
        if isinstance(_activation_date, Unset):
            activation_date = UNSET
        else:
            activation_date = isoparse(_activation_date)

        email = d.pop("email", UNSET)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        phone = d.pop("phone", UNSET)

        stripe_customer_id = d.pop("stripe_customer_id", UNSET)

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: Union[Unset, datetime.datetime]
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = isoparse(_timestamp)

        customers = cls(
            id=id,
            sso_id=sso_id,
            activation_date=activation_date,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            stripe_customer_id=stripe_customer_id,
            timestamp=timestamp,
        )

        customers.additional_properties = d
        return customers

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
