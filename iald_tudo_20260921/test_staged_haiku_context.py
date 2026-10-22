"""Offline context routes against the measured package and current public tools."""
import copy
import os
import unittest
import tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from haiku_stage_fixture import extract, measured, KERNEL, PUBLIC, CORE
from test_claude_route_bridge import motors
from test_claude_guard_real_converter import converter
from claude_profiles import HAIKU, SONNET
from claude_route_bridge import RouteBridge
from claude_memory_package import load_package
from claude_context_snapshot import (MeasuredSnapshot, context_metadata, attach_openai_tools,
                                     verify_native_tools)


class ContextIntegration(unittest.TestCase):
    def setUp(self):
        self.record = {'plano': 'gratuito', 'motor': 'claude', 'modelo_claude': HAIKU.model}
        self.cfg = motors.Config(chave='fixture', provedor='claude', modelo=SONNET.model,
                                modelo_operador=SONNET.model, contas=frozenset({'luiz'}))
        self.env = {'session': {'username': 'tester'}, 'jsonify': lambda v: v,
            'request': SimpleNamespace(headers={'X-IALD-Context':'anthropic-native-v1'}),
            '_motor_do_usuario': lambda user: (self.record['motor'], self.record),
            '_HAIKU_PROFILE': HAIKU, '_HaikuSnapshot': MeasuredSnapshot,
            '_haiku_metadata': context_metadata, '_haiku_attach_tools': attach_openai_tools,
            '_verify_haiku_tools': verify_native_tools, 'iald_motores': motors,
            'iald_kernel': KERNEL, 'iald_fontes_publicas': PUBLIC, 'iald_core_indexado': CORE,
            'iald_motor_claude': converter, 'CLAUDE_CFG': self.cfg, 'MOTORES_CFG': self.cfg,
            '_load_haiku_snapshot': lambda *a: measured(), 'load_package': object(),
            'SERVE_DIR': 'fixture', 'os': os,
            'HolographicMemory': SimpleNamespace(MARGEM_SEGURANCA=.92, RESPONSE_BUDGET=8192, CPT=2.91),
            'HOLO_MEMORY': SimpleNamespace(janela_do_modelo=lambda: 131072)}
        extract({'_haiku_tool_definitions', '_haiku_snapshot', '_haiku_selected', '_load_haiku_package', '_haiku_client_ready',
                 'api_contexto', 'api_motor', '_limites_da_conta', '_alerta_saldo_operador'}, self.env)
        self.bridge = RouteBridge(motors=motors, base_config=self.cfg,
            package_loader=self.env['_load_haiku_package'], enabled=True,
            public_daily_usd=1, public_group_daily_usd=5)
        self.env['CLAUDE_ROUTES'] = self.bridge
        self.env['_cfg_do_motor'] = lambda m, r: self.bridge.configuration(r, 'tester')

    def test_public_context_reports_measured_200k_and_not_legacy_32k(self):
        data, status = self.env['api_contexto']()
        self.assertEqual(status, 200)
        self.assertEqual((data['n_ctx'], data['memoria_tokens_medidos']), (200000, 183135))
        self.assertEqual(data['reserva_dinamica_medida'], 10271)
        self.assertEqual(data['margem_tokens'], 1024)
        self.assertLess(data['margem'], 1)
        self.assertIsNone(data['cpt'])
        self.assertNotIn('measurement_receipt', data)
        self.assertNotIn('C:', str(data))

    def test_current_tool_drift_refuses_status_without_any_network(self):
        changed = copy.deepcopy(CORE.tool_definitions())
        changed[0]['function']['description'] += ' drift'
        self.env['iald_core_indexado'] = SimpleNamespace(tool_definitions=lambda: changed)
        data, status = self.env['api_contexto']()
        self.assertEqual(status, 503)
        self.assertFalse(data['disponivel'])
        self.assertNotIn('n_ctx', data)

    def test_missing_package_and_disabled_public_budget_return_503(self):
        for failure in ('package', 'budget'):
            if failure == 'package':
                self.bridge.package_loader = Mock(side_effect=FileNotFoundError('private path'))
            else:
                self.bridge.package_loader = self.env['_load_haiku_package']
                self.bridge.public_daily_usd = None
            data, status = self.env['api_contexto']()
            self.assertEqual(status, 503)
            self.assertNotIn('private path', str(data))

    def test_limits_match_actual_schemas_without_private_atlas(self):
        data = self.env['_limites_da_conta']('claude', self.record, 'gratuito')
        self.assertEqual(data['janela'], 200000)
        self.assertEqual(data['max_saida'], 4096)
        self.assertFalse(data['pensar'])
        self.assertFalse(data['imagens'])
        self.assertEqual(len(data['ferramentas']), 7)
        self.assertNotIn('iald_atlas_read', data['ferramentas'])

    def test_other_provider_context_retains_legacy_contract(self):
        self.record['motor'] = 'nativa'
        data, status = self.env['api_contexto']()
        self.assertEqual((data['n_ctx'], data['cpt'], status), (131072, 2.91, 200))

    def test_old_client_does_not_receive_native_context_it_cannot_parse(self):
        self.env['request'].headers={}
        data,status=self.env['api_contexto']()
        self.assertEqual(status,426)
        self.assertNotIn('cpt',data)

    def test_non_object_manifest_returns_motor_503_instead_of_uncaught_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory,'manifest.json').write_text('[]',encoding='utf8')
            self.bridge.package_loader=lambda:load_package(directory)
            self.env['_cfg_do_motor']=lambda m,r,u:self.bridge.configuration(r,u)
            self.env.update({'_motor_selection_id':lambda *a:'claude-haiku',
                '_opcoes_de_motor':lambda *a:[], '_consentimento_do_motor':lambda *a:{},
                '_consentimentos_registrados':lambda *a:[]})
            data,status=self.env['api_motor']()
            self.assertEqual(status,503)
            self.assertFalse(data['disponivel'])
            self.assertNotIn(directory,str(data))

    def test_operational_balances_do_not_enter_conversation_even_for_admin(self):
        balance = Mock()
        self.assertIsNone(self.env['_alerta_saldo_operador']({'admin': True}, [], 'luiz', [balance]))
        balance.alerta_para_conversa.assert_not_called()


if __name__ == '__main__':
    unittest.main()
