"""Offline tests. No production imports; no credentials, accounts or network."""
import ast
import hashlib
import io
import itertools
import json
from pathlib import Path
import socket
import sqlite3
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT/'patched'), str(ROOT/'baseline')]
memory = types.ModuleType('iald_app_memory')
memory.routing_state = lambda: None
memory.routing_result = Mock()
wallet = types.ModuleType('iald_wallet_runtime')
wallet.enabled = lambda: False
wallet.routing_begin = Mock(return_value='wallet-event')
wallet.routing_end = Mock()
sys.modules['iald_app_memory'] = memory
sys.modules['iald_wallet_runtime'] = wallet
import iald_auto_router as router
import iald_task_policy as policy


def extracted(filename, name, namespace):
    tree = ast.parse((ROOT/'baseline'/filename).read_text(encoding='utf-8'))
    nodes = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(nodes) == 1, (name, len(nodes))
    exec(compile(ast.Module(body=nodes,type_ignores=[]),filename,'exec'),namespace)
    return namespace[name]


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT)
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(patch.stopall)
        patch.object(socket.socket,'connect',side_effect=AssertionError('Network forbidden')).start()
        self.backend = types.SimpleNamespace(availability=lambda:{'status':'ready'},
            validate_prompt=lambda p:None, ENDPOINT='offline://jev', _key=lambda:'offline-fixture')
        patch.object(router,'backend',return_value=self.backend).start()
        self.control={'release':'fixture','source_sha256':hashlib.sha256(b'fixture').hexdigest()}
        patch.object(router,'memory_slice',return_value=('fixture memory',dict(self.control,release_source_sha256=self.control['source_sha256']))).start()
        patch.object(router.jev_control,'load_contract',return_value=self.control).start()
        patch.object(router.jev_control,'contract_state',side_effect=lambda c:c).start()
        patch.object(router.jev_control,'resolve',side_effect=lambda *a,**k:dict(work_path=self.work_path)).start()
        self.work_path='answer'
        self.calls=0
        self.proposal='openai'
        self.confidence=.95
        self.body=None
        memory.routing_result.reset_mock()
        wallet.routing_end.reset_mock()

    def post(self,*a,**kw):
        self.calls+=1
        self.body=kw['json']
        answers={}
        for name,q in self.body['questions'].items():
            keys=list(q['criteria'])
            chosen=self.proposal if name=='executor' else ('direct' if name=='collaboration' else keys[0])
            answers[name]={'type':'choice','choice':chosen,'confidence':self.confidence,
                'probabilities':{k:float(k==chosen) for k in keys}}
        return types.SimpleNamespace(status_code=200,json=lambda:{'model':'jev-1.13.0','answers':answers,'usage':{'input_tokens':100}})

    def choose(self,candidates,prompt='Olá',**kwargs):
        return router.choose(prompt,candidates,root=self.root,post=self.post,validation_probe=True,**kwargs)

    def test_conversation_host_overrides_valid_jev_preference(self):
        chosen,receipt=self.choose(['claude-haiku','openai','mimo','kimi'])
        self.assertEqual(chosen,'kimi')
        self.assertEqual(receipt['choice'],'openai')
        self.assertEqual(receipt['operator_preference']['selected'],'kimi')
        self.assertEqual(receipt['candidates'],['kimi','mimo','openai'])
        self.assertEqual(self.calls,1)
        memory.routing_result.assert_called_once()
        wallet.routing_end.assert_called_once()

    def test_mimo_when_kimi_missing(self):
        self.assertEqual(self.choose(['openai','mimo'])[0],'mimo')

    def test_code_manager_requires_tools(self):
        self.assertEqual(self.choose(['kimi','mimo','openai','claude-sonnet'],'Revise código Python')[0],'mimo')
        self.assertNotIn('kimi',self.body['questions']['executor']['criteria'])

    def test_code_worker_prefers_kimi(self):
        self.proposal='mimo'
        self.assertEqual(self.choose(['mimo','kimi'],'Etapa implement: código Python',worker=True)[0],'kimi')

    def test_delegation_text_also_prefers_kimi(self):
        self.proposal='mimo'
        self.assertEqual(self.choose(['mimo','kimi'],'Etapa review: resumo',worker=True)[0],'kimi')

    def test_tool_projection_precedes_preference(self):
        self.proposal='kimi';self.work_path='retrieve'
        self.assertEqual(self.choose(['kimi','mimo','openai'])[0],'mimo')

    def test_operator_bench_excludes_kimi(self):
        self.assertEqual(self.choose(['kimi','openai','mimo'],operator_context={})[0],'mimo')

    def test_jev_selects_claude_refused_no_retry(self):
        self.proposal='claude-haiku'
        with self.assertRaisesRegex(ValueError,'candidate_mismatch'):
            self.choose(['claude-haiku','mimo','openai'])
        self.assertEqual(self.calls,1)
        self.assertEqual(router.report(self.root)[0]['status'],'failed_or_uncertain')
        memory.routing_result.assert_not_called()

    def test_jev_selects_noneligible_refused(self):
        self.proposal='kimi'
        with self.assertRaises(ValueError):self.choose(['mimo','openai'])
        self.assertEqual(self.calls,1)

    def test_only_claude_no_jev_call(self):
        with self.assertRaisesRegex(ValueError,'non-Claude'):self.choose(['claude-haiku','claude-sonnet'])
        self.assertEqual(self.calls,0)

    def test_kimi_cannot_manage_artifacts(self):
        with self.assertRaisesRegex(ValueError,'capable'):self.choose(['kimi'],'Crie planilha')
        self.assertEqual(self.calls,0)

    def test_low_confidence_single_eligible_kimi(self):
        self.proposal='kimi';self.confidence=.4
        self.assertEqual(self.choose(['kimi'])[0],'kimi')

    def test_uncertain_send_no_fallback(self):
        post=Mock(side_effect=TimeoutError('offline uncertainty'))
        with self.assertRaises(TimeoutError):
            router.choose('Olá',['mimo','kimi'],root=self.root,post=post,validation_probe=True)
        post.assert_called_once()
        self.assertEqual(router.report(self.root)[0]['regime']['state'],'uncertain')

    def test_all_subsets_and_order_independence(self):
        keys=['kimi','mimo','openai','deepseek','nativa','claude-haiku','claude-sonnet']
        for flags in itertools.product((False,True),repeat=len(keys)):
            candidates=[k for k,f in zip(keys,flags) if f]
            result=policy.automatic_candidates(candidates)
            self.assertLessEqual(set(result),set(candidates))
            self.assertFalse(any(k.startswith('claude') for k in result))
            self.assertEqual(result,policy.automatic_candidates(list(reversed(candidates))))
            if 'kimi' in candidates:self.assertEqual(result[0],'kimi')
            elif 'mimo' in candidates:self.assertEqual(result[0],'mimo')

    def test_unknown_provider_rejected(self):
        with self.assertRaises(ValueError):self.choose(['unapproved'])
        self.assertEqual(self.calls,0)

    def test_manual_luiz_and_account_lock_preserved(self):
        self.assertTrue(router.manual_allowed({'plano':'operador'},'luiz'))
        self.assertFalse(router.manual_allowed({'plano':'operador'},'someone-else'))
        self.assertFalse(router.manual_allowed({'bloqueado':True},'luiz'))
        lease=router.acquire('offline-user')
        try:self.assertIsNone(router.acquire('offline-user'))
        finally:lease.release()

    def test_public_kimi_permission_preserved(self):
        allowed=extracted('iald_app_providers.py','allowed',{'MODELS':{'kimi':{},'mimo':{},'deepseek':{}}})
        self.assertTrue(allowed({'plano':'gratuito'},'public-fixture','kimi'))
        self.assertFalse(allowed({'bloqueado':True},'public-fixture','kimi'))
        self.assertFalse(allowed({},'public-fixture','kimi'))
        self.assertFalse(allowed({'plano':'gratuito'},'public-fixture','claude-sonnet'))

    def test_real_delegate_options_consent_quota_availability(self):
        # Execute the host's unchanged nested options function, not a mirror.
        consent={'kimi':True,'mimo':True};budget={'kimi':True,'mimo':True}
        rows=[{'id':k,'disponivel':True} for k in consent]
        options=extracted('iald_web_server.py','options',dict(authorize=lambda:{'plano':'gratuito'},user='public-fixture',
            app_providers=types.SimpleNamespace(options=lambda *a:rows),
            iald_motores=types.SimpleNamespace(consentiu=lambda r,k:consent[k]),
            _automatic_budget_available=lambda r,u,k:budget[k]))
        self.assertEqual(policy.preferred_executor(options()),'kimi')
        consent['kimi']=False
        self.assertEqual(policy.preferred_executor(options()),'mimo')
        consent['kimi']=True;budget['kimi']=False
        self.assertEqual(policy.preferred_executor(options()),'mimo')
        budget['kimi']=True;rows[0]['disponivel']=False
        self.assertEqual(policy.preferred_executor(options()),'mimo')
        consent['mimo']=False
        self.assertEqual(options(),[])

    def test_baseline_byte_hashes(self):
        for row in json.loads((ROOT/'baseline.json').read_text(encoding='utf-8-sig')):
            self.assertEqual(hashlib.sha256((ROOT/'baseline'/row['name']).read_bytes()).hexdigest(),row['sha256'])

    def test_source_change_refuses_dispatch(self):
        patch.object(router.jev_control,'load_contract',side_effect=[self.control,dict(self.control,release='changed')]).start()
        with self.assertRaisesRegex(ValueError,'changed during routing'):self.choose(['mimo','openai'])
        memory.routing_result.assert_not_called()
        self.assertEqual(self.calls,1)

    def test_budget_reservations_exhaust_and_isolate_accounts(self):
        path=self.root/'budget.sqlite3'
        class ClosingConnection(sqlite3.Connection):
            def __exit__(self,*args):
                try:return super().__exit__(*args)
                finally:self.close()
        connect=lambda:sqlite3.connect(path,factory=ClosingConnection)
        with connect() as db:
            db.execute('CREATE TABLE calls (day TEXT,user TEXT,cap REAL,actual REAL,quota_key TEXT,group_name TEXT)')
            db.execute('INSERT INTO calls VALUES (?,?,?,?,?,?)',('2026-10-14','other',4,None,'other','group'))
        guard=types.SimpleNamespace(check=lambda *a:None,clock=lambda:datetime(2026,10,14,tzinfo=timezone.utc),_connect=connect)
        self.assertTrue(router.budget_remaining(guard,'me',1,10,quota_key='me'))
        with connect() as db:
            db.execute('INSERT INTO calls VALUES (?,?,?,?,?,?)',('2026-10-14','me',1,None,'me','group'))
        self.assertFalse(router.budget_remaining(guard,'me',1,10,quota_key='me'))
        self.assertFalse(router.budget_remaining(guard,'third',1,5,quota_key='third'))

    def test_manual_permission_and_budget_functions_unchanged(self):
        before=ast.parse((ROOT/'baseline/iald_auto_router.py').read_text(encoding='utf-8'))
        after=ast.parse((ROOT/'patched/iald_auto_router.py').read_text(encoding='utf-8'))
        for name in ('allowed','manual_allowed','default_for','acquire','budget_remaining','bind_scope','route_instruction'):
            nodes=[next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name) for tree in (before,after)]
            self.assertEqual(ast.dump(nodes[0]),ast.dump(nodes[1]))


if __name__=='__main__':
    output=io.StringIO()
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RoutingTests))
    (ROOT/'testreport.txt').write_text(output.getvalue(),encoding='utf-8')
    report={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'passed':result.wasSuccessful(),'network_calls':0,'scope':'offline staged code; host I/O mocked; no live accounts or providers'}
    (ROOT/'testreport.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(output.getvalue());sys.exit(not result.wasSuccessful())
