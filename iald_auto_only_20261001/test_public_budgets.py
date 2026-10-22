"""Independent offline review: staged code, AST server functions, synthetic SQLite.

Never imports the web server, reads account/config stores, or calls a provider.
"""
import ast
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import threading
from types import SimpleNamespace
import unittest
import uuid

WORK = Path(__file__).resolve().parent
STAGE = WORK / 'stage'
ROOT = Path(r'C:/IALD/projetos_pyhton/IALD')
sys.dont_write_bytecode = True
sys.path[:0] = [str(STAGE), str(ROOT)]
import iald_task_bridge as bridge
import iald_auto_router as router
import iald_app_providers as providers
from claude_account_policy import available_models
from claude_profiles import SONNET


def extracted(path, names, env, constants=False):
    tree = ast.parse(path.read_bytes())
    nodes = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names:
            node.decorator_list = []
            nodes.append(node)
        elif constants and isinstance(node, ast.Assign):
            nodes.append(node)
    assert {n.name for n in nodes if isinstance(n, (ast.FunctionDef, ast.ClassDef))} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), env)
    return env


# Extract only the actual SQLite guard and its constants; no memory/config imports.
budget = extracted(ROOT / 'iald_orcamento.py', {'BudgetError', 'SpendingGuard', '_today'},
    dict(datetime=datetime, timezone=timezone, contextmanager=contextmanager,
         json=json, math=math, Path=Path, sqlite3=sqlite3, uuid=uuid), constants=True)
BudgetError, SpendingGuard = budget['BudgetError'], budget['SpendingGuard']
spend = extracted(STAGE / 'iald_app_spend.py', {'PublicAccount', '_positive'},
    dict(json=json, math=math, Path=Path, re=re, threading=threading,
         MODELS=providers.MODELS, BudgetError=BudgetError, SpendingGuard=SpendingGuard))
PublicAccount = spend['PublicAccount']


def cfg(**changes):
    result = SimpleNamespace(modelo='synthetic-haiku', precos=lambda model: (1., .1, 5., 1.25),
        cota_operador_usd=.5, cota_usuario_usd=.5, cota_global_usd=5.,
        somente_limite_global=False, haiku_public_group_limit=.7,
        task_quota_key='synthetic-identity', task_plan='gratuito')
    result.__dict__.update(changes)
    return result


def body():
    return {'model': providers.MODELS['mimo']['model'], 'max_completion_tokens': 131072,
            'messages': [{'role': 'user', 'content': 'Synthetic public request'}]}


class PublicBudgetTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=WORK)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.guard = SpendingGuard(self.root / 'synthetic.sqlite3')
        self.entries = []
        self.ledger = SimpleNamespace(registrar=lambda *a, **k: self.entries.append((a, k)))

    def test_sandbox_cannot_bypass_exhausted_shared_haiku_group(self):
        self.guard.reserve('other', 'synthetic-haiku', .7, 1., 5., group='haiku_public', group_limit=.7)
        account = bridge.SandboxAccount(self.guard, cfg(), 'liana', self.ledger)
        with self.assertRaises(BudgetError): account.before(1000, 8192)
        self.assertIsNone(account.key)

    def test_sandbox_shares_existing_identity_quota(self):
        self.guard.reserve('previous-name', 'synthetic-haiku', .49, .5, 5.,
                           quota_key='synthetic-identity', group='haiku_public', group_limit=.7)
        account = bridge.SandboxAccount(self.guard, cfg(), 'liana', self.ledger)
        with self.assertRaises(BudgetError): account.before(1000, 8192)

    def test_sandbox_ledger_retains_identity_and_plan(self):
        account = bridge.SandboxAccount(self.guard, cfg(), 'liana', self.ledger)
        account.before(1000, 8192)
        account.settle({'input_tokens': 100, 'output_tokens': 10})
        account.close()
        self.assertEqual(self.entries[0][1]['chave_cota'], 'synthetic-identity')
        self.assertEqual(self.entries[0][1]['plano'], 'gratuito')
        self.assertTrue(self.entries[0][1]['estimado'])

    def test_cancel_without_usage_retains_sandbox_hold(self):
        account = bridge.SandboxAccount(self.guard, cfg(), 'liana', self.ledger)
        account.before(1000, 8192)
        before = self.guard.used_today()
        account.close(); account.close()
        self.assertGreater(before, 0)
        self.assertEqual(self.guard.used_today(), before)

    def test_mimo_outer_and_child_accounts_share_daily_hold(self):
        key = hashlib.sha256(b'liana').hexdigest()
        outer = PublicAccount(self.root, key, .2, .6, 2.)
        child = PublicAccount(self.root, key, .2, .6, 2.)
        outer.before('mimo', body(), 1024)
        with self.assertRaises(BudgetError): child.before('mimo', body(), 1024)
        outer.close(); child.close()
        with self.assertRaises(BudgetError):
            PublicAccount(self.root, key, .2, .6, 2.).before('mimo', body(), 1024)

    def test_mimo_two_accounts_share_group(self):
        first = PublicAccount(self.root, 'a' * 64, .2, .2, 2.)
        second = PublicAccount(self.root, 'b' * 64, .2, .2, 2.)
        first.before('mimo', body(), 1024)
        with self.assertRaises(BudgetError): second.before('mimo', body(), 1024)
        first.close(); second.close()

    def test_luiz_does_not_acquire_new_public_group_limit(self):
        operator = cfg(cota_global_usd=5., somente_limite_global=True)
        del operator.haiku_public_group_limit
        self.guard.reserve('public', 'synthetic-haiku', .7, 1., 5., group='haiku_public', group_limit=.7)
        account = bridge.SandboxAccount(self.guard, operator, 'luiz', self.ledger)
        account.before(1000, 8192)
        self.assertIsNotNone(account.key)
        account.close()


