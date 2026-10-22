"""Public MiMo reservations; no transport, configuration loading or operator policy.

The route must inject daily/group from CLAUDE_ROUTES.public_budget() and total
from CLAUDE_ROUTES.base.cota_global_usd. Do not instantiate for Luiz. This uses
those limit VALUES in a separate database: it does not combine Haiku spending
with MiMo spending. One instance belongs to one request, across its tool rounds.

Call before() immediately before each dispatch, settle() once with validated
usage_cost output, and close() in the transport finally block. Never dispatch
after a BudgetError. Missing usage consumes the full hold, not an estimate of
visible text. No method sends, retries, reads credentials or changes settings.
"""
import json
import math
from pathlib import Path
import re
import threading

from iald_app_providers import MODELS
from iald_orcamento import BudgetError, SpendingGuard


def _positive(value):
    if type(value) not in (int, float):
        raise BudgetError('Limites/preços inválidos; envio bloqueado.')
    try:
        result = float(value)
    except (OverflowError, ValueError):
        raise BudgetError('Limites/preços inválidos; envio bloqueado.') from None
    if not math.isfinite(result) or result <= 0:
        raise BudgetError('Limites/preços inválidos; envio bloqueado.')
    return result


class PublicAccount:
    """Request-local cursor; SpendingGuard serializes shared SQLite reservations."""

    def __init__(self, root, account_key_hash, daily, group, total):
        if not isinstance(account_key_hash, str) or not re.fullmatch(r'[0-9a-f]{64}', account_key_hash):
            raise BudgetError('Identificador de cota inválido; envio bloqueado.')
        self.daily, self.group, self.total = map(_positive, (daily, group, total))
        if not self.daily <= self.group <= self.total:
            raise BudgetError('Limites de cota inconsistentes; envio bloqueado.')
        self.account_key_hash = account_key_hash
        self.pending = None
        self.closed = False
        self._lock = threading.RLock()
        folder = Path(root) / '.iald_runtime' / 'app_evaluation'
        folder.mkdir(parents=True, exist_ok=True)
        self.guard = SpendingGuard(folder / 'public_spend.sqlite3')

    def before(self, provider, body, input_bound):
        """Reserve uncached UTF-8 input bound plus the model's maximum output.

        The caller's bound must cover the complete final JSON, including tools
        and previous reasoning/results. No tokenizer/API or CPT conversion.
        Return the reservation ID only after SQLite has committed the hold.
        """
        with self._lock:
            if self.closed or self.pending is not None:
                raise BudgetError('Conta encerrada ou chamada anterior sem uso final; envio bloqueado.')
            if provider not in ('mimo','deepseek') or not isinstance(body, dict):
                raise BudgetError('Reserva pública indisponível para este provedor.')
            spec = MODELS[provider]
            maximum = spec.get('output')
            output_field = 'max_tokens' if provider == 'deepseek' else 'max_completion_tokens'
            other_field = 'max_completion_tokens' if provider == 'deepseek' else 'max_tokens'
            output = body.get(output_field)
            if (body.get('model') != spec.get('model')
                    or type(maximum) is not int or maximum <= 0
                    or type(output) is not int or not 0 < output <= maximum
                    or other_field in body
                    or type(body.get('n', 1)) is not int or body.get('n', 1) != 1):
                raise BudgetError('Modelo ou limite de saída inválido; envio bloqueado.')
            if type(input_bound) is not int or input_bound <= 0:
                raise BudgetError('Limite de entrada inválido; envio bloqueado.')
            try:
                size = len(json.dumps(body, ensure_ascii=False, allow_nan=False).encode('utf-8'))
                rates = tuple(_positive(v) for v in spec['rates'])
                if len(rates) != 3 or input_bound < size:
                    raise ValueError()
                cap = (input_bound * max(rates[0], rates[1]) + maximum * rates[2]) / 1_000_000
                cap = _positive(cap)
            except (TypeError, ValueError, KeyError, OverflowError, UnicodeError) as exc:
                if isinstance(exc, BudgetError):
                    raise
                raise BudgetError('Entrada/preços não verificáveis; envio bloqueado.') from None
            key = self.guard.reserve(self.account_key_hash, spec['model'], cap,
                self.daily, self.total, quota_key=self.account_key_hash,
                group='mimo_public', group_limit=self.group)
            self.pending = dict(key=key, rates=rates)
            return key

    def discard_undispatched(self):
        """Only for a locally rejected request whose transport never started."""
        with self._lock:
            if self.pending is not None:
                self.guard.settle(self.pending['key'],amount=0)
                self.pending=None

    def settle(self, measured):
        """Persist actual usage; preserve the guard's over-reservation pause."""
        with self._lock:
            if self.closed or self.pending is None:
                raise BudgetError('Nenhuma reserva pendente para este consumo.')
            if not isinstance(measured, dict):
                raise BudgetError('Uso inválido; reserva mantida.')
            pin, out, cached = (measured.get(k) for k in
                                ('input_tokens', 'output_tokens', 'cached_tokens'))
            amount = measured.get('cost_estimate_usd')
            if (any(type(v) is not int or v < 0 for v in (pin, out, cached))
                    or cached > pin or type(amount) not in (int, float)):
                raise BudgetError('Uso inválido; reserva mantida.')
            try:
                a, c, o = self.pending['rates']
                expected = ((pin - cached) * a + cached * c + out * o) / 1_000_000
                valid = (math.isfinite(amount) and amount >= 0 and math.isfinite(expected)
                         and math.isclose(amount, expected, rel_tol=1e-12, abs_tol=1e-12))
            except (OverflowError, TypeError, ValueError):
                valid = False
            if not valid:
                raise BudgetError('Custo inválido ou inconsistente; reserva mantida.')
            self.guard.settle(self.pending['key'], amount=amount)
            # Clear only after successful persistence. A failed close/settle can
            # be invoked again locally; this never retries a provider request.
            self.pending = None
            self.guard.check(self.account_key_hash, self.account_key_hash)

    def close(self):
        """Idempotent close; retain the entire pending reservation on uncertainty."""
        with self._lock:
            if self.closed:
                return
            if self.pending is not None:
                self.guard.settle(self.pending['key'])
                self.pending = None
            self.closed = True
