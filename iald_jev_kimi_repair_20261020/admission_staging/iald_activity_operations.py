"""Server-owned activity boundaries. No credentials, provider selection or retries."""
from contextlib import contextmanager
from contextvars import ContextVar
import base64
import copy
import hashlib
import json
import threading

from iald_memory.activity import ActivityRuntime

_PARENT = ContextVar('iald_activity_parent_operation', default=None)


class Lifecycle:
    def __init__(self, binding, *, origin, origin_ref=None):
        self.binding = binding
        self.lock = threading.RLock()
        self.counts = {}
        self.runtime = ActivityRuntime(binding.store, binding.context_id, binding.scope,
            {'id': 'app.execution.' + binding.request_id, 'kind': 'agent'})
        result = self.runtime.begin(binding.request_id, binding.current_input,
            origin=origin, origin_ref=origin_ref)
        if result['replayed']:
            raise ValueError('Existing activity requires recovery; dispatch is not replayed')
        self.ticket = result['ticket']
        self.response = Operation(self, 'response', parent=None)

    def start(self, label, *, key=None):
        # A new HTTP request cannot resume this object. Its durable request ID must
        # be recovered instead. Every ordinal/key is recorded BEFORE any effect.
        with self.lock:
            count = self.counts.get(label, 0) + 1
            self.counts[label] = count
            stable = str(key) if key is not None else str(count)
            opid = 'op_' + hashlib.sha256((label + ':' + stable).encode()).hexdigest()
            parent = _PARENT.get() or 'response'
            self.binding.checkpoint('operation.' + opid, {
                'protocol': 'iald-app-operation/v1', 'context_id': self.binding.context_id,
                'scope': self.binding.scope, 'request_id': self.binding.request_id,
                'operation_id': opid, 'parent_operation': parent, 'label': label,
                'server_key': stable})
            return Operation(self, opid, parent=parent)


class Operation:
    def __init__(self, lifecycle, operation_id, *, parent):
        self.lifecycle, self.id, self.parent = lifecycle, operation_id, parent
        self.done = False
        with lifecycle.lock:
            receipt = lifecycle.runtime.preflight(lifecycle.ticket, operation_id, refresh=True)
            lifecycle.ticket = receipt['ticket']

    def complete(self, value, *, terminal=False):
        with self.lifecycle.lock:
            try:
                result = self.lifecycle.runtime.complete(self.lifecycle.ticket, self.id,
                    value, terminal=terminal, refresh=True)
            except Exception:
                # Custody may have committed before a freshness/lease error.
                # Preserve that original error; never relabel a returned op uncertain.
                self._has_custody()
                raise
            self.done = True
            self.lifecycle.ticket = result.get('ticket') or self.lifecycle.runtime.recover(self.lifecycle.binding.request_id)['ticket']
            return result

    def _has_custody(self):
        runtime = self.lifecycle.runtime
        snapshot = runtime._get()
        request_id = self.lifecycle.binding.request_id
        handle_id = runtime._operation(request_id, self.id)
        handle = next((h for h in snapshot['p']['handles'] if h['id'] == handle_id), None)
        if not handle or handle.get('status') != 'completed':
            return False
        record = runtime._record(snapshot, handle.get('result_record_id'))
        result = runtime._data(record, 'result')  # Verify bytes/pin before recognizing custody.
        if result['request_id'] != request_id or result['operation_id'] != self.id:
            raise ValueError('Custody operation identity mismatch')
        self.done = True
        return True

    def uncertain(self, reason='Execution did not return a complete result; never replay automatically'):
        with self.lifecycle.lock:
            if not self.done and not self._has_custody():
                return self.lifecycle.runtime.mark_uncertain(self.lifecycle.ticket, self.id, reason)


def start(binding, label, *, key=None):
    lifecycle = getattr(binding, '_lifecycle', None)
    return lifecycle.start(label, key=key) if lifecycle else None


@contextmanager
def operation(binding, label, *, key=None):
    op = start(binding, label, key=key)
    token = _PARENT.set(op.id if op else None)
    try:
        yield op
    finally:
        _PARENT.reset(token)
        if op and not op.done:
            op.uncertain()


def call(binding, label, fn, *args, operation_key=None, **kwargs):
    with operation(binding, label, key=operation_key) as op:
        value = fn(*args, **kwargs)
        if op:
            op.complete(value)
        return value


