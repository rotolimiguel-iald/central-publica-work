"""Offline regression for the proposed local assembly ceiling, without private data.

Default: construct the proposed change in memory from the production source.
Optional --candidate PATH validates a separately prepared module with the same change.
Never imports the web server, reads credentials, or calls a provider.
"""
from contextlib import ExitStack
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock, patch
import ast
import hashlib
import json
import math
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(R), r'C:\Users\rotol\AppData\Roaming\Python\Python314\site-packages']
SOURCE = R/'iald_memoria_canonica.py'
ORIGINAL_BYTES = SOURCE.read_bytes()
ORIGINAL = ORIGINAL_BYTES.decode('utf-8-sig')
OLD = "metadata['context_tokens'] > 340000"
NEW = "metadata['context_tokens'] > MAX_CLUSTER_CONTEXT_TOKENS"
DECLARATION = (
    '# Local o200k assembly ceiling, not a provider window or spending limit.\n'
    '# Outbound requests still pass adapter window/output and spending guards.\n'
    'MAX_CLUSTER_CONTEXT_TOKENS = 400_000\n\n\n'
)
assert ORIGINAL.count(OLD) == 1
PROPOSED = ORIGINAL.replace('class MemoryUnavailable(ValueError):', DECLARATION+'class MemoryUnavailable(ValueError):', 1).replace(OLD, NEW, 1)
if '--candidate' in sys.argv:
    i = sys.argv.index('--candidate')
    PROPOSED = Path(sys.argv[i+1]).read_text(encoding='utf-8-sig')
    del sys.argv[i:i+2]

def load_source(name, source):
    module = ModuleType(name)
    module.__file__ = str(SOURCE)
    exec(compile(source, str(SOURCE), 'exec'), module.__dict__)
    return module

original = load_source('_review_original_memory', ORIGINAL)
candidate = load_source('_review_candidate_memory', PROPOSED)
import iald_cluster as cluster_module
import iald_orcamento as budget

ATLAS = ('## I. FUNDAMENTOS\n### I.1 Identidade\nFOUNDATION_SENTINEL\n'
         '### I.6 História\nHISTORICAL_SENTINEL\n'
         '## V. PRIVADO\nPRIVATE_SENTINEL\n'
         '## VII. REGRA\nRULE_SENTINEL\n## VIII. FIM\nOTHER_SENTINEL\n')

class Assembly(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='assembly_review_', dir=HERE)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root/'manifest.json'
        self.manifest.write_text('{}', encoding='utf-8')
        self.catalog = SimpleNamespace(source_sha='a'*64, context=lambda:'KERNEL_SENTINEL')

    def assemble(self, module, count, public=False, mode='nucleo_kernel', real_cluster=False):
        memory = module.CanonicalMemory(self.root/'atlas.md', mode, nucleus_manifest=self.manifest)
        snapshot = Mock(return_value=(ATLAS, {'mode':mode, 'atlas_sha256':hashlib.sha256(ATLAS.encode()).hexdigest()}))
        counter = Mock(return_value=count)
        with ExitStack() as stack:
            stack.enter_context(patch.object(memory, 'snapshot', snapshot))
            stack.enter_context(patch.object(memory, 'current_state', return_value=('CURRENT_SENTINEL', {})))
            stack.enter_context(patch.object(memory, 'fixed_nucleus', return_value=('NUCLEUS_SENTINEL', {})))
            stack.enter_context(patch.object(module, 'mother_instruction', return_value=('MOTHER_SENTINEL', {})))
            stack.enter_context(patch.object(module, 'operational_core', return_value=('CORE_SENTINEL', {})))
            stack.enter_context(patch.object(module, 'published_evidence', return_value=('EVIDENCE_SENTINEL', {})))
            stack.enter_context(patch.object(module, 'deployment_contract', return_value=('CONTRACT_SENTINEL', {})))
            stack.enter_context(patch.object(module.iald_fontes_publicas, 'context', return_value='PUBLIC_SOURCE_SENTINEL'))
            stack.enter_context(patch.object(module, 'active_cluster', cluster_module.active_cluster if real_cluster else Mock(return_value=('CLUSTER_SENTINEL', {'cluster_always_present':True}))))
            stack.enter_context(patch.object(module, 'count_tokens', counter))
            try:
                result = memory.prompt('', self.catalog, public=public)
            finally:
                self.last_counter = counter
                self.last_snapshot = snapshot
        return result

    def test_only_assembly_ceiling_changes(self):
        tree = ast.parse(PROPOSED)
        declarations = [n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='MAX_CLUSTER_CONTEXT_TOKENS' for t in n.targets)]
        if not declarations:
            self.assertEqual(PROPOSED, ORIGINAL.replace(OLD, "metadata['context_tokens'] > 400000", 1))
            return
        self.assertEqual(len(declarations), 1)
        self.assertEqual(ast.literal_eval(declarations[0].value), 400000)
        restored = PROPOSED.replace(NEW, OLD, 1)
        t = ast.parse(restored)
        t.body = [n for n in t.body if not (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id=='MAX_CLUSTER_CONTEXT_TOKENS' for x in n.targets))]
        self.assertEqual(ast.dump(t), ast.dump(ast.parse(ORIGINAL)))

    def test_reported_private_count_passes_with_identical_full_prefix(self):
        with self.assertRaises(original.MemoryUnavailable):
            self.assemble(original, 343709)
        refused_prefix = self.last_counter.call_args.args[0]
        result, metadata = self.assemble(candidate, 343709)
        self.assertEqual(result.encode(), refused_prefix.encode())
        self.assertEqual(metadata['context_tokens'], 343709)
        self.assertEqual(metadata['context_sha256'], hashlib.sha256(result.encode()).hexdigest())
        for part in ['FOUNDATION','RULE','NUCLEUS','MOTHER','CORE','EVIDENCE','CLUSTER','KERNEL','CURRENT']:
            self.assertIn(part+'_SENTINEL', result)
        self.assertNotIn('PRIVATE_SENTINEL', result)
        self.assertNotIn('HISTORICAL_SENTINEL', result)

    def test_public_prefix_unchanged_and_never_reads_private_atlas(self):
        before = self.assemble(original, 337027, public=True)
        self.last_snapshot.assert_not_called()
        after = self.assemble(candidate, 337027, public=True)
        self.last_snapshot.assert_not_called()
        self.assertEqual(before, after)
        self.assertFalse(after[1]['private_atlas_included'])
        self.assertNotIn('PRIVATE_SENTINEL', after[0])

    def test_exact_ceiling_is_inclusive(self):
        self.assertEqual(self.assemble(candidate, 400000)[1]['context_tokens'], 400000)

    def test_over_ceiling_refused_in_both_scopes_and_modes(self):
        for public in (False, True):
            for mode in ('atlas_integral','nucleo_kernel'):
                with self.subTest(public=public, mode=mode), self.assertRaises(candidate.MemoryUnavailable):
                    self.assemble(candidate, 400001, public=public, mode=mode)

    def test_cluster_hash_and_release_checks_are_not_bypassed(self):
        text = b'\n### Fixture\nINTACT_CLUSTER\n'
        path = self.root/'cluster.md'
        path.write_bytes(text)
        config = {'path':str(path), 'sha256':hashlib.sha256(text).hexdigest(),
                  'release_source_sha256':'a'*64,'release':'v390','commit':'b'*40,'core_sections':1}
        self.manifest.write_text(json.dumps({'active_cluster':config}), encoding='utf-8')
        prompt, meta = self.assemble(candidate, 343709, real_cluster=True)
        self.assertIn(text.decode(), prompt)
        self.assertTrue(meta['cluster_always_present'])
        for change in ({'sha256':'0'*64}, {'release_source_sha256':'c'*64}, {'core_sections':2}):
            with self.subTest(change=change):
                self.manifest.write_text(json.dumps({'active_cluster':{**config, **change}}), encoding='utf-8')
                with self.assertRaises(ValueError):
                    self.assemble(candidate, 343709, real_cluster=True)
        self.assertEqual(path.read_bytes(), text)

    def test_production_bytes_untouched(self):
        self.assertEqual(SOURCE.read_bytes(), ORIGINAL_BYTES)

