"""Explicit model capabilities and measured context budgets for IALD.

Prepared integration module; no network, credentials, or account mutations.
Token arguments are provider counts, never o200k estimates.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    model: str
    window: int
    max_output: int
    memory_target: int | None
    internal_only: bool
    input_usd_per_million: float
    output_usd_per_million: float
    default_output: int = 4096


SONNET = Profile('claude-sonnet-5-5', 1000000, 128000, None, True, 2.0, 10.0)
# Legacy certificate remains readable for other providers; never a 5.5 token count.
LEGACY_HAIKU = Profile('claude-haiku-4-5-20251001', 200000, 64000, 180000, False, 1.0, 5.0)
# Rates for >100k prompts: the deployed scientific memory is above that tier.
HAIKU = Profile('claude-haiku-5-5', 1000000, 128000, 180000, False, 0.50, 2.50, 16384)


def profile_for(model):
    if model in (SONNET.model, 'claude-sonnet-5'):
        return SONNET
    if model == HAIKU.model:
        return HAIKU
    if model in (LEGACY_HAIKU.model, 'claude-haiku-4-5'):
        return LEGACY_HAIKU
    raise ValueError('Unverified Claude model: explicit capabilities required')


def reasoning_parameters(model, max_output, thinking_budget=0, *, effort=None):
    """Use the explicit model capability, not a family-name heuristic."""
    profile = profile_for(model)
    if type(max_output) is not int or not 1 <= max_output <= profile.max_output:
        raise ValueError('Invalid output budget')
    if profile in (SONNET, HAIKU):
        if thinking_budget:
            raise ValueError('Manual thinking budget is unsupported by this model')
        effort = effort or ('medium' if profile is HAIKU else 'high')
        if effort not in ('low', 'medium', 'high'):
            raise ValueError('Unreviewed effort')
        return {'thinking': {'type': 'adaptive'}, 'output_config': {'effort': effort}}
    if thinking_budget == 0:
        return {'thinking': {'type': 'disabled'}}
    if type(thinking_budget) is not int or not 1024 <= thinking_budget < max_output:
        raise ValueError('Haiku thinking budget must fit inside output budget')
    return {'thinking': {'type': 'enabled', 'budget_tokens': thinking_budget}}


def context_budget(model, *, counted_model, permanent_tokens,
                   request_input_tokens, reserved_output_tokens, margin_tokens=1024):
    """Require exact whole-request counts; the permanent prefix is already included.

    Recount after every tool result. Overflow returns a visible refusal; this
    function never truncates the kernel, retrieved evidence or conversation.
    """
    profile = profile_for(model)
    if profile_for(counted_model) is not profile:
        raise ValueError('Token measurement belongs to another model')
    values = (permanent_tokens, request_input_tokens, reserved_output_tokens, margin_tokens)
    if any(type(n) is not int or n < 0 for n in values):
        raise ValueError('Missing or invalid provider token measurement')
    if permanent_tokens > request_input_tokens:
        raise ValueError('Whole request must include permanent memory')
    if not 1 <= reserved_output_tokens <= profile.max_output:
        raise ValueError('Invalid reserved output')
    remaining = profile.window - request_input_tokens - reserved_output_tokens - margin_tokens
    memory_target_met = profile.memory_target is None or permanent_tokens >= profile.memory_target
    ready = remaining >= 0 and memory_target_met
    action = ('load_required_memory_then_recount' if not memory_target_met else
              'send' if ready else 'rebuild_explicitly_then_recount')
    return {
        'model': profile.model,
        'memory_target': profile.memory_target,
        'permanent_tokens': permanent_tokens,
        'request_input_tokens': request_input_tokens,
        'reserved_output_tokens': reserved_output_tokens,
        'margin_tokens': margin_tokens,
        'remaining_tokens': remaining,
        'fits': remaining >= 0,
        'memory_target_met': memory_target_met,
        'ready': ready,
        'action': action,
    }
