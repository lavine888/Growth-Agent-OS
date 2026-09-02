from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Event:
    actor_id: str
    event: str
    timestamp: datetime | None = None
    source: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Event":
        actor_id = str(payload.get("actor_id", "")).strip()
        event = str(payload.get("event", "")).strip()
        if not actor_id:
            raise ValueError("event is missing actor_id")
        if not event:
            raise ValueError("event is missing event name")

        raw_timestamp = payload.get("timestamp")
        timestamp = None
        if raw_timestamp:
            value = str(raw_timestamp).replace("Z", "+00:00")
            timestamp = datetime.fromisoformat(value)

        properties = payload.get("properties") or {}
        if not isinstance(properties, dict):
            raise ValueError("properties must be an object")

        source = payload.get("source")
        return cls(
            actor_id=actor_id,
            event=event,
            timestamp=timestamp,
            source=str(source) if source is not None else None,
            properties=properties,
        )


@dataclass(frozen=True)
class FunnelStepResult:
    step: str
    actors: int
    conversion_from_previous: float | None
    drop_from_previous: int | None


@dataclass(frozen=True)
class FunnelReport:
    total_actors: int
    steps: tuple[FunnelStepResult, ...]

    @property
    def biggest_drop_step(self) -> FunnelStepResult | None:
        candidates = [step for step in self.steps[1:] if step.conversion_from_previous is not None]
        if not candidates:
            return None
        return min(candidates, key=lambda step: step.conversion_from_previous or 0.0)
