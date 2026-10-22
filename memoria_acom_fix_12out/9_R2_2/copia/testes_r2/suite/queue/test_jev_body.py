"""Offline invariants: no remote request is made by this suite."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from iald_orchestrator import jev_decisions as d, nos_packet as n

class Checks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.policy=self.root/"policy.json"
        self.policy.write_text(json.dumps({"phase":"CALIBRATION","daily_call_limit":50,"max_packet_chars":9000}))
        self.packet={"prompt":"scientific context","receipt":{"schema":n.SCHEMA,"unit":"F9.9","mode":"calibration",
              "selection":"SCIENTIFIC_ALLOWLIST_REREAD_NO_LEGAL_CONTENT","sources":[{"id":"source"}],
              "canonical_memory":{"generation":"g"},"packet_sha256":n.sha(b"scientific context")}}
        self.questions={"D1":{"type":"noul","instructions":"Does prior work exist?"}}
        self.data={"model":d.MODEL,"answers":{"D1":{"type":"noul","noul":0.8}},
                   "usage":{"input_tokens":100,"output_tokens":10}}

    def calls(self, response):
        return (patch.object(d,"ROOT",self.root/"ledger"),patch.object(d,"POLICY",self.policy),
                patch("iald_orchestrator.jev.availability",return_value={"status":"ready"}),
                patch("iald_orchestrator.jev._key",return_value="synthetic-not-a-real-key"),
                patch.object(d,"_event",return_value={"ok":True}),
                patch.object(d.urllib.request,"urlopen",response))

    def test_packet_tamper_is_rejected(self):
        self.packet["prompt"]+="!"
        with self.assertRaises(ValueError):n.verify(self.packet)

    def test_legal_and_secret_projection_is_refused(self):
        for text in ["ACOM","Escritório","WIPO", "iald_stack_v7.py"]:
            with self.assertRaises(ValueError):n.safe_text(text)

    def test_uncertain_attempt_is_not_repeated(self):
        from unittest.mock import Mock
        transport=Mock(side_effect=TimeoutError)
        from contextlib import ExitStack
        with ExitStack() as stack:
            for p in self.calls(transport):stack.enter_context(p)
            for i in range(2):
                with self.assertRaises(RuntimeError):d.ask("Read the source",self.questions,self.packet)
        self.assertEqual(transport.call_count,1)

    def test_success_is_idempotent_and_labels_are_not_sent(self):
        from unittest.mock import MagicMock
        from contextlib import ExitStack
        transport=MagicMock();transport.return_value.__enter__.return_value.read.return_value=json.dumps(self.data).encode()
        self.packet["receipt"]["expected"]=0
        with ExitStack() as stack:
            for p in self.calls(transport):stack.enter_context(p)
            x=d.ask("Read the source",self.questions,self.packet)
            y=d.ask("Read the source",self.questions,self.packet)
        self.assertEqual(transport.call_count,1)
        body=json.loads(transport.call_args.args[0].data)
        self.assertNotIn("expected",json.dumps(body))
        self.assertEqual(x[0],y[0]);self.assertFalse(y[1]["authority_granted"])

    def test_calibration_before_shadow(self):
        self.packet["receipt"]["mode"]="shadow"
        with patch.object(d,"POLICY",self.policy):
            with self.assertRaises(ValueError):d.ask("Read the source",self.questions,self.packet)

    def test_invalid_probabilities_are_refused(self):
        for x in [float("nan"),-0.01,1.01,True]:
            with self.assertRaises(ValueError):d.number(x)

    def test_wrong_model_and_missing_answer(self):
        for k,v in [("model","jev-new"),("answers",{})]:
            data=copy.deepcopy(self.data);data[k]=v
            with self.assertRaises(ValueError):d.validate_answers(data,self.questions)

    def test_accuracy_and_brier_use_labels_not_confidence(self):
        cases=[{"id":"a","axis":"D1","expected":0,"question":{"type":"noul"}},
               {"id":"b","axis":"D1","expected":1,"question":{"type":"noul"}}]
        data2=copy.deepcopy(self.data);data2["answers"]["D1"]["noul"]=0.9
        result=d.metrics(cases,{"a":self.data,"b":data2})
        self.assertAlmostEqual(result["mean_brier"],.325)
        self.assertEqual(result["accuracy"],.5)
        self.assertEqual(sum(b["n"] for b in result["reliability"]),2)
        self.assertFalse(d.metrics(cases,{"a":self.data})["complete"])

    def test_provider_pin_and_original_memory_preserved(self):
        # Unknown historic branch IDs do not acquire invented board packets.
        memory={"prompt":"original","receipt":{"packet_sha256":"x"}}
        self.assertIs(n.augment(memory,{"branch_id":"ORDEM_018_SENSITIVITY"},"claude","system"),memory)

if __name__=="__main__":unittest.main()
