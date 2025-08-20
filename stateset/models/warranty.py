from dataclasses import dataclass
from typing import Optional


@dataclass
class Warranty:
    id: str
    product_id: str
    customer_id: str
    status: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    created: Optional[str] = None
    updated: Optional[str] = None

