import json
import tempfile
import unittest
from pathlib import Path

from growth_agent_os.approvals import ApprovalQueue, ApprovalRequest, ApprovalStatus
from growth_agent_os.experiments import Experiment, ExperimentStatus
from growth_agent_os.ingestion import ingest_payload
from growth_agent_os.metrics import load_events


class V03Tests(unittest.TestCase):
    def test_experiment_lifecycle(self) -> None:
        experiment = Experiment(
            id="exp-1",
            name="Demo creative",
            hypothesis="Real classroom demos improve trial conversion",
            primary_metric="trial_booked_rate",
            owner="growth_director",
        )
        experiment.start()
        self.assertEqual(experiment.status, ExperimentStatus.RUNNING)
        experiment.complete()
        self.assertEqual(experiment.status, ExperimentStatus.COMPLETED)
        self.assertIsNotNone(experiment.started_at)
        self.assertIsNotNone(experiment.ended_at)

    def test_approval_queue(self) -> None:
        queue = ApprovalQueue()
        request = ApprovalRequest(id="approval-1", action="publish", requested_by="content_agent")
        queue.submit(request)
        self.assertEqual(len(queue.pending()), 1)
        request.approve()
        self.assertEqual(request.status, ApprovalStatus.APPROVED)
        self.assertEqual(queue.pending(), [])

    def test_ingest_payload_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "events.jsonl"
            count = ingest_payload(
                {
                    "actor_id": "family-1",
                    "event": "trial_booked",
                    "source": "landing_page",
                    "properties": {"campaign": "demo"},
                },
                output,
            )
            self.assertEqual(count, 1)
            events = load_events(output)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].actor_id, "family-1")
            self.assertEqual(events[0].event, "trial_booked")
            self.assertEqual(events[0].properties["campaign"], "demo")


if __name__ == "__main__":
    unittest.main()
