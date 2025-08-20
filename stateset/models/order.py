from dataclasses import dataclass
from typing import List, Optional


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: float


@dataclass
class Order:
    id: str
    customer_id: str
    status: str
    total_amount: float
    items: List[OrderItem]
    created: Optional[str] = None
    updated: Optional[str] = None

