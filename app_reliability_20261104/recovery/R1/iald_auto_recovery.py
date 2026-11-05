"""Narrow AUTO recovery: an initial, explicit OpenAI HTTP refusal only.

No credentials, disk, API, environment or scientific contract access. The host
must pass this object only from its authenticated public AUTO route. A HTTP200
seals the attempt even if no tokens have arrived. Exceptions/text/SSE never
constitute proof that a request was refused before execution.
"""
from copy import deepcopy
import json
import threading
import time


class DefinitiveRefusal(Exception):
    def __init__(self, status, code):
        self.status, self.code = status, code
        self.settled = False
        super().__init__('Initial provider request definitively refused')


def refusal_code(response):
    status = response.status_code
    allowed = {
        401: {'invalid_api_key', 'expired_secret_key'},
        403: {'invalid_api_key', 'expired_secret_key', 'model_access_denied'},
        404: {'model_not_found'},
        429: {'insufficient_quota', 'billing_hard_limit_reached'},
    }
    if type(status) is not int or status not in allowed:
        return None
    # Read through the existing activity Response: custody precedes recovery.
    # Missing/failed custody propagates; no recovery on read/decode failure.
    raw = response.content
    if not isinstance(raw, bytes) or len(raw) > 16384:
        return None
    try:
        body = json.loads(raw)
    except (ValueError, UnicodeError):
        return None
    if not isinstance(body, dict) or set(body) != {'error'}:
        return None
    error = body['error']
    if not isinstance(error, dict) or set(error) - {'code', 'type', 'param', 'message'}:
        return None
    code = error.get('code')
    if isinstance(code, str) and code in allowed[status]:
        return code
    return None


class Circuit:
    """Process-local, bounded TTL; configuration replacement invalidates it.

    Opaque config identity, not a key fingerprint. Manual paths never consult it.
    No persisted health or credential state. A repaired key loaded into the same
    object becomes eligible after at most ttl seconds.
    """
    def __init__(self, ttl=300, clock=time.monotonic):
        self.ttl, self.clock = ttl, clock
        self.lock = threading.Lock()
        self.generation, self.until = None, 0

    def block(self, generation):
        with self.lock:
            self.generation, self.until = generation, self.clock() + self.ttl

    def excludes(self, generation):
        with self.lock:
            return {'openai'} if self.generation is generation and self.clock() < self.until else set()


CIRCUIT = Circuit()


class Attempt:
    def __init__(self):
        self.calls = 0
        self.refusal = None

    def before_send(self):
        self.calls += 1

    def inspect(self, response):
        # All later calls (including reasoning-effort/429 retries/tool rounds)
        # are excluded. A successful initial header seals this attempt.
        if self.calls != 1:
            return
        code = refusal_code(response)
        if code:
            self.refusal = DefinitiveRefusal(response.status_code, code)
            raise self.refusal


def metadata_only(chunk):
    """Only complete, host metadata frames/comments may precede recovery."""
    if isinstance(chunk, bytes):
        try:
            chunk = chunk.decode('utf-8')
        except UnicodeError:
            return False
    if not isinstance(chunk, str) or not chunk.endswith('\n\n'):
        return False
    for line in chunk.splitlines():
        if not line or line.startswith(':'):
            continue
        if not line.startswith('data:'):
            return False
        try:
            value = json.loads(line[5:].strip())
        except ValueError:
            return False
        if (not isinstance(value, dict) or not value
                or set(value) - {'iald_modelo', 'iald_status'}):
            return False
        status = value.get('iald_status')
        if status is not None and (not isinstance(status, dict)
                or status.get('fase') != 'pensando' or 'tool' in status):
            return False
    return True


def unavailable():
    # Operational notice only: never fabricate assistant content from an error.
    yield 'data: ' + json.dumps({'iald_aviso': {'tipo': 'falha_motor',
        'texto': 'Não foi possível concluir com outro modelo autorizado. O pedido foi preservado.'}}, ensure_ascii=False) + '\n\n'
    yield 'data: [DONE]\n\n'


class Recovery:
    def __init__(self, request, generation, circuit=CIRCUIT):
        self.request = deepcopy(request)
        self.generation, self.circuit = generation, circuit
        self.excluded = set(circuit.excludes(generation))
        self.attempt = Attempt()
        self.reselected = False
        self.scope = None
        self.scope_base = None
        self.science = None

    def check_science(self, receipt):
        binding = (receipt['control_binding'], receipt['memory'])
        if self.science is not None and self.science != binding:
            raise ValueError('Scientific source changed during recovery')
        self.science = deepcopy(binding)

    def bind_scope(self, scope, receipt, router):
        # Same scope/control/job/wallet; restore the unbound capability set so
        # the new JEV plan is checked afresh instead of inheriting the old plan.
        if self.scope_base is None:
            self.scope_base = (deepcopy(scope.tools), getattr(scope, 'instructions', ''), scope.execute)
        tools, instructions, execute = self.scope_base
        scope.tools, scope.instructions, scope.execute = deepcopy(tools), instructions, execute
        router.bind_scope(scope, receipt)
        self.scope = scope

    def wrap(self, response, reselect):
        original = response.response

        def flow():
            blocked = False
            replacement = None
            try:
                try:
                    for chunk in original:
                        blocked = blocked or not metadata_only(chunk)
                        yield chunk
                    return
                except DefinitiveRefusal as exc:
                    if (exc is not self.attempt.refusal or not exc.settled
                            or blocked or self.reselected):
                        yield from unavailable()
                        return
                    # Original generators have unwound/settled before this catch.
                    self.circuit.block(self.generation)
                    self.excluded.add('openai')
                    self.reselected = True
                    yield 'data: ' + json.dumps({'iald_status': {'fase': 'pensando',
                        'rotulo': 'selecionando outro modelo autorizado'}}, ensure_ascii=False) + '\n\n'
                try:
                    replacement = reselect()
                    if (getattr(replacement, 'status_code', None) != 200
                            or getattr(replacement, 'mimetype', None) != 'text/event-stream'):
                        yield from unavailable()
                        return
                    yield from replacement.response
                except Exception:
                    # No third selection, no raw exception in output.
                    yield from unavailable()
            finally:
                close = getattr(original, 'close', None)
                if close:
                    close()
                if replacement is not None:
                    replacement.close()

        response.response = flow()
        return response
