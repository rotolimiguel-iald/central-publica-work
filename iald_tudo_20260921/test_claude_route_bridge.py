from pathlib import Path
import importlib.util,unittest
from claude_route_bridge import RouteBridge
from claude_profiles import HAIKU
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
spec=importlib.util.spec_from_file_location('motors_under_test',ROOT/'iald_motores.py')
motors=importlib.util.module_from_spec(spec);spec.loader.exec_module(motors)

class RouteTests(unittest.TestCase):
    def setUp(self):
        self.cfg=motors.Config(provedor=motors.CLAUDE,chave='fixture-not-real',
            modelo='claude-sonnet-5',modelo_operador='claude-sonnet-5',contas=frozenset({'luiz'}),
            max_saida=16000,cache_ttl='5m',cota_global_usd=15)
        self.bridge=RouteBridge(motors=motors,base_config=self.cfg,package_loader=lambda:object(),enabled=True,
                                public_daily_usd=1,public_group_daily_usd=5)
    def test_actual_config_public_haiku_and_provider_consent(self):
        record={'plano':'gratuito'}
        fields=self.bridge.select('claude-haiku',record,'testador')
        cfg=self.bridge.configuration(dict(record,**fields),'testador')
        self.assertEqual(cfg.modelo,HAIKU.model);self.assertEqual(cfg.max_saida,4096)
        self.assertEqual(cfg.precos(HAIKU.model),(1,.1,5,1.25))
        self.assertEqual(self.cfg.max_saida,16000)
        self.assertEqual(self.bridge.consent(record)['provedor'],'Anthropic')
        self.assertFalse(self.bridge.consent(record)['dado'])
    def test_hour_cache_price(self):
        self.cfg.cache_ttl='1h'
        cfg=self.bridge.configuration({'plano':'gratuito'},'testador')
        self.assertEqual(cfg.precos(HAIKU.model)[3],2)
    def test_loader_failure_removes_haiku_and_blocks_selection(self):
        def fail():raise ValueError('invalid package')
        self.bridge.package_loader=fail
        self.assertEqual(self.bridge.options({'plano':'gratuito'},'testador'),[])
        with self.assertRaises(PermissionError):self.bridge.select('claude-haiku',{'plano':'gratuito'},'testador')
    def test_disabled_haiku_keeps_existing_operator_sonnet(self):
        self.bridge.enabled=False
        self.assertEqual([o['id']for o in self.bridge.options({'admin':True},'luiz')],['claude-sonnet'])
    def test_revoked_operator_list_denies_sonnet(self):
        self.cfg.contas=frozenset()
        with self.assertRaises(PermissionError):self.bridge.select('claude-sonnet',{'admin':True},'luiz')
    def test_provider_consent_does_not_accept_openai_record(self):
        record={motors.CAMPO_CONSENTIMENTO[motors.OPENAI]:motors.registro_de_consentimento('app',motors.OPENAI)}
        self.assertFalse(self.bridge.consent(record)['dado'])

    def test_public_activation_requires_explicit_usable_budget(self):
        for daily,group in [(None,None),(.02,5),(1,0),(1,16),(True,5),(float('nan'),5)]:
            self.bridge.public_daily_usd=daily;self.bridge.public_group_daily_usd=group
            self.assertEqual(self.bridge.options({'plano':'gratuito'},'testador'),[])
            self.assertEqual(len(self.bridge.options({'admin':True},'luiz')),2)

    def test_public_limits_are_separate_and_operator_global_exemption_survives(self):
        cfg=self.bridge.configuration({'plano':'gratuito'},'testador')
        self.assertEqual(motors.limites_do_plano(cfg,'gratuito')['usd_dia'],1)
        self.assertEqual(cfg.haiku_public_group_limit,5)
        self.assertEqual(cfg.cota_global_usd,15)
        record={'admin':True,'plano':'operador','somente_limite_global':True,'modelo_claude':HAIKU.model}
        operator=self.bridge.configuration(record,'luiz')
        self.assertTrue(operator.somente_limite_global)
        self.assertFalse(hasattr(operator,'haiku_public_group_limit'))
        self.assertEqual(motors.limites_do_plano(operator,'operador')['usd_dia'],15)

    def test_availability_checks_effective_custom_price_not_default(self):
        for rates in [(1,.1,1000,1.25),(1,float('nan'),5,1.25),(1,.1,5),(-1,.1,5,1.25)]:
            self.cfg.precos_tabela[HAIKU.model]=rates
            self.assertEqual(self.bridge.options({'plano':'gratuito'},'testador'),[])

if __name__=='__main__':unittest.main()
