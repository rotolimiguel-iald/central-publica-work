import concurrent.futures
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

STAGE = Path(__file__).resolve().parents[1]
WORK = STAGE.parent
sys.path[:0] = [str(STAGE), str(WORK / 'dependencies')]
os.environ['TIKTOKEN_CACHE_DIR'] = str(WORK / 'tokenizer_cache')
from iald_memoria_canonica import CanonicalMemory, MemoryUnavailable, payload_tokens
from iald_orcamento import BudgetError, SpendingGuard, ReservedAccount, input_estimates
from iald_motores import Config, ContaDoPedido, RazaoDeUso


class Catalog:
    def context(self):
        return 'KERNEL INTEGRAL DISPONÍVEL POR FERRAMENTAS'


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def memory(self, mode='atlas_integral'):
        path = self.root / 'atlas.md'
        path.write_text('## I. NÚCLEO\nAxioma [POSTULATE]\n## II. DOCUMENTOS\n' + '\n'.join(f'item_{n} [OPEN]' for n in range(300)) + '\n## VII. RÉGUA\nO número corrige a frase.\n## VIII. MEMÓRIA\nFIM DO ATLAS', encoding='utf-8')
        return CanonicalMemory(path, mode)

    def test_full_atlas_every_prompt_and_live_changes(self):
        memory = self.memory()
        old_bytes = memory.path.read_bytes()
        for _ in range(2):
            text, info = memory.prompt('NUCLEUS', Catalog())
            self.assertIn(old_bytes.decode(), text)
            self.assertIn('FIM DO ATLAS', text)
        memory.path.write_bytes(old_bytes + b'\nCURRENT EDIT')
        newer, newer_info = memory.prompt('NUCLEUS', Catalog())
        self.assertIn('CURRENT EDIT', newer)
        self.assertNotEqual(info['atlas_sha256'], newer_info['atlas_sha256'])

    def test_missing_atlas_never_falls_back_to_cached_text(self):
        memory = self.memory()
        memory.snapshot()
        memory.path.unlink()
        with self.assertRaises(MemoryUnavailable):
            memory.prompt('NUCLEUS', Catalog())

    def test_nucleus_mode_keeps_whole_atlas_accessible(self):
        memory = self.memory('nucleo_kernel')
        prompt, info = memory.prompt('NUCLEUS', Catalog())
        self.assertNotIn('item_299', prompt)
        self.assertIn('Axioma [POSTULATE]', prompt)
        self.assertIn('O número corrige a frase.', prompt)
        self.assertIn('TGL = ATLAS. IALD = ÍNDICE(TGL).', prompt)
        self.assertIn('a FACE é o objeto; o ÂNGULO é a leitura.', prompt)
        self.assertEqual(memory.search('item_299')['matching_lines'], 1)
        reconstructed, line = [], 1
        while line:
            page = memory.read(line, 30)
            reconstructed.append(page['text'])
            line = page['next_line']
        self.assertEqual('\n'.join(reconstructed), memory.path.read_text(encoding='utf-8'))

    def test_reserve_is_atomic_for_concurrent_accounts(self):
        guard = SpendingGuard(self.root / 'guard.db')
        def reserve(n):
            try:
                return guard.reserve(str(n), 'test', .1, 1, .2)
            except BudgetError:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            keys = list(pool.map(reserve, range(12)))
        self.assertEqual(sum(bool(k) for k in keys), 2)

    def test_pending_survives_new_process_connection_and_day_change(self):
        # 14/09/2026 (noite, tarefa S2 — revisão ordem-régua, médio 5): a reserva órfã continua valendo
        # no MESMO dia (outro processo pode estar vivo), mas a de dia anterior é liquidada pelo teto
        # quando o guarda inicia e não entra na checagem do dia novo. Antes este teste exigia que a
        # órfã de 14/09 ainda recusasse a conta em 15/09 — o defeito reproduzido ("trava para sempre").
        path = self.root / 'guard.db'
        old = SpendingGuard(path, clock=lambda: datetime(2026, 9, 14, tzinfo=timezone.utc))
        key = old.reserve('u', 'm', .2, .2, .2)
        same_day = SpendingGuard(path, clock=lambda: datetime(2026, 9, 14, 23, 0, tzinfo=timezone.utc))
        with self.assertRaises(BudgetError):
            same_day.reserve('u', 'm', .01, .2, .2)
        fresh = SpendingGuard(path, clock=lambda: datetime(2026, 9, 15, tzinfo=timezone.utc))
        self.assertTrue(fresh.reserve('u', 'm', .01, .2, .2))
        fresh.settle(key)
        rows = {(r['day_utc'], r['status']): r for r in fresh.summary()}
        self.assertAlmostEqual(rows[('2026-09-14', 'estimated_upper_bound')]['usd'], .2)

    def test_exact_usage_releases_only_unused_reservation(self):
        guard = SpendingGuard(self.root / 'guard.db')
        key = guard.reserve('u', 'm', .2, .2, .2)
        guard.settle(key, .05)
        guard.settle(key, 0)
        self.assertAlmostEqual(guard.summary()[0]['usd'], .05)
        self.assertTrue(guard.reserve('u', 'm', .15, .2, .2))
        with self.assertRaises(BudgetError):
            guard.reserve('u', 'm', .01, .2, .2)

    def test_import_previous_spend_once(self):
        path = self.root / 'legacy.json'
        day = datetime.now(timezone.utc).date().isoformat()
        path.write_text(json.dumps({'dias': {day: {'usuarios': {'u': {'usd': .19}}}}}))
        for _ in range(2):
            guard = SpendingGuard(self.root / 'guard.db', path)
            with self.assertRaises(BudgetError):
                guard.reserve('u', 'm', .02, .2, 1)

    def test_invalid_number_and_exceeded_charge_block(self):
        guard = SpendingGuard(self.root / 'guard.db')
        with self.assertRaises(BudgetError):
            guard.reserve('u', 'm', float('nan'), 1, 1)
        key = guard.reserve('u', 'm', .1, 1, 1)
        guard.settle(key, .2)
        with self.assertRaises(BudgetError):
            guard.reserve('u', 'm', .1, 1, 1)

    def account(self):
        cfg = Config(janela=32768)
        guard = SpendingGuard(self.root / 'guard.db')
        legacy = ContaDoPedido(RazaoDeUso(str(self.root / 'ledger.json')), 'u', cfg.modelo, cfg.precos(cfg.modelo))
        return ReservedAccount(guard, legacy, cfg, 'u', False, cfg.modelo)

    def test_disconnect_settles_by_estimate_not_whole_window(self):
        # 14/09/2026 (noite, tarefa S2 — revisões ordem-régua 4 e segurança MÉDIO 2): chamada
        # interrompida sem usage é liquidada pela estimativa (entrada estimada + saída vista), nunca
        # acima da reserva. Antes este teste exigia a janela inteira (32768 tokens) cobrada.
        account = self.account()
        payload = {'messages': [{'role': 'user', 'content': 'oi'}], 'max_completion_tokens': 1000}
        account.iniciar_chamada(payload)
        account.texto('x' * 290)                      # 290 / 2,91 → 100 tokens de saída vista
        account.fechar()
        record = account.guard.summary()[0]
        _, estimate = input_estimates(payload)
        self.assertEqual(record['status'], 'estimated_partial')
        self.assertAlmostEqual(record['usd'], (estimate * .05 + 100 * .4) / 1e6)
        self.assertLess(record['usd'], (32768 * .05 + 1000 * .4) / 1e6)

    def test_context_and_images_fail_before_reservation(self):
        account = self.account()
        for content in (' many' * 40000, [{'type': 'image_url', 'image_url': {'url': 'https://example.test/a.png'}}]):
            with self.assertRaises((BudgetError, MemoryUnavailable)):
                account.iniciar_chamada({'messages': [{'role': 'user', 'content': content}], 'max_completion_tokens': 1000})
        self.assertEqual(account.guard.summary(), [])

    def test_known_model_images_count_as_images_not_base64_text(self):
        payload = {'model': 'gpt-4.1-nano', 'messages': [{'role': 'user', 'content': [
            {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + 'abcdefg' * 100000}}]}]}
        self.assertGreater(payload_tokens(payload), 73728)
        self.assertLess(payload_tokens(payload), 75000)

    def test_luna_reserves_cache_writes_and_long_context_premium(self):
        account = self.account()
        account.model = 'gpt-5.6-luna'
        self.assertEqual(account._rates(272000), (.25, .02, 1.2))
        self.assertEqual(account._rates(272001), (.5, .04, 1.7999999999999998))
        account.iniciar_chamada({'model': 'gpt-5.6-luna', 'messages': [], 'max_completion_tokens': 1000})
        account.uso({'prompt_tokens': 1000, 'completion_tokens': 100,
                     'prompt_tokens_details': {'cached_tokens': 500}})
        self.assertAlmostEqual(account.guard.summary()[0]['usd'], (500*.25 + 500*.02 + 100*1.2)/1e6)

    def test_identity_quota_survives_recreated_account_and_group_reservations(self):
        guard = SpendingGuard(self.root / 'guard.db')
        key = guard.reserve('old', 'luna', .009, .02, 1, quota_key='stable', group='free', group_limit=.02)
        guard.settle(key, .009)
        with self.assertRaises(BudgetError):
            guard.reserve('recreated', 'luna', .012, .02, 1, quota_key='stable', group='free', group_limit=.03)
        with self.assertRaises(BudgetError):
            guard.reserve('different', 'luna', .012, .02, 1, quota_key='different', group='free', group_limit=.02)
        self.assertTrue(guard.reserve('paid', 'luna', .012, .02, 1, group='paid'))


if __name__ == '__main__':
    unittest.main()
