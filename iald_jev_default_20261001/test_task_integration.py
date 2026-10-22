"""Offline integration regressions: memory-only stores, mocked SDK/HTTP, server AST."""
import ast
from copy import deepcopy
import hashlib
import io
import json
import logging
from pathlib import Path
import sys
import re
import threading
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
STAGE = Path(__file__).parent / 'stage'
sys.path.insert(0, str(STAGE))
import iald_task_bridge as bridge
import iald_task_session as sessions
import iald_task_sandbox as sandbox
import iald_app_providers as providers
import iald_auto_router as router


class MemoryStore:
    def __init__(self, *args):
        self.writes = []

    def ingest(self, owner, name, raw):
        self.writes.append((owner, name, raw))
        identity = 'artifact-' + str(len(self.writes))
        return dict(id=identity, filename=name, sha256=hashlib.sha256(raw).hexdigest(),
                    bytes=len(raw), url='/api/task-artifacts/' + identity)


def memory_session(root, owner, store, authorize, delegate, python, definition):
    # Real execute(), but no filesystem constructor/journal.
    session = sessions.TaskSession.__new__(sessions.TaskSession)
    session.id = 'integration';session.owner = owner;session.store = store
    session.authorize = authorize;session.delegate = delegate;session.python = python
    session.tools = [];session.steps = {};session.results = {};session.counts = {}
    session.lock = threading.Lock();session.saved = []
    session._save = lambda: session.saved.append(deepcopy(session.steps))
    return session


class Guard:
    def __init__(self): self.calls = []
    def reserve(self, *args): self.calls.append(('reserve', args));return 'hold'
    def settle(self, *args, **kwargs): self.calls.append(('settle', args, kwargs))


class SDK:
    def __init__(self):
        self.calls = [];self.messages = self;self.on_count = lambda: None
    def with_options(self, **kwargs):
        assert kwargs['max_retries'] == 0
        return self
    def count_tokens(self, **kwargs):
        self.calls.append(('count', kwargs));self.on_count()
        return SimpleNamespace(input_tokens=183135)
    def create(self, **kwargs):
        self.calls.append(('create', kwargs))
        return {'id': 'msg_test', 'stop_reason': 'end_turn',
                'usage': {'input_tokens': 183135, 'output_tokens': 20},
                'content': [
                    {'type': 'server_tool_use', 'id': 'srvtoolu_test',
                     'name': 'bash_code_execution', 'input': {'command': 'python code.py'}},
                    {'type': 'bash_code_execution_tool_result', 'tool_use_id': 'srvtoolu_test',
                     'content': {'type': 'bash_code_execution_result', 'return_code': 0,
                                 'stdout': '42\n', 'stderr': '', 'content': []}}]}


class Response:
    def __init__(self, flow): self.response = flow;self.is_streamed = True;self.callbacks = []
    def call_on_close(self, fn): self.callbacks.append(fn)
    def close(self):
        try: self.response.close()
        finally:
            for fn in self.callbacks: fn()


def server_functions(names, namespace):
    tree = ast.parse((STAGE / 'iald_web_server.py').read_text(encoding='utf-8'))
    nodes = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), 'server_ast', 'exec'), namespace)
    return namespace


def wait_until(predicate):
    deadline = time.monotonic() + 3
    while not predicate():
        if time.monotonic() > deadline: raise AssertionError('Worker did not finish')
        threading.Event().wait(.01)


