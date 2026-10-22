"""Offline fixtures only. Router functions compiled from staged AST, no runtime imports."""
from pathlib import Path
import ast, copy, hashlib, importlib.util, json, tempfile, types, unittest, uuid, time
from datetime import datetime, timezone
from unittest.mock import Mock

S=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda b:hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('staged_control',S/'iald_jev_control.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
contract=json.loads((S/'jev_control_v394_v2_bound_R2.json').read_bytes())
baseline=json.loads((S/'BUILD_EVIDENCE_R2.json').read_bytes())

class ProjectionOverflow(Exception):
    def __init__(self,n):self.required_chars=n

def router_namespace():
    names={'memory_slice','_auditable_projection','_fit_routing_payload','choose'}
    tree=ast.parse((S/'iald_auto_router.py').read_bytes())
    tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    ns=dict(ROOT=S,jev_control=c,Path=Path,json=json,hashlib=hashlib,uuid=uuid,
            datetime=datetime,timezone=timezone,time=time,RoutingContextOverflow=type('RoutingContextOverflow',(Exception,),{}))
    exec(compile(tree,str(S/'iald_auto_router.py'),'exec'),ns)
    return ns

def common_packet(optional=0,required=100):
    # Explicit SYNTHETIC receipt; never presented as real ledger custody.
    text='M'*required+'O'*optional
    return dict(memory_id='synthetic-offline-fixture',projection=text,
        projection_receipt=dict(context_id='synthetic-offline-fixture',revision=1,
            state_sha256=sha(b'synthetic-full-state'),event_hash=sha(b'synthetic-event')),
        coverage=dict(required_chars=required,actual_chars=len(text),omitted_records=0,
            projection_sha256=sha(text.encode())))

class Integration(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=S,prefix='offline_')
        self.root=Path(self.temp.name)
        self.ns=router_namespace()
        self.c=copy.deepcopy(contract)
        self.m=json.loads((S/'iald_nucleo_fixo.json').read_bytes())
        # Scientific fixture files are data, never executed/imported.
        for field,pin in [('program','source_sha256'),('result','result_sha256'),('proof_manifest','proof_manifest_sha256')]:
            p=self.root/(field+'.txt');p.write_bytes(('fixture-'+field).encode())
            self.c[pin]=sha(p.read_bytes());self.m['published_evidence'][field]['path']=str(p)
        for key in ['operational_core','active_cluster']:
            p=self.root/(key+'.txt');p.write_bytes(('fixture-'+key).encode())
            self.m[key].update(path=str(p),sha256=sha(p.read_bytes()),release_source_sha256=self.c['source_sha256'])
        cp=S/'core_packet_v394_bound_R2.txt'
        (self.root/cp.name).write_bytes(cp.read_bytes())
        canonical=self.root/'canonical.md'
        canonical.write_bytes(cp.read_bytes().decode('utf-8-sig').replace('\r\n','\n').encode()+b'\nadditional fixture fields')
        source=next(e for e in self.m['entries'] if e['id']=='um_forma_canonica_integral')
        source.update(path=str(canonical),public_sha256=sha(canonical.read_bytes()))
        self.bind()
    def tearDown(self):self.temp.cleanup()
    def bind(self):
        p=self.root/'contract.json';p.write_bytes(json.dumps(self.c,ensure_ascii=False).encode())
        self.m['jev_control'].update(path=str(p),sha256=sha(p.read_bytes()),source_sha256=self.c['source_sha256'])
        (self.root/'iald_nucleo_fixo.json').write_bytes(json.dumps(self.m,ensure_ascii=False).encode())
    def reject(self,fn,*args,**kw):
        with self.assertRaises((c.ControlError,ValueError)):fn(*args,**kw)
    def body(self,common=None):
        text,source=c.load_core_packet(self.root,self.c)
        body=dict(model=c.MODEL,state=dict(canonical_memory=text,source=source,iald_control=c.contract_state(self.c)),questions={'axis':{'type':'choice','criteria':{'yes':'yes'}}})
        if common is not None:body['state']['common_memory']=common
        return body
    def test_v2_load_complete(self):
        self.assertEqual(c.load_contract(self.root),self.c)
        text,source=self.ns['memory_slice'](self.root,self.c)
        self.assertEqual(len(text),8000);self.assertEqual(source['packet_bytes'],8429)
        self.assertEqual(source['sha256_da_fonte'],sha((S/'core_packet_v394_bound_R2.txt').read_bytes()))
    def test_v1_compatible_without_packet(self):
        self.c={k:v for k,v in self.c.items() if k in c.CONTRACT_KEYS};self.c['schema']=c.SCHEMA
        self.bind();(self.root/'core_packet_v394_bound_R2.txt').unlink()
        self.assertEqual(c.load_contract(self.root)['schema'],c.SCHEMA)
        text,source=self.ns['memory_slice'](self.root,self.c)
        self.assertEqual(len(text),8000);self.assertNotIn('packet_sha256',source)
    def test_altered_packet(self):
        p=self.root/'core_packet_v394_bound_R2.txt';p.write_bytes(p.read_bytes()+b'x')
        self.reject(c.load_contract,self.root)
    def test_rehashed_wrong_excerpt(self):
        p=self.root/'core_packet_v394_bound_R2.txt';p.write_bytes(b'wrong')
        self.c['core_packet']['sha256']=sha(p.read_bytes());self.bind()
        self.reject(c.load_contract,self.root)
    def test_wrong_packet_version(self):
        self.c['core_packet']['um_version']='v393';self.bind();self.reject(c.load_contract,self.root)
    def test_missing_packet(self):
        (self.root/'core_packet_v394_bound_R2.txt').unlink();self.reject(c.load_contract,self.root)
    def test_packet_path_escape(self):
        self.c['core_packet']['arquivo']='../escape';self.bind();self.reject(c.load_contract,self.root)
    def test_altered_canonical(self):
        (self.root/'canonical.md').write_bytes(b'changed');self.reject(c.load_contract,self.root)
    def test_v2_admission_does_not_truncate_or_duplicate(self):
        body=self.body();body['state']['mandatory']='X'*40000
        before=body['state']['canonical_memory'];admission=self.ns['_fit_routing_payload'](body)
        self.assertEqual(admission['context_mode'],'long');self.assertEqual(body['state']['canonical_memory'],before)
        self.assertEqual(sum(v==before for v in body['state'].values() if isinstance(v,str)),1)
    def test_optional_only_projection_and_custody_pointer(self):
        initial=common_packet(60000)
        def project(max_chars):
            result=common_packet(max(0,max_chars-100));result['coverage']['omitted_records']=1
            return result
        self.ns['app_memory']=types.SimpleNamespace(routing_state=project,ProjectionOverflow=ProjectionOverflow)
        body=self.body(initial);text=body['state']['canonical_memory']
        self.ns['_fit_routing_payload'](body)
        p=body['state']['holographic_projection']
        self.assertEqual(p['full_state_pointer'],initial['projection_receipt'])
        self.assertGreater(p['omitted_optional_records'],0)
        self.assertTrue(body['state']['common_memory']['projection'].startswith('M'*100))
        self.assertEqual(body['state']['canonical_memory'],text)
        self.assertEqual(p['inscrito_por']['scope'],'projection_not_original_authorship')
    def test_mandatory_overflow_visible(self):
        body=self.body(common_packet(0,300000));self.ns['app_memory']=types.SimpleNamespace(ProjectionOverflow=ProjectionOverflow)
        with self.assertRaises(self.ns['RoutingContextOverflow']):self.ns['_fit_routing_payload'](body)
        self.assertEqual(len(body['state']['common_memory']['projection']),300000)
        self.assertEqual(len(body['state']['canonical_memory']),8000)
    def test_projection_tampering(self):
        value=common_packet();value['projection']+='tamper'
        self.reject(self.ns['_auditable_projection'],value)
    def test_missing_custody_visible(self):
        value=common_packet();del value['projection_receipt']['state_sha256']
        self.reject(self.ns['_auditable_projection'],value)
    def test_revision_change_refuses_projection(self):
        initial=common_packet(60000)
        projected=common_packet();projected['projection_receipt']['revision']=2
        self.ns['app_memory']=types.SimpleNamespace(routing_state=lambda **kw:projected,ProjectionOverflow=ProjectionOverflow)
        self.reject(self.ns['_fit_routing_payload'],self.body(initial))
    def test_terminal_receipt_and_no_reentry(self):
        receipt=c.new_receipt('fixture',self.c['source_sha256'],['kimi'],contract=self.c)
        for target in ['inscribed','observed','resolved']:receipt=c.transition(receipt,target)
        self.assertEqual(receipt['stopping_receipt']['transitions'],3)
        self.assertEqual(receipt['stopping_receipt']['history_sha256'],c.digest(receipt['history']))
        self.reject(c.transition,receipt,'inscribed')
    def test_bounded_pruning_reserves_refusal(self):
        self.c['stopping_criterion']['max_transicoes']=3
        receipt=c.new_receipt('fixture',self.c['source_sha256'],['kimi','mimo'],contract=self.c)
        for target in ['inscribed','observed']:receipt=c.transition(receipt,target)
        self.reject(c.transition,receipt,'pruned',candidates=['mimo'])
        receipt=c.transition(receipt,'refused')
        self.assertEqual(receipt['stopping_receipt']['verdict'],'refused');self.reject(c.transition,receipt,'inscribed')
    def test_budget_too_small_before_transport(self):
        self.c['stopping_criterion']['max_transicoes']=2
        self.reject(c.new_receipt,'fixture',self.c['source_sha256'],['kimi'],contract=self.c)
    def test_graph_and_no_candidate_expansion(self):
        receipt=c.new_receipt('fixture',self.c['source_sha256'],['kimi'],contract=self.c)
        self.reject(c.transition,receipt,'resolved')
        receipt=c.transition(receipt,'inscribed');receipt=c.transition(receipt,'observed')
        self.reject(c.transition,receipt,'pruned',candidates=['mimo'])
    def test_v1_receipt_unchanged(self):
        value=c.new_receipt('fixture',self.c['source_sha256'],['kimi'])
        self.assertNotIn('host_policy',value)
        for target in ['inscribed','observed','resolved']:value=c.transition(value,target)
        self.assertNotIn('stopping_receipt',value)
    def test_permission_and_private_tools_fail_closed(self):
        offered=c.questions(False,False);chosen={'scientific_mode':'explanation','work_path':'retrieve','memory_action':'verify_sources'}
        answers={k:dict(type='choice',choice=chosen[k],confidence=1,probabilities={v:int(v==chosen[k]) for v in q['criteria']}) for k,q in offered.items()}
        decision=c.resolve(answers,['mimo'],{},False)
        self.assertFalse(decision['authorization_granted'])
        self.assertEqual(c.allowed_tool_names(decision,['fetch_tgl','private_secret','bench_run']),['fetch_tgl'])
        answers['work_path']['choice']='operator_bench';self.reject(c.resolve,answers,['mimo'],{},False)
    def test_mock_dispatch_error_single_call_persisted(self):
        ns=self.ns
        ns.update(DESCRIPTIONS={'kimi':'text'},backend=lambda:types.SimpleNamespace(availability=lambda:dict(status='ready'),validate_prompt=lambda x:None,ENDPOINT='offline://fixture',_key=lambda:'synthetic-not-a-key'),
            available=lambda:True,observations=lambda *a:{},bootstrap_intent=types.SimpleNamespace(classify=lambda p:None),
            task_policy=types.SimpleNamespace(model_identities=lambda c,m:{'kimi':None},automatic_candidates=lambda c:c,classify=lambda p:{},eligible_managers=lambda c,t:c,
                capability_catalog=lambda *a,**kw:{},executor_criteria=lambda *a:{'kimi':'text'}),
            execution_guide=types.SimpleNamespace(strategy_question=lambda w:{'type':'choice','criteria':{'direct':'direct'}},routing_guide=lambda *a,**kw:{},VERSION='offline-fixture'),
            wallet_runtime=types.SimpleNamespace(enabled=lambda:False,routing_begin=lambda x:None,routing_end=lambda *a:None))
        post=Mock(side_effect=TimeoutError('synthetic-no-network'))
        ns['app_memory']=types.SimpleNamespace(routing_state=lambda:None,http_call=lambda name,fn,*a,**kw:fn(*a,**kw))
        with self.assertRaises(TimeoutError):ns['choose']('offline test',['kimi'],root=self.root,post=post)
        self.assertEqual(post.call_count,1)
        records=list((self.root/'.iald_runtime/app_routing').glob('*.json'));self.assertEqual(len(records),1)
        value=json.loads(records[0].read_bytes());self.assertEqual(value['calls'],1)
        self.assertEqual(value['regime']['stopping_receipt']['verdict'],'uncertain')
        self.assertIn('FAILED_OR_UNCERTAIN_NO_RETRY',value['transitions'])
    def test_other_ast_guards_preserved(self):
        allow={'iald_jev_control.py':{'load_core_packet','load_contract','new_receipt','transition'},
               'iald_auto_router.py':{'memory_slice','_auditable_projection','_fit_routing_payload','choose'}}
        for name,changed in allow.items():
            before=ast.parse((R/name).read_bytes());after=ast.parse((S/name).read_bytes())
            strip=lambda t:ast.dump(ast.Module(body=[n for n in t.body if not (isinstance(n,ast.FunctionDef) and n.name in changed)],type_ignores=[]),include_attributes=False)
            self.assertEqual(strip(before),strip(after),name)
    def test_manifest_minimal_and_all_plan_bytes(self):
        before=json.loads((R/'iald_nucleo_fixo.json').read_bytes());after=json.loads((S/'iald_nucleo_fixo.json').read_bytes())
        for key in ('path','sha256'):before['jev_control'].pop(key);after['jev_control'].pop(key)
        self.assertEqual(before,after)
        for item in json.loads((S/'install_plan_R2.json').read_bytes())['files']:
            self.assertEqual(sha(Path(item['source']).read_bytes()),item['sha256'])
            self.assertTrue(Path(item['source']).is_relative_to(S))
            dest=Path(item['destination']);self.assertEqual(sha(dest.read_bytes()) if dest.exists() else None,item['baseline'])
    def test_original_contract_and_inventory_not_modified(self):
        self.assertEqual(sha(Path(baseline['original_v2']['path']).read_bytes()),baseline['original_v2']['sha256'])
        for name,pin in baseline['baseline'].items():self.assertEqual(sha((R/name).read_bytes()),pin)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Integration)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    evidence=dict(schema='iald.offline-tests.v1',status='PASS' if result.wasSuccessful() else 'FAIL',
        tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        synthetic_fixtures=True,provider_requests=0,runtime_imports=0,scientific_execution=False,
        files={n:sha((S/n).read_bytes()) for n in ['iald_jev_control.py','iald_auto_router.py','test_integration_R2.py']},
        cases=sorted(unittest.defaultTestLoader.getTestCaseNames(Integration)))
    target=S/'TEST_RESULTS_R2.json'
    if target.exists():raise RuntimeError('Never overwrite test evidence; choose a new result name')
    with target.open('xb') as f:f.write(json.dumps(evidence,ensure_ascii=False,indent=2).encode())
    raise SystemExit(0 if result.wasSuccessful() else 1)
