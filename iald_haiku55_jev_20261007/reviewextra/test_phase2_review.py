"""Independent offline adversarial review of the Phase 2 routing changes."""
from pathlib import Path
from unittest.mock import patch
import copy, hashlib, json, sys, unittest

W = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(W/'stage'), str(W/'jev_tests'),
    r'C:\IALD\projetos_pyhton\IALD',
    r'C:\Users\rotol\AppData\Roaming\Python\Python314\site-packages']
import iald_execution_guide as guide
import iald_auto_router as router
import iald_task_policy as policy
import iald_jev_control as control
import test_router_control as fixture


class GuideTests(unittest.TestCase):
    def test_invalid_probabilities_rejected(self):
        good = fixture.answer(guide.STRATEGIES, 'independent_check')
        for bad in (True, float('nan'), float('inf'), -1, 1.1):
            a=copy.deepcopy(good);a['confidence']=bad
            with self.subTest(field='confidence', value=repr(bad)), self.assertRaises(ValueError):
                guide.resolve_strategy(a)
            a=copy.deepcopy(good);a['probabilities']['direct']=bad
            with self.subTest(field='probability', value=repr(bad)), self.assertRaises(ValueError):
                guide.resolve_strategy(a)

    def test_support_and_maximality_rejected(self):
        good = fixture.answer(guide.STRATEGIES, 'independent_check')
        cases=[]
        a=copy.deepcopy(good);a['choice']='direct';cases.append(a)
        a=copy.deepcopy(good);a['probabilities']['unoffered']=0;cases.append(a)
        a=copy.deepcopy(good);a['grant_admin']=True;cases.append(a)
        a=copy.deepcopy(good);a['probabilities']={k:.1 for k in guide.STRATEGIES};cases.append(a)
        for a in cases:
            with self.subTest(case=a), self.assertRaises(ValueError):guide.resolve_strategy(a)

    def test_worker_direct_only_and_copies(self):
        self.assertEqual(set(guide.strategy_question(True)['criteria']), {'direct'})
        with self.assertRaises(ValueError):
            guide.resolve_strategy(fixture.answer(guide.STRATEGIES,'independent_check'),True)
        a=guide.routing_guide('code',['mimo'],worker=True,operator_available=True)
        self.assertNotIn('operator_bench',a)
        a['models']['mimo']['use']='changed'
        self.assertNotEqual(guide.CARDS['mimo']['use'],'changed')

    def test_low_confidence_is_direct(self):
        result=guide.resolve_strategy(fixture.answer(guide.STRATEGIES,'independent_check',.69))
        self.assertEqual(result['strategy'],'direct');self.assertFalse(result['authority_granted'])

    def test_public_media_has_no_internal_credential_diagnostic(self):
        media=policy.capabilities()['execution_guide']['media']
        self.assertEqual(media['image']['runtime'],'NOT_INTEGRATED')
        self.assertEqual(media['video']['runtime'],'NOT_INTEGRATED')
        serialized=json.dumps(media)
        self.assertNotIn('api.model.images.request',serialized)
        self.assertNotIn('DENIED_ON_',serialized)


class RoutingTests(unittest.TestCase):
    setUp=fixture.RoutingTests.setUp
    post=fixture.RoutingTests.post
    choose=fixture.RoutingTests.choose
    make_scope=fixture.RoutingTests.make_scope
    receipt=fixture.RoutingTests.receipt

    def test_direct_removes_delegation_at_execution_boundary(self):
        self.selected.update(work_path='create_artifact', collaboration='direct')
        _,receipt=self.choose('Crie arquivo.')
        scope=self.make_scope();execute=scope.execute
        router.bind_scope(scope,receipt,root=self.root)
        self.assertNotIn('delegate_task',[x['function']['name'] for x in scope.tools])
        self.assertEqual(scope.execute('delegate_task',{})['status'],'UNAVAILABLE')
        execute.assert_not_called()
        scope.execute('create_artifact',{});execute.assert_called_once()

    def test_collaboration_cannot_add_missing_tools_or_operator_rights(self):
        for strategy in ('delegate_then_review','independent_check'):
            self.selected.update(work_path='create_artifact',collaboration=strategy)
            _,receipt=self.choose('Crie arquivo.')
            scope=self.make_scope();scope.tools=[x for x in scope.tools if x['function']['name']!='delegate_task']
            router.bind_scope(scope,receipt,root=self.root)
            self.assertNotIn('delegate_task',[x['function']['name'] for x in scope.tools])
            self.assertEqual(scope.execute('bench_run',{})['status'],'UNAVAILABLE')

    def test_invalid_collaboration_no_second_call(self):
        self.mutate=lambda r:r['answers']['collaboration'].update(confidence=True)
        with self.assertRaises(ValueError):self.choose()
        self.assertEqual(len(self.calls),1)
        self.assertEqual(self.receipt()['status'],'failed_or_uncertain')

    def test_guide_and_prompt_size_admission(self):
        self.selected.update(executor='claude-haiku',collaboration='direct')
        _,receipt=self.choose('Explique a TGL.',candidates=tuple(policy.EXECUTOR_MODELS)+('openai','nativa'),operator_context={'role':'operador'})
        body=self.calls[0][1]['json']
        self.assertLessEqual(receipt['admission']['state_longest_question_bytes'],32000)
        self.assertLessEqual(receipt['admission']['request_bytes'],60000)
        digest=hashlib.sha256(json.dumps(body['state']['execution_guide'],sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest()
        self.assertEqual(receipt['execution_guide_sha256'],digest)
        self.assertNotIn('synthetic-secret',json.dumps(receipt))
        count=len(self.calls)
        with self.assertRaises(ValueError):self.choose('界'*12000)
        self.assertEqual(len(self.calls),count)

    def test_public_guide_excludes_operator_bench(self):
        self.choose()
        body=self.calls[0][1]['json']
        self.assertNotIn('operator_bench',body['state']['execution_guide'])
        self.assertNotIn('operator_bench',body['questions']['work_path']['criteria'])

if __name__ == '__main__': unittest.main(verbosity=2)