class ScopeTests(PublicBudgetTests):
    def setUp(self):
        super().setUp()
        self.records = {name: {'plano': 'gratuito', 'consents': {'automatico', 'mimo', 'kimi', 'claude'}}
                        for name in ('luiz', 'liana', 'alanacaroline', 'ordinary')}
        self.streams = []
        self.remote_sends = 0
        self.revoke_during_routing = False
        self.route_count = 0

        def choose(prompt, candidates, **kwargs):
            self.route_count += 1
            self.assertNotIn('deepseek', candidates)
            if self.revoke_during_routing:
                self.records[self.user]['consents'].discard('mimo')
            return 'mimo', {'id': 'synthetic-routing'}

        def stream(provider, messages, tools, execute, **kwargs):
            self.streams.append(kwargs)
            account = kwargs['spending']
            try:
                if account: account.before(provider, body(), 1024)
                self.remote_sends += 1  # Synthetic counter; no network function exists.
                if account: account.settle(providers.usage_cost('mimo',
                    {'prompt_tokens': 100, 'completion_tokens': 10, 'total_tokens': 110}))
                yield 'data: ' + json.dumps({'choices': [{'delta': {'content': 'Synthetic draft'}}]}) + '\n\n'
                yield 'data: [DONE]\n\n'
            finally:
                if account: account.close()

        motors = SimpleNamespace(CLAUDE='claude', consentiu=lambda record, key: key in record.get('consents', ()),
                                 plano_de=lambda record: record['plano'])
        routes = SimpleNamespace(package=lambda: SimpleNamespace(prefix='Synthetic verified public memory'),
            public_budget=lambda: (.2, .6), base=SimpleNamespace(cota_global_usd=2.),
            select=lambda key, record, owner: {'motor': 'claude', 'modelo_claude': 'synthetic-haiku'},
            configuration=lambda record, owner: cfg())
        offered = SimpleNamespace(MODELS=providers.MODELS, allowed=providers.allowed,
            options=lambda record, owner: [{'id': key, 'disponivel': True}
                for key in providers.MODELS if providers.allowed(record, owner, key)])
        self.env = extracted(STAGE / 'iald_web_server.py', {'_new_app_task_scope', '_automatic_budget_available'},
            dict(load_users_estrito=lambda: self.records, app_router=SimpleNamespace(AUTO=router.AUTO,
                 allowed=router.allowed, choose=choose, budget_remaining=router.budget_remaining), iald_motores=motors, app_providers=offered,
                 CLAUDE_ROUTES=routes, task_bridge=bridge, SERVE_DIR=self.root,
                 APP_EVALUATION=SimpleNamespace(stream=stream), app_spend=SimpleNamespace(PublicAccount=PublicAccount),
                 hashlib=hashlib, iald_motor_claude=SimpleNamespace(cliente_para=lambda config: None),
                 _guarda_do_motor=lambda motor: self.guard, RAZAO_CLAUDE=self.ledger,
                 _chave_cota_de=lambda record, owner: 'synthetic-identity'))

    def scope(self, user='liana'):
        self.user = user
        return self.env['_new_app_task_scope'](user)

    def test_scope_delegate_has_real_user_budget_and_distinct_execution_lock(self):
        scope = self.scope()
        result = scope.execute('delegate_task', {'role': 'implement', 'objective': 'Synthetic draft'})
        self.assertEqual(result['status'], 'DRAFT_COMPLETED')
        real_key = hashlib.sha256(b'liana').hexdigest()
        self.assertEqual(self.streams[0]['spending'].account_key_hash, real_key)
        self.assertNotEqual(self.streams[0]['account_key'], real_key)
        self.assertEqual(self.remote_sends, 1)

    def test_scope_budget_failure_prevents_child_send_and_is_not_retried(self):
        key = hashlib.sha256(b'liana').hexdigest()
        outer = PublicAccount(self.root, key, .2, .6, 2.)
        outer.before('mimo', body(), 1024)
        scope = self.scope()
        args = {'role': 'implement', 'objective': 'Synthetic draft'}
        self.assertEqual(scope.execute('delegate_task', args)['status'], 'FAILED_OR_UNCERTAIN')
        self.assertEqual(scope.execute('delegate_task', args)['status'], 'PREVIOUS_ATTEMPT_UNCERTAIN')
        self.assertEqual(self.remote_sends, 0)
        self.assertEqual(self.route_count, 1)
        outer.close()

    def test_scope_revocation_after_router_prevents_child_send(self):
        scope = self.scope()
        self.revoke_during_routing = True
        result = scope.execute('delegate_task', {'role': 'implement', 'objective': 'Synthetic draft'})
        self.assertEqual(result['status'], 'FAILED_OR_UNCERTAIN')
        self.assertEqual(self.remote_sends, 0)
        self.assertEqual(self.streams, [])

    def test_scope_nonexistent_blocked_or_without_auto_consent_is_denied(self):
        self.records['liana']['bloqueado'] = True
        for user in ('liana', 'missing'):
            with self.subTest(user=user), self.assertRaises(PermissionError): self.scope(user)
        self.records['ordinary']['consents'].discard('automatico')
        with self.assertRaises(PermissionError): self.scope('ordinary')

    def test_scope_luiz_keeps_no_public_mimo_budget(self):
        scope = self.scope('luiz')
        result = scope.execute('delegate_task', {'role': 'implement', 'objective': 'Synthetic draft'})
        self.assertEqual(result['status'], 'DRAFT_COMPLETED')
        self.assertIsNone(self.streams[0]['spending'])

    def test_scope_journal_does_not_store_prompt_or_account_name(self):
        scope = self.scope('alanacaroline')
        scope.execute('delegate_task', {'role': 'implement', 'objective': 'PRIVATE-SYNTHETIC-CANARY'})
        journal = scope.path.read_text(encoding='utf-8')
        self.assertNotIn('alanacaroline', journal)
        self.assertNotIn('PRIVATE-SYNTHETIC-CANARY', journal)


