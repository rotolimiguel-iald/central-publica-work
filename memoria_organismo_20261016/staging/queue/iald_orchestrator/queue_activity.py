"""Server-owned activity bindings in the EXISTING queue ledger.

The local queue retains its IALD/operator scope. No caller-selected actor, file,
principal or context is accepted here. Cross-account app delegation requires an
explicit authenticated adapter; a ticket is not authentication. These tables
index queue entities/outcomes, not a second semantic memory database.
"""
import json
import uuid
from . import operational_memory as opmem

ACTOR = {'id': 'iald-queue-activity', 'kind': 'agent'}

def init_db(db):
    db.executescript('''
      CREATE TABLE IF NOT EXISTS queue_activity_bindings (
        entity_id TEXT PRIMARY KEY, kind TEXT NOT NULL, parent_id TEXT,
        context_id TEXT NOT NULL, request_id TEXT NOT NULL,
        binding_json TEXT NOT NULL, ticket_json TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS queue_activity_returns (
        entity_id TEXT NOT NULL, operation_id TEXT NOT NULL, digest TEXT NOT NULL,
        result_json TEXT NOT NULL, outcome_json TEXT,
        PRIMARY KEY(entity_id, operation_id, digest));
    ''')

def runtime_for(runtime, reference):
    opmem.core()
    from iald_memory.activity import ActivityRuntime
    return ActivityRuntime(opmem.store(runtime), reference, opmem.SCOPE, ACTOR)

def _row(runtime, kind, entity_id):
    uuid.UUID(entity_id)
    table = {'task': 'tasks', 'coord': 'coordination_jobs'}[kind]
    with runtime.db() as db:
        row = db.execute('SELECT * FROM '+table+' WHERE id=?', (entity_id,)).fetchone()
    if row is None:
        raise ValueError('Activity entity missing')
    return dict(row)

def _binding(row, kind, parent_id):
    return {'kind': kind, 'id': row['id'], 'request_id': row['request_id'],
        'context_id': row['memory_context_id'], 'scope': opmem.SCOPE, 'parent_id': parent_id,
        'prompt': row['prompt'], 'objective': row.get('routing_prompt') or row['prompt'],
        'constraints': json.loads(row['execution_constraints'] or 'null')}

def validate_parent(runtime, parent_id, prompt, request_id, objective, reference):
    row = _row(runtime, 'coord', parent_id)
    expected_id = str(uuid.uuid5(uuid.NAMESPACE_URL, 'iald-coordination:'+parent_id))
    if (row['stage'] != 'execution_dispatching' or row['prepared_prompt'] != prompt
            or row['request_id'] is None or expected_id != request_id
            or row['memory_context_id'] != reference or row['prompt'] != objective):
        raise ValueError('Server coordination/child binding mismatch')
    load(runtime, 'coord', parent_id)
    return row

def admit(runtime, kind, entity_id, parent_id=None):
    row = _row(runtime, kind, entity_id)
    if row['activity_version'] != 1:
        raise ValueError('Legacy entity requires explicit migration; no execution')
    data = _binding(row, kind, parent_id)
    if parent_id:
        parent, ar, ticket = load(runtime, 'coord', parent_id)
        if parent['context_id'] != data['context_id'] or parent['objective'] != data['objective']:
            raise ValueError('Parent scope/context differs')
    else:
        if data['context_id'] != opmem.context_id(data['request_id']):
            raise ValueError('Queue identity differs; no implicit context adoption')
        opmem.sync(runtime, data['context_id'])
        ar = runtime_for(runtime, data['context_id'])
        ticket = ar.begin(data['request_id'], data['objective'], origin='authenticated_operator')['ticket']
    with runtime.db() as db:
        db.execute('BEGIN IMMEDIATE')
        old = db.execute('SELECT * FROM queue_activity_bindings WHERE entity_id=?', (entity_id,)).fetchone()
        if old:
            if json.loads(old['binding_json']) != data:
                raise ValueError('Activity binding payload changed')
        else:
            db.execute('INSERT INTO queue_activity_bindings VALUES(?,?,?,?,?,?,?)',
                (entity_id,kind,parent_id,data['context_id'],ticket['request_id'],opmem.encode(data),opmem.encode(ticket)))
    # Coordination is a durable operation spanning preparation/worker/synthesis.
    # It is not permission to send Work: each external stage gets its own intent.
    if kind == 'coord':
        recovered = ar.recover(ticket['request_id'])
        operation = operation_id('coord', entity_id)
        if not any(h.get('operation_id') == operation for h in recovered['handles']):
            preflight(runtime, kind, entity_id)
    return describe(runtime, kind, entity_id)

