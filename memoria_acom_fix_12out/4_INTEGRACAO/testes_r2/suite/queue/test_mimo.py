import copy
import json
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from iald_orchestrator import mimo, secret_store
from iald_orchestrator.policy import route


def response():
    return {'model': mimo.MODEL, 'choices': [{'finish_reason': 'stop', 'message': {'content': '42'}}],
            'usage': {'prompt_tokens': 100, 'completion_tokens': 2, 'total_tokens': 102,
                      'prompt_tokens_details': {'cached_tokens': 20}}}


class MimoTests(unittest.TestCase):
    def test_token_accounting_and_no_internal_reasoning(self):
        data = response()
        data['choices'][0]['message']['reasoning_content'] = 'INTERNAL_NOT_FOR_STORAGE'
        value = mimo.parse_response(data)
        self.assertEqual(value['text'], '42')
        self.assertEqual(value['cost_estimate_usd'], '0.000036612')
        self.assertNotIn('INTERNAL_NOT_FOR_STORAGE', json.dumps(value))

    def test_truncation_tools_model_and_missing_usage_fail(self):
        for mutate in [lambda d: d['choices'][0].update(finish_reason='length'),
                       lambda d: d['choices'][0]['message'].update(tool_calls=[{'name': 'shell'}]),
                       lambda d: d.update(model='other'), lambda d: d.pop('usage'),
                       lambda d: d['usage'].update(total_tokens=101),
                       lambda d: d['usage']['prompt_tokens_details'].update(cached_tokens=101)]:
            data = response(); mutate(data)
            with self.assertRaises(RuntimeError): mimo.parse_response(data)

    def test_no_redirect_leaks_api_credential(self):
        with self.assertRaises(RuntimeError):
            mimo.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.com')

    def test_unauthorized_paid_provider_remains_excluded(self):
        row = {'id':'mimo','status':'ready','billing':'authorized_api','tier':'advanced',
               'context_budget':12000,'daily_run_limit':None,'billing_authorized':False}
        self.assertIsNone(route('Prova', [row], {})['selected'])
        row['billing_authorized'] = True
        self.assertEqual(route('Prova', [row], {'mimo':10000})['selected'], 'mimo')

    def test_dpapi_roundtrip_and_encrypted_backup(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(secret_store, 'KEY_FILE', Path(folder)/'key.dpapi'):
            dummy = 'DUMMY_ONLY_NO_REAL_CREDENTIAL_12345'
            secret_store.store_mimo(dummy)
            raw = secret_store.KEY_FILE.read_bytes()
            self.assertNotIn(dummy.encode(), raw)
            self.assertEqual(secret_store.load_mimo(), dummy)
            secret_store.store_mimo(dummy+'6')
            backups = list(Path(folder).glob('*.bak_*'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), raw)
            self.assertNotIn(dummy, json.dumps(secret_store.key_metadata()))

    def test_transport_uses_header_and_has_no_tools(self):
        captured = {}
        class Reply:
            def __init__(self):
                from validation.test_mimo_stream import frames
                self.body = io.BytesIO(frames())
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def readline(self,size): return self.body.readline(size)
        class Transport:
            def open(self, req, timeout):
                captured.update(url=req.full_url, data=json.loads(req.data), headers=dict(req.header_items()))
                return Reply()
        with patch.object(mimo, 'authorization', return_value={'enabled': True}), patch.object(mimo, 'load_mimo', return_value='DUMMY'), patch.object(mimo.urllib.request, 'build_opener', return_value=Transport()):
            self.assertEqual(mimo.execute('public test', max_output=32)['text'], '42')
        self.assertEqual(captured['url'], mimo.URL)
        self.assertEqual(captured['headers']['Api-key'], 'DUMMY')
        self.assertNotIn('tools', captured['data'])
        self.assertTrue(captured['data']['stream'])
        self.assertEqual(captured['data']['max_completion_tokens'], 32)
        self.assertEqual(captured['data']['thinking'], {'type':'disabled'})

    def test_protected_storage_route_does_not_return_secret(self):
        from flask import Flask
        from iald_orchestrator.web import install
        with tempfile.TemporaryDirectory() as folder, patch('iald_orchestrator.web.Runtime'):
            app = Flask(__name__)
            install(app, lambda: None)
            client = app.test_client()
            endpoint = '/admin/api/orchestrator/connections/mimo/key'
            with patch.object(secret_store, 'store_mimo') as store:
                self.assertEqual(client.post(endpoint,json={'key':'DUMMY'}).status_code,403)
                result = client.post(endpoint,json={'key':'DUMMY'},headers={'Origin':'http://localhost'})
                self.assertEqual(result.status_code,200)
                store.assert_called_once_with('DUMMY')
                self.assertNotIn('DUMMY', result.get_data(as_text=True))
                self.assertEqual(result.headers['Cache-Control'], 'no-store')

if __name__ == '__main__': unittest.main()
