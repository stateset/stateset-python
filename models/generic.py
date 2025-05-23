from typing import Any, Dict
from attrs import define, field

@define
class GenericModel:
    """Fallback model for resources without a specific schema."""

    additional_properties: Dict[str, Any] = field(init=False, factory=dict)

    def __init__(self, **kwargs: Any) -> None:
        self.additional_properties = dict(kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.additional_properties)

    @classmethod
    def from_dict(cls, src: Dict[str, Any]) -> "GenericModel":
        return cls(**src)
