"""Transport-isolated control integration and real task-scope restrictions."""
from pathlib import Path
from types import SimpleNamespace
import copy
import importlib
import json
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(W/'app_patch'), str(R)]
import iald_auto_router as router
import iald_jev_control as control

def answer(criteria, selected, confidence=0.95):
    others = len(criteria)-1
    probs = {k:(0.98 if k==selected else 0.02/others) for k in criteria} if others else {selected:1.0}
    return {'type':'choice','choice':selected,'confidence':confidence,'probabilities':probs}

class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=W)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.contract = {'release':'v380','source_sha256':'a'*64,'record':'Synthetic source-bound contract'}
        self.source = {'release':'v380','source_sha256':'b'*64,'release_source_sha256':'a'*64,'url':'https://example.invalid/science','characters':100}
        self.backend = SimpleNamespace(availability=lambda:{'status':'ready'},validate_prompt=lambda _:None,
                         ENDPOINT='https://example.invalid/systemone',_key=lambda:'synthetic-secret')
        for name, replacement in (
            ('backend', lambda:self.backend), ('available', lambda:True),
            ('memory_slice', lambda _:('Public science. '*300,self.source)), ('observations',lambda *_:{})):
            p=patch.object(router,name,replacement);p.start();self.addCleanup(p.stop)
        for name, replacement in (('load_contract',lambda _:copy.deepcopy(self.contract)),('contract_state',lambda c:c)):
            p=patch.object(control,name,replacement);p.start();self.addCleanup(p.stop)
        self.selected = {'scientific_mode':'explanation','work_path':'answer','memory_action':'use_loaded','executor':'mimo'}
        self.confidences={};self.calls=[];self.mutate=None

    def post(self, url, **kwargs):
        self.calls.append((url,kwargs))
        body=kwargs['json']
        result={'model':'jev-1.13.0','usage':{'input_tokens':1000,'output_tokens':20},'answers':{}}
        for key,question in body['questions'].items():
            choice=self.selected[key]
            result['answers'][key]=answer(question['criteria'],choice,self.confidences.get(key,.95))
        if self.mutate:self.mutate(result)
        return SimpleNamespace(status_code=200,json=lambda:result)

    def choose(self, text='Uma explicação.', candidates=('mimo','openai'), **kwargs):
        return router.choose(text,list(candidates),root=self.root,post=self.post,validation_probe=True,**kwargs)

    def receipt(self):
        return json.loads(next((self.root/'.iald_runtime/app_routing').glob('*.json')).read_bytes())

    def test_scientific_intent_and_source_survive_one_call(self):
        self.selected['scientific_mode']='mathematical_solution'
        selected, receipt=self.choose('Articule a solução matemática da TGL.')
        self.assertEqual(selected,'mimo');self.assertEqual(len(self.calls),1)
        self.assertEqual(receipt['regime']['state'],'resolved')
        self.assertEqual(receipt['control']['scientific_mode'],'mathematical_solution')
        self.assertEqual(self.receipt()['status'],'selected')
        self.assertIn('Solução matemática',router.route_instruction(receipt))
        self.assertNotIn('synthetic-secret',json.dumps(receipt))

    def test_public_question_does_not_offer_operator_path(self):
        self.choose()
        self.assertNotIn('operator_bench',self.calls[0][1]['json']['questions']['work_path']['criteria'])
        self.assertNotIn('operator_context',self.calls[0][1]['json']['state'])

    def test_only_local_capability_projection_can_change_executor(self):
        self.selected.update(work_path='create_artifact',executor='kimi')
        selected,receipt=self.choose('Prepare uma entrega.',candidates=('kimi','mimo'))
        self.assertEqual(selected,'mimo');self.assertEqual(len(self.calls),1)
        self.assertEqual(receipt['regime']['candidates'],['mimo'])
        self.assertIn('pruned',receipt['regime']['history'])

    def test_mathematical_calculation_is_not_confused_with_confirmation(self):
        self.selected.update(scientific_mode='mathematical_solution',work_path='execute_calculation')
        _,receipt=self.choose('Calcule a matriz descrita.')
        names=control.allowed_tool_names(receipt['control'],['execute_python','bench_run'])
        self.assertEqual(names,['execute_python'])

    def test_worker_has_no_live_tool_capability(self):
        self.selected.update(work_path='execute_calculation')
        _,receipt=self.choose(worker=True)
        self.assertEqual(control.allowed_tool_names(receipt['control'],['execute_python','bench_run','delegate_task']),[])

    def test_low_path_confidence_does_not_authorize_effects(self):
        self.selected['work_path']='create_artifact';self.confidences['work_path']=.3
        _,receipt=self.choose()
        self.assertEqual(control.allowed_tool_names(receipt['control'],['create_artifact','execute_python','bench_run']),[])

    def test_uncertain_domain_does_not_cancel_requested_export(self):
        self.selected['work_path']='create_artifact';self.confidences['scientific_mode']=.3
        _,receipt=self.choose()
        self.assertIn('create_artifact',control.allowed_tool_names(receipt['control'],['create_artifact']))

    def test_invalid_typed_decision_stops_before_any_executor(self):
        self.mutate=lambda data:data['answers']['memory_action'].update(type='noul')
        with self.assertRaises(ValueError):self.choose()
        self.assertEqual(len(self.calls),1);self.assertEqual(self.receipt()['status'],'failed_or_uncertain')

    def test_extra_answer_rejected(self):
        self.mutate=lambda data:data['answers'].update(grant_admin=True)
        with self.assertRaises(ValueError):self.choose()

    def test_unverified_model_rejected(self):
        self.mutate=lambda data:data.update(model='jev-unverified')
        with self.assertRaises(ValueError):self.choose()

    def test_boolean_usage_rejected(self):
        self.mutate=lambda data:data['usage'].update(input_tokens=True)
        with self.assertRaises(ValueError):self.choose()

    def test_nonmaximal_executor_rejected(self):
        self.mutate=lambda data:data['answers']['executor'].update(choice='openai')
        with self.assertRaises(ValueError):self.choose()

    def test_timeout_is_inscribed_uncertain_and_not_retried(self):
        post=Mock(side_effect=TimeoutError())
        with self.assertRaises(TimeoutError):
            router.choose('Teste',['mimo'],root=self.root,post=post,validation_probe=True)
        self.assertEqual(post.call_count,1);self.assertEqual(self.receipt()['regime']['state'],'uncertain')

    def test_source_change_after_call_rejects_dispatch(self):
        self.mutate=lambda data:self.contract.update(source_sha256='c'*64)
        with self.assertRaises(ValueError):self.choose()
        self.assertEqual(self.receipt()['regime']['state'],'refused')

    def test_context_admission_happens_before_transport(self):
        with self.assertRaises(ValueError):self.choose('界'*12000)
        self.assertEqual(self.calls,[])

    def test_source_excerpt_only_is_reduced_for_long_requests(self):
        text='x'*12000
        with patch.object(router,'memory_slice',lambda _:('é'*8000,self.source)):
            _,receipt=self.choose(text)
        sent=self.calls[0][1]['json']
        self.assertEqual(sent['state']['request'],text)
        self.assertLess(len(sent['state']['canonical_memory']),8000)
        self.assertEqual(receipt['memory']['characters'],len(sent['state']['canonical_memory']))
        self.assertLessEqual(receipt['admission']['state_longest_question_bytes'],32000)

    def make_scope(self):
        names=['create_artifact','execute_python','delegate_task','get_task_capabilities','read_task_artifact',
               'bench_capabilities','bench_query','bench_map','bench_plan','bench_run','bench_result']
        return SimpleNamespace(tools=[{'function':{'name':n}} for n in names],instructions='Existing instructions',
                               record={},_save=Mock(),execute=Mock(return_value={'status':'RETURNED'}))

    def test_scope_removes_effects_from_explanation(self):
        _,receipt=self.choose();scope=self.make_scope();original=scope.execute
        router.bind_scope(scope,receipt,root=self.root)
        self.assertEqual(scope.execute('bench_run',{} )['status'],'UNAVAILABLE')
        self.assertEqual(scope.execute('execute_python',{} )['status'],'UNAVAILABLE')
        original.assert_not_called();scope._save.assert_called_once()
        self.assertTrue(scope.instructions.startswith('Existing instructions'))

    def test_operator_scope_is_intersection_not_capability_grant(self):
        self.selected.update(work_path='operator_bench',scientific_mode='empirical_test')
        _,receipt=self.choose(operator_context={'role':'operador','capabilities':['local_scientific_bench']})
        scope=self.make_scope();scope.tools=[t for t in scope.tools if t['function']['name']!='bench_run']
        router.bind_scope(scope,receipt,root=self.root)
        offered={t['function']['name'] for t in scope.tools}
        self.assertIn('bench_plan',offered);self.assertNotIn('bench_run',offered)
        self.assertEqual(scope.execute('bench_run',{})['status'],'UNAVAILABLE')

    def test_new_contract_before_scope_fails_closed(self):
        _,receipt=self.choose();self.contract['source_sha256']='c'*64
        with self.assertRaises(ValueError):router.bind_scope(self.make_scope(),receipt,root=self.root)

if __name__=='__main__':
    unittest.main(verbosity=2)