class OutboundGuards(unittest.TestCase):
    def account(self, provider='openai', window=500000):
        cfg = SimpleNamespace(janela=window, provedor=provider, fator_tokens=1.6 if provider=='claude' else 1.0,
                              cota_usuario_usd=3, cota_operador_usd=5, cota_global_usd=20,
                              precos=lambda _: (1.0, .1, 5.0))
        guard, legacy = Mock(), Mock()
        account = budget.ReservedAccount(guard, legacy, cfg, 'tester', False, 'test-model', group='public', group_limit=7)
        return account, guard, legacy

    def test_assembled_memory_does_not_bypass_request_window_or_output(self):
        for provider in ('openai','claude'):
            account, guard, legacy = self.account(provider, window=350000)
            with self.subTest(provider=provider), patch.object(budget,'input_estimates',return_value=(343709,343709)):
                with self.assertRaises(budget.WindowError):
                    account.iniciar_chamada({'max_completion_tokens':16384})
            guard.reserve.assert_not_called()
            legacy.iniciar_chamada.assert_not_called()

    def test_tools_history_and_output_still_cause_refusal(self):
        account, guard, legacy = self.account(window=400000)
        with patch.object(budget,'input_estimates',return_value=(395000,410000)):
            with self.assertRaises(budget.WindowError):
                account.iniciar_chamada({'max_completion_tokens':16384})
        guard.reserve.assert_not_called()
        legacy.iniciar_chamada.assert_not_called()

    def test_financial_reservation_and_provider_factor_remain(self):
        for provider,factor in [('openai',1.0),('claude',1.6)]:
            account, guard, legacy = self.account(provider)
            with patch.object(budget,'input_estimates',return_value=(343709,370000)):
                payload={'max_completion_tokens':16384}
                account.iniciar_chamada(payload)
            args=guard.reserve.call_args.args
            self.assertAlmostEqual(args[2],(math.ceil(math.ceil(370000*factor)*1.15)+16384*5)/1e6)
            self.assertEqual(args[3:],(3,20))
            self.assertEqual(guard.reserve.call_args.kwargs['group_limit'],7)
            legacy.iniciar_chamada.assert_called_once_with(payload)

    def test_financial_refusal_still_stops_dispatch(self):
        account, guard, legacy=self.account()
        guard.reserve.side_effect=budget.BudgetError('Fixture budget exhausted','usd_dia')
        with patch.object(budget,'input_estimates',return_value=(343709,370000)):
            with self.assertRaises(budget.BudgetError):
                account.iniciar_chamada({'max_completion_tokens':16384})
        legacy.iniciar_chamada.assert_not_called()

if __name__ == '__main__':
    unittest.main(verbosity=2)
