"""Core data models for Growth Agent OS."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class AgentRole(StrEnum):
    GROWTH_MANAGER = "growth_manager"
    RESEARCHER = "researcher"
    CONTENT_STRATEGIST = "content_strategist"
    CONTENT_PRODUCER = "content_producer"
    ACQUISITION = "acquisition"
    ANALYST = "analyst"


class WorkStatus(StrEnum):
    PLANNED = "planned"
    BLOCKED_FOR_APPROVAL = "blocked_for_approval"
    READY = "ready"
    COMPLETED = "completed"


@dataclass(slots=True)
class BusinessContext:
    name: str
    product: str
    goal: str
    icp: str
    channels: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    metrics: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Experiment:
    name: str
    hypothesis: str
    primary_metric: str
    success_criterion: str
    owner: AgentRole


@dataclass(slots=True)
class WorkItem:
    id: str
    owner: AgentRole
    title: str
    objective: str
    inputs: list[str]
    expected_output: str
    requires_approval: bool = False
    status: WorkStatus = WorkStatus.PLANNED
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class GrowthPlan:
    context: BusinessContext
    experiments: list[Experiment]
    work_items: list[WorkItem]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
