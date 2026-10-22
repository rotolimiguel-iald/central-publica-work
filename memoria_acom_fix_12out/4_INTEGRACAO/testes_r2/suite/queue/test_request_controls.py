"""Provider locks, maximum capacity and uncertain outcomes; no remote calls."""
from contextlib import ExitStack
from pathlib import Path
import json, tempfile, unittest, uuid
from unittest.mock import patch, MagicMock
from iald_orchestrator import canonical_memory as memory, providers, request_controls as controls, mimo
from iald_orchestrator.runtime import Runtime

def constraints(provider='mimo'):
    return dict(mission_id='ORDEM_016',branch_id='A2.3',lemma_id='A2.3.a',role='draft',required_provider=provider,max_calls=1)

def connections():
    return [dict(id=n,status='ready',tier='advanced',billing='authorized_api' if n=='mimo' else 'subscription',billing_authorized=True,context_budget=1048576,output_token_budget=131072,daily_run_limit=None) for n in ('claude','kimi','mimo')]

class ControlsTests(unittest.TestCase):
    def test_bench_mission_is_named_and_other_missions_stay_closed(self):
        bench = dict(constraints('kimi'), mission_id='TGL_BANCADA_OFICIAL',
                     branch_id='cockpit-v2', lemma_id='architecture')
        self.assertEqual(controls.normalize(bench)['required_provider'], 'kimi')
        self.assertEqual(self.runtime.preview('Teste', bench)['selected'], 'kimi')
        with self.assertRaises(ValueError):
            controls.normalize(dict(bench, mission_id='UNRELATED'))
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.stack=ExitStack()
        self.stack.enter_context(patch.object(Runtime,'source_status',return_value={'ok':True}))
        self.stack.enter_context(patch.object(providers,'discover',side_effect=connections))
        self.packet={'prompt':'canonical sources '+('x'*50000),'receipt':{'generation':'a'*64,'sources':[{'file':'canon.md'}],'memory_mode':'maximum'}}
        self.packet['receipt']['packet_sha256']=memory.digest(self.packet['prompt'].encode())
        self.stack.enter_context(patch.object(memory,'prepare',return_value=self.packet))
        self.runtime=Runtime(self.root,recover=False)
    def tearDown(self):self.stack.close();self.temp.cleanup()
    def test_required_executor_never_falls_back(self):
        with patch.object(providers,'execute') as execute:
            self.assertEqual(self.runtime.preview('Teste',constraints())['selected'],'mimo')
            rows=connections();rows[2]['status']='unavailable'
            with patch.object(providers,'discover',return_value=rows):
                with self.assertRaises(ValueError):self.runtime.submit('Teste',str(uuid.uuid4()),execution_constraints=constraints(),start_worker=False)
            execute.assert_not_called()
    def test_uncertain_result_consumes_unit_without_retry(self):
        c=constraints();rid=str(uuid.uuid4())
        with patch.object(providers,'execute',side_effect=TimeoutError) as execute:
            task=self.runtime.submit('Teste',rid,execution_constraints=c,start_worker=False)
            self.runtime._drain()
            self.assertEqual(self.runtime.task(task['id'])['status'],'failed')
            same=self.runtime.submit('Teste',rid,execution_constraints=c,start_worker=False)
            self.runtime._drain();self.assertEqual(same['id'],task['id']);self.assertEqual(execute.call_count,1)
            with self.assertRaises(ValueError):self.runtime.submit('Teste',rid,execution_constraints=constraints('kimi'),start_worker=False)
    def test_maximum_providers_ignore_old_daily_branch_and_lemma_caps(self):
        with self.runtime.db() as db:
            for i in range(45):
                db.execute('INSERT INTO request_budget_ledger VALUES(?,?,?,?,?,?,?,?,?,?,NULL)',(str(i),'ORDEM_016','A2.3','A2.3.a','draft','kimi','2099','0','0','RETURNED'))
            for n in ('mimo','kimi'):controls.check(db,controls.normalize(constraints(n)),{})
            with self.assertRaises(ValueError):controls.check(db,controls.normalize(constraints('claude')), {})
    def test_source_and_generation_restrictions_remain(self):
        for extra in ({'allowed_sources':['other.md']},{'memory_generation':'b'*64}):
            with self.assertRaises(ValueError):self.runtime.preview('Teste',dict(constraints(),**extra))
    def test_wrong_provider_rejected_before_transport(self):
        with patch('iald_orchestrator.kimi.execute') as execute:
            from iald_orchestrator import operational_memory as om
            c=controls.normalize(constraints())
            packet=om.attach(self.packet,om.preview_projection('Teste',c),providers.SYSTEM,'mimo',c)
            with self.assertRaises(ValueError):providers.execute('kimi','Teste',self.root,memory_packet=packet,execution_constraints=c)
            execute.assert_not_called()
    def test_large_packet_not_cut_to_old_transport_cap(self):
        for name in ('mimo','kimi'):
            with patch(f'iald_orchestrator.{name}.connection_status',return_value='ready'),patch(f'iald_orchestrator.{name}.execute',return_value={'text':'ok','usage':{}}) as execute:
                from iald_orchestrator import operational_memory as om
                c=controls.normalize(constraints(name))
                packet=om.attach(self.packet,om.preview_projection('Teste',c),providers.SYSTEM,name,c)
                providers.execute(name,'Teste',self.root,memory_packet=packet,execution_constraints=c)
                sent=execute.call_args.args[0];self.assertIn(self.packet['prompt'],sent);self.assertNotIn('1500 palavras',sent)
    def test_mimo_payload_uses_maximum_output_and_thinking(self):
        response=MagicMock();response.__enter__.return_value.read.return_value=b'{}'
        opener=MagicMock();opener.open.return_value=response
        with patch.object(mimo,'authorization',return_value={'enabled':True}),patch.object(mimo,'load_mimo',return_value='fixture-only'),patch.object(mimo.urllib.request,'build_opener',return_value=opener),patch.object(mimo,'read_stream',return_value={}),patch.object(mimo,'parse_response',return_value={'text':'ok'}):
            mimo.execute('x'*50000)
        payload=json.loads(opener.open.call_args.args[0].data)
        self.assertEqual(payload['max_completion_tokens'],131072);self.assertEqual(payload['thinking'],{'type':'enabled'})
    def test_unknown_restrictions_and_stale_financial_cap_rejected(self):
        for extra in ({'ignored':True},{'max_cost_usd':'0.50'}):
            with self.assertRaises(ValueError):controls.normalize(dict(constraints(),**extra))
    def test_measured_accounting_is_not_a_billing_claim(self):
        c=controls.normalize(constraints());r={'model':mimo.MODEL,'usage':{'prompt_tokens':100000,'completion_tokens':10000,'total_tokens':110000}}
        with self.runtime.db() as db:
            controls.reserve(db,'one',c,controls.quote(c),'2026')
            controls.settle(db,'one',c,r)
            with self.assertRaises(ValueError):controls.reserve(db,'one',c,controls.quote(c),'2026')
        self.assertEqual(r['request_cost_accounting']['status'],'MEASURED_TOKENS_PRICED_NOT_INVOICE')

class MaximumMemoryTests(unittest.TestCase):
    def test_maximum_memory_grows_past_old_cap_but_preserves_scope(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'um_absoluto_forma_canonica.md';source.write_text(('Canonical mathematical source.\n'*3000),encoding='utf-8')
            catalog=root/'catalog.json';catalog.write_text(json.dumps({'files':[{'source':str(source),'sha256':memory.digest(source.read_bytes())}]}))
            memory.build(root/'index',catalog)
            small=memory.prepare('Canonical',root/'index');large=memory.prepare('Canonical',root/'index',mode='maximum')
            self.assertGreater(large['receipt']['context_bytes'],small['receipt']['context_bytes']*3)
            self.assertLess(large['receipt']['context_bytes'],mimo.MAX_INPUT_BYTES)
            self.assertEqual(large['receipt']['coverage'],'PARTIAL_RETRIEVAL_NOT_FULL_CORPUS')
            with self.assertRaises(ValueError):memory.prepare('Canonical',root/'index',mode='maximum',allowed_sources=['absent'])

if __name__=='__main__':unittest.main()
