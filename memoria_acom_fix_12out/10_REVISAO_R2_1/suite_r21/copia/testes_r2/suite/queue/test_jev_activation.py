"""Local checks for Jev activation without a provider call."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Flask, jsonify

from iald_orchestrator import jev
from iald_orchestrator.runtime import Runtime
from iald_orchestrator.web import install


class JevActivationTests(unittest.TestCase):
    def test_availability_fails_closed_until_validated(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'activation.json'
            with (patch.object(jev, 'ACTIVATION', path),
                  patch.object(jev, 'key_metadata', return_value={'stored': True}),
                  patch.dict('os.environ', {'TYPESAFE_API_KEY': '', 'JEV_API_KEY': ''})):
                self.assertEqual(jev.availability()['status'], 'configured_not_tested')
                path.write_text(json.dumps({'enabled': True, 'probe_status': 'dispatching'}))
                self.assertFalse(jev.availability()['enabled'])
                path.write_text(json.dumps({'enabled': True, 'probe_status': 'ready',
                                            'model': 'jev-1.13.0'}))
                self.assertEqual(jev.availability()['status'], 'ready')

    def test_admin_key_storage_requires_auth_and_same_origin(self):
        with tempfile.TemporaryDirectory() as folder:
            app = Flask(__name__)
            allowed = [False]
            def guard():
                return None if allowed[0] else (jsonify(error='login'), 401)
            with patch('iald_orchestrator.web.Runtime', return_value=Runtime(folder, recover=False)):
                install(app, guard)
            client = app.test_client()
            url = '/admin/api/orchestrator/connections/jev/key'
            body = {'key': 'synthetic-key-12345678901234567890'}
            self.assertEqual(client.post(url, json=body).status_code, 401)
            allowed[0] = True
            self.assertEqual(client.post(url, json=body,
                                         headers={'Origin': 'https://other.example'}).status_code, 403)
            with (patch('iald_orchestrator.jev_secret_store.store_key') as store,
                  patch('iald_orchestrator.safe_files.save_json') as save):
                response = client.post(url, json=body, headers={'Origin': 'http://localhost'})
                self.assertEqual(response.status_code, 200)
                self.assertFalse(response.json['enabled'])
                store.assert_called_once_with(body['key'])
                self.assertEqual(save.call_args.args[1]['probe_status'], 'configured_not_tested')
                self.assertNotIn(body['key'], json.dumps(response.json))

    def test_low_confidence_cannot_downgrade_deterministic_floor(self):
        data = {'model': 'jev-1.13.0', 'answers': {'complexity': {
            'choice': 'standard', 'confidence': .2,
            'probabilities': {'standard': .5, 'deep': .5}}}}
        self.assertEqual(jev.parse_answer(data, 'Audite uma demonstração matemática')['complexity'], 'deep')


if __name__ == '__main__':
    unittest.main()
