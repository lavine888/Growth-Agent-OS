from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .adapters import EventAdapter, MappingAdapter


def ingest_payload(payload: dict[str, Any], output: str | Path, adapter: EventAdapter | None = None) -> int:
    adapter = adapter or MappingAdapter()
    events = list(adapter.normalize(payload))
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as handle:
        for event in events:
            row = {
                "actor_id": event.actor_id,
                "event": event.event,
                "timestamp": event.timestamp.isoformat() if event.timestamp else None,
                "source": event.source,
                "properties": event.properties,
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(events)
