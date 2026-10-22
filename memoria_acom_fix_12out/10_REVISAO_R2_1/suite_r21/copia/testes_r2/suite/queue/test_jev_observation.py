"""Provider-free checks for the idempotent Jev scientific observation."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import uuid

import observe_jev_science as pilot
from iald_orchestrator.runtime import Runtime, now


class JevObservationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.receipt = Path(self.folder.name) / "observation.json"
        self.memory = {"receipt": {"packet_sha256": "a" * 64, "generation": "b" * 64}}
        self.response = {"model": "jev-1.13.0", "usage": {"input_tokens": 40, "output_tokens": 8},
                         "answers": {
                             "complexity": {"choice": "deep", "confidence": 0.9},
                             "source_relevance": {"score": 1.8, "confidence": 0.8},
                             "claim_supported": {"noul": 0.02},
                             "requires_independent_check": {"noul": 0.98},
                         }}

    def test_second_run_uses_receipt_without_new_provider_call(self):
        with (patch.object(pilot, "RECEIPT", self.receipt),
              patch.object(pilot, "availability", return_value={"status": "ready"}),
              patch.object(pilot, "prepare", return_value=self.memory),
              patch.object(pilot, "ask_with_memory", return_value=(self.response, self.memory["receipt"])) as ask,
              contextlib.redirect_stdout(io.StringIO())):
            pilot.main()
            pilot.main()
        self.assertEqual(ask.call_count, 1)
        record = json.loads(self.receipt.read_bytes())
        self.assertEqual(record["status"], "completed")
        self.assertEqual(record["effects"], "NO_ROUTING_OR_GATE_CHANGE")
        self.assertEqual(record["answers"]["claim_supported"], 0.02)

    def test_uncertain_call_is_not_repeated(self):
        with (patch.object(pilot, "RECEIPT", self.receipt),
              patch.object(pilot, "availability", return_value={"status": "ready"}),
              patch.object(pilot, "prepare", return_value=self.memory),
              patch.object(pilot, "ask_with_memory", side_effect=TimeoutError) as ask,
              contextlib.redirect_stdout(io.StringIO())):
            pilot.main()
            pilot.main()
        self.assertEqual(ask.call_count, 1)
        self.assertEqual(json.loads(self.receipt.read_bytes())["status"], "uncertain")

    def test_free_form_task_does_not_egress_to_jev(self):
        runtime = Runtime(self.folder.name, recover=False)
        task_id, request_id = str(uuid.uuid4()), str(uuid.uuid4())
        with runtime.db() as db:
            db.execute("INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status) "
                       "VALUES(?,?,?,?,?,'queued')",
                       (task_id, request_id, "texto jurídico não autorizado", now(), now()))
        packet = {"prompt": "common memory", "receipt": {"generation": "b" * 64,
                  "memory_mode": "standard", "sources": []}}
        with (patch.object(runtime, "source_status", return_value={"ok": True}),
              patch.object(runtime, "connections", return_value=[]),
              patch.object(runtime, "counts", return_value={}),
              patch("iald_orchestrator.runtime.canonical_memory.prepare", return_value=packet),
              patch("iald_orchestrator.runtime.route", return_value={"selected": None, "candidates": []}),
              patch("iald_orchestrator.runtime.jev.classify_with_jev") as ask):
            runtime._perform(task_id, "texto jurídico não autorizado")
        ask.assert_not_called()
        self.assertEqual(runtime.task(task_id)["decision"]["jev"]["status"],
                         "not_called_without_scientific_scope")


if __name__ == "__main__":
    unittest.main()
