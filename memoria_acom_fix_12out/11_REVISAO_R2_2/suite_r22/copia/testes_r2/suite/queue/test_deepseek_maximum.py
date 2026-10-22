"""Regression for the operator-authorized DeepSeek maximum routing scope."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from iald_orchestrator import deepseek, providers
from iald_orchestrator.policy import route
from iald_orchestrator.request_controls import normalize, restrict
from iald_orchestrator.runtime import Runtime


class DeepSeekMaximumTests(unittest.TestCase):
    def provider(self):
        # Test the real discovery policy while keeping credentials and network out.
        with patch.object(providers, 'client_command', return_value=None), \
             patch.object(providers.urllib.request, 'urlopen', side_effect=OSError), \
             patch.object(deepseek, 'connection_status', return_value='ready'), \
             patch.object(deepseek, 'authorization', return_value={'enabled': True}), \
             patch('iald_orchestrator.deepseek_secret_store.key_metadata', return_value={'stored': True}), \
             patch('iald_orchestrator.mimo.connection_status', return_value='unavailable'), \
             patch('iald_orchestrator.mimo.authorization', return_value={'enabled': False}), \
             patch('iald_orchestrator.secret_store.key_metadata', return_value={'stored': False}):
            return next(p for p in providers.discover() if p['id'] == 'deepseek')

    def test_real_provider_handles_long_lean_and_theorem_requests(self):
        p = self.provider()
        self.assertEqual(p['tier'], 'advanced')
        self.assertEqual(p['routing_scope'], 'ALL_COMPLEXITIES_OPERATOR_AUTHORIZED')
        self.assertEqual(p['thinking_effort'], 'max')
        self.assertEqual(p['context_budget'], 1048576)
        self.assertEqual(p['output_token_budget'], 393216)
        for prompt in ('Compare hipóteses Lean.', 'Demonstre este teorema.', 'Contexto científico. ' * 900):
            decision = route(prompt, [p], {'deepseek': 10000})
            self.assertEqual(decision['task']['complexity'], 'deep')
            self.assertEqual(decision['selected'], 'deepseek')
        self.assertIsNone(p['daily_run_limit'])
        self.assertIsNone(p['financial_cap_usd'])

    def test_maximum_scope_preserves_access_context_and_provider_lock(self):
        p = self.provider()
        for change in ({'status': 'provider_limit_reported'}, {'billing_authorized': False},
                       {'context_budget': 100}, {'quota_remaining': 0}):
            self.assertIsNone(route('Compare hipóteses Lean.', [dict(p, **change)], {})['selected'])
        c = normalize(dict(mission_id='ORDEM_016', branch_id='test', lemma_id='maximum',
                           role='draft', required_provider='deepseek', max_calls=1))
        fallback = dict(p, id='kimi')
        rows = restrict([dict(p, status='unavailable'), fallback], c)
        self.assertIsNone(route('Compare hipóteses Lean.', rows, {})['selected'])

    def test_runtime_preview_keeps_the_full_prompt_and_maximum_memory(self):
        p = self.provider()
        prompt = 'Compare hipóteses Lean. ' + 'Source line. ' * 1500
        c = dict(mission_id='ORDEM_016', branch_id='test', lemma_id='maximum',
                 role='draft', required_provider='deepseek', max_calls=1)
        packet = {'prompt': prompt + '\nScientific context. ' * 25000,
                  'receipt': {'memory_mode': 'deepseek_maximum', 'generation': 'fixture', 'sources': []}}
        with tempfile.TemporaryDirectory() as folder:
            runtime = Runtime(folder, recover=False)
            with patch.object(runtime, 'source_status', return_value={'ok': True}), \
                 patch.object(runtime, 'connections', return_value=[p]), \
                 patch('iald_orchestrator.runtime.canonical_memory.prepare', return_value=packet) as prepare, \
                 patch.object(providers, 'execute') as execute:
                decision = runtime.preview(prompt, c)
            self.assertEqual(decision['selected'], 'deepseek')
            self.assertEqual(prepare.call_args.args[0], prompt)
            self.assertEqual(prepare.call_args.kwargs['mode'], 'deepseek_maximum')
            self.assertEqual(decision['execution_constraints']['max_output_tokens'], 393216)
            execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()