class BudgetGateTests(ScopeTests):
    def setUp(self):
        super().setUp()
        self.reading = dict(gasto_global=0., gasto_plano=0., gasto_conta=0.,
                            usd_dia_cota=0., tokens_dia=0, tokens_mes=0)
        self.config = cfg(cota_global_gratuito_usd=1., planos={
            'gratuito': dict(usd_dia=.5, tokens_dia=100, tokens_mes=300,
                             max_saida=100, agente=True, pensar=True)})
        del self.config.haiku_public_group_limit
        names = {'config_da_conta', 'limites_do_plano', 'verificar_permissao'}
        env = dict(PLANOS={'gratuito', 'operador', 'assinante'}, GRATUITO='gratuito',
                   OPERADOR='operador', plano_de=lambda record: record['plano'])
        for name in ('MSG_RAZAO_ILEGIVEL', 'MSG_GLOBAL', 'MSG_GLOBAL_GRATUITO',
                     'MSG_CONTA_DIA', 'MSG_GRATUITO_DIA', 'MSG_GRATUITO_MES',
                     'MSG_CONTA_MES', 'MSG_MINUTO'):
            env[name] = name
        extracted(ROOT / 'iald_motores.py', names, env)
        for name in names: setattr(self.env['iald_motores'], name, env[name])
        self.env['iald_motores'].GRATUITO = 'gratuito'
        self.env['iald_motores'].OPERADOR = 'operador'
        self.env['MOTORES_CFG'] = self.config
        self.env['_razao_do_motor'] = lambda motor: SimpleNamespace(
            leitura_de_cota=lambda *args: dict(self.reading))
        self.env['CLAUDE_ROUTES'].configuration = lambda record, user: cfg(
            cota_global_gratuito_usd=1., planos=self.config.planos)

    def gate(self, provider, user='ordinary'):
        return self.env['_automatic_budget_available'](self.records[user], user, provider)

    def exhaust_mimo(self, user='ordinary', amount=.2, group_limit=.6):
        key = hashlib.sha256(user.encode()).hexdigest()
        account = PublicAccount(self.root, key, amount, group_limit, 2.)
        account.guard.reserve(key, 'synthetic', amount, amount, 2.,
                              quota_key=key, group='mimo_public', group_limit=group_limit)
        account.close()

    def test_delegate_exhausted_account_stops_before_jev_and_preserves_no_repeat(self):
        self.exhaust_mimo()
        self.records['ordinary']['consents'].discard('kimi')
        scope = self.scope('ordinary')
        args = {'role': 'implement', 'objective': 'Synthetic draft'}
        self.assertEqual(scope.execute('delegate_task', args)['status'], 'FAILED_OR_UNCERTAIN')
        self.assertEqual(scope.execute('delegate_task', args)['status'], 'PREVIOUS_ATTEMPT_UNCERTAIN')
        self.assertEqual(self.route_count, 0)
        self.assertEqual(self.remote_sends, 0)

    def test_public_mimo_reads_group_holds_without_creating_calls(self):
        self.exhaust_mimo('liana', .6)
        self.assertFalse(self.gate('mimo'))
        self.assertFalse(self.gate('mimo'))
        account = PublicAccount(self.root, hashlib.sha256(b'ordinary').hexdigest(), .2, .6, 2.)
        with account.guard._connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM calls').fetchone()[0], 1)
        account.close()

    def manager(self, offered):
        self.env['app_router'].DESCRIPTIONS = router.DESCRIPTIONS
        self.env['app_providers'].wire_messages = lambda *args: None
        self.env['_opcoes_de_motor'] = lambda record, user: [
            {'id': key, 'disponivel': True} for key in offered]
        self.env['_consentimento_automatico'] = lambda *args: {'dado': True}
        self.env['_sse_aviso'] = lambda message, kind, *args: SimpleNamespace(kind=kind)
        self.env['_new_app_task_scope'] = lambda user: None
        self.env['_dispatch_guard'] = lambda *args: lambda: None
        extracted(STAGE / 'iald_web_server.py', {'_chat_automatico_autorizado'}, self.env)
        return self.env['_chat_automatico_autorizado'](
            {'messages': [{'role': 'user', 'content': 'Synthetic request'}]},
            'ordinary', self.records['ordinary'], True, 10)

    def test_manager_all_exhausted_returns_limit_without_jev(self):
        self.exhaust_mimo()
        self.assertEqual(self.manager(['mimo']).kind, 'limite')
        self.assertEqual(self.route_count, 0)
        self.assertEqual(self.remote_sends, 0)

    def test_manager_filters_exhausted_provider_before_jev(self):
        self.exhaust_mimo()
        self.records['ordinary']['consents'].add('openai')
        seen = []
        def choose(prompt, candidates):
            seen.append(candidates)
            return candidates[0], {'id': 'synthetic'}
        self.env['app_router'].choose = choose
        self.env['_chat_openai'] = lambda *args, **kwargs: SimpleNamespace(kind='synthetic-openai')
        self.assertEqual(self.manager(['mimo', 'openai']).kind, 'synthetic-openai')
        self.assertEqual(seen, [['openai']])

    def test_openai_existing_plan_ledger_limits_all_gate_routing(self):
        self.assertTrue(self.gate('openai'))
        for key, value in dict(gasto_global=5., gasto_plano=1., gasto_conta=.5,
                               usd_dia_cota=.5, tokens_dia=100, tokens_mes=300).items():
            with self.subTest(key=key):
                self.reading[key] = value
                self.assertFalse(self.gate('openai'))
                self.reading[key] = 0

    def test_openai_active_holds_use_real_identity_and_current_plan(self):
        self.guard.reserve('previous-name', 'synthetic', .5, .5, 5.,
                           quota_key='synthetic-identity', group='gratuito', group_limit=1.)
        self.assertFalse(self.gate('openai'))

    def test_haiku_shared_group_blocks_before_routing(self):
        self.guard.reserve('other', 'synthetic', .7, 1., 5.,
                           quota_key='other', group='haiku_public', group_limit=.7)
        self.assertFalse(self.gate('claude-haiku'))
        self.assertTrue(self.gate('openai'))

    def test_invalid_guard_read_fails_closed_in_server(self):
        with self.guard._connect() as db: db.execute('DROP TABLE calls')
        self.assertFalse(self.gate('openai'))

    def test_operator_mimo_and_family_kimi_retain_existing_policy(self):
        self.exhaust_mimo('luiz')
        self.assertTrue(self.gate('mimo', 'luiz'))
        self.assertTrue(self.gate('kimi', 'liana'))
        self.assertTrue(self.gate('kimi', 'ordinary'))
        self.records['liana']['bloqueado'] = True
        self.assertFalse(self.gate('kimi', 'liana'))


