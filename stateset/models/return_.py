from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ReturnItem:
    product_id: str
    quantity: int
    reason: Optional[str] = None


@dataclass
class Return:
    id: str
    order_id: str
    status: str
    items: List[ReturnItem]
    created: Optional[str] = None
    updated: Optional[str] = None

