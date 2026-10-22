"""Privileged LOCAL migration of never-dispatched legacy coordination UUIDs.

No provider, worker, HTTP, new mission reference or caller-selected actor/path.
The existing queue ledger holds a durable intent and each ACOM write intent.
Recovery replays those exact local writes; a foreign revision is never rebased.
"""
import json
import uuid
from . import operational_memory as om, queue_activity as qa
from .process_lock import process_lock

PROTOCOL = 'iald-legacy-activity-migration/v1'

def _init(db):
    db.execute('''CREATE TABLE IF NOT EXISTS queue_activity_migrations (
      job_id TEXT PRIMARY KEY, event_id TEXT UNIQUE NOT NULL, plan_json TEXT NOT NULL,
      status TEXT NOT NULL, result_json TEXT, last_error TEXT)''')
    db.execute('''CREATE TABLE IF NOT EXISTS queue_activity_migration_steps (
      sequence INTEGER PRIMARY KEY, job_id TEXT NOT NULL, event_id TEXT NOT NULL,
      payload_json TEXT NOT NULL, receipt_json TEXT, UNIQUE(job_id,event_id))''')

def _row(db, uid):
    uuid.UUID(uid)
    row = db.execute('SELECT * FROM coordination_jobs WHERE id=?',(uid,)).fetchone()
    if row is None: raise ValueError('Legacy UUID missing')
    return dict(row)

def _snapshot(db, row):
    supplement = db.execute('SELECT * FROM scientific_contract_bindings WHERE job_id=?',(row['id'],)).fetchone()
    return {'row':row,'scientific_binding':dict(supplement) if supplement else None}

def _digest(value): return om.digest(om.encode(value))

def _safe(db, row):
    if row['activity_version'] != 0 or row['stage'] not in ('awaiting_dispatch','prompt_ready'):
        raise ValueError('Only never-dispatched legacy stages are eligible')
    if any(row.get(k) is not None for k in ('thread_id','execution_task_id','final_text','error','synthesis_source')):
        raise ValueError('External/terminal/uncertain metadata present')
    if row['memory_context_id'] != om.context_id(row['request_id']):
        raise ValueError('Original context missing or differs; no adoption')
    if row['stage']=='awaiting_dispatch':
        if any(row.get(k) is not None for k in ('prepared_prompt','draft_source','assistance_reason')):
            raise ValueError('Unexpected preparation on undispatched legacy job')
    elif not row['prepared_prompt'] or row['draft_source']!='iald_coordinator':
        raise ValueError('Prepared legacy job needs local coordinator provenance')
    for event in db.execute('SELECT * FROM coordination_events WHERE job_id=?',(row['id'],)):
        allowed = ((event['action']=='bind_scientific_contract' and event['from_stage']==event['to_stage']=='awaiting_dispatch') or
                   (event['action']=='prepare_without_work' and event['from_stage']=='awaiting_dispatch' and event['to_stage']=='prompt_ready'))
        if not allowed: raise ValueError('Prior external, uncertain or unrecognized coordination event')
    child = str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+row['id']))
    if db.execute('SELECT 1 FROM tasks WHERE id IN (?,?) OR request_id IN (?,?) OR memory_context_id=? OR scientific_binding_job_id=?',
        (row['id'],child,row['request_id'],child,row['memory_context_id'],row['id'])).fetchone():
        raise ValueError('Existing child/task (including unbound deterministic child)')
    if db.execute('SELECT 1 FROM attempts WHERE task_id IN (?,?)',(row['id'],child)).fetchone():
        raise ValueError('Prior attempt, including orphan identity')
    if db.execute('SELECT 1 FROM request_budget_ledger WHERE task_id IN (?,?)',(row['id'],child)).fetchone():
        raise ValueError('Prior execution reservation')
    if db.execute('SELECT 1 FROM memory_outbox WHERE context_id=? AND receipt_json IS NULL',(row['memory_context_id'],)).fetchone():
        raise ValueError('Unresolved legacy outbox; reconcile separately')
    if db.execute('SELECT 1 FROM queue_activity_bindings WHERE entity_id=?',(row['id'],)).fetchone():
        raise ValueError('Existing activity binding conflicts with legacy migration')
    if db.execute('SELECT 1 FROM queue_activity_returns WHERE entity_id=?',(row['id'],)).fetchone():
        raise ValueError('Existing return conflicts with never-dispatched migration')

def _memory(runtime, row):
    state = om.store(runtime).get(row['memory_context_id'],om.SCOPE)
    if state['objective'] != row['prompt'] or state['constraints'] != (json.loads(row['execution_constraints'] or 'null') or {}):
        raise ValueError('Original inscription/constraints differ')
    return state

