"""Prepared per-call context guard; no credentials, network or production imports.

The integration supplies a trusted memory measurement and a count callback for
the final native Anthropic request. This module never estimates provider tokens.
"""
from dataclasses import dataclass
import hashlib
import json
from claude_profiles import context_budget, profile_for, HAIKU

def serialize(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)

@dataclass(frozen=True)
class MemoryMeasurement:
    model: str
    prefix_sha256: str
    permanent_tokens: int

class ContextRejected(ValueError):
    def __init__(self, decision):
        super().__init__(decision['action'])
        self.decision = decision

def guarded_call(request, *, authorized_model, memory, count_request, send_request, margin_tokens=1024):
    """Count the complete final request before every send, including tool turns.

    authorized_model is selected by server-side account policy, not client input.
    memory is loaded from a separately verified deployment measurement, not from
    an HTTP request. Callbacks receive independent copies; count failures stop
    the send. The returned count/decision contains no prompt or user text.
    """
    snapshot = serialize(request)
    wire = json.loads(snapshot)
    if wire.get('model') != authorized_model:
        raise ValueError('Request model differs from server authorization')
    profile = profile_for(authorized_model)
    if profile_for(memory.model) is not profile:
        raise ValueError('Memory measurement belongs to another model')
    blocks = wire.get('system')
    if not isinstance(blocks, list) or not blocks or blocks[0].get('type') != 'text':
        raise ValueError('Measured permanent memory must be the first system block')
    prefix = blocks[0].get('text')
    if not isinstance(prefix, str) or not prefix:
        raise ValueError('Permanent memory absent')
    if hashlib.sha256(prefix.encode('utf-8')).hexdigest() != memory.prefix_sha256:
        raise ValueError('Permanent memory differs from measured deployment')
    if profile is HAIKU:
        if (wire.get('thinking', {}).get('type') not in ('adaptive', 'disabled')
                or wire.get('output_config', {}).get('effort') not in ('low', 'medium', 'high')
                or any(k in wire for k in ('temperature', 'top_p', 'top_k'))):
            raise ValueError('Unreviewed Haiku 5.5 parameters')
        if not wire.get('messages') or wire['messages'][-1].get('role') != 'user':
            raise ValueError('Assistant prefill unsupported')
    counted_copy = json.loads(snapshot)
    measured = count_request(counted_copy)
    if serialize(counted_copy) != snapshot:
        raise ValueError('Counter mutated the measured request')
    if type(measured) is not int or measured <= 0:
        raise ValueError('Provider token count unavailable')
    decision = context_budget(authorized_model, counted_model=memory.model,
                              permanent_tokens=memory.permanent_tokens,
                              request_input_tokens=measured,
                              reserved_output_tokens=wire.get('max_tokens'),
                              margin_tokens=margin_tokens)
    if not decision['ready']:
        raise ContextRejected(decision)
    # Do not send the caller's mutable object or the counter's mutable copy.
    return send_request(json.loads(snapshot)), decision
