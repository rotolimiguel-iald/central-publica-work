"""Offline real SQLite/SpendingGuard tests. No API, real accounts or credentials.

Run: C:\\Python314\\python.exe -B -X utf8 <this file>
Only temporary fixture databases are written; ROOT modules are imported read-only.
"""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

W = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.dont_write_bytecode = True
sys.path[:0] = [str(W / 'stage'), str(ROOT)]


def audit(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto', 'subprocess.Popen'):
        raise RuntimeError('Network/process execution forbidden in spend fixtures')
    if event == 'open' and isinstance(args[0], (str, bytes)):
        name = Path(args[0].decode() if isinstance(args[0], bytes) else args[0]).name.lower()
        if name.startswith('.env') or name in ('iald_users.json', 'iald_pedidos_acesso.json', 'um.py',
                                               'iald_stack_v7.py', 'iald_psion_state.json'):
            raise RuntimeError('Private/canonical state forbidden')


sys.addaudithook(audit)
from iald_app_spend import PublicAccount, BudgetError
from iald_app_providers import MODELS, usage_cost


class SpendTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='iald-spend-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.body = dict(model=MODELS['mimo']['model'], messages=[dict(role='user', content='synthetic á')],
                         max_completion_tokens=MODELS['mimo']['output'], stream=True)
        self.bound = len(json.dumps(self.body, ensure_ascii=False).encode('utf-8'))
        self.cap = (self.bound * .435 + 131072 * .87) / 1e6

    def account(self, name='fixture-a', daily=1., group=5., total=15.):
        return PublicAccount(self.root, hashlib.sha256(name.encode()).hexdigest(), daily, group, total)

    def rows(self):
        with closing(sqlite3.connect(self.root / '.iald_runtime/app_evaluation/public_spend.sqlite3')) as db:
            return db.execute('SELECT id,user,cap,actual,status,group_name FROM calls ORDER BY rowid').fetchall()

    def measured(self, pin=100, out=10, cached=20):
        return usage_cost('mimo', dict(prompt_tokens=pin, completion_tokens=out, total_tokens=pin+out,
                                     prompt_tokens_details={'cached_tokens': cached}))

    def test_exact_rate_full_output_and_immutable_wire(self):
        a = self.account(); original = deepcopy(self.body)
        key = a.before('mimo', self.body, self.bound)
        self.assertEqual(self.body, original)
        row = self.rows()[0]
        self.assertEqual(row[0], key); self.assertAlmostEqual(row[2], self.cap)
        self.assertIsNone(row[3]); self.assertEqual(row[4:], ('reserved', 'mimo_public'))
        measured = self.measured()
        a.settle(measured)
        self.assertAlmostEqual(self.rows()[0][3], (80*.435 + 20*.0036 + 10*.87)/1e6)
        a.close()
        self.assertEqual(self.rows()[0][4], 'settled')

    def test_daily_refusal_before_dispatch(self):
        a = self.account(daily=self.cap/2); sends = []
        with self.assertRaises(BudgetError) as caught:
            a.before('mimo', self.body, self.bound)
            sends.append('must not send')
        self.assertEqual(caught.exception.bloqueado_por, 'usd_dia')
        self.assertEqual(sends, []); self.assertEqual(self.rows(), [])

    def test_separate_rounds_and_new_instance_share_account_quota(self):
        a = self.account(daily=self.cap*1.5)
        first = a.before('mimo', self.body, self.bound); a.settle(self.measured())
        second = a.before('mimo', self.body, self.bound)
        self.assertNotEqual(first, second); a.close()
        b = self.account(daily=self.cap*1.5)
        with self.assertRaises(BudgetError): b.before('mimo', self.body, self.bound)
        self.assertEqual([r[4] for r in self.rows()], ['settled', 'estimated_upper_bound'])

    def test_uncertain_round_cannot_be_replaced(self):
        a = self.account(); key = a.before('mimo', self.body, self.bound)
        with self.assertRaises(BudgetError): a.before('mimo', self.body, self.bound)
        self.assertEqual(self.rows()[0][0], key); self.assertEqual(len(self.rows()), 1)
        a.close(); a.close()
        self.assertEqual(self.rows()[0][3], self.rows()[0][2])
        self.assertEqual(self.rows()[0][4], 'estimated_upper_bound')
        with self.assertRaises(BudgetError): a.before('mimo', self.body, self.bound)

    def test_invalid_usage_retains_cap(self):
        for value in (None, dict(self.measured(), cost_estimate_usd=float('nan')),
                      dict(self.measured(), cost_estimate_usd=0), dict(self.measured(), cached_tokens=101),
                      dict(self.measured(), input_tokens=True)):
            with self.subTest(value_type=type(value).__name__):
                a = self.account(); a.before('mimo', self.body, self.bound)
                with self.assertRaises(BudgetError): a.settle(value)
                self.assertIsNotNone(a.pending); a.close()
                self.assertEqual(self.rows()[-1][4], 'estimated_upper_bound')

    def test_over_cap_is_recorded_and_pauses_next_round(self):
        a = self.account(); a.before('mimo', self.body, self.bound)
        usage = self.measured(pin=1_000_000, out=131072, cached=0)
        with self.assertRaises(BudgetError) as caught: a.settle(usage)
        self.assertEqual(caught.exception.bloqueado_por, 'conferencia')
        self.assertEqual(self.rows()[0][3], usage['cost_estimate_usd'])
        self.assertGreater(self.rows()[0][3], self.rows()[0][2])
        with self.assertRaises(BudgetError): a.before('mimo', self.body, self.bound)
        a.close(); self.assertEqual(len(self.rows()), 1)

    def test_close_persistence_failure_keeps_cursor_for_local_recovery(self):
        a = self.account(); a.before('mimo', self.body, self.bound)
        with patch.object(a.guard, 'settle', side_effect=BudgetError('fixture write failure')):
            with self.assertRaises(BudgetError): a.close()
        self.assertFalse(a.closed); self.assertIsNotNone(a.pending)
        a.close(); self.assertEqual(self.rows()[0][4], 'estimated_upper_bound')

    def test_settle_persistence_failure_keeps_cursor(self):
        a = self.account(); a.before('mimo', self.body, self.bound)
        with patch.object(a.guard, 'settle', side_effect=BudgetError('fixture write failure')):
            with self.assertRaises(BudgetError): a.settle(self.measured())
        self.assertIsNotNone(a.pending)
        a.close(); self.assertEqual(self.rows()[0][3], self.rows()[0][2])

    def test_group_reservations_are_atomic_across_instances(self):
        limit = self.cap * 1.5
        accounts = [self.account('fixture-'+str(i), daily=limit, group=limit) for i in range(2)]
        barrier = threading.Barrier(2)
        def reserve(a):
            barrier.wait(timeout=5)
            try: a.before('mimo', self.body, self.bound); return 'reserved'
            except BudgetError as e: return e.bloqueado_por
        with ThreadPoolExecutor(max_workers=2) as pool: results = list(pool.map(reserve, accounts))
        self.assertCountEqual(results, ['reserved', 'global'])
        self.assertEqual(len(self.rows()), 1)
        for a in accounts: a.close()

    def test_total_includes_other_groups_in_this_database(self):
        a = self.account(daily=self.cap*2, group=self.cap*2, total=self.cap*2)
        a.guard.reserve('other-fixture', 'other', self.cap*1.5, 15, 15, group='other')
        with self.assertRaises(BudgetError) as caught: a.before('mimo', self.body, self.bound)
        self.assertEqual(caught.exception.bloqueado_por, 'global')

    def test_limits_and_hash_fail_closed_before_database_creation(self):
        for bad in (None, True, 0, -1, float('nan'), float('inf'), '1'):
            with self.assertRaises(BudgetError): self.account(daily=bad)
        with self.assertRaises(BudgetError): self.account(daily=6, group=5)
        with self.assertRaises(BudgetError): PublicAccount(self.root, 'raw-username', 1, 5, 15)
        self.assertFalse((self.root/'.iald_runtime').exists())

    def test_wrong_provider_model_output_or_underbound_never_reserves(self):
        a = self.account()
        for provider in ('kimi', 'deepseek', 'openai'):
            with self.assertRaises(BudgetError): a.before(provider, self.body, self.bound)
        for body, bound in [(dict(self.body, model='other'), self.bound), (self.body, self.bound-1),
                            (dict(self.body, n=2), self.bound+100),
                            (dict(self.body, max_completion_tokens=131073), self.bound+100),
                            (dict(self.body, max_completion_tokens=True), self.bound+100),
                            (self.body, True)]:
            with self.assertRaises(BudgetError): a.before('mimo', body, bound)
        self.assertEqual(self.rows(), [])

    def test_price_invalid_never_reserves(self):
        a = self.account()
        for rates in ((float('nan'), .0036, .87), (0, .0036, .87), (True, .0036, .87)):
            with patch.dict(MODELS['mimo'], rates=rates):
                with self.assertRaises(BudgetError): a.before('mimo', self.body, self.bound)
        self.assertEqual(self.rows(), [])

    def test_smaller_output_still_reserves_full_model_maximum(self):
        a = self.account(); body = dict(self.body, max_completion_tokens=1)
        a.before('mimo', body, self.bound)
        self.assertAlmostEqual(self.rows()[0][2], self.cap)
        a.close()


    def run_evaluation(self, account, response):
        # Real staged Evaluation + real SpendingGuard. Only credential provider
        # and HTTP are fixtures; no network function can run under the audit hook.
        import iald_app_providers as providers
        from types import SimpleNamespace
        sent = []
        def post(*args, **kwargs):
            sent.append(kwargs['headers'])
            return response
        ev = providers.Evaluation(self.root)
        with patch.object(providers, 'adapter', return_value=SimpleNamespace(load_mimo=lambda: 'fixture-key')):
            output = ''.join(ev.stream('mimo', [dict(role='system', content='fixture core'),
                dict(role='user', content='fixture request')], [], lambda *args: None,
                memory_sha256='fixture', account_key=account.account_key_hash,
                http_post=post, spending=account))
        return output, sent, ev.report()['records'][0]

    def test_evaluation_refusal_zero_dispatch_no_repeat(self):
        a = self.account(daily=.001)
        output, sent, record = self.run_evaluation(a, None)
        self.assertEqual(sent, [])
        self.assertEqual(record['calls'], [])
        self.assertIn('"tipo": "limite"', output)
        self.assertIn('"bloqueado_por": "usd_dia"', output)
        self.assertTrue(a.closed)
        self.assertEqual(self.rows(), [])

    def test_evaluation_http_refusal_one_dispatch_full_hold_no_retry(self):
        from types import SimpleNamespace
        response = SimpleNamespace(status_code=429, close=lambda: None)
        a = self.account()
        output, sent, record = self.run_evaluation(a, response)
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0], {})  # headers cleared even after failure
        self.assertEqual(record['status'], 'failed_or_uncertain')
        self.assertEqual(self.rows()[0][4], 'estimated_upper_bound')
        self.assertEqual(self.rows()[0][3], self.rows()[0][2])
        self.assertTrue(a.closed)

    def test_evaluation_success_settles_real_usage(self):
        from types import SimpleNamespace
        usage = dict(prompt_tokens=100, completion_tokens=10, total_tokens=110,
                     prompt_tokens_details={'cached_tokens': 20})
        chunk = dict(model=MODELS['mimo']['model'], usage=usage,
                     choices=[dict(index=0, delta={'content': 'fixture answer'}, finish_reason='stop')])
        response = SimpleNamespace(status_code=200, close=lambda: None,
            iter_lines=lambda **kw: iter([('data: '+json.dumps(chunk)).encode(), b'data: [DONE]']))
        a = self.account()
        output, sent, record = self.run_evaluation(a, response)
        self.assertEqual(len(sent), 1); self.assertEqual(sent[0], {})
        self.assertEqual(record['status'], 'completed')
        self.assertAlmostEqual(self.rows()[0][3], self.measured()['cost_estimate_usd'])
        self.assertEqual(self.rows()[0][4], 'settled'); self.assertTrue(a.closed)



if __name__ == '__main__':
    unittest.main(verbosity=2)
