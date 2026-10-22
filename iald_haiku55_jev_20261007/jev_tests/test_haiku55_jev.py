"""Focused Haiku manager/capability/metrics regression. No remote transport."""
from pathlib import Path
import hashlib,json,sqlite3,sys,tempfile,unittest,ast
from unittest.mock import patch
W=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(W/'stage'),str(Path(__file__).resolve().parent)]
import iald_task_policy as policy
import iald_auto_router as router
import iald_jev_control as control
import test_router_control as old

class CatalogTests(unittest.TestCase):
    def test_real_candidate_module_paths(self):
        for module in (policy,router,control):self.assertEqual(Path(module.__file__).parent,W/'stage')
    def test_limits_come_from_recorded_api_metadata(self):
        receipt=json.loads((W/'anthropic_model_metadata.json').read_bytes())['metadata']
        info=policy.capability_catalog(['claude-haiku'])['claude-haiku']
        self.assertEqual(info['model_id'],receipt['id'])
        self.assertEqual(info['provider_limits'],{'context_tokens':receipt['max_input_tokens'],'max_output_tokens':receipt['max_tokens']})
        self.assertEqual(info['app_output_reserve'],16384)
        self.assertEqual(info['thinking_modes'],['adaptive','disabled'])
        self.assertFalse(receipt['capabilities']['thinking']['types']['enabled']['supported'])
    def test_only_integrated_capabilities_no_permission_grant(self):
        info=policy.capability_catalog(['claude-haiku'])['claude-haiku']
        self.assertTrue(info['task_manager']);self.assertFalse(info['operator_bench'])
        self.assertIn('image_input',info['not_integrated']);self.assertIn('hosted_web_search',info['not_integrated'])
        self.assertEqual(policy.capabilities()['publishing'],'not_enabled')
        self.assertEqual(policy.capabilities()['parallel_execution'],'not_enabled')
    def test_worker_has_no_effect_or_interactive_tool_catalog(self):
        for item in policy.capability_catalog(['mimo','kimi','claude-haiku'],worker=True).values():
            for key in ('source_tools','task_manager','artifact_tools','text_delegation','operator_bench'):self.assertFalse(item[key])
    def test_one_manager_matrix_and_unknown_models_fail_closed(self):
        rows=['kimi','nativa','claude-haiku','openai']
        for task in ('code','calculation','website','research'):self.assertEqual(policy.eligible_managers(rows,task),['claude-haiku','openai'])
        with self.assertRaises(ValueError):policy.capability_catalog(['invented'])
        with self.assertRaises(ValueError):policy.capability_catalog(['claude-haiku'],{'claude-haiku':'claude-haiku-4-5-20251001'})
    def test_catalog_is_not_mutable_shared_state(self):
        policy.capability_catalog()['claude-haiku']['provider_limits']['context_tokens']=1
        self.assertEqual(policy.capability_catalog()['claude-haiku']['provider_limits']['context_tokens'],1000000)
    def test_metrics_exact_model_not_family_or_unknown_cost(self):
        with tempfile.TemporaryDirectory(dir=W) as tmp:
            root=Path(tmp);p=root/'.iald_runtime/app_evaluation/metrics.sqlite3';p.parent.mkdir(parents=True)
            with sqlite3.connect(p) as db:
                db.execute('CREATE TABLE turns(data TEXT)')
                for model,elapsed,cost in [('claude-haiku-4-5-20251001',999,9),('claude-haiku-5-5',3,0.2),('claude-haiku-5-5',5,None),('claude-sonnet-5-5',100,8)]:
                    db.execute('INSERT INTO turns VALUES(?)',(json.dumps({'provider':'claude','model':model,'status':'completed','elapsed_seconds':elapsed,'calls':[{'cost_estimate_usd':cost}]}),))
                db.execute('INSERT INTO turns VALUES(?)',(json.dumps({'provider':'openai','model':'active-model','status':'completed','elapsed_seconds':4,'calls':[{'cost_estimate_usd':None}]}),))
            db.close()
            h=router.observations(['claude-haiku'],root)['providers']['claude-haiku']
            self.assertEqual((h['samples'],h['median_seconds'],h['median_cost_usd']),(2,4,0.2))
            self.assertEqual(router.observations(['openai'],root)['providers']['openai']['samples'],0)
            o=router.observations(['openai'],root,{'openai':'active-model'})['providers']['openai']
            self.assertEqual(o['samples'],1);self.assertIsNone(o['median_cost_usd'])
    def test_metadata_errors_do_not_load_other_providers(self):
        with tempfile.TemporaryDirectory(dir=W) as tmp:
            self.assertEqual(router.observations(['claude-haiku'],Path(tmp))['status'],'no_samples')
            with self.assertRaises(ValueError):policy.model_identities(['claude-haiku'],{'unknown':'x'})
    def test_scientific_control_core_and_effect_checks_unchanged(self):
        prior=ast.parse((W/'original/iald_jev_control.py').read_bytes());new=ast.parse((W/'stage/iald_jev_control.py').read_bytes())
        before={n.name:ast.dump(n,include_attributes=False) for n in prior.body if isinstance(n,ast.FunctionDef)}
        after={n.name:ast.dump(n,include_attributes=False) for n in new.body if isinstance(n,ast.FunctionDef)}
        self.assertEqual(set(before),set(after))
        self.assertEqual([k for k in before if before[k]!=after[k]],['questions'])

