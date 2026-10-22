"""Run the actual server dispatcher AST without importing the web process."""
from pathlib import Path
from types import SimpleNamespace as NS
import ast,sys,unittest
from unittest.mock import Mock
W=Path(__file__).resolve().parent
sys.path[:0]=[str(W/'stage'),r'C:\IALD\projetos_pyhton\IALD']
import iald_execution_guide as guide
import iald_jev_control as control
import iald_task_policy as policy

class Dispatch(unittest.TestCase):
    def setUp(self):
        self.rows=[{'id':'claude-haiku','modelo':'claude-haiku-5-5','disponivel':True}]
        self.current={'approved':True};self.scope=NS(control=object());self.response=NS()
        self.choose=Mock(return_value=('claude-haiku',{'status':'selected'}))
        self.bind=Mock();self.dispatch=Mock(return_value=self.response)
        self.ns=dict(app_router=NS(allowed=lambda r,u:bool(r),DESCRIPTIONS={'claude-haiku':'x'},AUTO='automatico',
            choose=self.choose,bind_scope=self.bind,route_instruction=lambda r:'Validated instruction'),
            _consentimento_automatico=lambda *a:{'dado':True},
            _sse_aviso=lambda *a:('refused',a),jsonify=lambda x:x,
            app_providers=NS(wire_messages=lambda *a:None,MODELS={}),
            _opcoes_de_motor=lambda *a:self.rows,_automatic_budget_available=lambda *a:True,
            MODERACAO_LIGADA=False,iald_motores=NS(consentiu=lambda r,m:bool(r)),
            operator_bench=NS(is_operator=lambda *a:False),
            load_users_estrito=lambda:{'guest':self.current},
            _new_app_task_scope=Mock(return_value=self.scope),
            CLAUDE_ROUTES=NS(select=lambda *a:{'modelo_claude':'claude-haiku-5-5'}),
            _dispatch_guard=lambda *a:lambda:None,_chat_claude=self.dispatch)
        tree=ast.parse((W/'stage/iald_web_server.py').read_bytes())
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_chat_automatico_autorizado')
        exec(compile(ast.Module([node],type_ignores=[]),'actual dispatcher','exec'),self.ns)
    def call(self):
        return self.ns['_chat_automatico_autorizado']({'messages':[{'role':'user','content':'Crie uma planilha.'}]},'guest',{'approved':True},True,30)
    def test_public_haiku_receives_scoped_tools_and_model_identity(self):
        self.assertIs(self.call(),self.response)
        self.assertEqual(self.choose.call_args.kwargs['model_ids'],{'claude-haiku':'claude-haiku-5-5'})
        self.bind.assert_called_once_with(self.scope,{'status':'selected'})
        self.assertIs(self.dispatch.call_args.kwargs['task_scope'],self.scope)
    def test_revoked_account_never_dispatches(self):
        self.current={};self.assertEqual(self.call()[0],'refused');self.dispatch.assert_not_called()
    def test_explicit_unavailable_budget_never_calls_jev(self):
        self.ns['_automatic_budget_available']=lambda *a:False
        self.assertEqual(self.call()[0],'refused');self.choose.assert_not_called();self.dispatch.assert_not_called()

class Playbook(unittest.TestCase):
    def test_worker_cannot_choose_recursive_delegation(self):
        self.assertEqual(set(guide.strategy_question(True)['criteria']),{'direct'})
    def test_low_confidence_is_direct_without_new_authority(self):
        p={'direct':.1,'delegate_then_review':.8,'independent_check':.1}
        out=guide.resolve_strategy({'type':'choice','choice':'delegate_then_review','probabilities':p,'confidence':.2})
        self.assertEqual(out['strategy'],'direct');self.assertFalse(out['authority_granted'])
    def test_invalid_probabilities_refuse(self):
        with self.assertRaises(ValueError):guide.resolve_strategy({'type':'choice','choice':'direct','probabilities':{'direct':float('nan')},'confidence':1})
    def test_public_has_no_bench_instruction_or_host_paths(self):
        import json
        g=guide.routing_guide('code',['claude-haiku','mimo'])
        self.assertNotIn('operator_bench',g);self.assertNotIn('C:\\',json.dumps(g))
    def test_media_not_confused_with_text_generation(self):
        self.assertEqual(guide.MEDIA['image']['runtime'],'NOT_INTEGRATED')
        self.assertEqual(guide.MEDIA['video']['runtime'],'NOT_INTEGRATED')
        self.assertNotIn('generate_image',control.FAMILY_TOOLS['artifact_runtime'])

if __name__=='__main__':unittest.main(verbosity=2)
