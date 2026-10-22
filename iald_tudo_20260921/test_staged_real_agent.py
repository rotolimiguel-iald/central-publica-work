"""Real chat, agent loop, converter and SQLite ledger; only API/tool results are fixtures."""
import copy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock
import test_staged_chat_flow as flow
from haiku_stage_fixture import extract
from test_claude_native_account import NativeAccount, budget


class RealAgentIntegration(unittest.TestCase):
    def setUp(self):
        self.base = flow.ChatFlowTests(methodName='runTest')
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.env = self.base.env
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.guard = budget.SpendingGuard(str(Path(self.tmp.name) / 'guard.db'))
        self.ledger = flow.motors.RazaoDeUso(str(Path(self.tmp.name) / 'ledger.json'))
        adapter = SimpleNamespace(**{k:v for k,v in vars(flow.converter).items() if not k.startswith('__')})
        client = Mock(); client.with_options.return_value = client
        adapter.cliente_para = lambda cfg: client
        self.counted, self.sent = [], []
        self.executed = Mock(return_value='published fixture evidence')
        self.overflow = False
        self.tool_name = 'search_tgl'

        def count(client, wire):
            self.counted.append(copy.deepcopy(wire))
            has_result = any(b.get('type') == 'tool_result'
                for m in wire['messages'] if isinstance(m['content'], list) for b in m['content'])
            return (195000 if self.overflow else 184800) if has_result else 184609

        def provider(checked_adapter, cfg, payload, **kwargs):
            wire = checked_adapter.converter_pedido(cfg, payload,
                prefixo=kwargs['prefix'], estado=kwargs['state'])
            wire.pop('output_config', None); wire['thinking'] = {'type': 'disabled'}
            counted = kwargs['counter'](wire)
            self.sent.append(copy.deepcopy(wire))
            if len(self.sent) == 1:
                event = {'choices': [{'delta': {'tool_calls': [{'index': 0, 'id': 'fixture_call',
                    'function': {'name': self.tool_name, 'arguments': '{"query":"Hamiltoniano"}'}}]},
                    'finish_reason': 'tool_calls'}]}
                details = {'cached_tokens': 0, 'cache_write_tokens': 183135}
            else:
                event = {'choices': [{'delta': {'content': 'answer with retrieved evidence'}, 'finish_reason': 'stop'}]}
                details = {'cached_tokens': 183135, 'cache_write_tokens': 0}
            usage = {'prompt_tokens': counted, 'completion_tokens': 8, 'prompt_tokens_details': details}
            lines = ['data: ' + json.dumps(event), 'data: ' + json.dumps({'choices': [], 'usage': usage}), 'data: [DONE]']
            return flow.converter.RespostaClaude(200, {'content-type': 'text/event-stream'}, linhas=iter(lines)), None

        def keepalive(call):
            if False: yield None
            return call()

        self.env.update({'_HaikuNativeAccount': NativeAccount, 'iald_orcamento': budget,
            '_guarda_do_motor': lambda m: self.guard, 'RAZAO_CLAUDE': self.ledger,
            'iald_motor_claude': adapter, '_count_haiku_native_request': count,
            'post_guarded': provider, '_executar_ferramenta_claude': self.executed,
            '_com_keepalive': keepalive, 'MAX_AGENT_LOOPS': 2, 'LLAMA_URL': 'http://fixture.invalid',
            '_ROTULO_FERRAMENTA': {}, 'AGENT_MAX_RESULT_CHARS': 20000, 'auth_log': lambda *a: None,
            '_linhas_da_recusa': lambda *a: iter(['data: {"iald_aviso":"context rejected"}\n\n']),
            '_sse_aviso': lambda *a: SimpleNamespace(response=['data: {"iald_aviso":"unavailable"}\n\n'])})
        extract({'agent_loop'}, self.env)

    def test_two_real_tool_turns_count_final_payload_and_settle_cache_prices(self):
        response = self.base.call()
        body = ''.join(response.body)
        self.assertIn('answer with retrieved evidence', body)
        self.assertEqual(len(self.sent), 2)
        self.assertEqual(len(self.counted), 2)
        self.assertEqual(self.sent[1]['tool_choice'], {'type': 'none'})
        self.assertTrue(all(len(w['tools']) == 7 for w in self.sent))
        self.assertIn('published fixture evidence', str(self.sent[1]['messages']))
        self.executed.assert_called_once()
        self.assertAlmostEqual(self.guard.used_today(), self.ledger.gasto_hoje('tester')[0], places=7)
        self.assertLess(self.guard.used_today(), .26)

    def test_tool_result_overflow_blocks_second_generation_and_keeps_first_usage(self):
        self.overflow = True
        body = ''.join(self.base.call().body)
        self.assertIn('context rejected', body)
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(len(self.counted), 2)
        self.assertGreater(self.guard.used_today(), 0)
        self.assertAlmostEqual(self.guard.used_today(), self.ledger.gasto_hoje('tester')[0], places=7)

    def test_model_cannot_execute_a_tool_outside_the_seven_public_definitions(self):
        self.tool_name = 'iald_atlas_read'
        body = ''.join(self.base.call().body)
        self.assertIn('answer with retrieved evidence', body)
        self.executed.assert_not_called()
        self.assertIn('Ferramenta não autorizada', str(self.sent[1]['messages']))


if __name__ == '__main__':
    unittest.main()
