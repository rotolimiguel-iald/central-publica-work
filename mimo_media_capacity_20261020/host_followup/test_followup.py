import ast,copy,hashlib,json,sqlite3,sys,unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock
HERE=Path(__file__).resolve().parent
WORK=HERE.parent;LIVE=Path('C:/IALD/projetos_pyhton/IALD')
sys.path[:0]=[str(WORK/'host_stage'),str(LIVE)]
from test_host import HostTests,extract,glue,media
import iald_media_budget as budget
from claude_memory_package import load_package
PACKAGE=load_package(LIVE/'.iald_runtime/haiku',canonical_manifest=LIVE/'iald_nucleo_fixo.json')

scoped=json.loads((HERE/'SCOPED_ACOM_INPUT.json').read_text())
wirepath=Path('C:/IALD/MEMORIA_IALD/state/activity_artifacts/532f6902924d86e0f05a798a334bee442cc0a3d416788d17c3f7a3fc2cefe973.json')
wirebytes=wirepath.read_bytes()
assert hashlib.sha256(wirebytes).hexdigest()==wirepath.stem
wire=json.loads(wirebytes)
assert wire['context_id']==scoped['context_id'] and wire['scope']==scoped['scope']
answer=json.loads(wire['payload']['wire_utf8'])['answers']['media_policy']
usage=json.loads(wire['payload']['wire_utf8'])['usage']

class Followup(unittest.TestCase):
    def setUp(self):
        self.fixture=HostTests('test_lazy_caps_no_storage_and_scope_binding');self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
    def plans(self):
        metadata=json.loads((HERE/'SCOPED_JOB_METADATA.json').read_text())['media'][0]['metadata']
        body=dict(model='mimo-v2.6-pro',messages=[dict(role='system',content=PACKAGE.prefix),dict(role='user',content=json.loads(scoped['objective']))])
        metadata=dict(metadata,encoded_bytes_upper=4*((metadata['bytes']+2)//3)+128)
        items=budget.adapt_resolved_metadata([metadata])
        return budget.options(body,items,glue.video_proposals(items),rates=dict(input=.435,cache_read=.0036,output=.87))
    def test_exact_received_answer_root_and_negative_unknown(self):
        plans=self.plans()
        with self.assertRaisesRegex(budget.BudgetRefusal,'Uncertain media policy; no automatic quality substitution'):
            budget.resolve_policy(answer,plans)
        valid=copy.deepcopy(answer);valid['confidence']=.70
        self.assertEqual(budget.resolve_policy(valid,plans),'standard')
        valid['choice']='unoffered'
        with self.assertRaises(budget.BudgetRefusal):budget.resolve_policy(valid,plans)
    def test_actual_host_catch_after_one_mock_chooser_no_executor(self):
        ns=self.fixture.server_ns();ns['MediaBudgetError']=budget.BudgetRefusal
        ns['_load_shared_science_package']=lambda:PACKAGE
        runtime=NS(canonicalize=lambda c,**kw:c,authorize_dispatch=lambda:True,
                   budget_metadata=lambda c:[dict(kind='audio',duration_seconds=120.)],
                   routing_options=lambda *a,**kw:self.plans())
        ns['_private_runtime_for']=lambda *a,**kw:runtime
        ns['_chat_avaliacao']=Mock(side_effect=AssertionError('No executor after refused policy'))
        def choose(*args,**kw):budget.resolve_policy(answer,kw['media_budget_options'])
        ns['app_router'].choose=Mock(side_effect=choose)
        tree=ast.parse((HERE/'iald_web_server.py').read_bytes())
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('_chat_automatico_autorizado','_private_preview_body')]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'actual followup host AST','exec'),ns)
        original=dict(iald_conv='c_mvh7ykird3r4',messages=[dict(role='user',content=json.loads(scoped['objective']))])
        saved=copy.deepcopy(original)
        result=ns['_chat_automatico_autorizado'](original,'luiz',{},True,0)
        self.assertEqual(result['code'],'politica_midia_incerta');self.assertEqual(original,saved)
        ns['app_router'].choose.assert_called_once();ns['_chat_avaliacao'].assert_not_called()
        for error,code in ((budget.BudgetRefusal('PRIVATE_PATH_SENTINEL'),'anexo_excede_contexto'),(media.MediaError('PRIVATE_PATH_SENTINEL'),'anexo_validacao_recusada')):
            ns['app_router'].choose.side_effect=error
            result=ns['_chat_automatico_autorizado'](original,'luiz',{},True,0)
            self.assertEqual(result['code'],code);self.assertNotIn('PRIVATE_PATH_SENTINEL',result['message'])

def load_tests(loader,tests,pattern):return loader.loadTestsFromTestCase(Followup)
if __name__=='__main__':unittest.main(verbosity=2)
