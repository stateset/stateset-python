from dataclasses import dataclass
from typing import Optional


@dataclass
class Customers:
    id: str
    email: Optional[str] = None
    name: Optional[str] = None

