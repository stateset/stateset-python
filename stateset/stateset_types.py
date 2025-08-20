from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class UnsetType:
    pass


UNSET = UnsetType()


@dataclass
class StatesetObject:
    id: str


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"


class ReturnStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"


class WarrantyStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    VOID = "void"


@dataclass
class PaginationParams:
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None


@dataclass
class PaginatedList(Generic[T]):
    data: List[T] = field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 0
    total_pages: int = 1
    has_next: bool = False
    has_prev: bool = False