class Response:
    """Requests reader with custody of content/chunks or reconstructed lines.

    A closed partial stream stays uncertain. SSE DONE is an execution boundary,
    never semantic acceptance. This wrapper does not retry or change billing.
    """
    def __init__(self, response, op, expect_sse=False):
        self.response, self.op = response, op
        self.expect_sse = expect_sse or 'text/event-stream' in response.headers.get('Content-Type', '')
        self.parts = []

    def __getattr__(self, name):
        return getattr(self.response, name)

    def _finish(self, result):
        if not self.op.done:
            self.op.complete({'http_status': self.response.status_code, 'response': result})

    def _custody_raw(self, raw, representation='requests content/iter_content bytes'):
        readable = raw.decode('utf-8', errors='replace')
        # Check visible text BEFORE encoding; base64 is custody, not a guard bypass.
        from iald_memory import guard
        guard.assert_clean_text(readable, 'app.transport.received_bytes')
        self.op.lifecycle.binding.checkpoint('partial.' + self.op.id,
            {'status': 'UNCERTAIN', 'received_text': readable,
             'raw_base64': base64.b64encode(raw).decode('ascii'), 'raw_encoding': 'base64',
             'raw_sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw),
             'representation': representation})
        self.op.uncertain()

    def _decode(self, raw, representation='requests content/iter_content bytes'):
        try:
            return raw.decode('utf-8')
        except UnicodeDecodeError:
            self._custody_raw(raw, representation)
            raise

    def json(self, **kwargs):
        # Capture raw text first, even when parsing fails or freshness rejects it.
        raw = self.response.content
        self._finish(self._decode(raw))
        return self.response.json(**kwargs)

    @property
    def content(self):
        raw = self.response.content
        self._finish(self._decode(raw))
        return raw

    @property
    def text(self):
        self.content
        return self.response.text

    def _iterate(self, source, *, lines):
        raw_parts = []
        pending = b''
        sse = self.expect_sse
        representation = ('requests.iter_lines values joined with LF; original delimiters unavailable'
            if lines else 'requests content/iter_content bytes')
        def received():
            separator = b'\n' if lines else b''
            return self._decode(separator.join(raw_parts), representation)
        def terminal(line):
            if not line.startswith(b'data:'):
                return False
            payload = line[5:].strip()
            if payload == b'[DONE]':
                return True
            try:
                value = json.loads(payload)
            except (ValueError, UnicodeDecodeError):
                return False
            return isinstance(value, dict) and value.get('type') == 'message_stop'
        try:
            for part in source:
                raw = part if isinstance(part, bytes) else str(part).encode('utf-8')
                raw_parts.append(raw)
                pending += raw + (b'\n' if lines else b'')
                complete_lines = pending.split(b'\n')
                pending = complete_lines.pop()
                for line in complete_lines:
                    line = line.rstrip(b'\r')
                    sse = sse or line.startswith((b'data:', b'event:'))
                    if terminal(line):
                        self._finish({'stream': received(), 'representation': representation})
                yield part
            sse = sse or pending.startswith((b'data:', b'event:'))
            if terminal(pending.rstrip(b'\r')):
                self._finish({'stream': received(), 'representation': representation})
            text = received()
            if sse and not self.op.done:
                raise ValueError('SSE ended without a terminal control frame; result remains uncertain')
            self._finish({'stream': text, 'representation': representation})
        finally:
            if not self.op.done:
                partial = (b'\n' if lines else b'').join(raw_parts)
                self._custody_raw(partial, representation)

    def iter_lines(self, *args, **kwargs):
        return self._iterate(self.response.iter_lines(*args, **kwargs), lines=True)

    def iter_content(self, *args, **kwargs):
        return self._iterate(self.response.iter_content(*args, **kwargs), lines=False)

    def close(self):
        try:
            return self.response.close()
        finally:
            if not self.op.done:
                self.op.uncertain()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def http_call(binding, label, fn, *args, **kwargs):
    op = start(binding, label)
    try:
        result = fn(*args, **kwargs)
    except BaseException:
        if op: op.uncertain()
        raise
    return Response(result, op, expect_sse=bool(kwargs.get('stream'))) if op else result


def envelope(binding):
    """Trusted Python boundary only. No public route accepts this as credentials."""
    if binding is None or binding.activity is None:
        return None
    ticket = binding.activity.refresh(binding.ticket)
    return {'protocol': 'iald-app-worker/v1', 'context_id': binding.context_id,
        'scope': copy.deepcopy(binding.scope), 'request_id': binding.request_id,
        'parent_operation': _PARENT.get() or 'response', 'ticket': ticket}


def validate_envelope(binding, value):
    if not isinstance(value, dict) or binding is None or binding.activity is None:
        raise PermissionError('Missing authenticated server worker binding')
    expected = (binding.context_id, binding.scope, binding.request_id)
    actual = (value.get('context_id'), value.get('scope'), value.get('request_id'))
    if value.get('protocol') != 'iald-app-worker/v1' or actual != expected:
        raise PermissionError('Worker binding mismatch')
    if value.get('parent_operation') != (_PARENT.get() or 'response'):
        raise PermissionError('Worker parent operation mismatch')
    binding.activity.refresh(value['ticket'])
    return True
