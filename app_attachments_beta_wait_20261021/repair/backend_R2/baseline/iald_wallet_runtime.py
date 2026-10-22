"""Task-scoped monthly accounting. No credentials, transport or Flask imports.

Only the authenticated server creates a Task. Context is captured explicitly
for worker threads and for each generator step; a caller's JSON cannot grant
overdraft. Provider guards still enforce their global ceilings.
"""
from contextvars import ContextVar, copy_context
from contextlib import contextmanager
from pathlib import Path
import hashlib
import math
import threading
import uuid

from iald_monthly_wallet import Wallet, TERMINAL_STATUSES

_CURRENT = ContextVar('iald_monthly_task', default=None)


def current():
    return _CURRENT.get()


def enabled():
    return current() is not None


@contextmanager
def bind(task):
    token = _CURRENT.set(task)
    try:
        yield task
    finally:
        _CURRENT.reset(token)


class Task:
    def __init__(self, wallet, owner, task_id, user):
        self.wallet, self.owner, self.id, self.user = wallet, owner, task_id, user
        self.lock = threading.RLock()
        self.refs = 1
        self.terminal = 'completed'
        self.closed = False
        # None owns the request reference; retained workers have distinct tokens.
        # A repeated request cleanup cannot consume a live worker's reference.
        self._references = {None: True}
        self._final_status = None

    def retain(self):
        with self.lock:
            if self.closed or self.refs < 1:
                raise ValueError('Task already closed')
            self.refs += 1
            reference = object()
            self._references[reference] = True
            return reference

    def release(self, status='completed', *, reference=None):
        with self.lock:
            if status not in TERMINAL_STATUSES:
                raise ValueError('Invalid terminal status')
            if self.closed:
                return True
            if reference not in self._references:
                raise ValueError('Unknown task reference')
            if self._references[reference]:
                self._references[reference] = False
                self.refs = sum(self._references.values())
                if status == 'failed' or (status != 'completed' and self.terminal == 'completed'):
                    self.terminal = status
            return self.finalize()

    def finalize(self):
        """Retry durable finalization without releasing any request/worker."""
        with self.lock:
            if self.closed:
                return True
            if self.refs == 0:
                if self._final_status is None:
                    self._final_status = self.terminal
                # Pending usage makes this fail visibly; never discard it to
                # reopen a user's budget. Keep the same status even if a prior
                # finish committed before its caller observed an I/O failure.
                self.wallet.finish_task(self.owner, self.id, self._final_status)
                self.closed = True
            return self.closed

    def begin_call(self, event, cap, provider, model, **metadata):
        with self.lock:
            if self.closed or self.refs < 1:
                raise ValueError('Closed task cannot dispatch')
        result = self.wallet.begin_call(self.owner, self.id, event, cap, provider, model, **metadata)
        if not result.get("may_dispatch"):
            raise ValueError("Call already recorded; do not dispatch again")
        return result

    def settle(self, event, amount=None, status='estimated'):
        return self.wallet.settle_call(self.owner, self.id, event, amount_usd=amount, status=status, evidence="provider-receipt:"+event)

    def routing_state(self):
        snap = self.wallet.snapshot(self.owner)
        return {k: snap[k] for k in ('balance_usd', 'available_usd', 'debt_usd', 'exempt', 'next_release')}


def threaded(target):
    """Return a worker that owns a task reference until all accounting ends."""
    context = copy_context()
    task = current()
    reference = None
    if task:
        reference = task.retain()
    state = 'ready'
    worker_lock = threading.Lock()
    def run():
        nonlocal state
        with worker_lock:
            if state != 'ready':
                raise ValueError('Worker already started or cancelled')
            state = 'running'
        status = 'failed'
        try:
            result = context.run(target)
            status = 'completed'
            return result
        finally:
            with worker_lock:
                state = 'done'
            if task:
                task.release(status, reference=reference)
    def failed_start():
        nonlocal state
        with worker_lock:
            if state == 'running':
                return  # A live worker still owns its reference.
            if state == 'done':
                retry_only = True
            else:
                state = 'cancelled'
                retry_only = False
        if task:
            if retry_only:
                task.finalize()
            else:
                task.release('failed', reference=reference)
    return run, failed_start


