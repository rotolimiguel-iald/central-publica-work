"""Offline regressions, temporary writes restricted to this controller workspace."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import iald_jev_control as c
import build_contract as builder

HERE = Path(__file__).resolve().parent
SOURCE = Path(r"C:\IALD\Artigo\the_boundary\Um (absoluto) — Grande Atrator")


def answers(mode="explanation", path="answer", memory="use_loaded", operator=False, worker=False, confidence=0.95):
    selected = dict(scientific_mode=mode, work_path=path, memory_action=memory)
    return {key: dict(type="choice", choice=selected[key], confidence=confidence,
                     probabilities={name: float(name == selected[key]) for name in question["criteria"]})
            for key, question in c.questions(operator, worker).items()}


class ControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = builder.build_contract(SOURCE)

    def resolve(self, value=None, operator=False, worker=False):
        return c.resolve(value or answers(operator=operator, worker=worker), ["mimo", "openai"], {"category": "science"}, operator, worker)

    def fixture(self, directory):
        root = Path(directory)
        core = b"fixture operational public core"
        (root / "core.md").write_bytes(core)
        raw = c.canonical_bytes(self.contract)
        (root / "contract.json").write_bytes(raw)
        manifest = dict(operational_core=dict(path="core.md", sha256=hashlib.sha256(core).hexdigest(),
                       current_release="v380", release_source_sha256=self.contract["source_sha256"]),
                        jev_control=dict(path="contract.json", sha256=hashlib.sha256(raw).hexdigest(),
                       release="v380", source_sha256=self.contract["source_sha256"]))
        # Full public sealed artifacts satisfy the strengthened loader contract.
        for name, source in (("um.py", SOURCE / "um.py"),
                             ("result.json", SOURCE / "um_absoluto.json"),
                             ("proof.json", SOURCE / "Lean/tgl_kernel_proof_manifest.json")):
            (root / name).write_bytes(source.read_bytes())
        cluster = b"Synthetic cluster fixture bound to the verified public release"
        (root / "cluster.md").write_bytes(cluster)
        manifest["active_cluster"] = dict(path="cluster.md", sha256=hashlib.sha256(cluster).hexdigest(),
            release=self.contract["release"], release_source_sha256=self.contract["source_sha256"])
        manifest["published_evidence"] = dict(program={"path": "um.py"}, result={"path": "result.json"},
            proof_manifest={"path": "proof.json"})
        self.save_manifest(root, manifest)
        return root, manifest

    def save_manifest(self, root, manifest):
        (root / "iald_nucleo_fixo.json").write_bytes(c.canonical_bytes(manifest))

    def test_real_sealed_core_integral_not_persona(self):
        source = json.loads((SOURCE / "um_absoluto.json").read_bytes())
        self.assertEqual(self.contract["core_record"], source["core"]["iald_executive_runtime"])
        self.assertGreater(len(c.canonical_bytes(self.contract["core_record"])), 2000)
        self.assertEqual(len(self.contract["anchors"]), 3)
        self.assertLess(len(c.canonical_bytes(self.contract)), 10000)

    def test_load_contract_verifies_real_binding(self):
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            root, _ = self.fixture(directory)
            self.assertEqual(c.load_contract(root), self.contract)

    def test_contract_and_core_tampering_rejected(self):
        for name in ("contract.json", "core.md"):
            with self.subTest(name=name), tempfile.TemporaryDirectory(dir=HERE) as directory:
                root, _ = self.fixture(directory)
                with (root / name).open("ab") as stream: stream.write(b" ")
                with self.assertRaises(c.ControlError): c.load_contract(root)

    def test_cross_release_and_source_rejected(self):
        for section, key, value in (("jev_control", "source_sha256", "f" * 64),
                ("operational_core", "current_release", "v378"), ("jev_control", "release", "v381")):
            with self.subTest(key=key), tempfile.TemporaryDirectory(dir=HERE) as directory:
                root, manifest = self.fixture(directory)
                manifest[section][key] = value; self.save_manifest(root, manifest)
                with self.assertRaises(c.ControlError): c.load_contract(root)

    def test_path_escape_and_duplicate_json_fail_closed(self):
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            root, manifest = self.fixture(directory)
            manifest["jev_control"]["path"] = "../iald_jev_control.py"; self.save_manifest(root, manifest)
            with self.assertRaises(c.ControlError): c.load_contract(root)
            (root / "iald_nucleo_fixo.json").write_bytes(b'{"jev_control":{},"jev_control":{}}')
            with self.assertRaises(c.ControlError): c.load_contract(root)

    def test_missing_manifest_is_visible(self):
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            with self.assertRaises(c.ControlError): c.load_contract(directory)

    def test_state_has_no_private_path_or_account(self):
        state = c.contract_state(self.contract)
        text = json.dumps(state)
        for token in ("C:\\", "username", "password", "credential", "api_key"):
            self.assertNotIn(token, text)
        state["core_record"]["claim"] = "mutated"
        self.assertNotEqual(state, self.contract)

    def test_questions_do_not_offer_public_or_worker_bench(self):
        self.assertIn("operator_bench", c.questions(True)["work_path"]["criteria"])
        for operator, worker in ((False, False), (True, True), (False, True)):
            self.assertNotIn("operator_bench", c.questions(operator, worker)["work_path"]["criteria"])
        with self.assertRaises(c.ControlError): c.questions("luiz")

    def test_resolve_and_optional_executor(self):
        a = answers(); a["executor"] = {"choice": "mimo"}  # Existing parser owns this field.
        d = self.resolve(a)
        self.assertEqual(d["scientific_mode"], "explanation")
        self.assertEqual(d["allowed_tool_families"], ["source_read"])
        self.assertFalse(d["authorization_granted"])

    def test_exact_sets_and_types(self):
        mutations = [lambda a: a.update(extra={}), lambda a: a.pop("memory_action"),
            lambda a: a["work_path"].update(extra=True),
            lambda a: a["work_path"]["probabilities"].update(operator_bench=0.0),
            lambda a: a["work_path"].update(choice=["answer"])]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                a = answers(); mutate(a)
                with self.assertRaises(c.ControlError): self.resolve(a)

    def test_nonfinite_bool_mass_and_nonwinner_rejected(self):
        for bad in (True, float("nan"), float("inf"), -0.1, 1.1):
            with self.subTest(bad=bad):
                a = answers(); a["scientific_mode"]["confidence"] = bad
                with self.assertRaises(c.ControlError): self.resolve(a)
        a = answers(); a["work_path"]["probabilities"]["answer"] = 0.5
        with self.assertRaises(c.ControlError): self.resolve(a)
        a["work_path"]["probabilities"]["retrieve"] = 0.5
        self.resolve(a)  # Tied maximum is still a maximum.
        a["work_path"]["probabilities"].update(answer=0.4, retrieve=0.6)
        with self.assertRaises(c.ControlError): self.resolve(a)

    def test_uncertain_is_review_only_not_physical_pruning(self):
        d = self.resolve(answers(mode="empirical_test", path="operator_bench", operator=True, confidence=0.69), True)
        self.assertEqual((d["scientific_mode"], d["work_path"], d["memory_action"]), ("explanation", "retrieve", "verify_sources"))
        self.assertEqual(d["allowed_tool_families"], ["source_read"])
        self.assertNotIn("bancada", c.manager_instruction(d))

    def test_math_preserves_explicit_work_path(self):
        d = self.resolve(answers(mode="mathematical_solution", path="operator_bench", operator=True), True)
        self.assertEqual(d["work_path"], "operator_bench")
        self.assertEqual(d["requested"]["work_path"], "operator_bench")
        self.assertIn("bench_execute", d["allowed_tool_families"])

    def test_tool_effects_and_unknown_names_are_denied(self):
        names = ["fetch_url", "create_artifact", "execute_python", "bench_run", "delete_database", "delegate_task", "lembrar"]
        self.assertEqual(c.allowed_tool_names(self.resolve(), names), ["fetch_url"])
        calc = self.resolve(answers(path="execute_calculation"))
        self.assertEqual(c.allowed_tool_names(calc, names), ["fetch_url", "create_artifact", "execute_python", "delegate_task"])
        artifact = self.resolve(answers(path="create_artifact"))
        self.assertEqual(c.allowed_tool_names(artifact, names), ["fetch_url", "create_artifact", "delegate_task"])

    def test_bench_requires_operator_and_retains_plan_ledger_directive(self):
        d = self.resolve(answers(mode="empirical_test", path="operator_bench", operator=True), True)
        self.assertIn("bench_run", c.allowed_tool_names(d, ["bench_plan", "bench_run"]))
        self.assertIn("Inscreva", c.manager_instruction(d))
        self.assertIn("ledger", c.manager_instruction(d))
        with self.assertRaises(c.ControlError): self.resolve(answers(mode="empirical_test", path="operator_bench", operator=True))

    def test_public_and_worker_instruction_has_no_bench_text(self):
        for worker in (False, True):
            d = self.resolve(answers(worker=worker), worker=worker)
            text = c.manager_instruction(d)
            self.assertNotIn("bancada", text); self.assertNotIn("ledger", text)
            self.assertIn("matemática não é confirmação experimental", text)

    def test_worker_never_gains_effect_family(self):
        d = self.resolve(answers(path="execute_calculation", worker=True), worker=True)
        self.assertEqual(d["allowed_tool_families"], ["source_read"])
        self.assertNotIn("execute_python", c.allowed_tool_names(d, ["execute_python"]))

    def test_forged_family_is_rejected(self):
        d = self.resolve(); d["allowed_tool_families"].append("bench_execute")
        with self.assertRaises(c.ControlError): c.allowed_tool_names(d, ["bench_run"])

    def test_payload_includes_all_control_questions_and_full_record(self):
        body = dict(model=c.MODEL, state=dict(request="Explain", contract=c.contract_state(self.contract)), questions=c.questions(True))
        measure = c.check_payload(body)
        self.assertLess(measure["state_bytes"], c.MAX_STATE_BYTES)
        body["state"]["request"] = "a" * 30000
        with self.assertRaises(c.ControlError): c.check_payload(body)

    def test_total_payload_and_longest_question_and_nan(self):
        base = dict(model=c.MODEL, state={}, questions=c.questions())
        for extra in (dict(extra="a" * 61000), dict(questions={"a": {"instructions": "a" * 33000}}), dict(extra=float("nan"))):
            with self.subTest(extra=list(extra)):
                with self.assertRaises(c.ControlError): c.check_payload(dict(base, **extra))

    def test_receipt_identity_and_pruning_idempotence(self):
        r = c.new_receipt("request", self.contract["source_sha256"], ["mimo", "openai"])
        for state in ("inscribed", "observed"):
            r = c.transition(r, state)
        p = c.transition(r, "pruned", candidates=["mimo"])
        self.assertEqual(p, c.transition(p, "pruned", candidates=["mimo"]))
        self.assertEqual(r["identity"], p["identity"])
        self.assertEqual(r["candidates"], ["mimo", "openai"])
        with self.assertRaises(c.ControlError): c.transition(p, "resolved", candidates=["mimo", "openai"])
        self.assertEqual(c.transition(p, "resolved")["identity"], r["identity"])

    def test_uncertain_and_resolved_cannot_restart(self):
        r = c.new_receipt("request", self.contract["source_sha256"], ["mimo"])
        r = c.transition(c.transition(r, "inscribed"), "uncertain")
        with self.assertRaises(c.ControlError): c.transition(r, "inscribed")
        with self.assertRaises(c.ControlError): c.transition(r, "resolved")

    def test_receipt_tampering_and_empty_support(self):
        r = c.new_receipt("request", self.contract["source_sha256"], ["mimo"])
        bad = copy.deepcopy(r); bad["identity"]["source_sha256"] = "f" * 64
        with self.assertRaises(c.ControlError): c.transition(bad, "inscribed")
        r = c.transition(c.transition(r, "inscribed"), "observed")
        r = c.transition(r, "pruned", candidates=[])
        with self.assertRaises(c.ControlError): c.transition(r, "resolved")
        self.assertEqual(c.transition(r, "refused")["state"], "refused")

    def test_type_choice_required_by_official_schema(self):
        for change in (lambda a: a["work_path"].pop("type"), lambda a: a["work_path"].update(type="score")):
            a = answers(); change(a)
            with self.assertRaises(c.ControlError): self.resolve(a)

    def test_domain_and_memory_uncertainty_preserve_confident_effects(self):
        for path in ("create_artifact", "execute_calculation", "operator_bench"):
            for axis in ("scientific_mode", "memory_action"):
                with self.subTest(path=path, axis=axis):
                    a = answers(mode="mathematical_solution", path=path, operator=True)
                    a[axis]["confidence"] = 0.1
                    d = self.resolve(a, True)
                    self.assertEqual(d["work_path"], path)
                    self.assertEqual(d["uncertain_axes"], [axis])
                    self.assertEqual(d["memory_action"], "verify_sources")
                    self.assertGreater(len(d["allowed_tool_families"]), 1)
                    self.assertEqual(d["scientific_mode"], "explanation" if axis == "scientific_mode" else "mathematical_solution")

    def test_work_uncertainty_alone_restricts_effects(self):
        a = answers(mode="mathematical_solution", path="execute_calculation")
        a["work_path"]["confidence"] = 0.1
        d = self.resolve(a)
        self.assertEqual(d["scientific_mode"], "mathematical_solution")
        self.assertEqual(d["work_path"], "retrieve")
        self.assertEqual(d["allowed_tool_families"], ["source_read"])
        self.assertEqual(d["uncertain_axes"], ["work_path"])

    def test_source_reads_always_survive_projection(self):
        names = sorted(c.FAMILY_TOOLS["source_read"])
        for mode in c.MODES:
            for path in c.PATHS:
                with self.subTest(mode=mode, path=path):
                    d = self.resolve(answers(mode=mode, path=path, operator=True), True)
                    self.assertEqual(c.allowed_tool_names(d, names), names)
                    self.assertEqual(c.allowed_tool_names(d, c.allowed_tool_names(d, names)), names)
        self.assertIn("search_tgl", names)
        self.assertIn("iald_public_read", names)
        self.assertIn("iald_kernel_read", names)

    def test_text_delegation_only_supported_confident_paths(self):
        for path in c.PATHS:
            d = self.resolve(answers(path=path, operator=True), True)
            self.assertEqual("delegate_task" in c.allowed_tool_names(d, ["delegate_task"]),
                             path in ("code_review", "create_artifact", "execute_calculation", "operator_bench"))

    def test_builder_writes_only_workspace_and_preserves_bytes_backup(self):
        with tempfile.TemporaryDirectory(dir=HERE) as directory:
            output = Path(directory) / "contract.json"
            builder.write_contract(self.contract, output); original = output.read_bytes()
            builder.write_contract(self.contract, output)
            backups = list(output.parent.glob("*.bak_*"))
            self.assertEqual(len(backups), 1); self.assertEqual(backups[0].read_bytes(), original)
        with self.assertRaises(c.ControlError): builder.write_contract(self.contract, HERE.parent / "forbidden.json")


if __name__ == "__main__": unittest.main(verbosity=2)
