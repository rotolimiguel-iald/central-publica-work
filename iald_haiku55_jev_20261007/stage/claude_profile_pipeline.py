"""Prepared boundary joining account policy, conversion and native token guard.

No client or network is created here. Production must supply its authenticated
policy, measured memory certificate, existing converter and transport callbacks.
"""
from copy import copy, deepcopy
from claude_account_policy import authorize_model
from claude_profiles import HAIKU, profile_for, reasoning_parameters
from claude_request_guard import guarded_call


def profile_call(*, requested_model, server_policy, cfg, payload, prefix,
                 memory, converter, count_request, send_request, state=None,
                 thinking_budget=0):
    authorized = authorize_model(requested_model, **server_policy)
    incoming = payload.get('model')
    if incoming is not None and profile_for(incoming).model != authorized:
        raise PermissionError('Payload model differs from authorized selection')
    selected_cfg = copy(cfg)
    selected_cfg.modelo = authorized
    selected_payload = deepcopy(payload)
    selected_payload['model'] = authorized
    wire = converter(selected_cfg, selected_payload, prefixo=prefix, estado=state)
    if profile_for(authorized) is HAIKU:
        # The existing adapter always emits Sonnet parameters. Adjust only Haiku;
        # preserve the configured Sonnet effort, streaming state and cache blocks.
        wire.pop('output_config', None)
        wire.update(reasoning_parameters(authorized, wire['max_tokens'], thinking_budget,
                                         effort=getattr(selected_cfg, 'esforco_claude', 'medium')))
    elif thinking_budget:
        raise ValueError('Explicit thinking budget is only configured for Haiku')
    return guarded_call(wire, authorized_model=authorized, memory=memory,
                        count_request=count_request, send_request=send_request)
