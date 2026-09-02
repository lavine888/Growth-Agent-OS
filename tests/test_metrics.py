import unittest

from growth_agent_os.metrics import ordered_funnel_report
from growth_agent_os.models import Event


class FunnelTests(unittest.TestCase):
    def test_funnel_requires_order(self) -> None:
        steps = ["lead", "trial", "paid"]
        events = [
            Event(actor_id="a", event="lead"),
            Event(actor_id="a", event="trial"),
            Event(actor_id="a", event="paid"),
            Event(actor_id="b", event="paid"),
            Event(actor_id="b", event="lead"),
            Event(actor_id="b", event="trial"),
            Event(actor_id="c", event="lead"),
        ]

        report = ordered_funnel_report(events, steps)
        self.assertEqual([step.actors for step in report.steps], [3, 2, 1])
        self.assertEqual(report.biggest_drop_step.step, "paid")

    def test_duplicate_funnel_steps_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ordered_funnel_report([], ["lead", "lead"])


if __name__ == "__main__":
    unittest.main()
