"""Growth workflow orchestration."""

from __future__ import annotations

from .agents import build_default_work_items
from .models import AgentRole, BusinessContext, Experiment, GrowthPlan


class GrowthOrchestrator:
    """Build a measurable growth cycle from shared business context.

    v0.1 intentionally separates planning from side effects. Tool adapters can be
    added later without changing the core domain model.
    """

    def build_plan(self, context: BusinessContext) -> GrowthPlan:
        primary_metric = context.metrics[0] if context.metrics else "qualified_leads"
        experiment = Experiment(
            name="first-channel-message-fit",
            hypothesis=(
                f"A focused message for {context.icp} distributed through the highest-signal "
                "available channel will produce measurable intent."
            ),
            primary_metric=primary_metric,
            success_criterion=f"Define a numeric target for {primary_metric} before execution.",
            owner=AgentRole.GROWTH_MANAGER,
        )
        return GrowthPlan(
            context=context,
            experiments=[experiment],
            work_items=build_default_work_items(context),
        )