def _initial_memory_safe(state, row):
    from iald_memory.mission import MissionController
    _, mission, _ = MissionController(None,row['memory_context_id'],om.SCOPE).load_snapshot(state)
    if mission is not None: raise ValueError('Existing mission is not a legacy activity; no adoption')
    for h in state['p']['handles']:
        if (h.get('id') != row['id'] or set(h)-{'id','phase','queue_phase','no_repeat'} or
            h.get('phase') not in ('awaiting_dispatch','prompt_ready') or
            h.get('queue_phase',h.get('phase')) != row['stage']):
            raise ValueError('External, unknown or uncertain handle in legacy context')

def inspect(runtime, uid):
    """Read-only eligibility/digests. Does not create migration tables or ACOM."""
    with runtime.db() as db:
        row=_row(db,uid);snapshot=_snapshot(db,row)
        try: _safe(db,row); error=None
        except ValueError as exc: error=str(exc)
    state=_memory(runtime,row)
    if error is None:
        try: _initial_memory_safe(state,row)
        except ValueError as exc: error=str(exc)
    return {'protocol':PROTOCOL,'job_id':uid,'version':row['version'],'row_sha256':_digest(snapshot),
        'context_id':row['memory_context_id'],'memory_revision':state['revision'],
        'memory_state_sha256':state['receipt']['state_sha256'],'eligible':error is None,
        'refusal':error,'migration_performed':False,'dispatch_allowed':False}

class _TrackedStore:
    """Checkpoint every existing-store write; close the cross-ledger crash gap."""
    def __init__(self,runtime,uid,plan):
        self.runtime,self.uid,self.plan=runtime,uid,plan
        self.base=om.store(runtime);self.root=self.base.root
        self.revision=plan['expected_memory_revision'];self.state_sha=plan['expected_memory_state_sha256']

    def _queue_valid(self):
        with self.runtime.db() as db:
            row=_row(db,self.uid);_safe(db,row)
            if _snapshot(db,row)!=self.plan['snapshot']:raise ValueError('Legacy row/supplement changed after intent')

    def recover_steps(self):
        with self.runtime.db() as db:
            steps=db.execute('SELECT * FROM queue_activity_migration_steps WHERE job_id=? ORDER BY sequence',(self.uid,)).fetchall()
        for step in steps:
            payload=json.loads(step['payload_json'])
            if payload['expected_revision']!=self.revision:raise ValueError('Migration checkpoint chain differs')
            if step['receipt_json']:
                receipt=json.loads(step['receipt_json'])
            else:
                self._queue_valid()
                # Same event/payload may already have committed in ACOM. This
                # replay cannot send anything or change an unrelated revision.
                receipt=self.base.transition(**payload)
                self._checkpoint(step['event_id'],receipt)
            self.revision=receipt['revision'];self.state_sha=receipt['state_sha256']
        self.get(self.plan['snapshot']['row']['memory_context_id'],om.SCOPE)

    def _checkpoint(self,event,receipt):
        with self.runtime.db() as db:
            db.execute('UPDATE queue_activity_migration_steps SET receipt_json=? WHERE job_id=? AND event_id=?',
                       (om.encode(receipt),self.uid,event))

    def get(self,context_id,scope):
        self._queue_valid()
        state=self.base.get(context_id,scope)
        if state['revision']!=self.revision or state['receipt']['state_sha256']!=self.state_sha:
            raise ValueError('ACOM changed outside recorded migration; explicit reconciliation required')
        return state

    def transition(self,context_id,scope,expected_revision,event_id,actor,changes):
        state=self.get(context_id,scope)
        if expected_revision!=self.revision:raise ValueError('Migration memory CAS differs')
        payload=dict(context_id=context_id,scope=scope,expected_revision=expected_revision,event_id=event_id,actor=actor,changes=changes)
        with self.runtime.db() as db:
            db.execute('INSERT INTO queue_activity_migration_steps(job_id,event_id,payload_json) VALUES(?,?,?)',
                       (self.uid,event_id,om.encode(payload)))
        receipt=self.base.transition(**payload)
        self._checkpoint(event_id,receipt)
        self.revision=receipt['revision'];self.state_sha=receipt['state_sha256']
        return receipt

    def __getattr__(self,name):return getattr(self.base,name)

