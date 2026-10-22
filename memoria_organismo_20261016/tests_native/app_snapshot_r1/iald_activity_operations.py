"""Server-owned activity boundaries. No credentials, provider selection or retries."""
from contextlib import contextmanager
from contextvars import ContextVar
import copy
import hashlib
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
            raise RuntimeError('Existing activity requires recovery; dispatch is not replayed')
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
            result = self.lifecycle.runtime.complete(self.lifecycle.ticket, self.id,
                value, terminal=terminal, refresh=True)
            self.lifecycle.ticket = result.get('ticket') or self.lifecycle.runtime.recover(self.lifecycle.binding.request_id)['ticket']
            self.done = True
            return result

    def uncertain(self, reason='Execution did not return a complete result; never replay automatically'):
        if not self.done:
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
    """Requests-compatible reader; full received bytes are custodied before use.

    A closed partial stream stays uncertain. SSE DONE is an execution boundary,
    never semantic acceptance. This wrapper does not retry or change billing.
    """
    def __init__(self, response, op):
        self.response, self.op = response, op
        self.parts = []

    def __getattr__(self, name):
        return getattr(self.response, name)

    def _finish(self, result):
        if not self.op.done:
            self.op.complete({'http_status': self.response.status_code, 'response': result})

    def json(self, **kwargs):
        # Capture raw text first, even when parsing fails or freshness rejects it.
        raw = self.response.content
        self._finish(raw.decode('utf-8'))
        return self.response.json(**kwargs)

    @property
    def content(self):
        raw = self.response.content
        self._finish(raw.decode('utf-8'))
        return raw

    @property
    def text(self):
        value = self.response.text
        self._finish(value)
        return value

    def _iterate(self, source):
        try:
            for part in source:
                text = part.decode('utf-8') if isinstance(part, bytes) else str(part)
                self.parts.append(text)
                # The consumer can break immediately on this frame. Custody
                # precedes yielding it, including adapters that buffer SSE.
                if 'data: [DONE]' in text:
                    self._finish({'stream': self.parts})
                yield part
            self._finish({'stream': self.parts})
        finally:
            if not self.op.done:
                self.op.uncertain()

    def iter_lines(self, *args, **kwargs):
        return self._iterate(self.response.iter_lines(*args, **kwargs))

    def iter_content(self, *args, **kwargs):
        return self._iterate(self.response.iter_content(*args, **kwargs))

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
    return Response(result, op) if op else result


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
