"""Haiku accounting in provider tokens, using the existing atomic spend guard.

No credentials or storage are opened here. The server injects its ledger, guard
and exact native-request counter. Missing usage remains an estimated hold;
measured cache creation/read/input are settled at their respective prices.
"""
import math
from copy import deepcopy


def _integer(value, name):
    if type(value) is not int or value < 0:
        raise ValueError('Invalid provider ' + name)
    return value


def usage_amount(usage, rates):
    prompt = _integer(usage.get('prompt_tokens'), 'input')
    output = _integer(usage.get('completion_tokens'), 'output')
    details = usage.get('prompt_tokens_details') or {}
    read = _integer(details.get('cached_tokens', 0), 'cache read')
    write = _integer(details.get('cache_write_tokens', 0), 'cache write')
    if read + write > prompt:
        raise ValueError('Cache exceeds total input')
    if len(rates) != 4 or any(not math.isfinite(p) or p < 0 for p in rates):
        raise ValueError('Explicit input/read/output/write prices required')
    amount = ((prompt-read-write)*rates[0] + read*rates[1]
              + output*rates[2] + write*rates[3]) / 1_000_000
    return prompt, read, output, amount


class DeferredStartAccount:
    """For the legacy agent adapter only: its payload is not final yet.

    The Haiku send closure MUST call the real account.iniciar_chamada once,
    after the loop has set its final tool_choice, and before the provider.
    Usage/refusals still reach the same real account.
    """
    def __init__(self, account):
        self.account = account

    def iniciar_chamada(self, payload):
        pass

    def __getattr__(self, name):
        return getattr(self.account, name)


class NativeAccount:
    """The request ledger and reservation account for Haiku only.

    `usos` includes an estimated maximum output on an interrupted call so the
    next tool turn cannot reuse an uncertain token balance. Nothing is silently
    retried. Only a known pre-generation refusal can discard a reservation.
    """
    def __init__(self, *, motors, budget, guard, ledger, cfg, user, admin,
                 model, quota_key, plan, prefix_tokens, count_request):
        self.motors, self.budget, self.guard, self.ledger = motors, budget, guard, ledger
        self.cfg, self.user, self.admin, self.model = cfg, user, admin, model
        self.quota_key, self.plan = quota_key, plan
        self.prefix_tokens = prefix_tokens
        self.counter = count_request
        self.usos, self.calls = [], []
        self.pending = None
        self.closed = False
        self._persisted = 0

    def iniciar_chamada(self, payload):
        if self.closed:
            raise ValueError('Request account is closed')
        if self.pending is not None:
            self._finish_pending()
            raise self.budget.BudgetError('A chamada anterior não informou uso final; nova chamada bloqueada.', 'razao')
        self.guard.check(self.user, self.quota_key)
        count = _integer(self.counter(payload), 'count')
        output = _integer(payload.get('max_completion_tokens'), 'output limit')
        if count <= 0 or output <= 0 or output > 4096:
            raise self.budget.WindowError('Invalid Haiku request size')
        if count + output + 1024 > self.cfg.janela:
            raise self.budget.WindowError()
        rates = self.cfg.precos(self.model)
        usage_amount({'prompt_tokens': count, 'completion_tokens': output}, rates)
        reserved_input = math.ceil(count * self.budget.RESERVATION_MARGIN)
        cap = (reserved_input*max(rates[0], rates[1], rates[3]) + output*rates[2]) / 1_000_000
        limit = self.cfg.cota_operador_usd if self.admin else self.cfg.cota_usuario_usd
        if self.admin and getattr(self.cfg, 'somente_limite_global', False):
            limit = self.cfg.cota_global_usd
        key = self.guard.reserve(self.user, self.model, cap, limit,
            self.cfg.cota_global_usd, quota_key=self.quota_key,
            group='haiku_public' if hasattr(self.cfg,'haiku_public_group_limit') else self.plan,
            group_limit=getattr(self.cfg,'haiku_public_group_limit',
                self.cfg.cota_global_gratuito_usd if self.plan == self.motors.GRATUITO else None))
        self.pending = dict(key=key, input=count, output=output, rates=rates, cap=cap)

    def descartar_ultima_chamada(self):
        if self.pending is not None:
            self.guard.settle(self.pending['key'], 0)
            self.pending = None

    def uso(self, usage):
        if self.pending is None:
            return
        # Validate the whole usage before changing either the hold or ledger.
        try:
            values = usage_amount(usage, self.pending['rates'])
        except (ValueError, TypeError, KeyError) as exc:
            raise self.budget.BudgetError('Uso inválido; reserva mantida.') from exc
        self.guard.settle(self.pending['key'], values[3])
        saved = deepcopy(usage)
        self.usos.append(saved)
        self.calls.append((saved, values, False))
        self.pending = None

    def texto(self, text):
        # Visible characters cannot account for undisclosed output. On missing
        # final usage retain the output reservation, never assume zero cost.
        pass

    def _finish_pending(self):
        if self.pending is None:
            return
        call = self.pending
        self.guard.settle(call['key'])  # estimated_upper_bound, not a provider bill
        saved = {'prompt_tokens': call['input'], 'completion_tokens': call['output'],
                 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0}}
        self.usos.append(saved)
        self.calls.append((saved, (call['input'], 0, call['output'], call['cap']), True))
        self.pending = None

    def fechar(self):
        if self.closed:
            return
        self._finish_pending()
        for usage, (prompt, read, output, amount), estimated in self.calls[self._persisted:]:
            self.ledger.registrar(self.user, self.model, prompt, read, output, amount,
                estimado=estimated, chave_cota=self.quota_key, plano=self.plan,
                tokens=self.motors.tokens_contados(usage, self.prefix_tokens))
            self._persisted += 1
        self.closed = True
