"""Command-line interface for Growth Agent OS."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import BusinessContext
from .orchestrator import GrowthOrchestrator


def load_context(path: Path) -> BusinessContext:
    data = json.loads(path.read_text(encoding="utf-8"))
    return BusinessContext(**data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Growth Agent OS plan")
    parser.add_argument("config", type=Path, help="Path to a business context JSON file")
    parser.add_argument("--out", type=Path, help="Optional path to write the generated plan")
    args = parser.parse_args()

    plan = GrowthOrchestrator().build_plan(load_context(args.config))
    rendered = json.dumps(plan.to_dict(), indent=2, ensure_ascii=False)

    if args.out:
        args.out.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