class TaskIntegration(unittest.TestCase):
    def setUp(self):
        # Unexpected network use fails even if a test accidentally reaches requests.
        self.network = patch.dict(sys.modules, {'requests': SimpleNamespace(
            post=lambda *a, **kw: (_ for _ in ()).throw(AssertionError('Network forbidden')))})
        self.network.start();self.addCleanup(self.network.stop)
        self.sdk = SDK();self.guard = Guard();self.ledger_calls = []

    def scope(self, evaluation=None, authorize=None):
        cfg = SimpleNamespace(modelo='claude-haiku-4-5', precos=lambda model: (1, .1, 5, 1.25),
                              cota_global_usd=100, cota_operador_usd=10)
        fake_artifacts = SimpleNamespace(ArtifactStore=MemoryStore, TOOL_DEFINITION={})
        with patch.dict(sys.modules, {'iald_task_artifacts': fake_artifacts}), \
             patch.object(bridge, 'TaskSession', memory_session):
            return bridge.make_scope(root=STAGE, user='luiz',
                authorize=authorize or (lambda provider: {'admin': True}),
                options=lambda: ['mimo'], package=lambda: SimpleNamespace(prefix='PUBLIC_FIXED_CORE'),
                evaluation=evaluation, providers=providers,
                router=SimpleNamespace(choose=lambda *a, **kw: ('mimo', {'id': 'routing'})),
                sandbox_config=lambda: cfg, client_factory=lambda cfg: self.sdk,
                guard_factory=lambda: self.guard,
                ledger=SimpleNamespace(registrar=lambda *a, **kw: self.ledger_calls.append((a, kw))))

    def test_real_sandbox_accepts_server_dictionary_authorization(self):
        scope = self.scope()
        result = scope.execute('execute_python', {'code': 'print(42)'})
        self.assertEqual(result['state'], 'completed')
        self.assertTrue(result['success'])
        self.assertEqual(result['evidence_status'], 'execution_observed')
        observed = json.loads(result['execution_excerpt'])
        self.assertEqual(observed['commands'][0]['input']['command']['text'], 'python code.py')
        self.assertEqual(observed['results'][0]['stdout']['text'], '42\n')
        self.assertEqual(observed['results'][0]['return_code'], 0)
        self.assertEqual([name for name, _ in self.sdk.calls], ['count', 'create'])
        self.assertEqual(self.sdk.calls[1][1]['system'], 'PUBLIC_FIXED_CORE')
        self.assertEqual([call[0] for call in self.guard.calls], ['reserve', 'settle'])
        self.assertEqual(scope.control.active, 0)

    def test_false_authorization_never_dispatches(self):
        with self.assertRaises(PermissionError):self.scope(authorize=lambda provider: False)
        self.assertFalse(self.sdk.calls)

    def test_cancel_before_scope_execution_does_not_dispatch(self):
        scope = self.scope();released = []
        scope.control.close(lambda: released.append(True))
        self.assertEqual(scope.execute('execute_python', {'code': 'print(42)'})['status'], 'CANCELLED')
        self.assertFalse(self.sdk.calls);self.assertEqual(released, [True])

    def test_cancel_between_count_and_generation_reaches_sandbox(self):
        scope = self.scope();self.sdk.on_count = scope.control.cancel.set
        result = scope.execute('execute_python', {'code': 'print(42)'})
        self.assertEqual(result['state'], 'cancelled_before_dispatch')
        self.assertEqual([name for name, _ in self.sdk.calls], ['count'])
        self.assertFalse(self.guard.calls)

    def test_delegate_keeps_full_artifact_and_compact_json(self):
        text = '"\\\n' * 5000;seen = []
        def stream(*args, **kwargs):
            seen.append((args, kwargs))
            yield providers.sse({'choices': [{'delta': {'content': text}}]})
            yield providers.sse('[DONE]')
        scope = self.scope(SimpleNamespace(stream=stream))
        result = scope.execute('delegate_task', {'objective': 'Implement', 'role': 'implement'})
        wire = bridge.encode_task_result(result)
        self.assertEqual(json.loads(wire), result)
        self.assertEqual(len(result['text']), 3500)
        self.assertEqual(result['next_offset'], 3500)
        self.assertTrue(result['partial'])
        self.assertLess(wire.index('"artifacts"'), wire.index('"text"'))
        self.assertEqual(scope.store.writes[-1][2].decode(), text)
        self.assertIs(seen[0][1]['task_control'], scope.control)
        self.assertEqual(seen[0][0][2], [])
        self.assertTrue(seen[0][0][1][0]['content'].startswith('PUBLIC_FIXED_CORE'))

    def test_normal_child_completion_does_not_cancel_parent(self):
        ev = providers.Evaluation(STAGE);ev.save = lambda record: None
        control = bridge.TaskControl()
        def api(provider, messages, tools, execute, emit, *args):
            emit({'choices': [{'delta': {'content': 'draft'}}]})
        ev._api = api
        result = list(ev.stream('mimo', [], [], None, memory_sha256='test', task_control=control))
        self.assertIn('[DONE]', result[-1]);self.assertFalse(control.cancel.is_set())
        wait_until(lambda: control.active == 0)

    def test_disconnect_holds_lease_through_nested_worker_journal(self):
        ev = providers.Evaluation(STAGE)
        entered = threading.Event();finish_remote = threading.Event()
        saving_child = threading.Event();finish_save = threading.Event()
        child_ids = set();cancel_flags = []
        def save(record):
            if record['id'] in child_ids and record['status'] != 'started':
                saving_child.set()
                if not finish_save.wait(3): raise AssertionError('Final save not released')
        ev.save = save
        def api(provider, messages, tools, execute, emit, cancel, responses, record, *args):
            cancel_flags.append(cancel)
            if tools:
                execute('delegate_task', {'objective': 'Implement', 'role': 'implement'})
            else:
                child_ids.add(record['id']);entered.set()
                if not finish_remote.wait(3): raise AssertionError('Remote not released')
                if cancel.is_set(): raise InterruptedError()
                emit({'choices': [{'delta': {'content': 'draft'}}]})
        ev._api = api;scope = self.scope(ev)
        flow = ev.stream('mimo', [], [{}], scope.execute, memory_sha256='test',
                         account_key='parent', task_control=scope.control)
        response = Response(flow);response.iald_task_control = scope.control
        ns = server_functions({'_chat_automatico'}, dict(app_router=router, Response=Response,
            _chat_automatico_autorizado=lambda *args: response,
            _sse_aviso=lambda *args: (_ for _ in ()).throw(AssertionError(args))))
        try:
            with patch.object(router, 'available', return_value=True):
                response = ns['_chat_automatico']({}, 'luiz', {}, True, 0)
                next(response.response);self.assertTrue(entered.wait(3))
                response.close()
            self.assertTrue(scope.control.cancel.is_set())
            self.assertEqual(len(cancel_flags), 2)
            self.assertIs(cancel_flags[0], cancel_flags[1])
            self.assertIsNone(router.acquire('luiz'))
            finish_remote.set();self.assertTrue(saving_child.wait(3))
            self.assertIsNone(router.acquire('luiz'))
            finish_save.set();wait_until(lambda: scope.control.released)
            lease = router.acquire('luiz');self.assertIsNotNone(lease);lease.release()
            wait_until(lambda: not ev.active_accounts)
            self.assertTrue(any(step['status'] == 'failed_or_uncertain'
                                for snapshot in scope.saved for step in snapshot.values()))
        finally:
            finish_remote.set();finish_save.set();response.close()
            wait_until(lambda: scope.control.active == 0)

    def test_keepalive_worker_holds_lease_after_generator_closed(self):
        scope = self.scope();entered = threading.Event();finish = threading.Event();released = []
        def delegate(*args):
            entered.set()
            if not finish.wait(3):raise AssertionError('Worker not released')
            return {'status': 'DRAFT_COMPLETED'}
        scope.delegate = delegate
        ns = server_functions({'_com_keepalive'}, dict(threading=threading, AGENT_KEEPALIVE_SEC=.01))
        flow = ns['_com_keepalive'](lambda: scope.execute('delegate_task',
            {'objective': 'Implement', 'role': 'implement'}), task_control=scope.control)
        try:
            next(flow);self.assertTrue(entered.is_set());flow.close()
            scope.control.close(lambda: released.append(True))
            self.assertEqual(released, [])
            finish.set();wait_until(lambda: bool(released))
            self.assertEqual(released, [True])
            self.assertTrue(any(step['status'] == 'returned'
                                for snapshot in scope.saved for step in snapshot.values()))
        finally:finish.set();flow.close()

    def agent_result(self, name, result, *, control=None, cancel_in_tool=False):
        captured = [];turn = [0]
        def payload(body): captured.append(deepcopy(body));return body
        def lines(*args, **kwargs):
            turn[0] += 1
            if turn[0] == 1:
                delta = {'tool_calls': [{'index': 0, 'id': 'call1',
                         'function': {'name': name, 'arguments': '{}'}}]};finish = 'tool_calls'
            else:delta = {'content': 'done'};finish = 'stop'
            yield 'line', 'data: ' + json.dumps({'choices': [{'delta': delta, 'finish_reason': finish}]})
            yield 'fim', None
        def keep(fn, **kwargs):
            if False:yield
            value = fn()
            if cancel_in_tool: control.cancel.set()
            return value
        fake_motors = SimpleNamespace(OPENAI='openai', linhas_com_espera=lines, ErroProvedor=RuntimeError)
        ns = server_functions({'agent_loop'}, dict(json=json, MAX_AGENT_LOOPS=3,
            AGENT_MAX_RESULT_CHARS=6000, AGENT_KEEPALIVE_SEC=1, LLAMA_URL='https://invalid',
            PUBLIC_TOOLS=[], iald_motores=fake_motors, auth_log=lambda *a: None,
            log_request=lambda *a, **kw: None, _ROTULO_FERRAMENTA={}, _com_keepalive=keep,
            task_session=sessions, task_bridge=bridge))
        motor = SimpleNamespace(payload=payload, url='https://invalid', cabecalhos={},
            cfg=SimpleNamespace(timeout=1), provedor='openai', enviar=lambda *args: None)
        list(ns['agent_loop']([{'role': 'user', 'content': 'test'}], motor=motor,
            ferramentas=[{'function': {'name': name}}], executar=lambda *a, **kw: json.dumps(result),
            task_control=control))
        return captured[1]['messages'][-1]['content']

    def test_agent_preserves_escaped_draft_links_beyond_legacy_limit(self):
        result = {'status': 'DRAFT_COMPLETED', 'text': '"\\\n' * 1166,
                  'artifacts': [{'id': 'draft', 'url': '/api/task-artifacts/draft'}],
                  'partial': True, 'next_offset': 3498}
        wire = self.agent_result('delegate_task', result)
        self.assertGreater(len(wire), 6000);self.assertEqual(json.loads(wire), result)

    def test_agent_preserves_read_page_offsets_and_digest(self):
        result = {'status': 'PARTIAL', 'text': '\\\n' * 1750, 'offset': 3500,
                  'next_offset': 7000, 'total_chars': 10000, 'source_sha256': 'a' * 64}
        self.assertEqual(json.loads(self.agent_result('read_task_artifact', result)), result)

    def test_oversized_result_is_rejected_without_field_slicing(self):
        result = {'artifacts': [{'id': 'draft'}], 'text': 'x' * bridge.TASK_RESULT_MAX_CHARS}
        saved = deepcopy(result)
        with self.assertRaisesRegex(ValueError, 'not truncated'): bridge.encode_task_result(result)
        self.assertEqual(result, saved)

    def test_authorized_route_attaches_control_for_response_lifecycle(self):
        scope = self.scope();response = Response(iter(()))
        ns = server_functions({'_chat_automatico_autorizado'}, dict(
            app_router=router, app_providers=providers,
            _automatic_budget_available=lambda *a:True,
            _consentimento_automatico=lambda *a: {'dado': True},
            iald_motores=SimpleNamespace(consentiu=lambda *a: True),
            _opcoes_de_motor=lambda *a: [{'id': 'mimo', 'disponivel': True}],
            load_users_estrito=lambda: {'luiz': {'admin': True}},
            _new_app_task_scope=lambda *a: scope, _chat_avaliacao=lambda *a, **kw: response))
        with patch.object(router, 'choose', return_value=('mimo', {})):
            actual = ns['_chat_automatico_autorizado'](
                {'messages': [{'role': 'user', 'content': 'Implement'}]}, 'luiz', {'admin': True}, True, 0)
        self.assertIs(actual.iald_task_control, scope.control)

    def test_large_sandbox_receipt_becomes_complete_referenced_envelope(self):
        scope = self.scope()
        artifacts = [{'id': 'output', 'url': '/api/task-artifacts/output',
                      'mobile_url': '/task-download/output/' + 'T' * 43}]
        receipt_artifact = {'id': 'receipt', 'url': '/api/task-artifacts/receipt'}
        receipt = dict(state='completed', success=True, evidence_status='execution_observed',
            exact_code_execution_verified=False, artifacts=artifacts,
            receipt_artifact=receipt_artifact, results=['e' * 65536], commands=['python code.py'],
            dispatch_attempted=True, requires_continuation=False, execution_id='exec1', error=None)
        original = deepcopy(receipt)
        with patch.object(sandbox, 'execute', return_value=receipt):
            result = scope.execute('execute_python', {'code': 'print(42)'})
        self.assertEqual(receipt, original)
        self.assertEqual(result['evidence_status'], 'execution_observed')
        self.assertFalse(result['exact_code_execution_verified'])
        self.assertTrue(result['execution_excerpt_partial'])
        self.assertEqual(result['artifacts'], artifacts)
        self.assertEqual(result['receipt_artifact'], receipt_artifact)
        wire = self.agent_result('execute_python', result)
        self.assertLess(len(wire), bridge.TASK_RESULT_MAX_CHARS)
        self.assertEqual(json.loads(wire), result)

    def test_provider_tool_loop_preserves_complete_task_json(self):
        ev = providers.Evaluation(STAGE);ev.save = lambda record: None
        result = {'state': 'completed', 'success': True, 'execution_excerpt': 'x' * 18000,
                  'artifacts': [{'id': 'output', 'url': '/api/task-artifacts/output'}],
                  'receipt_artifact': {'id': 'receipt', 'url': '/api/task-artifacts/receipt'}}
        bodies = []
        class HTTP:
            status_code = 200
            def __init__(self, delta, finish):self.delta = delta;self.finish = finish
            def close(self):pass
            def iter_lines(self, **kwargs):
                yield ('data: ' + json.dumps({'model': providers.MODELS['mimo']['model'],
                    'choices': [{'delta': self.delta, 'finish_reason': self.finish}],
                    'usage': {'prompt_tokens': 100, 'completion_tokens': 10, 'total_tokens': 110}})).encode()
                yield b'data: [DONE]'
        def post(*args, **kwargs):
            bodies.append(deepcopy(kwargs['json']))
            if len(bodies) == 1:
                return HTTP({'tool_calls': [{'index': 0, 'id': 'call1', 'function': {
                    'name': 'execute_python', 'arguments': '{"code":"print(42)"}'}}]}, 'tool_calls')
            return HTTP({'content': 'done'}, 'stop')
        with patch.object(providers, 'adapter', return_value=SimpleNamespace(load_mimo=lambda: 'test-only')):
            list(ev.stream('mimo', [{'role': 'system', 'content': 'CORE'}],
                [{'function': {'name': 'execute_python'}}], lambda *args: result,
                memory_sha256='test', http_post=post))
        self.assertEqual(len(bodies), 2)
        self.assertEqual(json.loads(bodies[1]['messages'][-1]['content']), result)

    def test_werkzeug_real_handler_masks_only_ticket_path(self):
        ns = server_functions({'_TaskDownloadLogFilter', '_install_task_download_log_filter'},
                              dict(logging=logging, re=re))
        output = io.StringIO();handler = logging.StreamHandler(output)
        logger = logging.getLogger('werkzeug')
        original = logger.handlers[:], logger.filters[:], logger.level, logger.propagate, logger.disabled
        token = 'T' * 43;ticket = '/task-download/artifact-id/' + token
        record = logging.LogRecord('werkzeug', logging.INFO, 'test', 1, 'GET %s HTTP/1.1', (ticket,), None)
        try:
            logger.handlers = [handler];logger.filters = [];logger.setLevel(logging.INFO)
            logger.propagate = False;logger.disabled = False
            ns['_install_task_download_log_filter']();ns['_install_task_download_log_filter']()
            self.assertEqual(len(logger.filters), 1)
            logger.handle(record)
            self.assertNotIn(token, output.getvalue());self.assertNotIn(token, record.getMessage())
            self.assertEqual(record.args, ())
            self.assertIn('/task-download/artifact-id/[REDACTED]', output.getvalue())
            logger.warning('unrelated warning %s', token)
            self.assertIn('unrelated warning ' + token, output.getvalue())
            # An unrelated security logger/handler is not changed or suppressed.
            other = logging.Logger('security-test', logging.INFO);other.addHandler(handler)
            other.warning('audit %s', ticket)
            self.assertIn('audit ' + ticket, output.getvalue())
        finally:
            logger.handlers, logger.filters, logger.level, logger.propagate, logger.disabled = original
            handler.close()


if __name__ == '__main__':unittest.main(verbosity=2)
