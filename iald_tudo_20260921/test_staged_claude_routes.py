from pathlib import Path
import ast,copy,threading,unittest
from types import SimpleNamespace
from test_claude_route_bridge import motors
from claude_route_bridge import RouteBridge
from claude_profiles import HAIKU,SONNET
W=Path(__file__).resolve().parent
from haiku_stage_fixture import STAGE

class StagedRoutesTests(unittest.TestCase):
    def setUp(self):
        self.users={'testador':{'plano':'gratuito'},'luiz':{'admin':True,'plano':'operador'},
                    'bloqueado':{'plano':'gratuito','bloqueado':True}}
        self.saved=[];self.body={'motor':'claude-haiku'}
        cfg=motors.Config(chave='fixture',provedor=motors.CLAUDE,modelo=SONNET.model,
                          modelo_operador=SONNET.model,contas=frozenset({'luiz'}))
        bridge=RouteBridge(motors=motors,base_config=cfg,package_loader=lambda:object(),enabled=True,
                           public_daily_usd=1,public_group_daily_usd=5)
        self.env={'session':{'username':'testador'},'request':SimpleNamespace(is_json=True,headers={'X-IALD-Context':'anthropic-native-v1'}),
            'jsonify':lambda obj:obj,'_corpo_json':lambda:self.body,'_TRAVA_USUARIOS':threading.RLock(),
            '_carregar_usuarios_para_escrita':lambda:self.users,'save_users':lambda users:self.saved.append(copy.deepcopy(users)),
            '_conta_bloqueada':lambda r:bool(r.get('bloqueado')),'iald_motores':motors,
            'CLAUDE_ROUTES':bridge,'MOTORES_CFG':cfg,'_contas_claude':lambda:cfg.contas,
            '_modelo_nativo_resposta':lambda:{'rotulo':'Native'},'_motor_externo_indisponivel':lambda model:'',
            'MSG_SEM_ACESSO_NATIVA':'Native access denied','auth_log':lambda *args:None,
            'require_admin':lambda:None,'_HAIKU_PROFILE':HAIKU}
        self.env['request'].get_json=lambda **kwargs:self.body
        tree=ast.parse(STAGE.read_text(encoding='utf-8'))
        names={'api_motor_escolha','admin_definir_motor','_motor_efetivo','_motor_selection_id','_opcoes_de_motor','_consentimento_do_motor','_haiku_selected','_haiku_client_ready'}
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
        self.assertEqual(len(nodes),len(names))
        for node in nodes:node.decorator_list=[]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(STAGE),'exec'),self.env)
    def choose(self,option,user='testador'):
        self.body={'motor':option};self.env['session']['username']=user
        return self.env['api_motor_escolha']()
    def test_approved_public_haiku_persists_model_and_requests_anthropic_consent(self):
        reply=self.choose('claude-haiku')
        self.assertEqual(reply['motor'],'claude');self.assertEqual(reply['motor_selecao'],'claude-haiku')
        self.assertEqual(self.users['testador']['modelo_claude'],HAIKU.model)
        self.assertEqual(reply['consentimento']['provedor'],'Anthropic');self.assertFalse(reply['consentimento_dado'])
        self.assertEqual(len(self.saved),1);self.assertNotIn('acesso_nativa',self.users['testador'])
    def test_public_cannot_select_sonnet_or_native(self):
        self.assertEqual(self.choose('claude-sonnet')[1],409)
        self.assertEqual(self.choose('nativa')[1],403);self.assertEqual(self.saved,[])
    def test_luiz_can_switch_between_models(self):
        self.assertTrue(self.choose('claude-haiku','luiz')['ok'])
        self.assertTrue(self.choose('claude-sonnet','luiz')['ok'])
        self.assertEqual(self.users['luiz']['modelo_claude'],SONNET.model)
    def test_blocked_or_missing_account_cannot_select(self):
        for user in ('bloqueado','missing'):
            self.assertEqual(self.choose('claude-haiku',user)[1],403)
        self.assertEqual(self.saved,[])
    def test_non_json_and_unknown_selection_do_not_write(self):
        self.env['request'].is_json=False
        self.assertEqual(self.choose('claude-haiku')[1],415)
        self.env['request'].is_json=True
        self.assertEqual(self.choose('unknown')[1],400);self.assertEqual(self.saved,[])
    def test_package_failure_leaves_existing_selection(self):
        self.choose('claude-haiku');before=copy.deepcopy(self.users)
        def fail():raise ValueError('changed package')
        self.env['CLAUDE_ROUTES'].package_loader=fail
        self.assertEqual(self.choose('claude-haiku')[1],409)
        self.assertEqual(self.users,before)
        self.assertEqual(self.env['_motor_efetivo'](self.users['testador'],'testador'),'claude')
    def test_admin_grants_haiku_without_granting_native(self):
        reply=self.env['admin_definir_motor']('testador')
        self.assertTrue(reply['ok']);self.assertEqual(reply['motor_selecao'],'claude-haiku')
        self.assertNotIn('acesso_nativa',self.users['testador'])
    def test_admin_cannot_grant_sonnet_to_another_user(self):
        self.body={'motor':'claude-sonnet'}
        self.assertEqual(self.env['admin_definir_motor']('testador')[1],409)
        self.assertFalse(self.saved)
    def test_admin_access_check_precedes_mutation(self):
        self.env['require_admin']=lambda:({'error':'forbidden'},403)
        self.assertEqual(self.env['admin_definir_motor']('testador')[1],403)
        self.assertFalse(self.saved)
    def test_admin_reset_clears_both_provider_and_model(self):
        self.choose('claude-haiku');self.body={'motor':''}
        reply=self.env['admin_definir_motor']('testador')
        self.assertTrue(reply['ok']);self.assertNotIn('motor',self.users['testador'])
        self.assertNotIn('modelo_claude',self.users['testador'])

    def test_old_client_cannot_select_haiku_or_see_it_as_an_option(self):
        self.env['request'].headers={}
        self.assertEqual(self.choose('claude-haiku')[1],426)
        self.assertEqual(self.saved,[])
        rows=self.env['_opcoes_de_motor'](self.users['testador'],'testador')
        self.assertNotIn('claude-haiku',[r['id'] for r in rows])

if __name__=='__main__':unittest.main()
