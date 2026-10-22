"""Offline independent audit. All mutable fixtures stay below validation/."""
import ast
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import hashlib
import importlib.util
import ipaddress
import json
from pathlib import Path
import socket
import sqlite3
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
import uuid
from unittest.mock import patch
from urllib.parse import urlparse, urljoin

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / 'stage'
PINS = {}


def load(name):
    path = STAGE / (name + '.py')
    PINS[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


routes = load('iald_research_routes')
api = load('iald_operator_bench')
catalog = load('iald_bench_catalog')
public_fetch = load('iald_public_fetch')


class Store:
    def __init__(self):
        self.values = []

    def ingest(self, owner, name, raw):
        self.values.append((owner, name, raw))
        return dict(id='synthetic-artifact', filename=name, bytes=len(raw),
                    sha256=hashlib.sha256(raw).hexdigest(),
                    app_url='/app/index.html?artifact=synthetic-artifact',
                    mobile_url='SYNTHETIC-CAPABILITY-MUST-NOT-LEAK')


class Catalog:
    def __init__(self):
        self.calls = 0
        self.response = {'status': 'OK', 'value': 2}

    def provenance(self, operation, parameters):
        return {'source': 'synthetic-v1'}

    def request(self, operation, parameters):
        self.calls += 1
        return self.response


class IndependentBench(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=HERE, prefix='fixture_')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.record = {'admin': True, 'classe_usuario': 'operador'}
        self.store = Store()
        self.catalog = Catalog()
        self.bridge = api.OperatorBench(self.root, 'luiz', lambda _: self.record,
                                        self.store, self.catalog, self.root / 'bench')
        self.ledger = self.bridge.ledger()

    def plan(self, x=1):
        return self.ledger.plan('calculate', {'x': x}, {'source': 'synthetic-v1'},
                                'objective', 'hypothesis', 'falsifier')[0]['record']['id']

    def test_exact_operator_identity_and_public_exclusion(self):
        for user, record in [('other', self.record), ('Luiz', self.record),
                             ('luiz', {'admin': 1, 'classe_usuario': 'operador'}),
                             ('luiz', {'admin': True}),
                             ('luiz', dict(self.record, bloqueado=True))]:
            with self.subTest(user=user, record=record):
                self.assertFalse(api.is_operator(record, user))
                scope = NS(tools=[], store=self.store)
                self.assertIs(api.attach(scope, self.root, user, lambda _: record), scope)
                self.assertEqual(scope.tools, [])

    def test_revalidate_revoked_role_without_dispatch(self):
        identifier = self.plan()
        self.record['classe_usuario'] = 'usuario'
        self.assertEqual(self.bridge.execute('bench_run', {'route_id': identifier})['status'], 'FORBIDDEN')
        self.assertEqual(self.catalog.calls, 0)

    def test_concurrent_identical_plans_have_one_identity(self):
        with ThreadPoolExecutor(max_workers=5) as pool:
            ids = list(pool.map(lambda _: self.plan(), range(8)))
        self.assertEqual(len(set(ids)), 1)

    def test_claim_once_after_reopen(self):
        identifier = self.plan()
        self.assertTrue(self.ledger.claim(identifier))
        reopened = routes.Routes(self.ledger.path)
        self.assertFalse(reopened.claim(identifier))
        self.assertEqual(self.bridge.run(identifier)['status'], 'UNCERTAIN')
        self.assertEqual(self.catalog.calls, 0)

    def test_unfinished_claim_blocks_different_route_after_reopen(self):
        first, second = self.plan(1), self.plan(2)
        self.assertTrue(self.ledger.claim(first))
        reopened = routes.Routes(self.ledger.path)
        try:
            admitted = reopened.claim(second)
        except (ValueError, RuntimeError):
            admitted = False
        self.assertFalse(admitted, 'A distinct route was admitted despite an unresolved durable claim')

    def test_stale_check_cannot_overwrite_concurrent_completion(self):
        identifier = self.plan()
        def changed_during_check(operation, parameters):
            self.assertTrue(self.ledger.claim(identifier))
            self.ledger.event(identifier, 'RESULT_RECEIVED', {'result': {'value': 2}, 'sha256': routes.digest({'value': 2})})
            self.ledger.event(identifier, 'COMPLETED', {'artifact': {'id': 'preserved-result'}})
            return {'source': 'synthetic-v2'}
        self.catalog.provenance = changed_during_check
        self.bridge.run(identifier)
        self.assertEqual(self.ledger.get(identifier)['state'], 'COMPLETED',
                         'A stale pre-claim reader overwrote the concurrent final state')

    def test_summary_fits_app_transport(self):
        # All values are well below the upstream 16 MiB response contract.
        result = {f'field_{i}': 'x' * 1500 for i in range(24)}
        bounded = self.bridge._bounded(result, 'synthetic')
        size = len(json.dumps(bounded, ensure_ascii=False, separators=(',', ':'), allow_nan=False))
        self.assertLessEqual(size, 24000, 'App encode_task_result rejects this envelope')

    def test_summary_keeps_route_identity_at_top_level(self):
        result = dict(status='COMPLETED', route_id='synthetic-route', text='x' * 15000)
        bounded = self.bridge._bounded(result, 'synthetic')
        self.assertEqual(bounded.get('status'), 'COMPLETED')
        self.assertEqual(bounded.get('route_id'), 'synthetic-route')

    def test_artifacts_owner_and_capability_filter(self):
        artifact = self.bridge._artifact('synthetic.json', {'value': 1})
        self.assertEqual(self.store.values[0][0], 'luiz')
        self.assertNotIn('SYNTHETIC-CAPABILITY', json.dumps(artifact))
        self.assertIn('app_url', artifact)

    def test_complete_result_survives_artifact_failure(self):
        identifier = self.plan()
        self.ledger.claim(identifier)
        with patch.object(self.store, 'ingest', side_effect=OSError('synthetic-private-detail')):
            self.bridge._work(identifier)
        result = self.bridge.result(identifier)
        self.assertEqual(result['status'], 'RESULT_STORED_ARTIFACT_FAILED')
        self.assertEqual(json.loads(result['text']), self.catalog.response)
        self.assertNotIn('synthetic-private-detail', json.dumps(result))
        self.bridge.run(identifier)
        self.assertEqual(self.catalog.calls, 1)

    def test_load_acknowledgement_is_not_finished_research(self):
        identifier = self.ledger.plan('universe_load', {'domain': 'gw_strain'},
            {'source': 'synthetic-v1'}, 'load', 'complete arrays', 'missing arrays')[0]['record']['id']
        self.catalog.response = {'status': 'LOADING', 'loaded_files': 0, 'total_files': 8}
        self.ledger.claim(identifier)
        self.bridge._work(identifier)
        self.assertNotEqual(self.bridge.result(identifier)['status'], 'COMPLETED',
                            'The real resident worker returns LOADING before its load thread completes')

    def test_inquiry_followup_history_is_not_silently_lost(self):
        state = self.root / 'bench' / 'state'
        state.mkdir(parents=True)
        path = state / 'runs.sqlite3'
        with closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE runs(id INTEGER PRIMARY KEY, operation TEXT)')
            db.execute('CREATE TABLE inquiries(id INTEGER PRIMARY KEY, question TEXT)')
            db.execute('CREATE TABLE inquiry_events(id INTEGER PRIMARY KEY, inquiry_id INTEGER, event_type TEXT, note TEXT, related_inquiry_id INTEGER)')
            db.execute("INSERT INTO inquiries VALUES(1,'Synthetic original question')")
            db.execute("INSERT INTO inquiry_events VALUES(1,1,'withdrawn','unique-withdrawal-marker',NULL)")
        before = path.read_bytes()
        self.ledger.import_history(self.root / 'bench')
        self.assertEqual(path.read_bytes(), before)
        self.assertTrue(self.ledger.search('unique-withdrawal-marker')['nodes'],
                        'Existing inquiry_events notes/links are omitted from the imported history')


class CatalogBoundary(unittest.TestCase):
    def test_unknown_commands_urls_paths_are_rejected(self):
        for operation, params in [('shell', {'command': 'whoami'}),
                                  ('lab_describe', {'id': '../../private'}),
                                  ('identity_chain', {'url': 'http://127.0.0.1'}),
                                  ('cosmos_get_export', {'id': '../secret'})]:
            with self.subTest(operation=operation), self.assertRaises(catalog.BenchError):
                catalog.normalize(operation, params)

    def test_ram_complete_never_reloads_and_partial_never_releases(self):
        for state in ('READY', 'PARTIAL'):
            status = dict(status=state, domain='gw_strain', total_files=2,
                          loaded_files=2, errors=[], generation=1, worker_pid=2, load_id=str(uuid.uuid4()))
            with self.subTest(state=state), patch.object(catalog, '_gw_status', return_value=status), \
                 patch.object(catalog, '_http', side_effect=AssertionError('No HTTP dispatch allowed')):
                if state == 'READY':
                    self.assertEqual(catalog.request('universe_load', {})['status'], 'ALREADY_RESIDENT')
                else:
                    with self.assertRaises(catalog.BenchError): catalog.request('universe_load', {})


class PublicFetchBoundary(unittest.TestCase):
    def namespace(self, resolver, get):
        path = STAGE / 'iald_web_server.py'
        PINS[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        names = {'UrlRecusada', '_ip_publico', '_url_permitida', '_buscar_url_segura'}
        nodes = [n for n in ast.parse(path.read_text(encoding='utf-8-sig')).body
                 if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
        env = dict(ipaddress=ipaddress, urlparse=urlparse, urljoin=urljoin,
                   _resolver_ips=resolver, req_lib=NS(get=get), FETCH_MAX_REDIRECIONAMENTOS=5)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), env)
        return env

    def test_literal_and_resolved_loopback_do_not_reach_transport(self):
        get = lambda *a, **k: self.fail('Loopback transport was attempted')
        for address in ('127.0.0.1', '::1', '::ffff:127.0.0.1', '64:ff9b::7f00:1'):
            env = self.namespace(lambda *a: [address], get)
            with self.subTest(address=address), self.assertRaises(env['UrlRecusada']):
                env['_buscar_url_segura']('http://synthetic.invalid:18765/api/universe/status', {}, 1)

    def test_rebinding_cannot_return_loopback_bench_content(self):
        # First resolution passes; the separate requests resolution lands on loopback.
        # No DNS, socket, HTTP server, credentials or actual experiment is involved.
        resolutions = []
        def resolver(*args):
            ip = '8.8.8.8' if not resolutions else '127.0.0.1'
            resolutions.append(ip)
            return [ip]
        def get(url, **kwargs):
            peer = resolver(urlparse(url).hostname, 18765)[0]
            sock = NS(getpeername=lambda: (peer, 18765))
            return NS(status_code=200, headers={}, peer=peer,
                      raw=NS(_connection=NS(sock=sock)), close=lambda: None)
        env = self.namespace(resolver, get)
        class PinnedDialObserved(Exception):
            pass
        observed = []
        def dial(addresses, port, timeout):
            observed.extend(addresses)
            raise PinnedDialObserved()
        with patch.object(public_fetch, '_connect', dial):
            try:
                response, _ = env['_buscar_url_segura']('http://synthetic.invalid:18765/api/universe/event', {}, 1)
            except env['UrlRecusada']:
                return
            except PinnedDialObserved:
                self.assertEqual(resolutions, ['8.8.8.8'])
                self.assertTrue(observed)
                self.assertTrue(all(env['_ip_publico'](ip) for ip in observed))
                return
        self.assertTrue(env['_ip_publico'](response.peer),
                        'Public fetch returned a response from loopback after DNS rebinding')


if __name__ == '__main__':
    # Accidentally introduced network must be a visible test failure.
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden')):
        suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    evidence = dict(tests=result.testsRun, failures=[(str(t), text) for t, text in result.failures],
                    errors=[(str(t), text) for t, text in result.errors],
                    passed=result.wasSuccessful(), source_sha256=PINS,
                    network=False, experiments=False, paid_calls=0,
                    source_changed_during_run=[name for name, digest in PINS.items()
                        if hashlib.sha256((STAGE / name).read_bytes()).hexdigest() != digest])
    print(json.dumps(evidence, ensure_ascii=False))
    sys.exit(not result.wasSuccessful())
