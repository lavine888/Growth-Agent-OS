import unittest

from growth_agent_os.models import BusinessContext, WorkStatus
from growth_agent_os.orchestrator import GrowthOrchestrator


class GrowthOrchestratorTest(unittest.TestCase):
    def test_plan_builds_measurable_cycle(self) -> None:
        context = BusinessContext(
            name="Test",
            product="Product",
            goal="Get 10 qualified leads",
            icp="A narrow ICP",
            channels=["community"],
            metrics=["qualified_leads"],
        )

        plan = GrowthOrchestrator().build_plan(context)

        self.assertEqual(plan.experiments[0].primary_metric, "qualified_leads")
        self.assertEqual(len(plan.work_items), 5)
        self.assertTrue(any(item.requires_approval for item in plan.work_items))
        self.assertTrue(
            any(item.status == WorkStatus.BLOCKED_FOR_APPROVAL for item in plan.work_items)
        )


if __name__ == "__main__":
    unittest.main()
