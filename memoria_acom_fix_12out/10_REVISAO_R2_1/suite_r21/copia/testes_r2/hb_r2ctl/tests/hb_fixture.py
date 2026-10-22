# -*- coding: utf-8 -*-
"""Fixture comum das suites da frente HEARTBEAT (12/10/2026).

Carrega, por AST, o trecho REAL do heartbeat da copia modificada de iald_web_server.py (funcoes, classe
PsionHeartbeat e constantes HEARTBEAT_*/beta) num namespace com dependencias sinteticas:
  - FakeReq: substituto em processo de `requests` (post/get), com latencia e resposta configuraveis;
  - StubLlama: servidor de modelo FALSO = adaptador de transporte do proprio `requests` (sem socket, sem llama):
    o heartbeat chama req_lib.post(...) de verdade, o `requests` monta o pedido HTTP e o stub le os BYTES do
    corpo e responde no formato do llama.cpp (/health e /v1/chat/completions, com ou sem `timings`).
O psion e um arquivo SINTETICO no diretorio temporario (o real nunca e lido). O banco comum e um MemoryStore
sintetico no mesmo diretorio. Nenhum provedor, nenhuma rede: a guarda da auditoria roda byte a byte.
"""
import ast
import copy
import hashlib
import json
import math
import os
import secrets
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import requests
from requests.adapters import BaseAdapter

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
COPIA = FRONT / 'copia' / 'projetos_pyhton' / 'IALD'
sys.path[:0] = [str(HERE / 'app'), str(HERE / 'core')]
import iald_app_memory as memory            # a copia MODIFICADA (tests/app/iald_app_memory.py == copia/...)
from iald_memory import MemoryStore         # lib v1 congelada em tests/app/core (sha256 no MANIFESTO)

HEARTBEAT_SOURCE = COPIA / 'iald_web_server.py'
SCOPE = {'house': 'IALD_APP_SERVICES', 'principal': 'service.native-heartbeat'}
LEGACY_IDENT = 'app_service_' + memory.digest('native-heartbeat')
HEALTH_IDENT = 'app_service_' + memory.digest('native-heartbeat:health')


def r60_payload(ns, prompt, max_tokens=None):
    return {'model': 'qwen3', 'messages': [ns['HEARTBEAT_SYSTEM_MESSAGE'], prompt],
            'max_tokens': ns['HEARTBEAT_MAX_TOKENS'] if max_tokens is None else max_tokens,
            'temperature': 0.7, 'stream': False}


def wanted_assign(node):
    names = [t.id for t in node.targets if isinstance(t, ast.Name)]
    return bool(names) and len(names) == len(node.targets) and all(
        n.startswith('HEARTBEAT_') or n in ('_ALPHA_FINE', '_SQRT_E', '_BETA_TGL', '_BETA_RED', '_heartbeat_lock')
        for n in names)


def heartbeat_nodes(source):
    nodes = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef) and (node.name.startswith('_heartbeat_') or node.name in (
                'heartbeat_cycle', '_load_psion_state', '_save_psion_state', '_update_psion_from_heartbeat')):
            nodes.append(node)
        elif isinstance(node, ast.ClassDef) and node.name == 'PsionHeartbeat':
            nodes.append(node)
        elif isinstance(node, ast.Assign) and wanted_assign(node):
            nodes.append(node)
    return nodes


def load_heartbeat(root, extra=None, llama_url='http://offline.invalid', req_lib=None, quiet=True):
    """Exec the heartbeat segment of the modified copy with synthetic dependencies; returns the namespace."""
    source = HEARTBEAT_SOURCE.read_text(encoding='utf-8')
    nodes = heartbeat_nodes(source)
    root = Path(root)
    logs = root / 'logs'
    printed = []
    ns = dict(app_memory=memory, os=os, json=json, math=math, time=time, threading=threading, hashlib=hashlib,
              secrets=secrets, datetime=datetime, SERVE_DIR=str(root), LLAMA_URL=llama_url, req_lib=req_lib,
              _last_user_request_time=0.0, printed=printed)
    if quiet:
        ns['print'] = lambda *a, **kw: printed.append(' '.join(str(x) for x in a))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(HEARTBEAT_SOURCE), 'exec'), ns)
    ns.update(HEARTBEAT_STATE_FILE=str(root / 'psion_synthetic_state.json'), HEARTBEAT_LOG_DIR=str(logs),
              HEARTBEAT_TELEMETRY_FILE=str(logs / 'iald_heartbeat_telemetry.jsonl'),
              HEARTBEAT_HEALTH_FILE=str(logs / 'iald_heartbeat_health.json'))
    if extra:
        ns.update(extra)
    return ns


def seed_psion(ns, baseline=100.0, total_beats=10, cv=0.1):
    psion = ns['_load_psion_state']()
    psion['heartbeat'] = {'baseline_tok_s': baseline, 'stability_cv': cv, 'total_beats': total_beats,
                          'history': [], 'alerts': []}
    ns['_save_psion_state'](psion)
    return Path(ns['HEARTBEAT_STATE_FILE']).read_bytes()


def seed_health(ns, klass='ok', at=None):
    at = time.time() if at is None else at
    ns['_heartbeat_health_save']({'class': klass, 'since': at, 'last_memory_event_at': at,
                                  'last_memory_event_id': 'hb.seed', 'last_revision': 0, 'context_id': None})


