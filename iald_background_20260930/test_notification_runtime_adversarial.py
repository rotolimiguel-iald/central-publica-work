"""Offline callback contract tests, with synthetic identities and no Flask/server import.

The fake Flask surface supplies only callbacks and request-local identity. PushStore
is real; cipher, provider configuration and transport are explicitly test doubles.
Failures identify required behavior not yet implemented by the staged runtime.
"""
from pathlib import Path
from contextlib import closing
import sqlite3
import sys
import tempfile
import types
import unittest
import uuid
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent / 'server'))
import iald_chat_push as push
import iald_notification_runtime as runtime


class FakeCipher:
    def seal(self, raw): return b'test-only:' + raw[::-1]
    def open(self, raw): return raw[len(b'test-only:'):][::-1]


class FakeTransport:
    def __init__(self): self.calls = []
    def prepare(self): pass
    def send(self, **request):
        self.calls.append(request)
        return 200, b''


class FakeApp:
    def __init__(self): self.extensions = {}; self.before = []
    def route(self, *args, **kwargs): return lambda fn: fn
    def before_request(self, fn): self.before.append(fn); return fn


class NotificationRuntimeAdversarialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.transport = FakeTransport()
        self.store = push.PushStore(self.tmp.name, cipher=FakeCipher(), transport=self.transport)
        self.request = types.SimpleNamespace(headers={'Authorization': 'Bearer synthetic-auth'},
                                             path='/logout', is_json=True)
        self.g = types.SimpleNamespace(app_bearer=True)
        self.users = {'alice': {'password_hash': 'synthetic-password-version-1'}}
        flask = types.SimpleNamespace(request=self.request, session={'username': 'alice'},
                                      g=self.g, jsonify=lambda **kw: kw)
        self.callbacks = {}
        def register_stub(app, directory, **kwargs):
            self.callbacks.update(kwargs)
            return lambda: self.store
        self.addCleanup(patch.stopall)
        patch.dict(sys.modules, {'flask': flask}).start()
        patch.object(push, 'register', side_effect=register_stub).start()
        patch.object(runtime.Credentials, 'load', return_value=(
            types.SimpleNamespace(bearer=lambda: 'synthetic-provider-bearer'), None)).start()
        self.app = FakeApp()
        self.notify, self.purge = runtime.register(self.app, self.tmp.name, (),
            lambda: self.users, lambda record: bool(record.get('blocked')))
        owner, sid = self.callbacks['authenticate']()
        self.binding = self.store.bind(owner, sid, str(uuid.uuid4()), 'ios', 'production')['id']
        self.store.save_token(owner, sid, self.binding, 'ab' * 32, 'apns')
        self.job = str(uuid.uuid4())

    def test_cookie_identity_cannot_register_native_push(self):
        self.g.app_bearer = False
        with self.assertRaises(push.PushError) as error:
            self.callbacks['authenticate']()
        self.assertEqual(error.exception.status, 401)

    def test_current_bearer_logout_revokes_binding(self):
        self.app.before[0]()
        self.notify('alice', self.job)
        self.assertEqual(self.transport.calls, [])

    def test_same_authenticated_token_whitespace_revokes_original_binding(self):
        # Production _ler_token_app accepts both via cab[7:].strip().
        self.request.headers['Authorization'] = 'Bearer   synthetic-auth  '
        self.app.before[0]()
        self.notify('alice', self.job)
        self.assertEqual(len(self.transport.calls), 0,
                         'Equivalent authenticated bearer did not revoke original binding')

    def test_password_rotation_revokes_existing_push_authority(self):
        # require_auth invalidates the old bearer after this password version changes.
        self.users['alice']['password_hash'] = 'synthetic-password-version-2'
        self.notify('alice', self.job)
        self.assertEqual(len(self.transport.calls), 0,
                         'A push binding survived revocation of its authentication credential')

    def test_blocked_owner_does_not_receive_push(self):
        self.users['alice']['blocked'] = True
        self.notify('alice', self.job)
        self.assertEqual(self.transport.calls, [])

    def test_push_metadata_contains_only_generic_job_identifiers(self):
        self.notify('alice', self.job)
        payload = self.transport.calls[0]['payload']
        self.assertEqual(set(payload), {'aps', 'schema_version', 'event', 'event_id', 'job_id', 'binding_id'})
        self.assertEqual(payload['aps']['alert'], {'title': 'IALD', 'body': 'Sua resposta está pronta.'})
        self.assertEqual(payload['job_id'], self.job)
        self.assertNotIn('alice', str(self.store.receipts('alice', self.job)))

    def authority_expiry(self):
        path = Path(self.tmp.name) / '.iald_runtime' / 'native_push' / 'authorization.sqlite3'
        with closing(sqlite3.connect(path)) as db:
            return db.execute('SELECT expires FROM authority').fetchone()[0]

    def test_exact_expiry_revokes_before_dispatch(self):
        with patch.object(runtime.time, 'time', return_value=self.authority_expiry()):
            self.notify('alice', self.job)
        self.assertEqual(self.transport.calls, [])

    def test_expiry_survives_runtime_restart(self):
        expiry = self.authority_expiry()
        notify, _ = runtime.register(FakeApp(), self.tmp.name, (),
            lambda: self.users, lambda record: bool(record.get('blocked')))
        with patch.object(runtime.time, 'time', return_value=expiry + 1):
            notify('alice', self.job)
        self.assertEqual(self.transport.calls, [])

    def test_signed_expiry_callback_is_not_extended_by_activity(self):
        expiry = self.authority_expiry()
        observed = []
        def token_expiry(token):
            observed.append(token)
            return expiry
        runtime.register(FakeApp(), self.tmp.name, (),
            lambda: self.users, lambda record: bool(record.get('blocked')),
            token_expiry=token_expiry)
        self.request.headers['Authorization'] = 'Bearer   synthetic-auth  '
        with patch.object(runtime.time, 'time', return_value=expiry - 1):
            self.callbacks['authenticate']()
        self.assertEqual(observed, ['synthetic-auth'])
        self.assertEqual(self.authority_expiry(), expiry)
        with patch.object(runtime.time, 'time', return_value=expiry):
            with self.assertRaises(push.PushError) as error:
                self.callbacks['authenticate']()
            self.assertEqual(error.exception.status, 401)
            self.notify('alice', self.job)
        self.assertEqual(self.transport.calls, [])

    def test_recreated_account_does_not_inherit_binding(self):
        self.users['alice']['created'] = 'synthetic-new-account-generation'
        self.notify('alice', self.job)
        self.assertEqual(self.transport.calls, [])

    def test_authority_database_contains_no_raw_credentials(self):
        path = Path(self.tmp.name) / '.iald_runtime' / 'native_push' / 'authorization.sqlite3'
        raw = path.read_bytes()
        for secret in (b'alice', b'synthetic-auth', b'synthetic-password-version-1'):
            self.assertNotIn(secret, raw)


if __name__ == '__main__': unittest.main(verbosity=2)
