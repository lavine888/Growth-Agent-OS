from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ExperimentStatus(str, Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Experiment:
    id: str
    name: str
    hypothesis: str
    primary_metric: str
    owner: str
    status: ExperimentStatus = ExperimentStatus.DRAFT
    target: float | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def start(self) -> None:
        if self.status not in {ExperimentStatus.DRAFT, ExperimentStatus.PAUSED}:
            raise ValueError(f"cannot start experiment from {self.status.value}")
        self.status = ExperimentStatus.RUNNING
        self.started_at = self.started_at or datetime.now(timezone.utc)

    def pause(self) -> None:
        if self.status is not ExperimentStatus.RUNNING:
            raise ValueError("only running experiments can be paused")
        self.status = ExperimentStatus.PAUSED

    def complete(self) -> None:
        if self.status not in {ExperimentStatus.RUNNING, ExperimentStatus.PAUSED}:
            raise ValueError("only active experiments can be completed")
        self.status = ExperimentStatus.COMPLETED
        self.ended_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "hypothesis": self.hypothesis,
            "primary_metric": self.primary_metric,
            "owner": self.owner,
            "status": self.status.value,
            "target": self.target,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "metadata": self.metadata,
        }
