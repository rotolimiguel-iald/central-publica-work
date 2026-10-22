import ast,copy,hashlib,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace as NS
HERE=Path(__file__).resolve().parent
ROOT=Path('C:/IALD/projetos_pyhton/IALD')
FAILED_PATH=ROOT/'.iald_runtime/app_routing/f076f5697f224704b1eb5011f08795f1.json'
SELECTED_PATH=ROOT/'.iald_runtime/app_routing/b29a697f9cd8436e90fbbdbcd529b0ee.json'
FAILED=json.loads(FAILED_PATH.read_bytes());SELECTED=json.loads(SELECTED_PATH.read_bytes())
assert FAILED['error_type']=='BudgetRefusal' and SELECTED['status']=='selected'
SCOPED=json.loads((HERE.parent/'SCOPED_ACOM_INPUT.json').read_text())
row_hash=hashlib.sha256(json.dumps(FAILED,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()
EVIDENCE=dict(schema='iald.jev-connection-evidence.v1',verified_local_refusals={row_hash:dict(
    request_sha256=FAILED['request_sha256'],context_id=SCOPED['context_id'],scope=SCOPED['scope'],
    response_artifact_sha256='532f6902924d86e0f05a798a334bee442cc0a3d416788d17c3f7a3fc2cefe973',
    result_artifact_sha256='0568782f93b5e74523b9f809855abce9ed4cc603a6294f264b31aa0fb6cf25bc',
    reason='MEDIA_POLICY_CONFIDENCE_BELOW_REQUIRED_THRESHOLD',http_status=200)})

class Availability(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.evidence=self.root/'iald_jev_connection_evidence.json'
        self.evidence.write_text(json.dumps(EVIDENCE),encoding='utf-8')
        self.rows=[copy.deepcopy(FAILED),copy.deepcopy(SELECTED)];self.backend_status='ready'
        self.ns=dict(ROOT=self.root,Path=Path,json=json,hashlib=hashlib,report=lambda:self.rows,
            backend=lambda:NS(availability=lambda:dict(status=self.backend_status)))
        tree=ast.parse((HERE/'iald_auto_router.py').read_bytes())
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('available','_verified_local_routing_refusal')]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual availability AST','exec'),self.ns)
    def available(self):return self.ns['available']()
    def test_real_policy_refusal_pinned_received_transport_preserves_prior_selected(self):
        before=copy.deepcopy(self.rows)
        self.assertTrue(self.available());self.assertEqual(self.rows,before)
        self.assertEqual(self.rows[0]['status'],'failed_or_uncertain')
    def test_backend_unavailable_still_false(self):
        for status in ('awaiting_access','unavailable','invalid_activation_record'):
            self.backend_status=status;self.assertFalse(self.available())
    def test_real_network_auth_and_unknown_stay_closed(self):
        for error in ('ConnectionError','Timeout','HTTPError','ValueError','KeyError','Unknown'):
            failure=dict(status='failed_or_uncertain',error_type=error)
            for rows in ([failure,SELECTED],[FAILED,failure,SELECTED]):
                self.rows=rows;self.assertFalse(self.available())
    def test_no_selected_no_invented_success(self):
        for rows in ([],[FAILED],[dict(status='started'),FAILED]):
            self.rows=rows;self.assertFalse(self.available())
    def test_missing_tampered_evidence_and_unproven_budget_failure_fail_closed(self):
        self.evidence.unlink();self.assertFalse(self.available())
        changed=copy.deepcopy(EVIDENCE);changed['verified_local_refusals'][row_hash]['response_artifact_sha256']='0'*64
        self.evidence.write_text(json.dumps(changed));self.assertFalse(self.available())
        self.evidence.write_text(json.dumps(EVIDENCE));self.rows[0]['id']='changed';self.assertFalse(self.available())
    def test_future_response_health_local_only_and_inflight(self):
        healthy=dict(status='failed_or_uncertain',error_type='BudgetRefusal',connection_health=dict(status='response_received',http_status=200,model='jev-1.13.0',response_sha256='a'*64))
        self.rows=[dict(status='started'),healthy,SELECTED];self.assertTrue(self.available())
        healthy['connection_health']['http_status']=401;self.assertFalse(self.available())
        healthy['connection_health']['http_status']=200;healthy['error_type']='HTTPError';self.assertFalse(self.available())

if __name__=='__main__':unittest.main(verbosity=2)
