"""Scoped, recoverable holographic preparation for trusted native callers.

The existing algorithm remains the compressor. Auxiliary state is reconstructed
from a candidate in the same ACOM context; no singleton or second database exists.
The server authenticates Binding, not this module or its metadata. No providers.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import re
import uuid

import holographic_memory
from holographic_memory import HolographicMemory
from iald_memory import guard

PROTOCOL = 'iald-native-holographic/v1'
LABEL = 'native.holographic.v1'
FIELDS = ('_compress_count', '_total_tokens_saved', '_psionic_sentences_pruned',
          '_psionic_dedup_pruned', '_prefix_collapsed')


class NativeActivityError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


def _need(condition, reason):
    if not condition:
        raise NativeActivityError(reason)


class ScopedHolographicMemory(HolographicMemory):
    """Same angular/psionic formulas; stable full-text keys for new checkpoints."""
    @staticmethod
    def _content_hash(content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def snapshot_state(self):
        return {**{k: getattr(self, k) for k in FIELDS}, '_persistence': dict(self._persistence)}

    def restore_state(self, state):
        _need(isinstance(state, dict) and set(state) == set(FIELDS) | {'_persistence'}, 'invalid_holographic_state')
        _need(all(type(state[k]) is int and state[k] >= 0 for k in FIELDS), 'invalid_holographic_counters')
        persistence = state['_persistence']
        _need(isinstance(persistence, dict) and all(isinstance(k, str) and re.fullmatch('[0-9a-f]{64}', k)
              and type(v) is int and v >= 0 for k, v in persistence.items()), 'invalid_holographic_persistence')
        for key in FIELDS:
            setattr(self, key, state[key])
        self._persistence = dict(persistence)


def _algorithm():
    return hashlib.sha256(Path(holographic_memory.__file__).read_bytes()).hexdigest()


def _namespace(snapshot):
    return {'context_id': snapshot['context_id'], 'scope': snapshot['scope'],
            'anchor_sha256': snapshot['anchor_sha256']}


def _artifact(binding, value):
    raw = (canonical(value) + '\n').encode('utf-8')
    guard.assert_clean_text(raw.decode('utf-8'), 'native.holographic.artifact')
    _need(len(raw) <= 32 * 1024 * 1024, 'holographic_artifact_too_large')
    sha = hashlib.sha256(raw).hexdigest()
    folder = Path(binding.store.root) / 'native_holographic'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (sha + '.json')
    if not path.exists():
        temp = folder / ('.tmp_' + uuid.uuid4().hex)
        try:
            with temp.open('xb') as f:
                f.write(raw)
                f.flush()
                os.fsync(f.fileno())
            try:
                if os.name == 'nt':
                    os.rename(temp, path)
                else:
                    os.link(temp, path)
            except FileExistsError:
                pass
        finally:
            temp.unlink(missing_ok=True)
    _need(path.read_bytes() == raw, 'holographic_artifact_bytes_mismatch')
    return {'path': str(path.resolve()), 'sha256': sha}


def _read_checkpoint(binding, snapshot, record):
    if record.get('kind') != 'candidate' or record.get('statute') != 'DECLARADO':
        return None
    sources = record.get('sources', [])
    if not (len(sources) == 1 and sources[0].get('kind') == 'tool'
            and sources[0].get('ref', '').endswith(':checkpoint.' + LABEL)):
        return None
    value = json.loads(record['text'])
    _need(value['protocol'] == PROTOCOL and value['namespace'] == _namespace(snapshot),
          'holographic_checkpoint_scope_mismatch')
    pin = value['artifact']
    _need(isinstance(pin, dict) and isinstance(pin.get('sha256'), str)
          and re.fullmatch('[0-9a-f]{64}', pin['sha256']), 'invalid_holographic_pin')
    expected = (Path(binding.store.root) / 'native_holographic' / (pin['sha256'] + '.json')).resolve()
    _need(pin.get('path') == str(expected), 'holographic_checkpoint_path_mismatch')
    _, raw = guard.read_checked(expected, max_bytes=32 * 1024 * 1024, where='native.holographic.restore')
    _need(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'holographic_checkpoint_hash_mismatch')
    payload = json.loads(raw.decode('utf-8'))
    _need(payload['protocol'] == PROTOCOL and payload['namespace'] == _namespace(snapshot)
          and payload['input_sha256'] == value['input_sha256']
          and payload['invocation'] == value['invocation'], 'holographic_checkpoint_envelope_mismatch')
    _need(payload['algorithm_sha256'] == _algorithm(), 'holographic_algorithm_changed')
    _need(digest(payload['input_messages']) == payload['input_sha256']
          and digest(payload['output_messages']) == payload['output_sha256'], 'holographic_checkpoint_payload_mismatch')
    return payload


def prepare_messages(messages, *, binding, path, window, output_reserve=4096, compress=True):
    """Compress optional plain history, preserving sources and mandatory ACOM.

    project_messages must run AFTER this call, then the native template/tokenizer
    must count the final payload. A binding-less caller receives no compression or
    shared cache; the authenticated application gates remain the caller's duty.
    """
    _need(isinstance(messages, list) and all(isinstance(m, dict) for m in messages), 'invalid_native_history')
    result = deepcopy(messages)
    runtime = getattr(binding, 'activity', None) if binding is not None else None
    if runtime is None:
        return result, {'status': 'UNBOUND_NO_COMPRESSION_OR_SHARED_STATE'}
    _need(runtime.context_id == binding.context_id and runtime.scope == binding.scope
          and runtime.store is binding.store, 'native_binding_mismatch')
    ticket = binding.ticket
    runtime.refresh(ticket)  # Explicit local preparation; never grants dispatch.
    snapshot = binding.store.get(binding.context_id, binding.scope)
    _need(type(window) is int and window > 0 and type(output_reserve) is int
          and 0 < output_reserve < window, 'invalid_native_budget')
    # Tool/media/extra metadata are inseparable: keep the whole history intact.
    plain = all(set(m) == {'role', 'content'} and m['role'] in {'system', 'user', 'assistant'}
                and isinstance(m['content'], str) for m in messages)
    if not compress or not plain:
        return result, {'status': 'PRESERVED_STRUCTURED_OR_DISABLED', 'revision': snapshot['revision']}
    engine = ScopedHolographicMemory()
    # This is the configured budget, not a token measurement. Final native counter
    # verifies the actual server window. Never perform the legacy /props probe here.
    engine._janela_real = window
    engine.RESPONSE_BUDGET = output_reserve
    invocation = {'request_id': binding.request_id, 'path': path, 'window': window,
                  'output_reserve': output_reserve, 'input_sha256': digest(messages)}
    previous = None
    for record in reversed(snapshot['q']['records']):
        checkpoint = _read_checkpoint(binding, snapshot, record)
        if checkpoint is not None:
            if checkpoint['invocation'] == invocation:
                runtime.refresh(ticket)
                return deepcopy(checkpoint['output_messages']), {'status': 'REPLAYED_CHECKPOINT',
                    'record_id': record['id'], 'revision': snapshot['revision']}
            if previous is None:
                previous = (record['id'], checkpoint)
    if previous:
        engine.restore_state(previous[1]['state'])
    compressed = engine.compress_context(result)
    # Generated summaries are derived narrative, never new system instructions.
    original_systems = [m for m in result if m['role'] == 'system']
    for m in compressed:
        if m['role'] == 'system' and m not in original_systems:
            m['role'] = 'assistant'
            m['content'] = '[DECLARADO — resumo holográfico derivado; originais recuperáveis na ACOM]\n' + m['content']
    if compressed == result:
        runtime.refresh(ticket)
        return result, {'status': 'UNCHANGED', 'revision': snapshot['revision']}
    output_hashes = {digest(m) for m in compressed}
    payload = {'protocol': PROTOCOL, 'namespace': _namespace(snapshot), 'invocation': invocation,
        'algorithm_sha256': _algorithm(), 'key_scheme': 'sha256-full-utf8/v1',
        'source_receipt': snapshot['receipt'], 'parent_checkpoint_id': previous[0] if previous else None,
        'input_messages': result, 'input_sha256': digest(result),
        'output_messages': compressed, 'output_sha256': digest(compressed),
        'transformed_or_omitted_indices': [i for i,m in enumerate(result) if digest(m) not in output_hashes],
        'state': engine.snapshot_state(), 'budget_estimate': engine._ultimo_orcamento,
        'statute': 'DECLARADO', 'recovery': 'Current scoped ACOM record and pinned full artifact; no remote call.'}
    pin = _artifact(binding, payload)
    value = {'protocol': PROTOCOL, 'namespace': _namespace(snapshot), 'invocation': invocation,
        'input_sha256': payload['input_sha256'], 'source_revision': snapshot['revision'],
        'artifact': pin, 'statute': 'DECLARADO', 'meaning': 'Derived narrative/cache only; never a requirement or accepted fact.'}
    receipt = binding.checkpoint(LABEL, value)
    # Custody precedes refusal if human steering changed during compression.
    runtime.refresh(ticket)
    return compressed, {'status': 'CHECKPOINTED_CANDIDATE', 'receipt': receipt,
                        'artifact': pin, 'statute': 'DECLARADO'}
