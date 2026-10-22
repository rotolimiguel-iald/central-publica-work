"""Read-only staged-server audit. Only synthetic stores and diagnostic files are written."""
import ast
import io
import json
import logging
from pathlib import Path
import re
import sys
import unittest
from html.parser import HTMLParser
from urllib.parse import urlsplit
from unittest.mock import patch

WORK = Path(__file__).parent
STAGE = WORK / 'stage'
sys.dont_write_bytecode = True
sys.path.insert(0, str(STAGE))
import iald_task_artifacts as artifacts
import iald_artifact_view as view
import test_artifact_access as baseline


class Elements(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.items = []
        self.feed(source)
    def handle_starttag(self, tag, attrs): self.items.append((tag, dict(attrs)))


class StagedPrivacyTests(baseline.ArtifactAccessTests):
    @classmethod
    def setUpClass(cls): cls.tree = ast.parse((STAGE / 'iald_web_server.py').read_bytes())

    def setUp(self):
        super().setUp()
        env = self.app.view_functions['api_task_artifact'].__globals__
        env.update(artifact_view=view, URL_PUBLICA=artifacts.PUBLIC_BASE_URL, logging=logging, re=re)
        env['PUBLIC_ROUTES'].add('task_view')
        names = {'_identificacao_json_post', 'api_task_artifact_view', 'api_task_artifact_access',
                 'task_view', '_TaskDownloadLogFilter'}
        nodes = [n for n in self.tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
        self.assertEqual({n.name for n in nodes}, names)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), '<staged-view-routes>', 'exec'), env)
        self.env = env
        self.view_path = self.auth_path + '/view'
        self.access_path = self.auth_path + '/access'

    def test_authenticated_preview_is_owner_bound_and_does_not_rotate_ticket(self):
        ticket = self.store.tickets / (self.item['id'] + '.json')
        before = ticket.read_bytes()
        self.assertEqual(self.client.get(self.view_path).status_code, 401)
        self.assertEqual(self.client.get(self.view_path, headers={'Authorization': 'Bearer synthetic-bob'}).status_code, 404)
        response = self.client.get(self.view_path, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual(set(response.json), {'id', 'kind', 'filename', 'bytes', 'sha256', 'preview_html'})
        self.assertEqual(response.headers['Cache-Control'], 'private, no-store')
        self.assertEqual(ticket.read_bytes(), before)

    def test_access_requires_post_auth_json_origin_and_no_owner_override(self):
        self.assertEqual(self.client.post(self.access_path, json={}).status_code, 401)
        self.assertEqual(self.client.get(self.access_path, headers=self.headers).status_code, 405)
        self.assertEqual(self.client.post(self.access_path, data='{}', headers=self.headers).status_code, 415)
        self.assertEqual(self.client.post(self.access_path, json={'owner': 'bob'}, headers=self.headers).status_code, 400)
        self.assertEqual(self.client.post(self.access_path, json={}, headers={**self.headers, 'Origin': 'https://foreign.invalid'}).status_code, 403)
        response = self.client.post(self.access_path, json={}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json), {'id', 'download_url', 'preview_url', 'expires_at'})
        self.assertEqual(response.headers['Cache-Control'], 'private, no-store')
        self.assertEqual(self.client.get(self.ticket_path).status_code, 404)

    def test_capability_shell_has_empty_sandbox_and_restrictive_headers(self):
        response = self.client.post(self.access_path, json={}, headers=self.headers)
        path = urlsplit(response.json['preview_url']).path
        page = self.client.get(path)
        self.assertEqual(page.status_code, 200)
        self.assertEqual(page.mimetype, 'text/html')
        self.assertEqual(page.headers['Content-Security-Policy'], view.PAGE_CSP)
        for key, val in view.PRIVATE_HEADERS.items(): self.assertEqual(page.headers[key], val)
        parsed = Elements(page.get_data(as_text=True))
        frames = [attrs for tag, attrs in parsed.items if tag == 'iframe']
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0]['sandbox'], '')
        self.assertEqual(frames[0]['referrerpolicy'], 'no-referrer')
        self.assertNotIn('src', frames[0])
        inner = Elements(frames[0]['srcdoc'])
        policies = [attrs['content'] for tag, attrs in inner.items if tag == 'meta' and attrs.get('http-equiv') == 'Content-Security-Policy']
        self.assertEqual(policies, [view.PREVIEW_CSP])
        self.assertNotIn('script', [tag for tag, _ in parsed.items + inner.items])

    def test_capability_mismatch_and_expiry_fail_without_content(self):
        response = self.client.post(self.access_path, json={}, headers=self.headers)
        path = urlsplit(response.json['preview_url']).path
        invalid = path[:-1] + '!'
        self.assertEqual(self.client.get(invalid).status_code, 404)
        with patch.object(artifacts.time, 'time', return_value=10**12):
            expired = self.client.get(path)
        self.assertEqual(expired.status_code, 404)
        self.assertNotIn(b'Synthetic text', expired.data)
        self.assertEqual(expired.headers['Cache-Control'], 'private, no-store')
        self.assertEqual(expired.headers['Content-Security-Policy'], view.PAGE_CSP)

    def test_view_and_download_tokens_redacted_with_real_handler(self):
        log = logging.getLogger('artifact-audit-only')
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        filt = self.env['_TaskDownloadLogFilter']()
        handler.addFilter(filt); log.addHandler(handler)
        old_level, old_propagate = log.level, log.propagate
        log.setLevel(logging.INFO); log.propagate = False
        try:
            for route in ['view', 'download']:
                log.info('GET /task-%s/%s/%s', route, self.item['id'], 'SYNTHETIC_TOKEN')
            log.info('Other diagnostic remains visible')
        finally:
            log.removeHandler(handler); log.setLevel(old_level); log.propagate = old_propagate; handler.close()
        self.assertNotIn('SYNTHETIC_TOKEN', stream.getvalue())
        self.assertEqual(stream.getvalue().count('[REDACTED]'), 2)
        self.assertIn('Other diagnostic remains visible', stream.getvalue())

    def test_app_url_is_stable_identifier_without_capability(self):
        self.assertEqual(self.item['app_url'], artifacts.PUBLIC_BASE_URL + '/app/index.html?artifact=' + self.item['id'])
        old = self.item['app_url']
        view.access(self.store, 'alice', self.item['id'])
        self.assertEqual(artifacts.app_artifact_url(self.item['id']), old)

    def test_prepare_synthetic_browser_fixture_without_real_content_or_tokens(self):
        token = self.item['mobile_url'].rsplit('/', 1)[-1]
        page = view.ticket_page(self.store, self.item['id'], token).replace(token, 'SYNTHETIC_CAPABILITY')
        # Bypass validation only for an explicit defense-in-depth browser canary.
        hostile = '<html><head></head><body><p>Canary</p><script>window.__canaryExecuted=true</script><img src="https://no-network.invalid/pixel"></body></html>'
        with patch.object(view, '_checked_html', return_value=hostile):
            canary = view.ticket_page(self.store, self.item['id'], token).replace(token, 'SYNTHETIC_CAPABILITY')
        fixture = {'synthetic_only': True, 'csp': view.PAGE_CSP, 'page': page, 'canary': canary}
        (WORK / 'browser_preview_fixture.json').write_text(json.dumps(fixture), encoding='utf-8')


if __name__ == '__main__': unittest.main(verbosity=2)
