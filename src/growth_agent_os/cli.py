from __future__ import annotations

import argparse
import json
from pathlib import Path

from .orchestrator import GrowthOS


def _print_report(payload: dict[str, object]) -> None:
    print(f"Actors: {payload['total_actors']}")
    print("\nFunnel")
    print("-" * 68)
    for row in payload["steps"]:
        conversion = row["conversion_from_previous"]
        conversion_text = "start" if conversion is None else f"{conversion * 100:6.1f}%"
        drop = row["drop_from_previous"]
        drop_text = "-" if drop is None else str(drop)
        print(f"{row['step']:<28} {row['actors']:>5}  conv {conversion_text:>7}  drop {drop_text:>4}")
    print("-" * 68)
    print(f"Bottleneck: {payload['bottleneck']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="growth-os", description="Growth Agent OS local control plane")
    parser.add_argument("--root", type=Path, default=None, help="Repository/config root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    agents = subparsers.add_parser("agents", help="List configured agents")
    agents.add_argument("--json", action="store_true", dest="as_json")

    report = subparsers.add_parser("report", help="Calculate the ordered growth funnel")
    report.add_argument("events", type=Path)
    report.add_argument("--json", action="store_true", dest="as_json")

    plan = subparsers.add_parser("plan", help="Identify the current bottleneck and owner")
    plan.add_argument("events", type=Path)
    plan.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    os = GrowthOS(root=args.root)

    if args.command == "agents":
        if args.as_json:
            print(json.dumps(os.agents, ensure_ascii=False, indent=2))
        else:
            for agent in os.agents:
                print(f"{agent['id']:<18} {agent['mission']}")
        return 0

    if args.command == "report":
        payload = os.report(args.events)
        if args.as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            _print_report(payload)
        return 0

    if args.command == "plan":
        payload = os.plan(args.events)
        if args.as_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"Owner: {payload['owner']}")
            print(f"Status: {payload['status']}")
            print(f"Next: {payload['next_action']}")
            if payload.get("approval_policy"):
                print(f"Guardrail: {payload['approval_policy']}")
        return 0

    return 2