class Guard:
    """Keep the original global ledger; mirror each unique call to the wallet."""
    def __init__(self, original, task, provider):
        self.original, self.task, self.provider = original, task, provider
        self.events = {}

    def __getattr__(self, name):
        return getattr(self.original, name)

    def reserve(self, user, model, cap, user_limit, global_limit, **kwargs):
        # Monthly wallet replaces user/day and public-group caps, not the
        # independently configured provider-wide maximum or accounting checks.
        key = self.original.reserve(user, model, cap, global_limit, global_limit,
                                    quota_key=kwargs.get('quota_key'))
        event = hashlib.sha256((str(Path(self.original.path).resolve())+':'+key).encode()).hexdigest()
        try:
            with self.original._connect() as db:
                bound = db.execute('SELECT cap FROM calls WHERE id=?', (key,)).fetchone()[0]
            self.task.begin_call(event, bound, self.provider, model)
        except BaseException:
            self.original.settle(key, 0)  # Provider has not been called.
            raise
        self.events[key] = event
        return key

    def settle(self, key, amount=None, estimate=None):
        event = self.events.get(key)
        if event is None:
            raise ValueError('Reservation is outside this wallet task')
        self.original.settle(key, amount, estimate=estimate)
        with self.original._connect() as db:
            row = db.execute('SELECT actual,status FROM calls WHERE id=?', (key,)).fetchone()
        if row is None or row[0] is None:
            raise ValueError('Unsettled provider ledger')
        if row[1] != 'settled':
            self.task.settle(event)  # Missing usage consumes the registered bound.
        elif (getattr(self, 'estimated_components', False) or self.provider == 'openai') and row[0] > 0:
            self.task.settle(event, row[0], 'estimated_components')
        else:
            self.task.settle(event, row[0], 'measured')


def wrap_guard(original, provider):
    task = current()
    if original is None or not task or isinstance(original, Guard):
        return original
    return Guard(original, task, provider)


def permit(cfg, ledger, limiter, user, admin=False, plano=None, chave_cota=None, detalhado=False):
    """Legacy plan checks, replaced only inside an authenticated wallet task."""
    import iald_motores as motors
    if not enabled():
        return motors.verificar_permissao(cfg, ledger, limiter, user, admin,
            plano=plano, chave_cota=chave_cota, detalhado=detalhado)
    try:
        _, total = ledger.gasto_hoje(user)
        if total >= cfg.cota_global_usd:
            result = (False, motors.MSG_GLOBAL, 'global')
        elif not limiter.permitir(user):
            result = (False, motors.MSG_MINUTO, 'minuto')
        else:
            result = (True, '', '')
    except Exception:
        result = (False, motors.MSG_RAZAO_ILEGIVEL, 'razao')
    return result if detalhado else result[:2]


def provider_account(root, provider, total):
    """MiMo/DeepSeek use the existing cost-checked transport account."""
    if not enabled() or provider not in ('mimo', 'deepseek'):
        return None
    from iald_app_spend import PublicAccount
    return PublicAccount(root, current().owner, total, total, total)


def subscription_begin(model):
    """Kimi is a subscription in this stack; no marginal USD tariff is known.

    Record inclusion at zero incremental API cost, never fabricate a token
    price. The external receipt retains tokens; subscription fees stay outside
    this usage wallet. This is not a claim that the subscription is free.
    """
    task = current()
    if not task:
        return None
    event = uuid.uuid4().hex
    task.begin_call(event, 0, 'kimi', model, billing_basis='subscription_included_no_incremental_API_charge')
    return event


def subscription_end(event):
    if event:
        current().settle(event, 0, 'estimated')


def routing_begin(cap):
    if not enabled():
        return None
    event = uuid.uuid4().hex
    current().begin_call(event, cap, 'jev', 'jev-1.13.0')
    return event


def routing_end(event, usage=None):
    if not event:
        return
    count = usage.get('input_tokens') if isinstance(usage, dict) else None
    if type(count) is int and count >= 0:
        current().settle(event, count * 0.042 / 1_000_000, 'measured')
    else:
        current().settle(event)  # Recorded upper bound, never silent zero.


def sandbox_guard(guard):
    if isinstance(guard, Guard):
        guard.estimated_components = True
    return guard
