"""Regression tests use a disposable ledger and simulated provider transport."""
import ast,hashlib,importlib.util,json,socket,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
W=Path(__file__).resolve().parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'staging'),str(R)]
import iald_auto_router as router
import iald_app_memory as memory

def previous_router():
    spec=importlib.util.spec_from_file_location('previous_router',W/'baseline/iald_auto_router.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

class Regression(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup);self.addCleanup(patch.stopall)
        patch.object(socket.socket,'connect',side_effect=AssertionError('Network forbidden')).start()
        patch.object(memory,'_SHARED_ROOT',self.root/'memory').start()
        self.first='IALD, apresente-se. Carregue a memória completa disponível da TGL e resolva o problema da gravidade quântica.'
        self.binding=memory.begin(self.root,'synthetic-owner','testconversation',[{'role':'user','content':self.first}],'turn1')
        self.calls=0;self.continuity='continue';self.bad=False;self.body=None;self.throw=False
        self.control=router.jev_control.load_contract(R)
        self.backend=types.SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda x:x,ENDPOINT='offline://jev',_key=lambda:'test-only')
        self.source={'release':self.control['release'],'release_source_sha256':self.control['source_sha256']}
        self.prepared(router)
    def prepared(self,mod):
        patch.object(mod,'backend',return_value=self.backend).start()
        patch.object(mod,'observations',return_value={}).start()
        patch.object(mod.jev_control,'load_contract',return_value=self.control).start()
        patch.object(mod,'memory_slice',return_value=('Public source. '*600,dict(self.source))).start()
        patch.object(mod.wallet_runtime,'enabled',return_value=False).start()
        patch.object(mod.wallet_runtime,'routing_begin').start();patch.object(mod.wallet_runtime,'routing_end').start()
    def post(self,*args,**kwargs):
        self.calls+=1;self.body=kwargs['json']
        if self.throw:raise TimeoutError('uncertain synthetic call')
        answers={}
        for key,q in self.body['questions'].items():
            value={'executor':'mimo','scientific_mode':'mathematical_solution','work_path':'answer','memory_action':'use_loaded','collaboration':'direct','memory_continuity':self.continuity}[key]
            answers[key]={'type':'choice','choice':value,'confidence':.95,'probabilities':{k:float(k==value) for k in q['criteria']}}
        if self.bad:answers['executor']['choice']='claude-sonnet'
        return types.SimpleNamespace(status_code=200,json=lambda:{'model':'jev-1.13.0','answers':answers,'usage':{'input_tokens':100}})
    def choose(self,prompt='haja luz',mod=router,**kwargs):
        with memory.bound(self.binding):
            return mod.choose(prompt,['mimo','openai'],root=self.root,post=self.post,validation_probe=True,**kwargs)
    def answer_then_followup(self):
        self.binding.append('response','Solução: ação, equação, projeção, coerência. '*420,
            flow={'phase':'awaiting_review','next_action':'Continue the dialogue; no uncertain execution.',
                  'handles':[{'id':'app_request','request_id':'turn1','status':'completed'}]})
        self.binding=memory.begin(self.root,'synthetic-owner','testconversation',[{'role':'user','content':self.first},{'role':'assistant','content':'Previous answer retained in ledger.'},{'role':'user','content':'haja luz'}],'turn2')
    def test_reproduce_old_failure_and_fix_two_turns(self):
        self.choose(self.first);self.assertEqual(self.calls,1)
        self.answer_then_followup();old=previous_router();self.prepared(old)
        with self.assertRaisesRegex(router.jev_control.ControlError,'admission bounds'):self.choose(mod=old)
        self.assertEqual(self.calls,1)
        before=self.binding.projection();selected,receipt=self.choose()
        self.assertEqual(selected,'mimo');self.assertEqual(self.calls,2)
        self.assertEqual(self.body['state']['request'],'haja luz')
        self.assertEqual(receipt['request_sha256'],hashlib.sha256(b'haja luz').hexdigest())
        self.assertIn('recognized_intent',self.body['state']);self.assertIn('VERBO',router.route_instruction(receipt))
        self.assertLessEqual(receipt['admission']['state_bytes'],30000)
        common=self.body['state']['common_memory'];self.assertGreater(common['coverage']['omitted_records'],0)
        self.assertIn(self.first,common['projection'])
        snapshot=self.binding.snapshot();self.assertEqual(snapshot['objective'],self.first)
        self.assertTrue(any(len(x['text'])>17000 for x in snapshot['q']['records']))
        self.assertGreater(before['actual_chars'],common['coverage']['actual_chars'])
    def test_required_decisions_and_pending_survive(self):
        self.answer_then_followup()
        for label,kind,statute in [('Do not run the bench','decision','INPUT'),('Previous external operation is uncertain','pending','OPEN')]:
            self.binding.append(label,label,kind=kind,statute=statute,source_kind='tool')
        self.continuity='reconcile';_,receipt=self.choose()
        for text in ('Do not run the bench','Previous external operation is uncertain'):
            self.assertIn(text,self.body['state']['common_memory']['projection'])
        self.assertEqual(receipt['memory_continuity'],'reconcile')
        self.assertEqual(router.jev_control.allowed_tool_names(receipt['control'],['bench_run','search_tgl']),['search_tgl'])
    def test_required_overflow_never_sends(self):
        self.binding.append('required','restrição '*6000,kind='decision',statute='INPUT',source_kind='operator')
        with self.assertRaises(router.RoutingContextOverflow):self.choose()
        self.assertEqual(self.calls,0)
    def test_unicode_wire_not_character_count(self):
        self.binding.append('unicode','𝛽á\\\"\n'*3000)
        _,r=self.choose();self.assertLessEqual(r['admission']['state_bytes'],30000)
        self.assertLessEqual(r['admission']['state_longest_question_bytes'],32000)
    def test_manual_context_not_shrunk(self):
        self.answer_then_followup();before=self.binding.projection()
        with memory.bound(self.binding),patch.object(memory,'routing_result'):
            messages=[{'role':'system','content':'SCIENTIFIC-PREFIX'},{'role':'user','content':'haja luz'}]
            expected=memory.project_messages(messages)
            self.choose()
            self.assertEqual(memory.project_messages(messages),expected)
            self.assertEqual(self.binding.projection(),before)
            self.assertEqual(messages[0]['content'],'SCIENTIFIC-PREFIX')
    def test_current_revision_changes_refuse(self):
        self.answer_then_followup();original=memory.routing_state;count=0
        def changed(*a,**kw):
            nonlocal count
            count+=1;result=original(*a,**kw)
            if count>1:result['projection_receipt']['revision']+=1
            return result
        with patch.object(memory,'routing_state',side_effect=changed):
            with self.assertRaisesRegex(router.jev_control.ControlError,'changed'):self.choose()
        self.assertEqual(self.calls,0)
    def test_confidential_guard_remains(self):
        with self.assertRaises(memory.ConfidentialContent):
            self.binding.append('unsafe','read iald_stack_v7.py')
        self.assertEqual(self.calls,0)
    def test_timeout_not_retried(self):
        self.throw=True
        with self.assertRaises(TimeoutError):self.choose()
        self.assertEqual(self.calls,1)
        receipt=json.loads(next((self.root/'.iald_runtime/app_routing').glob('*.json')).read_bytes())
        self.assertEqual(receipt['status'],'failed_or_uncertain')
    def test_unknown_executor_is_refused(self):
        self.bad=True
        with self.assertRaises(ValueError):self.choose()
        self.assertEqual(self.calls,1)
    def test_worker_or_quoted_command_not_bootstrap(self):
        self.choose(worker=True);self.assertNotIn('recognized_intent',self.body['state'])
        self.choose('Explique a frase "haja luz"');self.assertNotIn('recognized_intent',self.body['state'])
    def test_web_only_automatic_error_surface_changed(self):
        def functions(folder):
            tree=ast.parse((W/folder/'iald_web_server.py').read_bytes())
            return {n.name:ast.dump(n) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
        old=functions('baseline');new=functions('staging')
        self.assertEqual({k for k in old if old[k]!=new[k]},{'_chat_automatico_autorizado'})
        self.assertIn('roteamento_contexto_excedido',new['_chat_automatico_autorizado'])

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
    report={'passed':result.wasSuccessful(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'network_calls':0}
    (W/'validation/test_fix.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    sys.exit(not result.wasSuccessful())