class NewRoutingTests(unittest.TestCase):
    setUp=old.RoutingTests.setUp
    post=old.RoutingTests.post
    choose=old.RoutingTests.choose
    receipt=old.RoutingTests.receipt
    make_scope=old.RoutingTests.make_scope
    def test_haiku_artifact_manager_and_scope(self):
        self.selected.update(executor='claude-haiku',work_path='create_artifact')
        chosen,receipt=self.choose('Crie uma planilha.',candidates=('claude-haiku','kimi'))
        self.assertEqual(chosen,'claude-haiku');self.assertEqual(len(self.calls),1)
        scope=router.bind_scope(self.make_scope(),receipt,root=self.root)
        names={t['function']['name'] for t in scope.tools}
        self.assertIn('create_artifact',names);self.assertNotIn('execute_python',names);self.assertNotIn('bench_run',names)
        self.assertEqual(receipt['executor_models']['claude-haiku'],'claude-haiku-5-5')
    def test_haiku_operator_context_does_not_exclude_conversation(self):
        self.selected['executor']='claude-haiku'
        chosen,_=self.choose(candidates=('claude-haiku',),operator_context={'role':'operador'})
        self.assertEqual(chosen,'claude-haiku')
    def test_calculation_plus_artifact_but_no_public_bench(self):
        self.selected.update(executor='claude-haiku',work_path='execute_calculation')
        _,receipt=self.choose('Calcule e entregue uma planilha.',candidates=('claude-haiku',))
        names=control.allowed_tool_names(receipt['control'],['execute_python','create_artifact','bench_run'])
        self.assertEqual(names,['execute_python','create_artifact'])
        state=self.calls[0][1]['json']['state'];self.assertFalse(state['executor_capabilities']['claude-haiku']['operator_bench'])
    def test_capability_projection_can_keep_haiku(self):
        self.selected.update(executor='kimi',work_path='create_artifact')
        chosen,receipt=self.choose('Prepare uma entrega.',candidates=('kimi','claude-haiku'))
        self.assertEqual(chosen,'claude-haiku');self.assertEqual(receipt['regime']['candidates'],['claude-haiku'])
    def test_worker_catalog_is_restricted(self):
        self.selected.update(executor='mimo',work_path='execute_calculation')
        self.choose(worker=True,candidates=('mimo',))
        info=self.calls[0][1]['json']['state']['executor_capabilities']['mimo']
        self.assertFalse(info['artifact_tools']);self.assertFalse(info['source_tools'])
    def test_model_identity_mismatch_prevents_call(self):
        with self.assertRaises(ValueError):self.choose(candidates=('claude-haiku',),model_ids={'claude-haiku':'claude-haiku-4-5-20251001'})
        self.assertEqual(self.calls,[])
    def test_catalog_hash_bound_in_receipt(self):
        self.selected['executor']='claude-haiku';_,receipt=self.choose(candidates=('claude-haiku',))
        catalog=self.calls[0][1]['json']['state']['executor_capabilities']
        expected=hashlib.sha256(json.dumps(catalog,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()
        self.assertEqual(receipt['capability_catalog_sha256'],expected)

if __name__=='__main__':unittest.main(verbosity=2)
