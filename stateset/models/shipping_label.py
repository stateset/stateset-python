from dataclasses import dataclass
from typing import Optional


@dataclass
class ShippingLabel:
    id: str
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    label_url: Optional[str] = None

