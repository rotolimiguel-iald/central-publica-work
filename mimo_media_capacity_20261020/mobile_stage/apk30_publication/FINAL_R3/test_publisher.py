"""Offline fixtures only: synthetic bytes, exact endpoint AST, no server import."""
import ast
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace
import tempfile
import unittest
import publish_apk30 as publisher


class PublisherTests(unittest.TestCase):
    def test_additive_preserves_existing(self):
        with tempfile.TemporaryDirectory(dir=publisher.HERE) as folder:
            root = Path(folder)
            source = root / 'fixture.bin'
            old = root / 'previous.apk'
            source.write_bytes(b'synthetic APK fixture')
            old.write_bytes(b'old bytes')
            before = publisher.pin(old)
            publisher.create_additive(source, root / 'new.apk', root, publisher.pin(source)['sha256'])
            self.assertEqual(publisher.pin(old), before)
            self.assertEqual((root / 'new.apk').read_bytes(), source.read_bytes())

    def test_existing_target_even_identical_refused(self):
        with tempfile.TemporaryDirectory(dir=publisher.HERE) as folder:
            root = Path(folder)
            source, target = root / 'fixture.bin', root / 'new.apk'
            source.write_bytes(b'same')
            target.write_bytes(b'same')
            with self.assertRaises(RuntimeError):
                publisher.create_additive(source, target, root, publisher.pin(source)['sha256'])
            self.assertEqual(target.read_bytes(), b'same')
            self.assertFalse((root / 'APK30.tmp').exists())

    def test_exclusive_intent_refuses_repeat(self):
        with tempfile.TemporaryDirectory(dir=publisher.HERE) as folder:
            path = Path(folder) / 'intent.json'
            publisher.exclusive_json(path, {'first': True})
            with self.assertRaises(FileExistsError):
                publisher.exclusive_json(path, {'first': False})
            self.assertTrue(json.loads(path.read_bytes())['first'])

    def test_staged_hash_mismatch_does_not_publish(self):
        with tempfile.TemporaryDirectory(dir=publisher.HERE) as folder:
            root = Path(folder)
            source = root / 'fixture.bin'
            source.write_bytes(b'fixture')
            with self.assertRaises(RuntimeError):
                publisher.create_additive(source, root / 'new.apk', root, '0' * 64)
            self.assertFalse((root / 'new.apk').exists())

    def test_missing_review_go_denied(self):
        with self.assertRaises(RuntimeError):
            publisher.authorize({}, {}, {}, {})

    def test_current_exact_auth_and_download_ast(self):
        # Extract only these exact definitions and literal policy sets. No module import,
        # Flask app, registration, network, users DB or server initialization occurs.
        server = Path('C:/IALD/projetos_pyhton/IALD/iald_web_server.py')
        tree = ast.parse(server.read_text(encoding='utf-8-sig'))
        nodes = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in ('require_auth', 'serve_download'):
                node.decorator_list = []
                nodes.append(node)
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('PUBLIC_ROUTES', 'PUBLIC_FILES', 'RE_DOWNLOAD_GRATUITO') for t in node.targets):
                nodes.append(node)
        self.assertEqual(len(nodes), 5)
        session = {}
        request = SimpleNamespace(endpoint='serve_download', path='/downloads/IALD-4.1-30.apk', method='GET', headers={}, args={}, is_json=False)
        user = {'password_hash': 'fixture', 'admin': False}
        sent = []
        scope = dict(re=re, hashlib=hashlib, datetime=datetime, timedelta=timedelta,
                     session=session, request=request, g=SimpleNamespace(), SESSION_TIMEOUT_HOURS=24,
                     load_users_estrito=lambda: {'fixture': user}, _conta_bloqueada=lambda u: False,
                     redirect=lambda u: ('redirect', u), url_for=lambda n, **k: '/' + n,
                     Response=lambda body, status: (status, body), jsonify=lambda d: d,
                     iald_motores=SimpleNamespace(plano_de=lambda u: 'free', GRATUITO='free'),
                     DOWNLOADS_DIR='fixture', os=SimpleNamespace(path=SimpleNamespace(join=lambda *p: '/'.join(p), isfile=lambda p: True)),
                     send_from_directory=lambda *a, **k: sent.append(a) or b'fixture-apk')
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(server), 'exec'), scope)
        self.assertNotIn('serve_download', scope['PUBLIC_ROUTES'])
        self.assertEqual(scope['require_auth'](), ('redirect', '/login'))
        self.assertEqual(sent, [])  # zero APK bytes for anonymous request
        session.update(authenticated=True, username='fixture', auth_version=hashlib.sha256(b'fixture').hexdigest(), last_active=datetime.now().isoformat())
        self.assertIsNone(scope['require_auth']())
        self.assertEqual(scope['serve_download']('IALD-4.1-30.apk'), b'fixture-apk')
        self.assertEqual(scope['serve_download']('other.txt')[0], 403)
        self.assertEqual(scope['serve_download']('../IALD-4.1-30.apk')[0], 403)


if __name__ == '__main__':
    unittest.main(verbosity=2)
