import ast
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import socket
import sys
import tempfile
import unittest
from unittest.mock import patch

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode = True
sys.path[:0] = [str(WORK / 'stage'), str(ROOT)]
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')
import iald_motores as mt
import iald_orcamento as budget

# Execute only these pure route helpers; never import/start the live server.
tree = ast.parse((WORK / 'stage/iald_web_server.py').read_text(encoding='utf-8'))
names = {'_bloqueio_da_cota', '_chave_cota_de', '_estado_da_cota_da_conta'}
helpers = ast.Module(body=[node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names], type_ignores=[])

class GlobalOnlyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='iald_global_only_')
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.base = mt.Config(cota_global_usd=1, cota_operador_usd=0,
                              pedidos_por_minuto=0,
                              planos={mt.OPERADOR: {'tokens_dia': 0, 'tokens_mes': 0, 'usd_dia': 0}})
        self.owner = {'admin': True, 'somente_limite_global': True}
        self.cfg = mt.config_da_conta(self.base, self.owner)
        self.ledger = mt.RazaoDeUso(str(self.path / 'usage.json'))
        self.rate = mt.JanelaDePedidos(0)

    def allowed(self, cfg=None, admin=True, plano=mt.OPERADOR):
        return mt.verificar_permissao(cfg or self.cfg, self.ledger, self.rate, 'owner',
            admin=admin, plano=plano, chave_cota='owner', detalhado=True)

    def test_only_explicit_trusted_operator_is_exempt(self):
        self.assertTrue(self.cfg.somente_limite_global)
        for record in ({'admin': True}, {'somente_limite_global': True},
                       {'admin': 'true', 'somente_limite_global': True},
                       {'admin': True, 'somente_limite_global': 'true'},
                       dict(self.owner, plano=mt.GRATUITO), dict(self.owner, plano=mt.ASSINANTE)):
            self.assertFalse(mt.config_da_conta(self.base, record).somente_limite_global)
        self.assertFalse(self.base.somente_limite_global)
        self.assertFalse(mt.config_da_conta(self.cfg, {'admin': True}).somente_limite_global)

    def test_all_personal_caps_bypassed_and_usage_kept(self):
        self.ledger.registrar('owner', 'test', 5, 0, 5, .5, chave_cota='owner', tokens=999999999, plano=mt.OPERADOR)
        self.assertTrue(self.allowed()[0])
        self.assertTrue(self.allowed(plano=None)[0])
        self.assertFalse(self.allowed(cfg=self.base)[0])
        self.assertFalse(self.allowed(admin=False)[0])
        state = mt.estado_da_cota(self.cfg, self.ledger, 'owner', mt.OPERADOR, 'owner')
        self.assertEqual(state['tokens_dia']['usado'], 999999999)
        for field in ('tokens_dia', 'tokens_mes', 'usd_dia'):
            self.assertIsNone(state[field]['limite'])
        self.assertEqual(state['global_usd_dia'], {'usado': .5, 'limite': 1})
        json.dumps(state, allow_nan=False)

    def test_global_still_blocks_at_cap_and_zero(self):
        self.ledger.registrar('someone_else', 'test', 1, 0, 1, 1)
        self.assertEqual(self.allowed()[2], 'global')
        self.assertEqual(self.allowed(plano=None)[2], 'global')
        self.cfg.cota_global_usd = 0
        self.assertEqual(self.allowed()[2], 'global')

    def test_unreadable_ledger_remains_closed(self):
        with patch.object(self.ledger, 'leitura_de_cota', side_effect=ValueError('test corrupt ledger')):
            self.assertEqual(self.allowed()[2], 'razao')
            self.assertIn('erro', mt.estado_da_cota(self.cfg, self.ledger, 'owner', mt.OPERADOR, 'owner'))

    def test_personal_rpm_only_bypassed_for_owner(self):
        base = mt.Config(cota_global_usd=1)
        self.assertEqual(self.allowed(cfg=base)[2], 'minuto')
        self.assertTrue(self.allowed(cfg=mt.config_da_conta(base, self.owner))[0])

    def test_route_metadata_uses_trusted_account_and_handles_null(self):
        guard = budget.SpendingGuard(self.path / 'metadata.sqlite3')
        key = guard.reserve('another_call', 'test', .7, 1, 1)
        scope = {'iald_motores': mt, 'MOTORES_CFG': self.base, 'RAZAO_OPENAI': self.ledger,
                 '_guarda_openai': lambda: guard}
        exec(compile(helpers, 'isolated_route_helpers', 'exec'), scope)
        state = scope['_estado_da_cota_da_conta']('owner', self.owner)
        self.assertEqual(state['bloqueado_por'], '')
        self.assertTrue(state['somente_limite_global'])
        self.assertEqual(state['global_usd_dia']['usado'], .7)
        guard.settle(key, .4)
        self.assertEqual(scope['_estado_da_cota_da_conta']('owner', self.owner)['global_usd_dia']['usado'], .4)
        other = scope['_estado_da_cota_da_conta']('other_admin', {'admin': True})
        self.assertEqual(other['bloqueado_por'], 'usd_dia')
        self.assertNotIn('global_usd_dia', other)
        with patch.object(guard, 'used_today', side_effect=ValueError('bad database')):
            self.assertIn('erro', scope['_estado_da_cota_da_conta']('owner', self.owner))
            self.assertNotIn('erro', scope['_estado_da_cota_da_conta']('other_admin', {'admin': True}))

    def test_real_reservation_inherits_global_and_blocks_overcommit(self):
        guard = budget.SpendingGuard(self.path / 'spending.sqlite3')
        legacy = mt.ContaDoPedido(self.ledger, 'owner', 'gpt-5-nano', self.cfg.precos('gpt-5-nano'))
        account = budget.ReservedAccount(guard, legacy, self.cfg, 'owner', True, 'gpt-5-nano')
        payload = {'messages': [{'role': 'user', 'content': 'hello'}], 'max_completion_tokens': 20}
        with patch.object(budget, 'input_estimates', return_value=(10, 10)):
            account.iniciar_chamada(payload)  # personal USD cap is zero
            self.assertIsNotNone(account.key)
            account.descartar_ultima_chamada()
            key = guard.reserve('someone_else', 'test', 1, 1, 1)
            with self.assertRaises(budget.BudgetError) as caught:
                account.iniciar_chamada(payload)
            self.assertEqual(caught.exception.bloqueado_por, 'global')
            guard.settle(key, 1)
            self.cfg.cota_global_usd = 2
            account.iniciar_chamada(payload)  # follows new global; no copied/stale cap
            account.descartar_ultima_chamada()
        account.fechar()

    def test_atomic_shared_cap_for_concurrent_requests(self):
        guard = budget.SpendingGuard(self.path / 'parallel.sqlite3')
        def reserve(i):
            try:
                return guard.reserve('owner', 'test', .6, 1, 1)
            except budget.BudgetError as exc:
                self.assertEqual(exc.bloqueado_por, 'global')
                return None
        with ThreadPoolExecutor(max_workers=2) as pool:
            keys = list(pool.map(reserve, range(2)))
        self.assertEqual(sum(k is not None for k in keys), 1)

if __name__ == '__main__':
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('No network in tests')):
        unittest.main(verbosity=2)
