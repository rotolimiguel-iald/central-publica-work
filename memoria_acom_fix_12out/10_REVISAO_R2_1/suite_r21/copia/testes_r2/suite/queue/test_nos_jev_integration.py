"""Isolated integration tests. Providers are mocked; no live queue is opened."""
import copy,hashlib,json,sqlite3,tempfile,unittest,uuid
from contextlib import closing
from pathlib import Path
from unittest.mock import patch
from iald_orchestrator import nos_packet as n, jev_body_shadow as s, jev_decisions as j, providers
from iald_orchestrator.runtime import Runtime,now
from iald_orchestrator.request_controls import normalize

class Integration(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.c=normalize(dict(mission_id="TGL_BANCADA_OFICIAL",branch_id="F9.9",lemma_id="test",role="draft",required_provider="kimi",max_calls=1))
  self.memory={"prompt":"original request and canonical evidence","receipt":{"generation":"a"*64,"packet_sha256":n.sha(b"original request and canonical evidence"),"sources":[{"file":"science.md"}],"memory_mode":"maximum"}}
  self.packet={"prompt":"scoped graph","receipt":{"schema":n.SCHEMA,"unit":"F9.9","packet_sha256":n.sha(b"scoped graph"),
   "selection":"SCIENTIFIC_ALLOWLIST_REREAD_NO_LEGAL_CONTENT","canonical_memory":{"generation":"a"*64},
   "sources":[{"path":str(self.root/"science.md")}]}}

 def test_old_branch_unchanged_and_no_graph_access(self):
  c=dict(self.c,branch_id="ORDEM_018_EXISTING")
  with patch.object(n.canonical_memory,"prepare",return_value=self.memory) as prepare,patch.object(n,"build") as build:
   self.assertIs(n.prepare_queue("task",c,"sys"),self.memory)
  self.assertEqual(prepare.call_count,1);build.assert_not_called()

 def test_graph_reservation_and_original_request_preserved(self):
  original=copy.deepcopy(self.c)
  with patch.object(n,"board_unit",return_value={"id":"F9.9"}),patch.object(n,"build",return_value=self.packet),patch.object(n.canonical_memory,"prepare",return_value=self.memory) as prepare:
   result=n.prepare_queue("task",self.c,"sys")
  self.assertEqual(prepare.call_count,2);self.assertGreater(prepare.call_args.kwargs["reserved_context_bytes"],0)
  self.assertTrue(result["prompt"].startswith(self.memory["prompt"]));self.assertEqual(self.c,original)
  self.assertEqual(result["receipt"]["canonical_packet_sha256"],self.memory["receipt"]["packet_sha256"])

 def test_forbidden_additional_source_rejected(self):
  with self.assertRaises(ValueError):
   n._attach(self.memory,dict(self.c,allowed_sources=["other.md"]),"kimi","sys",self.packet)

 def test_wrong_unit_packet_rejected(self):
  memory=copy.deepcopy(self.memory);memory["receipt"]["nos_vivo"]={"unit":"F1.1"}
  with patch.object(n,"board_unit",return_value={"id":"F9.9"}):
   with self.assertRaises(ValueError):n.augment(memory,self.c,"kimi","sys")

 def test_excessive_combined_context_refused(self):
  memory=copy.deepcopy(self.memory);memory["prompt"]="x"*910000
  with self.assertRaises(ValueError):n._attach(memory,self.c,"kimi","sys",self.packet)

 def test_shadow_never_observes_unscoped_or_precalibration(self):
  policy=self.root/"policy.json";policy.write_text('{"phase":"CALIBRATION"}')
  with patch.object(s,"POLICY",policy),patch.object(n,"board_unit",return_value={"id":"F9.9"}),patch.object(j,"ask") as ask:
   self.assertIn("not_called",s.observe("test","task",None,"kimi")["status"])
   self.assertIn("not_called",s.observe("test","task",self.c,"kimi")["status"])
  ask.assert_not_called()

 def test_shadow_failure_does_not_change_executor_or_success(self):
  runtime=Runtime(self.root/"queue",recover=False);taskid=str(uuid.uuid4())
  with runtime.db() as db:
   db.execute("INSERT INTO tasks(id,request_id,prompt,created_at,updated_at,status,execution_constraints) VALUES(?,?,?,?,?,'queued',?)",
    (taskid,str(uuid.uuid4()),"task",now(),now(),json.dumps(self.c)))
  decision={"selected":"kimi","candidates":[]}
  with patch.object(runtime,"source_status",return_value={"ok":True}),patch.object(runtime,"connections",return_value=[]),patch.object(runtime,"counts",return_value={}),patch.object(n,"prepare_queue",return_value=self.memory),patch("iald_orchestrator.runtime.route",return_value=decision),patch.object(s,"observe",side_effect=RuntimeError("observation only")),patch.object(providers,"execute",return_value={"text":"original executor result","usage":{},"verification":"PROVIDER_COMPLETED_NOT_FACT_CHECKED"}) as execute:
   runtime._perform(taskid,"task")
  self.assertEqual(execute.call_args.args[0],"kimi");self.assertEqual(execute.call_args.kwargs["execution_constraints"],self.c)
  result=runtime.task(taskid)
  self.assertEqual(result["status"],"result_ready");self.assertEqual(result["result"]["text"],"original executor result")
  self.assertEqual(result["result"]["jev_body_shadow"]["effects"],"NONE")

 def test_preview_is_local_and_estimates_augmented_packet(self):
  runtime=Runtime(self.root/"queue",recover=False)
  with patch.object(runtime,"source_status",return_value={"ok":True}),patch.object(runtime,"connections",return_value=[]),patch.object(runtime,"counts",return_value={}),patch.object(n,"prepare_queue",return_value=self.memory),patch("iald_orchestrator.runtime.route",return_value={"selected":"kimi","candidates":[]}),patch.object(s,"observe") as observe:
   decision=runtime.preview("task",self.c)
  observe.assert_not_called();self.assertEqual(decision["canonical_memory"],self.memory["receipt"])

 def test_fiftieth_decision_recomputes_without_model_and_preserves_unreviewed(self):
  folder=self.root/"fixture";folder.mkdir();(folder/"calibration").mkdir()
  fixture=folder/"CALIBRATION_CASES.v1.json";fixture.write_text(json.dumps({"cases":[{"id":"a","axis":"D1","question":{"type":"noul"},"expected":1}]}))
  (folder/"CALIBRATION_FREEZE.json").write_text(json.dumps({"sha256":hashlib.sha256(fixture.read_bytes()).hexdigest()}))
  (folder/"calibration/a.json").write_text(json.dumps({"case":"a","call_id":"0"}))
  root=self.root/"ledger";root.mkdir()
  with closing(sqlite3.connect(root/"ledger.sqlite3")) as db,db:
   db.execute("CREATE TABLE calls(record TEXT)")
   for k in range(50):
    db.execute("INSERT INTO calls VALUES(?)",(json.dumps({"id":str(k),"mode":"calibration" if k==0 else "shadow","status":"completed","response":{"answers":{"D1":{"noul":.9}}}}),))
  policy=self.root/"p.json";policy.write_text(json.dumps({"calibration_directory":str(folder)}))
  with patch.object(j,"ROOT",root),patch.object(j,"POLICY",policy),patch.object(j,"ask") as ask:
   report=j.publish_calibration()
  ask.assert_not_called();self.assertEqual(report["decision_count"],50);self.assertEqual(report["unreviewed_shadow"],49)
  self.assertEqual(report["observed_cases"],1);self.assertFalse(report["active_promotion"])

 def test_uncertain_shadow_intent_never_resends_on_new_graph(self):
  path=self.root/"state/jev_body_shadow/test_before.json";path.parent.mkdir(parents=True)
  identity=j.digest({"task_id":"test","phase":"before","prompt":"task","constraints":self.c,"result":None})
  path.write_text(json.dumps({"status":"dispatching","logical_identity":identity,"effects":"NONE"}))
  with patch.object(s,"BASE",self.root),patch.object(j,"ask") as ask,patch.object(n,"build") as build:
   outcome=s.observe("test","task",self.c,"kimi")
  self.assertEqual(outcome["status"],"dispatching");ask.assert_not_called();build.assert_not_called()

 def test_shadow_requires_measured_report_not_only_phase(self):
  policy=self.root/"policy.json";policy.write_text(json.dumps({"phase":"SHADOW","queue_shadow_enabled":True,"shadow_minimum_manager_accepted":True,"calibration_report":str(self.root/"absent.json")}))
  with patch.object(s,"POLICY",policy),patch.object(s,"BASE",self.root),patch.object(n,"board_unit",return_value={"id":"F9.9"}),patch.object(j,"ask") as ask:
   outcome=s.observe("test","task",self.c,"kimi")
  self.assertEqual(outcome["status"],"not_observed");ask.assert_not_called()


 def test_missing_manager_acceptance_prevents_shadow_observation(self):
  policy=self.root/"policy.json";policy.write_text(json.dumps({"phase":"SHADOW","queue_shadow_enabled":True,"shadow_minimum_manager_accepted":False}))
  with patch.object(s,"POLICY",policy),patch.object(s,"BASE",self.root),patch.object(n,"board_unit",return_value={"id":"F9.9"}),patch.object(j,"ask") as ask:
   outcome=s.observe("test","task",self.c,"kimi")
  self.assertEqual(outcome["status"],"awaiting_manager_acceptance");ask.assert_not_called()

 def test_direct_shadow_api_cannot_bypass_manager_acceptance(self):
  packet=copy.deepcopy(self.packet);packet["receipt"]["mode"]="shadow"
  policy=self.root/"policy.json";policy.write_text(json.dumps({"phase":"SHADOW","queue_shadow_enabled":True,"shadow_minimum_manager_accepted":False}))
  with patch.object(j,"POLICY",policy),patch.object(j.urllib.request,"urlopen") as remote:
   with self.assertRaisesRegex(ValueError,"Management acceptance"):j.ask("Read the case",{"D1":{"type":"noul","instructions":"Does it exist?"}},packet)
  remote.assert_not_called()
