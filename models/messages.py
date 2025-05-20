import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field
from dateutil.parser import isoparse

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="Messages")


@define
class Messages:
    """
    Attributes:
        id (Union[Unset, str]): The unique identifier for the message
        body (Union[Unset, str]): The body of the message
        to (Union[Unset, str]): The recipient of the message
        from_ (Union[Unset, str]): The sender of the message
        sent_receipt (Union[Unset, bool]): Indicates whether the message has been sent
        delivered_receipt (Union[Unset, bool]): Indicates whether the message has been delivered
        from_me (Union[Unset, bool]): Indicates whether the message is from the user
        user_id (Union[Unset, str]): The ID of the user associated with the message
        username (Union[Unset, str]): The username of the user associated with the message
        is_public (Union[Unset, bool]): Indicates whether the message is public
        created_at (Union[Unset, datetime.datetime]): The creation time of the message
        date (Union[Unset, datetime.date]): The date of the message
        time (Union[Unset, str]): The time of the message
        timestamp (Union[Unset, str]): The timestamp of the message
        message_number (Union[Unset, int]): The message number
        is_code (Union[Unset, bool]): Indicates whether the message is a code
        likes (Union[Unset, int]): The number of likes for the message
    """

    id: Union[Unset, str] = UNSET
    body: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    from_: Union[Unset, str] = UNSET
    sent_receipt: Union[Unset, bool] = UNSET
    delivered_receipt: Union[Unset, bool] = UNSET
    from_me: Union[Unset, bool] = UNSET
    user_id: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    is_public: Union[Unset, bool] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    time: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    message_number: Union[Unset, int] = UNSET
    is_code: Union[Unset, bool] = UNSET
    likes: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        body = self.body
        to = self.to
        from_ = self.from_
        sent_receipt = self.sent_receipt
        delivered_receipt = self.delivered_receipt
        from_me = self.from_me
        user_id = self.user_id
        username = self.username
        is_public = self.is_public
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        time = self.time
        timestamp = self.timestamp
        message_number = self.message_number
        is_code = self.is_code
        likes = self.likes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if body is not UNSET:
            field_dict["body"] = body
        if to is not UNSET:
            field_dict["to"] = to
        if from_ is not UNSET:
            field_dict["from"] = from_
        if sent_receipt is not UNSET:
            field_dict["sentReceipt"] = sent_receipt
        if delivered_receipt is not UNSET:
            field_dict["deliveredReceipt"] = delivered_receipt
        if from_me is not UNSET:
            field_dict["fromMe"] = from_me
        if user_id is not UNSET:
            field_dict["user_id"] = user_id
        if username is not UNSET:
            field_dict["username"] = username
        if is_public is not UNSET:
            field_dict["is_public"] = is_public
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if date is not UNSET:
            field_dict["date"] = date
        if time is not UNSET:
            field_dict["time"] = time
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if message_number is not UNSET:
            field_dict["messageNumber"] = message_number
        if is_code is not UNSET:
            field_dict["isCode"] = is_code
        if likes is not UNSET:
            field_dict["likes"] = likes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        body = d.pop("body", UNSET)

        to = d.pop("to", UNSET)

        from_ = d.pop("from", UNSET)

        sent_receipt = d.pop("sentReceipt", UNSET)

        delivered_receipt = d.pop("deliveredReceipt", UNSET)

        from_me = d.pop("fromMe", UNSET)

        user_id = d.pop("user_id", UNSET)

        username = d.pop("username", UNSET)

        is_public = d.pop("is_public", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        time = d.pop("time", UNSET)

        timestamp = d.pop("timestamp", UNSET)

        message_number = d.pop("messageNumber", UNSET)

        is_code = d.pop("isCode", UNSET)

        likes = d.pop("likes", UNSET)

        messages = cls(
            id=id,
            body=body,
            to=to,
            from_=from_,
            sent_receipt=sent_receipt,
            delivered_receipt=delivered_receipt,
            from_me=from_me,
            user_id=user_id,
            username=username,
            is_public=is_public,
            created_at=created_at,
            date=date,
            time=time,
            timestamp=timestamp,
            message_number=message_number,
            is_code=is_code,
            likes=likes,
        )

        messages.additional_properties = d
        return messages

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
