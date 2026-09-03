from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class ApprovalRequest:
    id: str
    action: str
    requested_by: str
    payload: dict[str, Any] = field(default_factory=dict)
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    decided_at: datetime | None = None

    def approve(self) -> None:
        if self.status is not ApprovalStatus.PENDING:
            raise ValueError("approval request is already decided")
        self.status = ApprovalStatus.APPROVED
        self.decided_at = datetime.now(timezone.utc)

    def reject(self) -> None:
        if self.status is not ApprovalStatus.PENDING:
            raise ValueError("approval request is already decided")
        self.status = ApprovalStatus.REJECTED
        self.decided_at = datetime.now(timezone.utc)


class ApprovalQueue:
    def __init__(self) -> None:
        self._items: dict[str, ApprovalRequest] = {}

    def submit(self, request: ApprovalRequest) -> None:
        if request.id in self._items:
            raise ValueError(f"duplicate approval id: {request.id}")
        self._items[request.id] = request

    def pending(self) -> list[ApprovalRequest]:
        return [item for item in self._items.values() if item.status is ApprovalStatus.PENDING]

    def get(self, request_id: str) -> ApprovalRequest:
        try:
            return self._items[request_id]
        except KeyError as exc:
            raise KeyError(f"unknown approval id: {request_id}") from exc
