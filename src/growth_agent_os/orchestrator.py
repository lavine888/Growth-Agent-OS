from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .metrics import load_events, ordered_funnel_report, report_to_dict


class GrowthOS:
    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else Path(__file__).resolve().parents[2]
        self.agent_config = self._load_json("config/agents.json")
        self.funnel_config = self._load_json("config/funnel.json")

    def _load_json(self, relative_path: str) -> dict[str, Any]:
        with (self.root / relative_path).open("r", encoding="utf-8") as handle:
            return json.load(handle)

    @property
    def agents(self) -> list[dict[str, Any]]:
        return list(self.agent_config["agents"])

    def report(self, event_path: str | Path) -> dict[str, object]:
        events = load_events(event_path)
        steps = list(self.funnel_config["steps"])
        return report_to_dict(ordered_funnel_report(events, steps))

    def plan(self, event_path: str | Path) -> dict[str, object]:
        report = self.report(event_path)
        bottleneck = report.get("bottleneck")
        if not bottleneck:
            return {
                "status": "insufficient_data",
                "owner": "analyst",
                "next_action": "Collect enough ordered funnel events to identify a bottleneck.",
                "report": report,
            }

        owners = self.funnel_config.get("owners", {})
        owner = owners.get(str(bottleneck), "growth_director")
        step_rows = report["steps"]
        row = next(item for item in step_rows if item["step"] == bottleneck)
        conversion = row["conversion_from_previous"]
        conversion_text = f"{conversion * 100:.1f}%" if isinstance(conversion, float) else "unknown"

        return {
            "status": "action_required",
            "owner": owner,
            "bottleneck": bottleneck,
            "next_action": (
                f"Investigate the transition into '{bottleneck}' first; observed conversion from the "
                f"previous step is {conversion_text}. Create one falsifiable experiment before increasing traffic."
            ),
            "approval_policy": (
                "Analysis and drafting may run automatically. Publishing, outreach, spend, pricing, and "
                "external mutations require human approval."
            ),
            "report": report,
        }