def load(runtime, kind, entity_id):
    row = _row(runtime, kind, entity_id)
    with runtime.db() as db:
        binding = db.execute('SELECT * FROM queue_activity_bindings WHERE entity_id=?', (entity_id,)).fetchone()
    if not binding or binding['kind'] != kind:
        raise ValueError('Activity binding missing; reconcile admission locally before execution')
    data = json.loads(binding['binding_json'])
    if data != _binding(row, kind, binding['parent_id']):
        raise ValueError('Activity entity changed')
    ticket = json.loads(binding['ticket_json'])
    if ticket['scope'] != opmem.SCOPE or ticket['actor'] != ACTOR or ticket['context_id'] != data['context_id']:
        raise ValueError('Activity server envelope mismatch')
    return data, runtime_for(runtime, data['context_id']), ticket

def _ticket(runtime, entity_id, ticket):
    with runtime.db() as db:
        db.execute('UPDATE queue_activity_bindings SET ticket_json=? WHERE entity_id=?',
            (opmem.encode(ticket), entity_id))

def operation_id(kind, entity_id, suffix=None):
    return kind+':'+entity_id+(':'+suffix if suffix else '')

def refresh(runtime, kind, entity_id):
    data, ar, ticket = load(runtime, kind, entity_id)
    ticket = ar.refresh(ticket)
    _ticket(runtime, entity_id, ticket)
    return ticket

def preflight(runtime, kind, entity_id, suffix=None):
    data, ar, ticket = load(runtime, kind, entity_id)
    result = ar.preflight(ticket, operation_id(kind, entity_id, suffix), refresh=True)
    _ticket(runtime, entity_id, result['ticket'])
    return result

def raw_return(runtime, kind, entity_id, result, suffix=None):
    # Always persist the entire received JSON before a freshness/cancel check.
    load(runtime, kind, entity_id)
    text = opmem.encode(result)
    opmem.core().guard.assert_clean_text(text, 'queue.activity.return')
    sha = opmem.digest(text)
    op = operation_id(kind, entity_id, suffix)
    with runtime.db() as db:
        db.execute('INSERT OR IGNORE INTO queue_activity_returns(entity_id,operation_id,digest,result_json) VALUES(?,?,?,?)',
            (entity_id, op, sha, text))
    return sha

def complete(runtime, kind, entity_id, result, *, terminal, suffix=None):
    sha = raw_return(runtime, kind, entity_id, result, suffix)
    data, ar, ticket = load(runtime, kind, entity_id)
    # A source/authority changed during the call cannot remain an optional
    # shadow diagnostic. Preserve bytes first, then hold this same context.
    from . import scientific_binding
    row = _row(runtime, kind, entity_id)
    with runtime.db() as db:
        _, supplement = (scientific_binding.task_effective(db,row) if kind=='task'
                         else scientific_binding.effective(db,row))
    try:
        scientific_binding.ready(runtime,supplement)
    except Exception:
        cancel(runtime,kind,entity_id,'Scientific dispatch premise changed on return; reconcile without resend.')
    try:
        outcome = ar.complete(ticket, operation_id(kind, entity_id, suffix), result,
            terminal=terminal, refresh=True)
        if outcome.get('ticket'):
            _ticket(runtime, entity_id, outcome['ticket'])
    except Exception as exc:
        outcome = {'integrated': False, 'accepted': False, 'return_preserved': True,
            'error': getattr(exc, 'code', type(exc).__name__), 'details': getattr(exc, 'details', {})}
    with runtime.db() as db:
        db.execute('UPDATE queue_activity_returns SET outcome_json=? WHERE entity_id=? AND operation_id=? AND digest=?',
            (opmem.encode(outcome),entity_id,operation_id(kind,entity_id,suffix),sha))
    return outcome

