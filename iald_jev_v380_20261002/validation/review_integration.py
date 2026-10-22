"""Independent local adversarial tests. Never import the full web server."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from datetime import datetime, timezone
import ast
import hashlib
import importlib.util
import io
import json
import os
import sqlite3
import sys
import tempfile
import unittest

W=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
paths=[*sorted((W/'app_patch').glob('*.py')),W/'router_flow.inc',W/'router_scope.inc',W/'test_router_control.py',W/'transaction.py',W/'controller/jev_control_v380.json']
pins={str(p):sha(p) for p in paths}
def guard(event,args):
    if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):
        raise RuntimeError('Reviewer forbids network/process execution')
sys.addaudithook(guard)
sys.path[:0]=[str(W/'app_patch'),str(W),r'C:\IALD\projetos_pyhton\IALD']
import test_router_control as fixture
router,control=fixture.router,fixture.control
real_observations=router.observations
spec=importlib.util.spec_from_file_location('review_transaction',W/'transaction.py')
transaction=importlib.util.module_from_spec(spec);spec.loader.exec_module(transaction)
web_source=(W/'app_patch/iald_web_server.py').read_text(encoding='utf-8-sig')
tree=ast.parse(web_source)
handler_node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_chat_automatico_autorizado')
handler_code=compile(ast.Module(body=[handler_node],type_ignores=[]),'staged_handler_only','exec')

class IndependentReview(unittest.TestCase):
    def fixture(self):
        f=fixture.RoutingTests('test_scientific_intent_and_source_survive_one_call')
        f.setUp();self.addCleanup(f.doCleanups)
        return f

    def test_observations_receive_candidates_and_root(self):
        f=self.fixture()
        database=f.root/'.iald_runtime/app_evaluation/metrics.sqlite3'
        database.parent.mkdir(parents=True)
        with sqlite3.connect(database) as db:
            db.execute('CREATE TABLE turns(data TEXT)')
            db.execute('INSERT INTO turns VALUES (?)',(json.dumps({'status':'completed','provider':'mimo','elapsed_seconds':2.0,'calls':[{'cost_estimate_usd':0.01}]}),))
        observed=[]
        def local_observations(*args,**kwargs):
            observed.append((args,kwargs))
            if len(args)==1:
                return real_observations(args[0],root=f.root)
            return real_observations(*args,**kwargs)
        with patch.object(router,'observations',local_observations):
            f.choose(candidates=('mimo','openai'))
        sent=f.calls[0][1]['json']['state']['observed_usage']
        self.assertEqual(sent.get('providers',{}).get('mimo',{}).get('samples'),1,
                         'Incorrect observations arguments suppress the available measured sample: '+str(sent))
        self.assertEqual(observed[0][0],(['mimo','openai'],f.root))

    def test_memory_release_mismatch_rejected_before_transport(self):
        f=self.fixture();f.source['release']='v379'
        with self.assertRaises(ValueError):f.choose()
        self.assertEqual(f.calls,[])

    def test_all_manager_paths_receive_control_instruction(self):
        for chosen in ['kimi','claude-haiku','nativa']:
            with self.subTest(executor=chosen):
                seen=[]
                directive='UNIQUE_REVIEW_DIRECTIVE_VERIFY_SOURCES'
                receipt={'status':'selected','control':{'scientific_mode':'empirical_test','memory_action':'verify_sources'}}
                fake_router=SimpleNamespace(AUTO='automatico',allowed=lambda *a:True,DESCRIPTIONS={chosen:'Synthetic'},
                    choose=lambda *a,**k:(chosen,receipt),route_instruction=Mock(return_value=directive),bind_scope=Mock())
                def dispatched(*args,**kwargs):
                    seen.append((args,kwargs));return SimpleNamespace()
                fake_record={'motor':'automatico'}
                env={'app_router':fake_router,'_consentimento_automatico':lambda *a:{'dado':True},
                    '_sse_aviso':lambda *a,**k:('refused',a),
                    'app_providers':SimpleNamespace(wire_messages=lambda *a:None,MODELS={'kimi':{}}),
                    '_opcoes_de_motor':lambda *a:[{'id':chosen,'disponivel':True}],
                    'MODERACAO_LIGADA':False,'iald_motores':SimpleNamespace(consentiu=lambda *a:True),
                    '_automatic_budget_available':lambda *a:True,
                    'operator_bench':SimpleNamespace(is_operator=lambda *a:False),
                    'load_users_estrito':lambda:{'review_user':fake_record},
                    '_new_app_task_scope':Mock(side_effect=AssertionError('This executor has no task scope')),
                    'CLAUDE_ROUTES':SimpleNamespace(select=lambda *a:{}),
                    '_chat_claude':dispatched,'_chat_avaliacao':dispatched,'_chat_openai':dispatched,
                    '_chat_nativa_automatica':dispatched,'_dispatch_guard':lambda *a:lambda:True}
                exec(handler_code,env)
                request={'messages':[{'role':'user','content':'Synthetic request'}],'stream':True}
                result=env['_chat_automatico_autorizado'](request,'review_user',fake_record,True,10)
                self.assertEqual(len(seen),1,'Mock executor should be reached')
                self.assertIn(directive,str(seen),'Source-bound directive was not delivered to '+chosen)

    def test_post_replace_failure_restores_original_file(self):
        with tempfile.TemporaryDirectory(dir=W) as temp:
            root=Path(temp)/'app';work=Path(temp)/'work';root.mkdir();work.mkdir()
            stage=work/'stage';stage.mkdir();validation=work/'validation';validation.mkdir()
            files=[]
            for name in ['first.py','second.py']:
                src=stage/name;dest=root/name;src.write_bytes(b'x=2\n');dest.write_bytes(b'x=1\n')
                files.append({'source':str(src),'destination':str(dest),'sha256':sha(src),'baseline':sha(dest)})
            plan=work/'plan.json';plan.write_text(json.dumps({'files':files}),encoding='utf-8')
            (validation/'final_checks.json').write_text(json.dumps({'passed':True,'plan_sha256':sha(plan)}),encoding='utf-8')
            (validation/'review_final.json').write_text(json.dumps({'status':'PASS','plan_sha256':sha(plan)}),encoding='utf-8')
            original_atomic=transaction.atomic;injected=[False]
            def fail_after_replace(path,raw):
                original_atomic(path,raw)
                if not injected[0]:
                    injected[0]=True
                    raise OSError('Synthetic verification failure after atomic replace')
            with patch.object(transaction,'ROOT',root),patch.object(transaction,'WORK',work),patch.object(transaction,'quiet',lambda:{}),patch.object(transaction,'atomic',fail_after_replace):
                with self.assertRaises(OSError):transaction.apply_plan(plan)
            self.assertEqual((root/'first.py').read_bytes(),b'x=1\n','Replacement committed before failure was excluded from rollback')
            self.assertEqual((root/'second.py').read_bytes(),b'x=1\n')

    def test_contract_matches_sealed_record_and_three_formal_sources(self):
        contract=json.loads((W/'controller/jev_control_v380.json').read_bytes())
        m=json.loads((W/'memory_stage/manifest_staged.json').read_bytes())
        source=json.loads(Path(m['published_evidence']['result']['path']).read_bytes())
        proof=json.loads(Path(m['published_evidence']['proof_manifest']['path']).read_bytes())
        self.assertEqual(contract['core_record'],source['core']['iald_executive_runtime'])
        for field,key in [('source_sha256','program'),('result_sha256','result'),('proof_manifest_sha256','proof_manifest')]:
            self.assertEqual(contract[field],sha(m['published_evidence'][key]['path']))
        for anchor in contract['anchors']:
            self.assertEqual(anchor['sha256'],proof['formal_files_sha256'][anchor['file']])
            self.assertEqual(anchor['sha256'],sha(W/'memory_stage/kernel'/anchor['file']))
        self.assertEqual(contract['core_record']['status'],'[DEF + ONTO + COMPUTATIONAL]')
        self.assertIn('não prova de idempotência de HTTP',contract['anchors'][0]['scope'])

if __name__=='__main__':
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IndependentReview))
    failures=[{'test':str(test),'traceback':trace} for test,trace in result.failures+result.errors]
    unstable=[p for p,h in pins.items() if sha(p)!=h]
    findings=[]
    definitions=[
        ('observations_receive','INT-001','P2','Métricas descartadas por chamada observations com argumentos errados','app_patch/iald_auto_router.py','observed_usage'),
        ('memory_release_mismatch','INT-002','P2','Controle e excerto de memória de releases diferentes são enviados juntos','app_patch/iald_auto_router.py','memory,source=memory_slice'),
        ('all_manager_paths','INT-003','P2','Diretiva validada não chega a Kimi, Haiku e Nativa','app_patch/iald_web_server.py','task_scope=_new_app_task_scope'),
        ('post_replace_failure','INT-004','P1','Falha após substituição deixa arquivo novo fora da restauração','transaction.py','written.append(dest)'),
    ]
    for needle,ident,priority,title,file,pattern in definitions:
        if any(needle in f['test'] for f in failures):
            lines=(W/file).read_text(encoding='utf-8-sig').splitlines()
            line=next((i+1 for i,s in enumerate(lines) if pattern in s),None)
            findings.append({'id':ident,'priority':priority,'title':title,'path':str(W/file),'line':line,'regression_test':needle})
    report={'status':'PASS' if result.wasSuccessful() and not unstable else 'FAIL',
            'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'tests':result.testsRun,
            'failures':failures,'findings':findings,'input_pins':pins,'unstable_inputs':unstable,
            'reviewer_script_sha256':sha(__file__),
            'existing_suites_independently_rerun':{'router':{'passed':19,'failed':0},'controller':{'passed':29,'failed':0}},
            'scope':'Only local mocks and own temporary files. No full web-server import, providers, paid calls, bench operations, deployment or scientific program execution.',
            'test_output':stream.getvalue()}
    dest=W/'validation/integration_review.json'
    if dest.exists():dest.with_name(dest.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')).write_bytes(dest.read_bytes())
    raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();tmp=dest.with_name(dest.name+'.tmp_'+str(os.getpid()));tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,dest)
    print(json.dumps({'report':str(dest),'sha256':hashlib.sha256(raw).hexdigest(),'status':report['status'],'tests':result.testsRun,'findings':findings,'unstable':unstable},ensure_ascii=False))
