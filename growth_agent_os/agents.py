"""Agent role definitions and deterministic v0.1 planning behavior."""

from __future__ import annotations

from dataclasses import dataclass

from .models import AgentRole, BusinessContext, WorkItem, WorkStatus


@dataclass(frozen=True, slots=True)
class AgentSpec:
    role: AgentRole
    mission: str
    outputs: tuple[str, ...]


AGENT_SPECS: dict[AgentRole, AgentSpec] = {
    AgentRole.GROWTH_MANAGER: AgentSpec(
        AgentRole.GROWTH_MANAGER,
        "Own the growth goal, prioritize experiments, and coordinate handoffs.",
        ("prioritized plan", "decision log", "next experiment"),
    ),
    AgentRole.RESEARCHER: AgentSpec(
        AgentRole.RESEARCHER,
        "Turn market, ICP, competitor, and channel evidence into usable context.",
        ("research brief", "ICP evidence", "channel opportunities"),
    ),
    AgentRole.CONTENT_STRATEGIST: AgentSpec(
        AgentRole.CONTENT_STRATEGIST,
        "Translate growth hypotheses into campaign angles and content systems.",
        ("campaign thesis", "content pillars", "channel plan"),
    ),
    AgentRole.CONTENT_PRODUCER: AgentSpec(
        AgentRole.CONTENT_PRODUCER,
        "Create channel-specific assets from an approved strategy.",
        ("drafts", "creative briefs", "asset variants"),
    ),
    AgentRole.ACQUISITION: AgentSpec(
        AgentRole.ACQUISITION,
        "Execute distribution and lead-generation workflows with explicit approval gates.",
        ("lead list", "distribution plan", "outreach queue"),
    ),
    AgentRole.ANALYST: AgentSpec(
        AgentRole.ANALYST,
        "Evaluate experiments against metrics and feed learning into the next cycle.",
        ("experiment readout", "metric deltas", "recommendation"),
    ),
}


_EXTERNAL_ACTION_KEYWORDS = ("publish", "send", "outreach", "spend", "launch", "post")


def requires_human_approval(title: str, objective: str) -> bool:
    text = f"{title} {objective}".lower()
    return any(keyword in text for keyword in _EXTERNAL_ACTION_KEYWORDS)


def make_work_item(
    item_id: str,
    owner: AgentRole,
    title: str,
    objective: str,
    inputs: list[str],
    expected_output: str,
) -> WorkItem:
    approval = requires_human_approval(title, objective)
    return WorkItem(
        id=item_id,
        owner=owner,
        title=title,
        objective=objective,
        inputs=inputs,
        expected_output=expected_output,
        requires_approval=approval,
        status=WorkStatus.BLOCKED_FOR_APPROVAL if approval else WorkStatus.READY,
    )


def build_default_work_items(context: BusinessContext) -> list[WorkItem]:
    channels = ", ".join(context.channels) if context.channels else "candidate channels"
    return [
        make_work_item(
            "research-001",
            AgentRole.RESEARCHER,
            "Build evidence-backed growth brief",
            f"Validate the ICP, pains, competitors, and opportunities for {context.product}.",
            ["business context", "existing customer evidence", "public market evidence"],
            "A structured research brief with claims, evidence, and unknowns.",
        ),
        make_work_item(
            "strategy-001",
            AgentRole.CONTENT_STRATEGIST,
            "Design first campaign hypothesis",
            f"Choose a message-market-channel hypothesis across {channels}.",
            ["research-001", "goal", "constraints"],
            "One campaign thesis, three angles, and a channel-specific content plan.",
        ),
        make_work_item(
            "content-001",
            AgentRole.CONTENT_PRODUCER,
            "Produce campaign asset drafts",
            "Create draft assets for the selected campaign without publishing them.",
            ["strategy-001", "brand context"],
            "Draft asset variants mapped to channel and audience intent.",
        ),
        make_work_item(
            "acquisition-001",
            AgentRole.ACQUISITION,
            "Prepare outreach and distribution queue",
            "Prepare qualified leads and distribution actions; sending requires human approval.",
            ["research-001", "strategy-001", "content-001"],
            "A ranked lead/distribution queue with rationale and proposed actions.",
        ),
        make_work_item(
            "analysis-001",
            AgentRole.ANALYST,
            "Define experiment measurement plan",
            "Specify baseline, event tracking, primary metric, and evaluation window.",
            ["goal", "strategy-001"],
            "A measurement contract that can be evaluated after execution.",
        ),
    ]