def migrate(runtime, *, job_id, expected_version, expected_row_sha256,
            expected_memory_revision, expected_memory_state_sha256, event_id):
    """Explicit OS-authenticated local command. Never grants remote authorization."""
    uuid.UUID(job_id);uuid.UUID(event_id)
    if type(expected_version) is not int or type(expected_memory_revision) is not int:
        raise ValueError('Integer CAS versions required')
    requested=dict(job_id=job_id,event_id=event_id,expected_version=expected_version,
        expected_row_sha256=expected_row_sha256,expected_memory_revision=expected_memory_revision,
        expected_memory_state_sha256=expected_memory_state_sha256)
    with process_lock(runtime.db_path,blocking=False) as locked:
        if not locked:raise ValueError('Queue worker/migration lock busy')
        with runtime.db() as db:
            _init(db);db.execute('BEGIN IMMEDIATE')
            old=db.execute('SELECT * FROM queue_activity_migrations WHERE job_id=?',(job_id,)).fetchone()
            if old:
                plan=json.loads(old['plan_json'])
                if plan['request']!=requested:raise ValueError('Migration intent identity/CAS conflict')
                if old['status']=='completed':return dict(json.loads(old['result_json']),replayed=True)
            else:
                row=_row(db,job_id);_safe(db,row);snapshot=_snapshot(db,row)
                if row['version']!=expected_version or _digest(snapshot)!=expected_row_sha256:
                    raise ValueError('Legacy row version/digest CAS differs')
                state=_memory(runtime,row);_initial_memory_safe(state,row)
                if state['revision']!=expected_memory_revision or state['receipt']['state_sha256']!=expected_memory_state_sha256:
                    raise ValueError('Legacy ACOM revision/hash CAS differs')
                plan=dict(request=requested,snapshot=snapshot,**requested)
                db.execute('INSERT INTO queue_activity_migrations VALUES(?,?,?,\'prepared\',NULL,NULL)',
                           (job_id,event_id,om.encode(plan)))
        try:
            tracked=_TrackedStore(runtime,job_id,plan);tracked.recover_steps()
            from iald_memory.activity import ActivityRuntime
            row=plan['snapshot']['row'];ar=ActivityRuntime(tracked,row['memory_context_id'],om.SCOPE,qa.ACTOR)
            ticket=ar.begin(row['request_id'],row['prompt'],origin='authenticated_operator')['ticket']
            op=qa.operation_id('coord',job_id)
            if not any(h.get('operation_id')==op for h in ar.recover(ticket['request_id'])['handles']):
                ticket=ar.preflight(ticket,op,refresh=True)['ticket']
            else:ticket=ar.refresh(ticket)
            # All ACOM transitions were checked/custodied before enabling the
            # existing act path. The queue stage and semantic columns stay exact.
            with runtime.db() as db:
                db.execute('BEGIN IMMEDIATE')
                current=_row(db,job_id);_safe(db,current)
                if _snapshot(db,current)!=plan['snapshot']:raise ValueError('Final legacy row CAS differs')
                state=tracked.get(row['memory_context_id'],om.SCOPE)
                data=qa._binding(row,'coord',None)
                db.execute('INSERT INTO queue_activity_bindings VALUES(?,?,?,?,?,?,?)',
                    (job_id,'coord',None,row['memory_context_id'],ticket['request_id'],om.encode(data),om.encode(ticket)))
                db.execute('INSERT INTO queue_activity_custody VALUES(?,?,?)',(job_id,'coord',om.encode(data)))
                if db.execute('UPDATE coordination_jobs SET activity_version=1,version=version+1 WHERE id=? AND version=? AND activity_version=0',
                    (job_id,expected_version)).rowcount!=1:raise ValueError('Final queue CAS lost')
                result={'protocol':PROTOCOL,'job_id':job_id,'context_id':row['memory_context_id'],
                    'original_row_sha256':expected_row_sha256,'version':expected_version+1,'activity_version':1,
                    'stage':row['stage'],'memory_receipt':state['receipt'],'event_id':event_id,
                    'replayed':False,'dispatch_allowed':False,'accepted':False,'migration_only':True}
                db.execute("UPDATE queue_activity_migrations SET status='completed',result_json=?,last_error=NULL WHERE job_id=?",
                           (om.encode(result),job_id))
            return result
        except BaseException as exc:
            with runtime.db() as db:
                db.execute('UPDATE queue_activity_migrations SET last_error=? WHERE job_id=?',
                           (type(exc).__name__+': '+str(exc)[:400],job_id))
            raise

def invoke(runtime, request):
    if not isinstance(request,dict):raise ValueError('JSON object required')
    if request.get('operation')=='inspect':
        if set(request)!={'operation','job_id'}:raise ValueError('Unexpected privileged CLI fields')
        return inspect(runtime,request['job_id'])
    if request.get('operation')=='migrate':
        fields={'job_id','expected_version','expected_row_sha256','expected_memory_revision','expected_memory_state_sha256','event_id'}
        if set(request)!=fields|{'operation'}:raise ValueError('Exact migration fields required')
        return migrate(runtime,**{k:request[k] for k in fields})
    raise ValueError('Privileged local migration operation unsupported')
