from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from .models import Event, FunnelReport, FunnelStepResult


def load_events(path: str | Path) -> list[Event]:
    events: list[Event] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
                events.append(Event.from_dict(payload))
            except (json.JSONDecodeError, ValueError) as exc:
                raise ValueError(f"invalid event at line {line_number}: {exc}") from exc
    return events


def ordered_funnel_report(events: Iterable[Event], steps: list[str]) -> FunnelReport:
    if not steps:
        raise ValueError("funnel must contain at least one step")
    if len(set(steps)) != len(steps):
        raise ValueError("funnel steps must be unique")

    events_by_actor: dict[str, list[Event]] = defaultdict(list)
    actor_order: list[str] = []
    seen_actors: set[str] = set()

    for event in events:
        events_by_actor[event.actor_id].append(event)
        if event.actor_id not in seen_actors:
            seen_actors.add(event.actor_id)
            actor_order.append(event.actor_id)

    progress: dict[str, int] = {}
    for actor_id in actor_order:
        next_step = 0
        for event in events_by_actor[actor_id]:
            if next_step >= len(steps):
                break
            if event.event == steps[next_step]:
                next_step += 1
        progress[actor_id] = next_step

    results: list[FunnelStepResult] = []
    previous_count: int | None = None
    for index, step in enumerate(steps, start=1):
        count = sum(1 for reached in progress.values() if reached >= index)
        if previous_count is None:
            conversion = None
            drop = None
        else:
            conversion = (count / previous_count) if previous_count else 0.0
            drop = previous_count - count
        results.append(
            FunnelStepResult(
                step=step,
                actors=count,
                conversion_from_previous=conversion,
                drop_from_previous=drop,
            )
        )
        previous_count = count

    return FunnelReport(total_actors=len(progress), steps=tuple(results))


def report_to_dict(report: FunnelReport) -> dict[str, object]:
    bottleneck = report.biggest_drop_step
    return {
        "total_actors": report.total_actors,
        "steps": [
            {
                "step": step.step,
                "actors": step.actors,
                "conversion_from_previous": (
                    round(step.conversion_from_previous, 4)
                    if step.conversion_from_previous is not None
                    else None
                ),
                "drop_from_previous": step.drop_from_previous,
            }
            for step in report.steps
        ],
        "bottleneck": bottleneck.step if bottleneck else None,
    }
