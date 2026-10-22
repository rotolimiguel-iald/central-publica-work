"""Transactional queue outbox for the common inscription/state/flow controller.

The queue remains the authority for dispatch. Memory is checked before dispatch;
post-return checkpoint failure cannot make a returned provider call retryable.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
import uuid

CORE_LIB = Path(r'C:\IALD\MEMORIA_IALD\lib')
COMMON_STATE = Path(r'C:\IALD\MEMORIA_IALD\state')
SCOPE = {'house': 'IALD', 'principal': 'operator'}
ACTOR = {'id': 'iald-queue', 'kind': 'system'}
SEPARATOR = '\n\nMEMORIA OPERACIONAL — INSCRICAO, ESTADO q E FLUXO p:\n'


def core():
    try:
        import iald_memory
    except ModuleNotFoundError as exc:
        if exc.name != 'iald_memory':
            raise
        sys.path.insert(0, str(CORE_LIB))
        import iald_memory
    return iald_memory


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def context_id(request_id):
    return 'queue_' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'IALD:operator:queue:' + request_id))


def init_db(db):
    db.execute('''CREATE TABLE IF NOT EXISTS memory_outbox (
      sequence INTEGER PRIMARY KEY, event_id TEXT UNIQUE NOT NULL,
      context_id TEXT NOT NULL, objective TEXT NOT NULL, constraints_json TEXT NOT NULL,
      changes_json TEXT NOT NULL, receipt_json TEXT)''')


def stage(db, reference, objective, constraints, event_id, *, phase, handle_id,
          next_action, result=None, source=None):
    """Called within the SAME transaction as the queue state mutation."""
    changes = {'flow': {'phase': phase, 'next_action': next_action,
                       'handles': [{'id': handle_id, 'phase': phase}]}}
    if result is not None:
        changes['candidates'] = [{'id': 'candidate_' + digest(event_id)[:40],
            'text': result, 'statute': 'DECLARADO',
            'source': {'kind': 'executor', 'ref': 'queue-event:' + event_id, **(source or {})}}]
    values = (reference, objective, encode(constraints or {}), encode(changes))
    prior = db.execute('SELECT * FROM memory_outbox WHERE event_id=?', (event_id,)).fetchone()
    if prior:
        if tuple(prior[k] for k in ('context_id','objective','constraints_json','changes_json')) != values:
            raise ValueError('Memory outbox event collision')
        return
    db.execute('INSERT INTO memory_outbox(event_id,context_id,objective,constraints_json,changes_json) VALUES(?,?,?,?,?)', (event_id, *values))


def store(runtime):
    return core().MemoryStore(runtime.memory_root)


def sync(runtime, reference):
    """Outbox replay is local; never calls or retries an executor."""
    memory = store(runtime)
    with runtime.db() as db:
        db.execute('BEGIN IMMEDIATE')
        rows = db.execute('SELECT * FROM memory_outbox WHERE context_id=? AND receipt_json IS NULL ORDER BY sequence', (reference,)).fetchall()
        for row in rows:
            state = memory.ensure_context(reference, objective=row['objective'], scope=SCOPE,
                actor=ACTOR, constraints=json.loads(row['constraints_json']))
            for _ in range(16):
                try:
                    receipt = memory.transition(reference, SCOPE, state['revision'], row['event_id'],
                        ACTOR, json.loads(row['changes_json']))
                    break
                except core().RevisionConflict:
                    state = memory.get(reference, SCOPE)
            else:
                raise ValueError('Concurrent memory writers: checkpoint not committed; no dispatch')
            db.execute('UPDATE memory_outbox SET receipt_json=? WHERE sequence=?', (encode(receipt), row['sequence']))
    return memory.get(reference, SCOPE)


def projection(runtime, reference, objective, constraints, max_chars=None):
    state = sync(runtime, reference)
    if state['objective'] != objective or state['constraints'] != (constraints or {}):
        raise ValueError('Memory inscription differs from queue original or constraints')
    value = store(runtime).project(reference, SCOPE,
        max_chars=max_chars or max(6500, len(objective) + len(encode(constraints or {})) + 4000))
    from .policy import FORBIDDEN
    if FORBIDDEN.search(value['text']):
        raise ValueError('Confidential reference in operational memory; dispatch refused')
    value['objective'] = objective
    value['receipt']['projection_sha256'] = digest(value['text'])
    return value


def attach(packet, projection, system, provider, constraints):
    if projection is None:
        return packet
    if digest(projection['text']) != projection['receipt']['projection_sha256']:
        raise ValueError('Operational projection altered')
    result = copy.deepcopy(packet)
    result['prompt'] += SEPARATOR + projection['text']
    receipt = result['receipt']
    receipt['pre_operational_packet_sha256'] = receipt['packet_sha256']
    receipt['operational_memory'] = copy.deepcopy(projection['receipt'])
    receipt['operational_memory']['included_record_ids'] = projection['included_record_ids']
    receipt['operational_memory']['omitted_record_ids'] = projection['omitted_record_ids']
    receipt['packet_sha256'] = digest(result['prompt'])
    receipt['context_bytes'] = len(result['prompt'].encode('utf-8'))
    cap = (1048576 - 8192 - (393216 if provider == 'deepseek' else 131072)
           if provider in {'kimi', 'mimo', 'deepseek'} else 39000)
    from . import request_controls as controls
    if controls.is_order18_opus(constraints):
        cap = 600000
    if len((system + result['prompt']).encode('utf-8')) > cap:
        raise ValueError('Operational memory exceeds context budget; no invariant truncation')
    controls.enforce_packet(result, constraints, system)
    return result


def verify_packet(packet):
    receipt = packet['receipt'].get('operational_memory')
    if not receipt:
        raise ValueError('Operational memory required; submit through the durable queue')
    if digest(packet['prompt']) != packet['receipt']['packet_sha256']:
        raise ValueError('Transport packet altered')
    if SEPARATOR not in packet['prompt']:
        raise ValueError('Operational projection missing from transport')
    text = packet['prompt'].rsplit(SEPARATOR, 1)[1]
    if digest(text) != receipt['projection_sha256']:
        raise ValueError('Operational projection hash mismatch')
    for field in ('context_id', 'objective_sha256', 'state_sha256', 'revision'):
        if field not in receipt:
            raise ValueError('Operational receipt incomplete')
    return receipt

def typed_projection(projection):
    if not projection or digest(projection['text']) != projection['receipt'].get('projection_sha256'):
        raise ValueError('Missing or altered operational projection')
    body=json.loads(projection['text'].rsplit('\n',1)[1])
    for field in ('context_id','objective_sha256','state_sha256','revision'):
        if body['receipt'].get(field) != projection['receipt'].get(field):
            raise ValueError('Operational projection identity mismatch')
    return body


def preview_projection(objective, constraints):
    """Measure the real controller envelope in disposable local state, no job."""
    import tempfile
    with tempfile.TemporaryDirectory(prefix='iald_memory_preview_') as folder:
        memory=core().MemoryStore(folder)
        reference=context_id('preview:'+digest(objective+encode(constraints or {})))
        memory.ensure_context(reference,objective=objective,scope=SCOPE,actor=ACTOR,constraints=constraints or {})
        memory.transition(reference,SCOPE,0,'preview-flow',ACTOR,{'flow':{
            'phase':'dispatch_intent','next_action':'Aguardar retorno sem repetir o envio.',
            'handles':[{'id':'00000000-0000-0000-0000-000000000000','phase':'execution_waiting'},
                       {'id':'00000000-0000-0000-0000-000000000001','phase':'dispatch_intent'}]}})
        value=memory.project(reference,SCOPE,max_chars=max(6500,len(objective)+len(encode(constraints or {}))+4000))
        value['objective']=objective
        value['receipt']['projection_sha256']=digest(value['text'])
        value['receipt']['preview_only']=True
        return value