def uncertain(runtime, kind, entity_id, reason, suffix=None):
    data, ar, ticket = load(runtime, kind, entity_id)
    return ar.mark_uncertain(ticket, operation_id(kind,entity_id,suffix), reason)

def cancel(runtime, kind, entity_id, reason):
    data, ar, ticket = load(runtime, kind, entity_id)
    p = ar.controller.project(max_chars=2000000)
    if not p['projection']['hold']:
        ar.controller.action({'operation':'hold','actor':ACTOR,'hold':True,'reason':reason,
            'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],
            'state_sha256':p['receipt']['state_sha256'],
            'event_id':'queue_cancel_'+opmem.digest(entity_id), 'sources':[ticket['source']]})
    # An in-flight remote call remains uncertain even though the queue says cancelled.
    for h in ar.recover(ticket['request_id'])['handles']:
        if h.get('kind') == 'activity_operation' and h.get('status') == 'dispatching':
            ar.mark_uncertain(ticket, h['operation_id'], reason)

def describe(runtime, kind, entity_id, max_chars=125000):
    data, ar, ticket = load(runtime,kind,entity_id)
    state = ar.recover(ticket['request_id'])
    return {'protocol':'iald-queue-activity/v1','scope':opmem.SCOPE,'context_id':data['context_id'],
        'request_id':state['request_id'],'entity_id':entity_id,'parent_id':data['parent_id'],
        'task_id':ticket['task_id'],'epoch':ticket['epoch'],'receipt':state['receipt'],
        'handles':state['handles'],'automatic_retry':False,'semantic_acceptance':False,
        'projection':ar.project(max_chars=max_chars)}

def verify_dispatch(runtime, entity_id, packet):
    current = refresh(runtime,'task',entity_id)
    receipt = packet['receipt']['operational_memory']
    for field in ('context_id','revision','state_sha256'):
        if receipt[field] != current[field]:
            raise ValueError('Activity projection changed before provider dispatch')
    if _row(runtime,'task',entity_id)['status'] not in ('queued','running'):
        raise ValueError('Task no longer dispatchable')

def recover(runtime, kind, entity_id):
    """Read existing durable state/returns. Never sends a provider or accepts."""
    result = describe(runtime,kind,entity_id)
    with runtime.db() as db:
        records = db.execute('SELECT * FROM queue_activity_returns WHERE entity_id=? ORDER BY rowid', (entity_id,)).fetchall()
    result['returns'] = [dict(r) for r in records]
    return result

def reconcile(runtime, kind, entity_id):
    """Explicit LOCAL custody replay from durable queue bytes; no external effect."""
    data, _, _ = load(runtime,kind,entity_id)
    op = operation_id(kind,entity_id)
    with runtime.db() as db:
        rows = db.execute('SELECT * FROM queue_activity_returns WHERE entity_id=? AND operation_id=?', (entity_id,op)).fetchall()
    if len(rows) != 1:
        raise ValueError('Exactly one durable return required; missing/divergent outcome stays unresolved')
    result = json.loads(rows[0]['result_json'])
    outcome = complete(runtime,kind,entity_id,result,terminal=kind=='coord' or data['parent_id'] is None)
    # Accounting/cancellation/queue disposition is a separate existing control.
    # A local memory reconciliation never promotes a failed ledger settlement.
    return outcome
