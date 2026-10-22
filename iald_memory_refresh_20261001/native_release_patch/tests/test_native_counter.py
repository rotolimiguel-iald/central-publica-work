"""Offline native-count regressions. Fake token IDs are never provider measurements."""
from copy import deepcopy
import json
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

STAGE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(STAGE), r'C:\IALD\projetos_pyhton\IALD']
import iald_native_memory as native


class CounterTests(unittest.TestCase):
    def setUp(self):
        self.block = patch.object(socket.socket, 'connect', side_effect=AssertionError('No network'))
        self.block.start()
        self.addCleanup(self.block.stop)
        self.payload = {'messages': [{'role': 'user', 'content': 'Question'}],
                        'max_tokens': 4096, 'chat_template_kwargs': {'enable_thinking': False}}

    def measure(self, payload=None, count=20000, serving=131072):
        calls = []
        def transport(base_url, endpoint, data=None):
            calls.append((base_url, endpoint, deepcopy(data)))
            if endpoint == '/props':
                return {'default_generation_settings': {'n_ctx': serving}}
            if endpoint == '/apply-template':
                return {'prompt': '<|im_start|>rendered fixture<|im_end|>'}
            if endpoint == '/tokenize':
                return {'tokens': [1] * count}
            raise AssertionError(endpoint)
        with patch.object(native, '_local_json', side_effect=transport):
            result = native.check_text_window(payload or self.payload, 131072)
        return result, calls

    def test_twenty_thousand_tokens_survive_large_utf8_payload(self):
        payload = deepcopy(self.payload)
        payload['messages'] = [
            {'role': 'system', 'content': 'server and client prefix ' * 3500},
            {'role': 'user', 'content': 'a' * 30000},
            {'role': 'assistant', 'content': 'b' * 30000},
            {'role': 'user', 'content': 'Continue a resposta.'}]
        before = deepcopy(payload)
        self.assertGreater(len(json.dumps(payload).encode()), 131072)
        result, calls = self.measure(payload, count=20000)
        self.assertEqual(result['input_tokens'], 20000)
        self.assertEqual(result['measurement'], 'LLAMA_LOCAL_TEMPLATE_AND_TOKENIZER')
        self.assertEqual(result['framing_allowance'], 256)
        self.assertEqual(payload, before)
        self.assertEqual(calls[1][2]['messages'], before['messages'])

    def test_exact_tools_kwargs_and_special_token_options_reach_counter(self):
        payload = deepcopy(self.payload)
        payload['tools'] = [{'type': 'function', 'function': {'name': 'fixture'}}]
        payload['tool_choice'] = 'auto'
        payload['parallel_tool_calls'] = True
        payload['messages'] += [{'role': 'assistant', 'content': None,
            'tool_calls': [{'id': 'one', 'type': 'function',
                'function': {'name': 'fixture', 'arguments': '{}'}}]},
            {'role': 'tool', 'tool_call_id': 'one', 'content': 'Complete uncut result'}]
        _, calls = self.measure(payload)
        self.assertEqual([c[1] for c in calls], ['/props', '/apply-template', '/tokenize'])
        self.assertEqual(calls[1][2], dict(payload, add_generation_prompt=True))
        self.assertEqual(calls[2][2], {'content': '<|im_start|>rendered fixture<|im_end|>',
                                    'add_special': True, 'parse_special': True})

    def test_real_token_boundary_not_byte_length(self):
        boundary = 131072 - 4096 - 256
        self.measure(count=boundary)
        with self.assertRaises(native.NativeContextError):
            self.measure(count=boundary + 1)

    def test_actual_serving_window_can_only_reduce_limit(self):
        with self.assertRaises(native.NativeContextError):
            self.measure(count=28000, serving=32000)
        value, _ = self.measure(count=20000, serving=262144)
        self.assertEqual(value['effective_window'], 131072)

    def test_tool_round_is_recounted_and_growth_refused(self):
        count = [20000]
        calls = []
        def transport(url, endpoint, data=None):
            calls.append(endpoint)
            if endpoint == '/props': return {'default_generation_settings': {'n_ctx': 131072}}
            if endpoint == '/apply-template': return {'prompt': 'fixture'}
            return {'tokens': [1] * count[0]}
        with patch.object(native, '_local_json', side_effect=transport):
            native.check_text_window(self.payload, 131072)
            self.payload['messages'].append({'role': 'tool', 'content': 'new data', 'tool_call_id': 'one'})
            count[0] = 130000
            with self.assertRaises(native.NativeContextError):
                native.check_text_window(self.payload, 131072)
        self.assertEqual(calls.count('/tokenize'), 2)

    def test_counter_failure_never_falls_back_to_estimated_success(self):
        with patch.object(native, '_local_json', side_effect=OSError('private path')):
            with self.assertRaises(native.NativeCounterUnavailable) as error:
                native.check_text_window(self.payload, 131072)
        self.assertNotIn('private path', str(error.exception))

    def test_invalid_counter_responses_fail_closed(self):
        for broken in ({'tokens': []}, {'tokens': [True]}, {'tokens': [-1]},
                       {'tokens': [1.5]}, {'tokens': '123'}, {}, {'tokens': None}):
            with self.subTest(broken=broken), patch.object(native, '_local_json', side_effect=[
                    {'default_generation_settings': {'n_ctx': 131072}}, {'prompt': 'fixture'}, broken]):
                with self.assertRaises(native.NativeCounterUnavailable):
                    native.check_text_window(self.payload, 131072)
        for broken in ({}, {'prompt': ''}, {'prompt': 1}):
            with self.subTest(broken=broken), patch.object(native, '_local_json', side_effect=[
                    {'default_generation_settings': {'n_ctx': 131072}}, broken]):
                with self.assertRaises(native.NativeCounterUnavailable):
                    native.check_text_window(self.payload, 131072)

    def test_media_not_transmitted_to_count_endpoint_or_mutated(self):
        payload = deepcopy(self.payload)
        payload['messages'][0]['content'] = [{'type': 'text', 'text': 'Question'},
            {'type': 'image_url', 'image_url': {'url': 'https://remote.invalid/private.png'}}]
        original = deepcopy(payload)
        value, calls = self.measure(payload)
        self.assertFalse(value['media_tokens_measured'])
        self.assertEqual(payload, original)
        self.assertEqual(calls[1][2]['messages'][0]['content'], 'Question')
        self.assertNotIn('remote.invalid', json.dumps(calls))

    def test_transport_cannot_target_remote_or_generation(self):
        for base in ('https://127.0.0.1:8081', 'http://example.test:8081',
                     'http://127.0.0.1:8081@evil.test', 'http://127.0.0.1:8081/path',
                     'http://127.0.0.1:0', 'http://127.0.0.1:65536'):
            with self.subTest(base=base), self.assertRaises(native.NativeCounterUnavailable):
                native._local_json(base, '/props')
        for endpoint in ('/v1/chat/completions', '/completion', '/tokenize?secret=1'):
            with self.subTest(endpoint=endpoint), self.assertRaises(native.NativeCounterUnavailable):
                native._local_json('http://127.0.0.1:8081', endpoint, {})

    def test_redirect_is_rejected(self):
        request = type('RequestFixture', (), {'full_url': 'http://127.0.0.1:8081/props'})()
        with self.assertRaises(HTTPError):
            native._NoRedirect().redirect_request(request, None, 302, 'redirect', {}, 'https://remote.invalid')


if __name__ == '__main__':
    unittest.main(verbosity=2)
