from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define, field

from ..stateset_types import UNSET, Unset

T = TypeVar("T", bound="Eval")


@define
class Eval:
    """Represents an evaluation record for an Agent response."""

    id: Union[Unset, str] = UNSET
    agent_id: Union[Unset, str] = UNSET
    score: Union[Unset, float] = UNSET
    feedback: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        agent_id = self.agent_id
        score = self.score
        feedback = self.feedback

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if score is not UNSET:
            field_dict["score"] = score
        if feedback is not UNSET:
            field_dict["feedback"] = feedback

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)
        agent_id = d.pop("agent_id", UNSET)
        score = d.pop("score", UNSET)
        feedback = d.pop("feedback", UNSET)

        eval_ = cls(
            id=id,
            agent_id=agent_id,
            score=score,
            feedback=feedback,
        )

        eval_.additional_properties = d
        return eval_

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
