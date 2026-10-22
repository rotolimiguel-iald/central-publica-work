"""Negative controls with disposable in-memory fixtures; no queue/runtime import."""
import copy
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import sys
import unittest
sys.dont_write_bytecode = True
from binding_prototype import Snapshot, Authority, propose, digest

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923")
CONTRACT = Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.TAKESAKI\CONTRATO_TAKESAKI_R1.json")
PIN = "8bf4c80cf5f42312181da97b8e47601a4aeee7b775d3e764c3fbb2fa1241b95d"
spec=importlib.util.spec_from_file_location("installed_controls", BASE / "iald_orchestrator/request_controls.py")
controls=importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.raw=CONTRACT.read_bytes()
        self.c=json.loads(self.raw)
        self.s=Snapshot(self.c["job_id"],self.c["request_id"],self.c["original_memory_context_id"],
                        self.c["original_prompt_sha256"],memory_objective_sha256=self.c["original_prompt_sha256"])
        order=self.c["authenticated_scope_order"]
        self.a=Authority("verified_direct_human_order",order["thread_id"],self.c["unit"],order["source"]["sha256"])
        # Fixtures intentionally assert pins; real disk verification is separate.
        self.pins={p["path"]:(p["sha256"],p["bytes"]) for p in
                   [order["source"],*self.c["primary_source_pins"],self.c["working_v392"]]}

    def call(self, **kw):
        args=dict(snapshot=self.s,raw=self.raw,expected_sha256=PIN,expected_version=0,
                  authority=self.a,verified_pins=self.pins,normalize=controls.normalize)
        args.update(kw)
        return propose(**args)

    def changed(self, mutate, **kw):
        c=copy.deepcopy(self.c); mutate(c)
        raw=json.dumps(c).encode()
        return self.call(raw=raw,expected_sha256=digest(raw),**kw)

    def test_valid_preserves_identity_and_anchor(self):
        before=copy.deepcopy(self.s); p=self.call()
        self.assertEqual(self.s,before); self.assertEqual(p.original_constraints_json,"null")
        self.assertEqual(json.loads(p.effective_constraints_json)["required_provider"],"kimi")
        self.assertNotIn("memory_generation",json.loads(p.effective_constraints_json))
        self.assertEqual(json.loads(p.event_json)["memory_context_id"],self.s.context_id)

    def test_exact_replay_is_read_only(self):
        p=self.call(); self.assertTrue(self.call(prior=p).replay)
        later=replace(self.s,stage="execution_waiting",version=7,task_exists=True,attempt_exists=True)
        self.assertTrue(self.call(snapshot=later,prior=p).replay)

    def test_byte_tamper(self):
        with self.assertRaises(ValueError): self.call(raw=self.raw+b" ")

    def test_all_original_identities(self):
        for field in ["job_id","request_id","original_memory_context_id","original_prompt_sha256"]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.changed(lambda c:c.update({field:"changed"}))

    def test_source_tamper_or_missing(self):
        for mode in ["missing","changed_hash","changed_size"]:
            pins=dict(self.pins); key=next(iter(pins))
            if mode=="missing": del pins[key]
            elif mode=="changed_hash": pins[key]=("0"*64,pins[key][1])
            else: pins[key]=(pins[key][0],pins[key][1]+1)
            with self.subTest(mode=mode), self.assertRaises(ValueError): self.call(verified_pins=pins)

    def test_authority_kind(self):
        for kind in ["agent","model","DECLARADO","verified_claude_text","unverified_human"]:
            with self.subTest(kind=kind), self.assertRaises(ValueError): self.call(authority=replace(self.a,kind=kind))

    def test_authority_scope(self):
        for key in ["thread_id","unit","order_sha256"]:
            with self.subTest(key=key), self.assertRaises(ValueError): self.call(authority=replace(self.a,**{key:"other"}))

    def test_non_null_original_or_acom_change(self):
        for kw in [{"original_constraints_json":"{}"},{"memory_anchor_constraints_json":"null"},
                   {"memory_objective_sha256":"0"*64}]:
            with self.subTest(kw=kw), self.assertRaises(ValueError): self.call(snapshot=replace(self.s,**kw))

    def test_stale_version(self):
        with self.assertRaises(ValueError): self.call(snapshot=replace(self.s,version=1))

    def test_stages_and_prior_actions(self):
        for stage in ["draft_dispatching","draft_waiting","prompt_ready","execution_dispatching",
                      "execution_waiting","failed","cancelled","completed"]:
            with self.subTest(stage=stage), self.assertRaises(ValueError): self.call(snapshot=replace(self.s,stage=stage))
        with self.assertRaises(ValueError): self.call(snapshot=replace(self.s,actions=("create","begin_draft")))

    def test_hidden_work_and_outbox(self):
        for field in ["prepared_prompt_exists","thread_exists","task_exists","attempt_exists","pending_memory_outbox"]:
            with self.subTest(field=field), self.assertRaises(ValueError): self.call(snapshot=replace(self.s,**{field:True}))

    def test_changed_supplement_even_equivalent_constraints(self):
        p=self.call()
        with self.assertRaises(ValueError): self.changed(lambda c:c.update(scientific_acceptance=c["scientific_acceptance"]+["extra"]),prior=p)

    def test_rebinding_provider(self):
        p=self.call()
        with self.assertRaises(ValueError): self.changed(lambda c:c["execution_constraints"].update(required_provider="deepseek"),prior=p)

    def test_unit_mismatch(self):
        with self.assertRaises(ValueError): self.changed(lambda c:c["execution_constraints"].update(branch_id="F5.3"))

    def test_unknown_constraint(self):
        with self.assertRaises(ValueError): self.changed(lambda c:c["execution_constraints"].update(ignore_gate=True))

    def test_max_calls_and_mission(self):
        for kw in [{"max_calls":2},{"max_calls":True},{"mission_id":"invented"}]:
            with self.subTest(kw=kw), self.assertRaises(ValueError): self.changed(lambda c:c["execution_constraints"].update(kw))

    def test_preserve_original_required(self):
        with self.assertRaises(ValueError): self.changed(lambda c:c.update(preserve_original=False))

    def test_bad_schema(self):
        with self.assertRaises(ValueError): self.changed(lambda c:c.update(schema="unknown"))


if __name__ == "__main__": unittest.main(verbosity=2)
