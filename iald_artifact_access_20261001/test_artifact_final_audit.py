"""Independent offline audit: AST-extracted routes, synthetic stores, no real server."""
import ast
import hashlib
from types import SimpleNamespace
import sys
import unittest

from flask import redirect, session
from test_artifact_stage_privacy import StagedPrivacyTests, artifacts, STAGE
sys.path.insert(0, str(STAGE))
import iald_task_sandbox as sandbox


class FinalAuditTests(StagedPrivacyTests):
    def setUp(self):
        super().setUp()
        self.env.update(COIN_AVAILABLE=False, iald_motores=SimpleNamespace(NATIVA='native'),
                        _motor_do_usuario=lambda owner: ('native', self.users[owner]),
                        _estado_entrada=lambda: (True,), auth_log=lambda *args: None,
                        COOKIE_ENTRADA='synthetic-oauth')
        names = {'_abrir_sessao_web', '_destino_web', '_concluir_navegador'}
        nodes = [n for n in self.tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
        self.assertEqual({n.name for n in nodes}, names)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<isolated-login-handoff>', 'exec'), self.env)
        self.env['PUBLIC_ROUTES'].update({'audit_login', 'audit_oauth'})

        @self.app.get('/app/index.html')
        def audit_app(): return 'Synthetic app shell'

        @self.app.post('/audit-login/<owner>')
        def audit_login(owner):
            self.env['_abrir_sessao_web'](owner)
            return redirect(self.env['_destino_web'](owner))

        @self.app.post('/audit-oauth/<owner>')
        def audit_oauth(owner):
            return self.env['_concluir_navegador']({'o': 'web'}, 'ativo', owner, 'synthetic')

    def launch(self):
        return self.client.get('/app/index.html', query_string={'artifact': self.item['id']})

    def test_final_login_preserves_only_uuid_then_consumes_it(self):
        response = self.launch()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], '/login')
        with self.client.session_transaction() as state:
            self.assertEqual(dict(state), {'pending_artifact_id': self.item['id']})
            state.update(untrusted_redirect='https://foreign.invalid', is_admin=True)
        self.assertEqual(self.client.get('/login').status_code, 200)
        response = self.client.post('/audit-login/alice')
        self.assertEqual(response.headers['Location'], '/app/index.html?artifact=' + self.item['id'])
        with self.client.session_transaction() as state:
            self.assertNotIn('pending_artifact_id', state)
            self.assertNotIn('untrusted_redirect', state)
            self.assertFalse(state['is_admin'])
        self.assertEqual(self.client.get(self.view_path).status_code, 200)
        response = self.client.post('/audit-login/alice')
        self.assertEqual(response.headers['Location'], '/iald_chat.html')

    def test_final_uuid_is_navigation_only_other_owner_still_denied(self):
        self.launch()
        self.assertEqual(self.client.post('/audit-login/bob').status_code, 302)
        self.assertEqual(self.client.get(self.view_path).status_code, 404)
        self.assertEqual(self.client.post(self.access_path, json={}, headers={'Origin': 'http://localhost'}).status_code, 404)

    def test_final_non_uuid_and_foreign_redirects_are_not_saved(self):
        for value in ['https://foreign.invalid', '../logout', self.item['id'] + '&next=https://foreign.invalid', '', 'x' * 1000]:
            with self.subTest(value=value):
                self.assertEqual(self.client.get('/app/index.html', query_string={'artifact': value}).status_code, 302)
                with self.client.session_transaction() as state:
                    self.assertNotIn('pending_artifact_id', state)
        self.assertEqual(self.client.post('/audit-login/alice').headers['Location'], '/iald_chat.html')

    def test_final_artifact_parameter_on_api_does_not_create_pending_redirect(self):
        self.assertEqual(self.client.get(self.view_path, query_string={'artifact': self.item['id']}).status_code, 401)
        with self.client.session_transaction() as state:
            self.assertNotIn('pending_artifact_id', state)

    def test_final_oauth_web_completion_preserves_pending_uuid(self):
        self.launch()
        response = self.client.post('/audit-oauth/alice')
        self.assertEqual(response.headers['Location'], '/app/index.html?artifact=' + self.item['id'])
        self.assertEqual(self.client.get(self.view_path).status_code, 200)

    def test_final_artifact_reopens_from_disk_without_in_memory_index(self):
        reopened = artifacts.ArtifactStore(self.root)
        path, metadata = reopened.resolve('alice', self.item['id'])
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), self.item['sha256'])
        self.assertEqual(metadata['id'], self.item['id'])
        self.assertEqual(artifacts.app_artifact_url(metadata['id']), self.item['app_url'])
        self.assertNotIn('app_url', metadata)  # Existing persisted schema needs no migration.
        with self.assertRaises(artifacts.ArtifactError):
            reopened.resolve('bob', self.item['id'])

    def test_final_sandbox_ignores_supplied_app_url_and_uses_real_store_uuid(self):
        stored = self.store.ingest('alice', 'result.txt', b'Synthetic result')
        reference = sandbox._artifact_reference({**stored, 'app_url': 'https://foreign.invalid/poison'}, 'result.txt')
        self.assertEqual(reference['app_url'], artifacts.app_artifact_url(stored['id']))
        self.assertNotIn('foreign.invalid', str(reference))
        for invalid in ['bad', '../escape', None, 123, {'id': stored['id']}, stored['id'] + '?token=x']:
            with self.subTest(invalid=invalid):
                self.assertNotIn('app_url', sandbox._artifact_reference({'id': invalid, 'app_url': stored['app_url']}, 'result.txt'))

    def test_final_sandbox_privacy_filters_are_preserved(self):
        from test_artifact_access import PRODUCTION
        original = ast.parse((PRODUCTION / 'iald_task_sandbox.py').read_bytes())
        staged = ast.parse((STAGE / 'iald_task_sandbox.py').read_bytes())
        def filters(tree):
            selected = []
            for node in tree.body:
                if isinstance(node, ast.FunctionDef) and node.name == '_public': selected.append(node)
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in {'_SECRET', '_CONFIDENTIAL'} for t in node.targets): selected.append(node)
            self.assertEqual(len(selected), 3)
            return [ast.dump(n, include_attributes=False) for n in selected]
        self.assertEqual(filters(original), filters(staged))
        ref = sandbox._artifact_reference({'id': 'Bearer synthetic-secret', 'sha256': 'iald_stack_v7.py'}, 'result.txt')
        self.assertNotIn('id', ref)
        self.assertNotIn('sha256', ref)
        self.assertNotIn('app_url', ref)


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(FinalAuditTests(name) for name in sorted(FinalAuditTests.__dict__) if name.startswith('test_final_'))


if __name__ == '__main__': unittest.main(verbosity=2)
