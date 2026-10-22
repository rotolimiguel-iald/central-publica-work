"""Exercise actual staged router AST blocks, no JEV/provider/network calls."""
import ast
import copy
import json
from pathlib import Path
import sys
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'routing_stage'))
import iald_media_budget as budget
import iald_task_policy as policy
import iald_routing_metrics as metrics


class SinglePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree=ast.parse((HERE/'iald_auto_router.py').read_text(encoding='utf-8'))
        cls.choose=next(n for n in cls.tree.body if isinstance(n,ast.FunctionDef) and n.name=='choose')
        item=dict(id='a'*32,kind='audio',sha256='b'*64,decoded_bytes=1000,encoded_bytes=1336,duration_seconds=120)
        payload=dict(model='mimo-v2.6-pro',max_completion_tokens=131072,
            messages=[dict(role='user',content=[dict(type='iald_media',media_ref='a'*32,kind='audio')])])
        cls.plan=budget.plan_request(payload,[item],rates=dict(input=.435,cache_read=.0036,output=.87))

    def prefix(self,plans,multimodal=True):
        fn=copy.deepcopy(self.choose)
        stop=next(i for i,n in enumerate(fn.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='mod' for t in n.targets))
        fn.body=fn.body[:stop]+[ast.Return(value=ast.Tuple(elts=[ast.Name(id='media_plans',ctx=ast.Load()),ast.Name(id='media_policy_view',ctx=ast.Load()),ast.Name(id='sole_media_policy',ctx=ast.Load())],ctx=ast.Load()))]
        ast.fix_missing_locations(fn)
        ns=dict(ROOT=HERE,copy=copy,task_policy=policy,routing_metrics=metrics,json=json,
                media_budget_policy=budget,DESCRIPTIONS=dict.fromkeys(('kimi','mimo')))
        exec(compile(ast.Module(body=[fn],type_ignores=[]),'<actual-router-prefix>','exec'),ns)
        media=dict(kinds=['audio'],counts=dict(image=0,audio=1,video=0)) if multimodal else None
        return ns['choose']('analise o audio',['kimi','mimo'],media=media,media_budget_options=plans)

    def questions(self,plans,sole):
        node=next(n for n in self.choose.body if isinstance(n,ast.If) and
                  isinstance(n.test,ast.BoolOp) and any(isinstance(c,ast.Assign) and
                  any(isinstance(t,ast.Subscript) and isinstance(t.slice,ast.Constant) and t.slice.value=='media_policy' for t in c.targets) for c in n.body))
        questions=dict(executor={'sentinel':'still JEV'},collaboration={'sentinel':'unchanged'})
        ns=dict(media_plans=plans,sole_media_policy=sole,questions=questions,media_budget_policy=budget)
        exec(compile(ast.Module(body=[copy.deepcopy(node)],type_ignores=[]),'<actual-question-gate>','exec'),ns)
        return questions

    def resolve(self,plans,sole,answer=None):
        node=next(n for n in ast.walk(self.choose) if isinstance(n,ast.If) and
                  any(isinstance(c,ast.Assign) and any(isinstance(t,ast.Subscript) and
                  isinstance(t.slice,ast.Constant) and t.slice.value=='media_policy_id' for t in c.targets) for c in n.body))
        record={};answers={} if answer is None else {'media_policy':answer}
        ns=dict(media_plans=plans,sole_media_policy=sole,media_policy_view=budget.routing_options(plans),
                media_budget_policy=budget,record=record,data={'answers':answers})
        exec(compile(ast.Module(body=[copy.deepcopy(node)],type_ignores=[]),'<actual-policy-resolution>','exec'),ns)
        return record

    def test_audio_120s_one_policy_needs_no_answer(self):
        plans,view,sole=self.prefix({'audio':self.plan})
        self.assertEqual(sole,'audio');self.assertEqual(len(view),1)
        self.assertNotIn('media_policy',self.questions(plans,sole))
        record=self.resolve(plans,sole)
        self.assertEqual(record['media_policy_id'],'audio')
        self.assertFalse(record['media_policy_selection']['confidence_gate_applied'])
        self.assertEqual(record['media_budget']['media_tokens_estimate'],750)

    def test_executor_and_other_questions_unchanged(self):
        questions=self.questions({'audio':self.plan},'audio')
        self.assertEqual(questions['executor'],{'sentinel':'still JEV'})
        self.assertEqual(questions['collaboration'],{'sentinel':'unchanged'})

    def test_one_admissible_plus_refused_is_single(self):
        plans,view,sole=self.prefix({'audio':self.plan,'not_feasible':{'status':'REFUSED','reason':'context'}})
        self.assertEqual(sole,'audio');self.assertEqual(set(view),{'audio'})
        self.assertEqual(self.resolve(plans,sole)['media_policy_id'],'audio')

    def test_two_equal_policies_still_require_host_collapse(self):
        plans,view,sole=self.prefix({'standard':self.plan,'detail':copy.deepcopy(self.plan)})
        self.assertIsNone(sole);self.assertIn('media_policy',self.questions(plans,sole))

    def test_multiple_policy_confidence_068_refuses(self):
        plans={'standard':self.plan,'detail':copy.deepcopy(self.plan)}
        answer=dict(type='choice',choice='standard',confidence=.68,probabilities={'standard':.68,'detail':.32})
        with self.assertRaises(budget.BudgetRefusal):self.resolve(plans,None,answer)

    def test_multiple_policy_confidence_070_passes(self):
        plans={'standard':self.plan,'detail':copy.deepcopy(self.plan)}
        answer=dict(type='choice',choice='standard',confidence=.70,probabilities={'standard':.7,'detail':.3})
        record=self.resolve(plans,None,answer)
        self.assertTrue(record['media_policy_selection']['confidence_gate_applied'])
        self.assertEqual(record['media_policy_selection']['mode'],'jev_choice')

    def test_zero_admissible_refuses_before_dispatch(self):
        with self.assertRaises(budget.BudgetRefusal):self.prefix({'bad':{'status':'REFUSED','reason':'context'}})

    def test_text_path_unchanged(self):
        plans,view,sole=self.prefix(None,multimodal=False)
        self.assertIsNone(plans);self.assertIsNone(view);self.assertIsNone(sole)

    def test_public_apis_and_no_retry_preserved(self):
        live=ast.parse(Path('C:/IALD/projetos_pyhton/IALD/iald_auto_router.py').read_text(encoding='utf-8'))
        signatures=lambda tree:{n.name:ast.dump(n.args) for n in tree.body if isinstance(n,ast.FunctionDef)}
        self.assertEqual(signatures(live),signatures(self.tree))
        self.assertIn('FAILED_OR_UNCERTAIN_NO_RETRY',(HERE/'iald_auto_router.py').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main(verbosity=2)
