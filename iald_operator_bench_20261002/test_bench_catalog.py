"""Offline contract/security tests. No bench/scientific module is imported."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).parent / "stage/iald_bench_catalog.py"


def load_module():
    spec = importlib.util.spec_from_file_location("bench_adapter_under_test", MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


with patch.object(socket, "create_connection", side_effect=AssertionError("live network forbidden")), \
     patch.object(subprocess, "Popen", side_effect=AssertionError("subprocess forbidden")):
    bench = load_module()


def ready():
    return {"status": "READY", "domain": "gw_strain", "load_id": "8560b710-3ad7-402b-a12e-9a0b1fdf1ad3",
            "generation": 1, "worker_pid": 99, "total_files": 1, "loaded_files": 1,
            "resident_bytes": 24, "errors": [], "worker_rss_bytes": 100, "elapsed_ms": 1,
            "series": [{"id": "a" * 24, "name": "H1.hdf5", "strain_array_sha256": "b" * 64,
                        "source_sha256": "c" * 64, "source_bytes": 24, "dt_s": .001, "rows": 3}]}


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.network = patch.object(socket, "create_connection", side_effect=AssertionError("live network forbidden"))
        self.network.start()
        self.addCleanup(self.network.stop)
        self.process = patch.object(subprocess, "Popen", side_effect=AssertionError("subprocess forbidden"))
        self.process.start()
        self.addCleanup(self.process.stop)

    def test_import_and_catalog_have_no_io(self):
        with patch.object(Path, "open", side_effect=AssertionError("file read during catalog")), \
             patch.object(bench, "_http", side_effect=AssertionError("HTTP during catalog")):
            listing = bench.catalog()
        self.assertEqual(len(listing["operations"]), 34)
        self.assertEqual({o["operation"] for o in listing["operations"]}, set(bench._OPS))
        self.assertLessEqual(len(json.dumps(listing, ensure_ascii=False).encode("utf-8")), 12000)
        listing["operations"][0]["description"] = "poison"
        self.assertNotEqual(bench.catalog()["operations"][0]["description"], "poison")

    def test_every_computation_requires_plan(self):
        expected = {"identity_chain", "dephasing", "inquiry", "universe_load", "universe_model",
                    "universe_event_view", "universe_event", "cosmos_status", "cosmos_evaluate",
                    "cosmos_save_scenario", "cosmos_export"}
        self.assertEqual({op for op in bench._OPS if bench.writes(op)}, expected)
        self.assertEqual({o["operation"] for o in bench.catalog()["operations"] if o["writes"]}, expected)

    def test_defaults_idempotent_and_numeric_identity(self):
        for op, value in (("cosmos_evaluate", {}), ("universe_load", {}),
                          ("universe_model", {"reading": "R-B"}),
                          ("relations", {"q": "  Identity "}),
                          ("cosmos_save_scenario", {"label": "  A  "}),
                          ("cosmos_export", {"reference_parameters": {}, "current_parameters": {}})):
            with self.subTest(op=op):
                normalized = bench.normalize(op, value)
                self.assertEqual(normalized, bench.normalize(op, normalized))
                self.assertEqual(bench._canonical(normalized), bench._canonical(bench.normalize(op, normalized)))
        self.assertEqual(bench.normalize("dephasing", {"omega_rad_s": 1, "tau_s": -0.0, "duration_s": 2}),
                         bench.normalize("dephasing", {"omega_rad_s": 1.0, "tau_s": 0, "duration_s": 2.0}))

    def test_full_catalog_examples_normalize(self):
        reg = {"primary_start_tM": 10., "reference_redshift": .1,
               "reference_mass_for_start_solar": 66., "start_times_tM": [6., 10.]}
        with patch.object(bench, "_read_json", return_value=reg):
            for op in bench.catalog("all")["operations"]:
                with self.subTest(op=op["operation"]):
                    value = bench.normalize(op["operation"], op["example"])
                    self.assertEqual(value, bench.normalize(op["operation"], value))

    def test_resident_receipt_is_compact_for_180_series(self):
        status = ready()
        status["series"] = [{**status["series"][0], "id": f"{i:024x}",
                             "metadata": {"text": "x" * 3000}} for i in range(180)]
        receipt = bench._resident_provenance(status)
        self.assertEqual(receipt["series_count"], 180)
        self.assertLess(len(json.dumps(receipt)), 1500)
        status["series"].reverse()
        self.assertEqual(receipt, bench._resident_provenance(status))
        status["series"][0]["metadata"]["text"] = "changed"
        self.assertNotEqual(receipt["series_sha256"], bench._resident_provenance(status)["series_sha256"])

    def test_calculation_provenance_includes_all_three_historical_pins(self):
        def pin(path, label):
            return {"source": label, "sha256": "1" * 64, "bytes": 1}
        with patch.object(bench, "_pin", side_effect=pin), patch.object(bench, "_http", side_effect=AssertionError):
            for operation, parameters in (("identity_chain", {}), ("dephasing", {"omega_rad_s": 1, "tau_s": 1, "duration_s": 1})):
                p = bench.provenance(operation, parameters)
                self.assertIn("bench/app.py", {x["source"] for x in p["executors"]})
                self.assertEqual({x["source"] for x in p["inputs"]}, {
                    "TGL_ATLAS.md", "historical_v368/estrutura_v368.json"})

    def test_strict_bad_parameters(self):
        cases = [("shell", {}), ("universe_release", {}), ("cosmos_evaluate", {"url": "http://evil"}),
                 ("cosmos_evaluate", {"H0": True}), ("cosmos_evaluate", {"H0": "67.4"}),
                 ("cosmos_evaluate", {"H0": float("nan")}), ("cosmos_evaluate", {"wa": float("inf")}),
                 ("cosmos_evaluate", {"model_id": "TGL_V3_TOTAL_FIXED_BETA", "wa": .1}),
                 ("lab_describe", {"id": "../secret"}), ("cosmos_scenario", {"id": "a" * 32}),
                 ("universe_model", {"reading": "R-A", "spin": 1}),
                 ("cosmos_save_scenario", {"label": "A\nB"}),
                 ("runs", {"page_size": 501}), ("runs", {"offset": .5}),
                 ("cosmos_export", {"reference_parameters": {}}),
                 ("lab_preview", {"id": "a" * 24, "x": "x", "y": "x"})]
        with patch.object(bench, "_http", side_effect=AssertionError("validation HTTP")):
            for op, parameters in cases:
                with self.subTest(op=op, parameters=parameters), self.assertRaises(bench.BenchError):
                    bench.normalize(op, parameters)

    def test_event_defaults_from_registered_file_without_worker(self):
        reg = {"primary_start_tM": 10., "reference_redshift": .1,
               "reference_mass_for_start_solar": 66., "start_times_tM": [6., 10.]}
        payload = {"reading": "R-GLOBAL", "detectors": {d: {"amplitude": 1e-21, "phase": 0} for d in ("H1", "L1")}}
        with patch.object(bench, "_read_json", return_value=reg), patch.object(bench, "_http", side_effect=AssertionError):
            normalized = bench.normalize("universe_event_view", payload)
            self.assertEqual(normalized["mass_source_solar"], 66 / 1.1)
            self.assertEqual(normalized, bench.normalize("universe_event_view", normalized))
            with self.assertRaises(bench.BenchError):
                bench.normalize("universe_event_view", {**payload, "start_tm": 11})

    def test_ready_load_never_posts(self):
        with patch.object(bench, "_http", return_value=ready()) as http:
            result = bench.request("universe_load", {})
        self.assertEqual(result["status"], "ALREADY_RESIDENT")
        http.assert_called_once_with(18765, "GET", "/api/universe/status")

    def test_active_partial_or_loading_is_preserved(self):
        for state in ("PARTIAL", "LOADING", "RELEASING"):
            with self.subTest(state=state), patch.object(bench, "_http", return_value={**ready(), "status": state}) as http:
                with self.assertRaises(bench.BenchError):
                    bench.request("universe_load", {})
                self.assertEqual(http.call_count, 1)

    def test_explicit_load_uses_exact_body(self):
        loading = {**ready(), "status": "LOADING", "loaded_files": 0}
        with patch.object(bench, "_http", side_effect=[{"status": "IDLE", "loaded_files": 0}, loading]) as http:
            result = bench.request("universe_load", {})
        self.assertEqual(result["status"], "LOADING")
        self.assertFalse(result["load_complete"])
        self.assertEqual(result["requested_domain"], "gw_strain")
        self.assertEqual(result["load_id"], loading["load_id"])
        self.assertEqual(result["generation"], loading["generation"])
        self.assertTrue(result["dispatched"])
        self.assertEqual(http.call_args.args, (18765, "POST", "/api/universe/load", {"domain": "gw_strain"}))

    def test_load_receipt_mismatch_is_uncertain_without_retry(self):
        invalid = [{"domain": "other"}, {"load_id": None}, {"generation": True},
                   {"generation": 0}, {"total_files": 0}, {"loaded_files": True},
                   {"status": "READY", "loaded_files": 0}, {"errors": None}]
        for change in invalid:
            with self.subTest(change=change), patch.object(bench, "_http", side_effect=[
                    {"status": "IDLE", "loaded_files": 0}, {**ready(), **change}]) as http:
                with self.assertRaises(bench.BenchError) as caught:
                    bench.request("universe_load", {})
                self.assertTrue(caught.exception.uncertain)
                self.assertEqual(caught.exception.code, "INVALID_LOAD_RECEIPT")
                self.assertEqual(http.call_count, 2)

    def test_load_partial_and_failure_receipts_remain_terminal_noncompletion(self):
        for state in ("PARTIAL", "FAILED"):
            receipt = {**ready(), "status": state, "loaded_files": 0,
                       "errors": [{"name": "H1.hdf5", "error": "fixture load failed"}]}
            with self.subTest(state=state), patch.object(bench, "_http", side_effect=[
                    {"status": "IDLE", "loaded_files": 0}, receipt]) as http:
                result = bench.request("universe_load", {})
            self.assertEqual(result["status"], state)
            self.assertEqual(result["errors"], receipt["errors"])
            self.assertFalse(result["load_complete"])
            self.assertEqual(http.call_count, 2)

    def test_only_explicit_status_queries_follow_background_load(self):
        loading = {**ready(), "status": "LOADING", "loaded_files": 0}
        with patch.object(bench, "_http", side_effect=[{"status": "IDLE", "loaded_files": 0}, loading,
                                                      loading, ready()]) as http:
            first = bench.request("universe_load", {})
            self.assertEqual(http.call_count, 2)
            second = bench.request("universe_status", {})
            final = bench.request("universe_status", {})
        self.assertEqual(first["load_id"], second["load_id"])
        self.assertEqual(first["generation"], final["generation"])
        self.assertEqual(final["status"], "READY")
        self.assertEqual(sum(call.args[1] == "POST" for call in http.call_args_list), 1)

    def test_ready_domain_conflict_never_posts(self):
        for state in ("IDLE", "READY"):
            value = {**ready(), "domain": "other", "status": state}
            if state == "IDLE":
                value["loaded_files"] = 0
            with self.subTest(state=state), patch.object(bench, "_http", return_value=value) as http:
                with self.assertRaises(bench.BenchError):
                    bench.request("universe_load", {})
                self.assertEqual(http.call_count, 1)

    def test_ready_receipt_requires_load_identity_even_without_post(self):
        with patch.object(bench, "_http", return_value={**ready(), "load_id": None}) as http:
            with self.assertRaises(bench.BenchError) as caught:
                bench.request("universe_load", {})
        self.assertFalse(caught.exception.uncertain)
        self.assertEqual(http.call_count, 1)

    def test_failed_state_is_preserved_only_for_gw_load_endpoints(self):
        receipt = {**ready(), "status": "FAILED", "loaded_files": 0, "errors": [{"error": "fixture"}]}
        with patch.object(bench.http.client, "HTTPConnection") as factory:
            response = factory.return_value.getresponse.return_value
            response.status = 200
            response.read.return_value = json.dumps(receipt).encode()
            response.getheader.return_value = "application/json"
            for method, path in (("GET", "/api/universe/status"), ("POST", "/api/universe/load")):
                self.assertEqual(bench._http(18765, method, path), receipt)
            with self.assertRaises(bench.BenchError):
                bench._http(18765, "POST", "/api/run", {})

    def test_model_never_starts_missing_worker(self):
        with patch.object(bench, "_http", return_value={"status": "IDLE"}) as http:
            with self.assertRaises(bench.BenchError):
                bench.request("universe_model", {"reading": "R-B"})
            self.assertEqual(http.call_count, 1)

    def test_exact_wire_envelopes(self):
        with patch.object(bench, "_http", return_value={"status": "ok"}) as http:
            bench.request("identity_chain", {})
            http.assert_called_with(18765, "POST", "/api/run", {"operation": "identity_chain"})
            bench.request("cosmos_export", {"reference_parameters": {}, "current_parameters": {"H0": 70}})
            p = http.call_args.args[3]
            self.assertEqual(len(p["current_parameters"]), 7)
            self.assertEqual(p["current_parameters"]["H0"], 70.0)

    def test_pagination_preserves_upstream_limits(self):
        with patch.object(bench, "_http", return_value=list(range(40))) as http:
            page = bench.request("runs", {"page_size": 7, "offset": 35})
        self.assertEqual(page["items"], list(range(35, 40)))
        self.assertIsNone(page["next_offset"])
        self.assertEqual(page["upstream_limit"], 40)
        http.assert_called_once_with(18765, "GET", "/api/runs")
        with patch.object(bench, "_http", return_value={"matches": [1, 2, 3], "limited": True}) as http:
            page = bench.request("relations", {"q": " A&B ", "page_size": 1})
        self.assertEqual(page["next_offset"], 1)
        self.assertTrue(page["metadata"]["limited"])
        self.assertIn("q=a%26b", http.call_args.args[2])

    def test_passive_provenance_ignores_rss_time_detects_generation(self):
        def pin(path, label):
            return {"source": label, "sha256": "1" * 64, "bytes": 1}
        status = ready()
        with patch.object(bench, "_pin", side_effect=pin), patch.object(bench, "_http", side_effect=lambda *a: copy.deepcopy(status)) as http:
            before = bench.provenance("universe_view", {"id": "a" * 24})
            status.update(worker_rss_bytes=999, elapsed_ms=32, worker_pid=123, data_read_operations=900)
            self.assertEqual(before, bench.provenance("universe_view", {"id": "a" * 24}))
            status["load_id"] = "new-load"
            self.assertNotEqual(before, bench.provenance("universe_view", {"id": "a" * 24}))
            self.assertTrue(all(call.args[1:] == ("GET", "/api/universe/status") for call in http.call_args_list))

    def test_cosmos_provenance_never_initializes_cache(self):
        def pin(path, label):
            return {"source": label, "sha256": "1" * 64, "bytes": 1}
        with patch.object(bench, "_pin", side_effect=pin), patch.object(bench, "_http", return_value={
                "service": "tgl-cosmology-resident-v1", "status": "RUNNING"}) as http:
            result = bench.provenance("cosmos_evaluate", {})
        http.assert_called_once_with(18766, "GET", "/api/cosmology/health")
        self.assertIsNone(result["runtime"]["cosmos"]["load_id"])
        self.assertEqual(len(result["inputs"]), 2)

    def test_file_hash_is_real_and_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "scientific.txt"
            path.write_bytes(b"a\r\nb")
            before = bench._pin(path, "fixture")
            self.assertEqual(before["sha256"], hashlib.sha256(b"a\r\nb").hexdigest())
            path.write_bytes(b"a\nb")
            self.assertNotEqual(before["sha256"], bench._pin(path, "fixture")["sha256"])

    def test_symlink_rejected_before_read(self):
        with patch.object(Path, "is_symlink", return_value=True), patch.object(Path, "open", side_effect=AssertionError):
            with self.assertRaises(bench.BenchError):
                bench._pin(Path("fake"), "fixture")

    def test_catalog_cannot_redirect_hash_to_private_file(self):
        with patch.object(bench, "_http", return_value={"items": [{"id": "a" * 24, "path": r"C:\Users\rotol\.env"}]}):
            with self.assertRaises(bench.BenchError):
                bench._catalog_source("a" * 24)

    def test_invalid_http_destination_never_connects(self):
        for args in ((443, "GET", "/api/overview"), (18765, "GET", "http://evil/api/overview"),
                     (18765, "POST", "/api/universe/release"), (18765, "GET", "/api/overview\r\nX:bad")):
            with self.subTest(args=args), patch.object(bench.http.client, "HTTPConnection", side_effect=AssertionError):
                with self.assertRaises(bench.BenchError):
                    bench._http(*args)

    def test_transport_no_proxy_cookie_redirect_or_retry(self):
        class Response:
            status = 200
            raw = b'{"status":"ok"}'
            content_type = "application/json"
            def read(self, limit):
                return self.raw[:limit]
            def getheader(self, name, default):
                return self.content_type
        response = Response()
        with patch.dict("os.environ", {"HTTP_PROXY": "http://evil", "ALL_PROXY": "http://evil"}), \
             patch.object(bench.http.client, "HTTPConnection") as factory:
            connection = factory.return_value
            connection.getresponse.return_value = response
            self.assertEqual(bench._http(18765, "POST", "/api/run", {"operation": "identity_chain"}), {"status": "ok"})
            factory.assert_called_once_with("127.0.0.1", 18765, timeout=120)
            headers = connection.request.call_args.kwargs["headers"]
            self.assertNotIn("Cookie", headers)
            self.assertEqual(headers["Origin"], "http://127.0.0.1:18765")
            for status, raw, content in ((302, b"", "application/json"), (200, b'{"x":1,"x":2}', "application/json"),
                                         (200, b'{"x":NaN}', "application/json"), (200, b'{"x":1e400}', "application/json"),
                                         (200, b'<html>', "text/html"), (503, b'{}', "application/json")):
                response.status, response.raw, response.content_type = status, raw, content
                connection.request.reset_mock()
                with self.subTest(status=status, raw=raw), self.assertRaises(bench.BenchError) as caught:
                    bench._http(18765, "POST", "/api/run", {})
                self.assertTrue(caught.exception.uncertain)
                self.assertEqual(connection.request.call_count, 1)

    def test_lost_response_is_uncertain_once(self):
        with patch.object(bench.http.client, "HTTPConnection") as factory:
            factory.return_value.getresponse.side_effect = TimeoutError("lost")
            with self.assertRaises(bench.BenchError) as caught:
                bench._http(18765, "POST", "/api/run", {})
            self.assertTrue(caught.exception.uncertain)
            self.assertEqual(factory.return_value.request.call_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
