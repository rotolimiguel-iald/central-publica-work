from pathlib import Path
import importlib.util,json,socket,sys,unittest,types
from unittest.mock import patch
W=Path(__file__).resolve().parents[1]
def deny(*a,**k): raise AssertionError('Independent review forbids network')
socket.socket.connect=deny
socket.socket.connect_ex=deny
socket.create_connection=deny
socket.getaddrinfo=deny
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
fix=load('review_fix',W/'test_fix.py')
from iald_memory import ScopeViolation
semantic=load('review_semantic',W/'semantic/test_bootstrap_intent.py')
class Independent(fix.Regression):
    def test_wallet_refusal_before_provider(self):
        with patch.object(fix.router.wallet_runtime,'enabled',return_value=True),patch.object(fix.router.wallet_runtime,'current',return_value=types.SimpleNamespace(routing_state=lambda:{'remaining':'0','admitted':False})),patch.object(fix.router.wallet_runtime,'routing_begin',side_effect=PermissionError('No paid admission')):
            with self.assertRaises(PermissionError):self.choose()
        self.assertEqual(self.calls,0)
    def test_scope_and_conversation_isolation(self):
        self.answer_then_followup()
        self.binding.append('private','OWNER_A_PRIVATE_DECISION',kind='decision',statute='INPUT',source_kind='operator')
        other=fix.memory.begin(self.root,'other-owner','testconversation',[{'role':'user','content':'OTHER_OBJECTIVE'}],'otherturn')
        with fix.memory.bound(other):
            _,r=fix.router.choose('haja luz',['mimo','openai'],root=self.root,post=self.post,validation_probe=True)
        self.assertNotIn('OWNER_A_PRIVATE_DECISION',self.body['state']['common_memory']['projection'])
        self.assertNotEqual(other.context_id,self.binding.context_id)
        with self.assertRaises(ScopeViolation):self.binding.store.get(self.binding.context_id,other.scope)
    def test_correction_lineage_and_flow_survive(self):
        self.answer_then_followup()
        snap=self.binding.snapshot()
        records=[dict(id='review.old',kind='decision',text='OLD_DECISION',statute='INPUT',sources=[dict(kind='operator',ref='review-source')]),dict(id='review.corrected',kind='decision',text='CORRECTED_DECISION',statute='INPUT',sources=[dict(kind='operator',ref='review-source')],supersedes='review.old')]
        self.binding.store.transition(self.binding.context_id,self.binding.scope,expected_revision=snap['revision'],event_id='review.correction',actor={'kind':'operator','id':'review'},changes={'records':records,'flow':{'phase':'requires_reconciliation','next_action':'DO_NOT_RESEND','handles':[{'id':'uncertain-call','status':'uncertain'}]}})
        self.continuity='reconcile';self.choose()
        text=self.body['state']['common_memory']['projection']
        for term in ('OLD_DECISION','CORRECTED_DECISION','DO_NOT_RESEND','uncertain-call'):self.assertIn(term,text)
    def test_full_wallet_and_operator_metadata_not_trimmed(self):
        self.answer_then_followup();wallet={'available_nano_usd':123,'permissions':['unchanged']}
        with patch.object(fix.router.wallet_runtime,'enabled',return_value=True),patch.object(fix.router.wallet_runtime,'current',return_value=types.SimpleNamespace(routing_state=lambda:wallet)):
            self.choose(operator_context={'review':'metadata retained'})
        self.assertEqual(self.body['state']['monthly_wallet'],wallet)
        self.assertEqual(self.body['state']['operator_context'],{'review':'metadata retained'})
suite=unittest.TestSuite()
suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(fix.Regression))
suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(semantic))
for name in ('test_wallet_refusal_before_provider','test_scope_and_conversation_isolation','test_correction_lineage_and_flow_survive','test_full_wallet_and_operator_metadata_not_trimmed'):suite.addTest(Independent(name))
r=unittest.TextTestRunner(verbosity=2).run(suite)
value={'passed':r.wasSuccessful(),'tests':r.testsRun,'failures':[(str(t),s) for t,s in r.failures],'errors':[(str(t),s) for t,s in r.errors],'network_calls':0,'transport':'synthetic post; socket calls denied before imports','production_runner_executed':False}
p=W/'validation/independent_tests.json'
if p.exists():
    import datetime
    p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(p.read_bytes())
tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8');assert tmp.stat().st_size>0;tmp.replace(p)
sys.exit(not r.wasSuccessful())