class PolicyTests(unittest.TestCase):
    def test_default_does_not_mutate_records_or_override_new_manual_choice(self):
        for user in ('luiz', 'liana', 'alanacaroline', 'ordinary'):
            record = {'motor': 'openai', 'plano': 'gratuito'}
            before = dict(record)
            self.assertTrue(router.default_for(record, user))
            self.assertEqual(record, before)
            record['motor_escolha_versao'] = router.DEFAULT_POLICY
            self.assertEqual(router.default_for(record, user), user != 'luiz')
        self.assertFalse(router.default_for({}, 'ordinary'))
        self.assertFalse(router.default_for({'bloqueado': True}, 'ordinary'))

    def test_provider_matrix_and_sonnet_owner_only_preserved(self):
        for user in ('luiz', 'liana', 'alanacaroline', 'ordinary'):
            record = {'plano': 'gratuito'}
            self.assertTrue(providers.allowed(record, user, 'mimo'))
            self.assertTrue(providers.allowed(record, user, 'kimi'))
            self.assertTrue(providers.allowed(record, user, 'deepseek'))
            models = available_models(username=user, account_approved=True, haiku_ready=True, sonnet_ready=True)
            self.assertEqual(SONNET.model in models, user == 'luiz')

    def test_automatic_consent_bootstraps_one_provider_without_granting_it(self):
        def consent(record, key):
            return {'provedor': key, 'dado': key in record['consents'], 'versao': 2 if key == router.AUTO else 1}
        env = extracted(STAGE / 'iald_web_server.py', {'_consentimento_automatico'},
            dict(app_router=router, _consentimento_do_motor=consent,
                 iald_motores=SimpleNamespace(consentiu=lambda record, key: key in record['consents']),
                 _opcoes_de_motor=lambda record, user: [{'id': key, 'disponivel': True} for key in ('mimo', 'openai')]))
        record = {'consents': set()}
        self.assertEqual(env['_consentimento_automatico'](record, 'ordinary')['provedor'], router.AUTO)
        record['consents'].add(router.AUTO)
        self.assertEqual(env['_consentimento_automatico'](record, 'ordinary')['provedor'], 'mimo')
        self.assertEqual(record['consents'], {router.AUTO})
        record['consents'].add('openai')
        self.assertTrue(env['_consentimento_automatico'](record, 'ordinary')['dado'])
        self.assertNotIn('mimo', record['consents'])


def load_tests(loader, tests, pattern):
    # Avoid inherited budget cases being repeated by ScopeTests.
    return unittest.TestSuite(cls(name) for cls in (PublicBudgetTests, ScopeTests, BudgetGateTests, PolicyTests)
                              for name in sorted(cls.__dict__) if name.startswith('test_'))


if __name__ == '__main__': unittest.main(verbosity=2)
