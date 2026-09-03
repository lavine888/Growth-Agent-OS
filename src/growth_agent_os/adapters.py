from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from .models import Event


class EventAdapter(ABC):
    """Boundary for converting external product/CRM/channel data into canonical events."""

    @abstractmethod
    def normalize(self, payload: dict[str, Any]) -> Iterable[Event]:
        raise NotImplementedError


@dataclass(frozen=True)
class MappingAdapter(EventAdapter):
    actor_field: str = "actor_id"
    event_field: str = "event"
    source: str | None = None

    def normalize(self, payload: dict[str, Any]) -> Iterable[Event]:
        mapped = dict(payload)
        if self.actor_field != "actor_id":
            mapped["actor_id"] = payload.get(self.actor_field)
        if self.event_field != "event":
            mapped["event"] = payload.get(self.event_field)
        if self.source is not None:
            mapped["source"] = self.source
        yield Event.from_dict(mapped)