def telemetry_lines(ns, suffix=''):
    path = Path(ns['HEARTBEAT_TELEMETRY_FILE'] + suffix)
    if not path.exists():
        return []
    out = []
    for raw in path.read_bytes().split(b'\n'):
        if not raw:
            continue
        line = json.loads(raw.decode('utf-8'))
        body = dict(line)
        sha = body.pop('line_sha256')
        canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(',', ':'), default=str)
        assert hashlib.sha256(canonical.encode('utf-8')).hexdigest() == sha, 'telemetry line digest mismatch'
        out.append(line)
    return out


def health_ledger():
    return MemoryStore(memory._SHARED_ROOT).get(HEALTH_IDENT, SCOPE)


def memory_events():
    """Events (beyond the anchor) in the heartbeat health ledger; 0 when the ledger does not exist."""
    try:
        return health_ledger()['revision']
    except ValueError:
        return 0


def llama_body(completion_tokens, predicted_n, predicted_ms, timings=True, text='synthetic response body'):
    value = {'id': 'fake', 'object': 'chat.completion',
             'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': text}, 'finish_reason': 'stop'}],
             'usage': {'prompt_tokens': 20, 'completion_tokens': completion_tokens, 'total_tokens': 20 + completion_tokens}}
    if timings:
        value['timings'] = {'prompt_n': 20, 'prompt_ms': 10.0, 'predicted_n': predicted_n, 'predicted_ms': predicted_ms}
    return value


class FakeResponse:
    def __init__(self, status, payload):
        self.status_code = status
        self._payload = payload
        self.headers = {'Content-Type': 'application/json'}

    def json(self):
        return self._payload


class FakeReq:
    """In-process fake of `requests`: records the exact JSON sent, sleeps `delay`, answers like llama.cpp."""
    def __init__(self, delay=0.0, status=200, timings=True, completion_tokens=64, predicted_n=64, predicted_ms=500.0,
                 raise_exc=None):
        self.delay, self.status, self.timings = delay, status, timings
        self.completion_tokens, self.predicted_n, self.predicted_ms = completion_tokens, predicted_n, predicted_ms
        self.raise_exc = raise_exc
        self.sent = []

    def post(self, url, json=None, timeout=None, **kw):
        self.sent.append(copy.deepcopy(json))
        if self.raise_exc is not None:
            raise self.raise_exc
        if self.delay:
            time.sleep(self.delay)
        return FakeResponse(self.status, llama_body(self.completion_tokens, self.predicted_n, self.predicted_ms, self.timings))

    def get(self, url, timeout=None, **kw):
        return FakeResponse(200, {'status': 'ok'})


class StubLlama(BaseAdapter):
    """Servidor de modelo FALSO: transporte HTTP do `requests` sem socket.

    `session()` devolve um requests.Session com este adaptador montado em http://; o heartbeat usa
    session.post/get como usaria o `requests` real. O stub recebe o PreparedRequest (metodo, URL,
    cabecalhos, corpo em bytes), registra o corpo decodificado e responde como o llama-server:
    GET /health -> {"status":"ok"}; POST /v1/chat/completions -> chat.completion com `usage` e,
    quando `timings=True`, o bloco `timings` do llama.cpp (predicted_n/predicted_ms).
    """
    def __init__(self, delay=0.0, status=200, timings=True, predicted_n=64, predicted_ms=400.0, completion_tokens=None,
                 health_status=200):
        super().__init__()
        self.delay, self.status, self.timings = delay, status, timings
        self.predicted_n, self.predicted_ms = predicted_n, predicted_ms
        self.completion_tokens = predicted_n if completion_tokens is None else completion_tokens
        self.health_status = health_status
        self.requests, self.lock = [], threading.Lock()
        self.url = 'http://stub-llama.invalid:8081'

    def session(self):
        s = requests.Session()
        s.trust_env = False
        s.mount('http://', self)
        s.mount('https://', self)
        return s

    def _response(self, request, status, value):
        r = requests.Response()
        r.status_code = status
        r.reason = 'OK' if status == 200 else 'ERROR'
        r._content = json.dumps(value).encode('utf-8')
        r.headers['Content-Type'] = 'application/json'
        r.encoding = 'utf-8'
        r.url = request.url
        r.request = request
        return r

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        body = request.body
        decoded = json.loads(body.decode('utf-8') if isinstance(body, bytes) else body) if body else None
        with self.lock:
            self.requests.append({'method': request.method, 'url': request.url, 'timeout': timeout,
                                  'content_type': request.headers.get('Content-Type'), 'body': decoded,
                                  'raw_bytes': len(body) if body else 0})
        if request.method == 'GET' and request.url.endswith('/health'):
            return self._response(request, self.health_status, {'status': 'ok'} if self.health_status == 200 else {'status': 'loading model'})
        if request.method == 'POST' and request.url.endswith('/v1/chat/completions'):
            if self.delay:
                time.sleep(self.delay)
            if self.status != 200:
                return self._response(request, self.status, {'error': 'stub failure'})
            return self._response(request, 200, llama_body(self.completion_tokens, self.predicted_n, self.predicted_ms,
                                                           self.timings, text='stub response body'))
        return self._response(request, 404, {'error': 'not found'})

    def close(self):
        pass
