"""External activity wrapper for existing Bancada HTTP contracts.

No engine import, calculation, new numerical default, guard bypass or mutation
of Bancada files. Admission is a trusted local operator action; execute accepts
only its server ledger UUID. Public/model tools cannot choose URL, actor, paths,
evidence or reviewer. A timeout preserves the single dispatch intent.
"""
import json
import re
import uuid
import urllib.request
from . import operational_memory as om, queue_activity as qa

ROUTES={'estado':'/api/estado','avaliar':'/api/avaliar','ajustar':'/api/ajustar',
        'comparar':'/api/comparar','amostrar':'/api/amostrar'}

def init(runtime):
    with runtime.db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS queue_bench_activity (
          request_id TEXT PRIMARY KEY, envelope_json TEXT NOT NULL,
          context_id TEXT NOT NULL, ticket_json TEXT, return_json TEXT,
          outcome_json TEXT, polls INTEGER NOT NULL DEFAULT 0)''')
        db.execute('''CREATE TABLE IF NOT EXISTS queue_bench_observations (
          request_id TEXT NOT NULL, sequence INTEGER NOT NULL, result_json TEXT NOT NULL,
          PRIMARY KEY(request_id,sequence))''')

def admit(runtime,request_id,command,action,payload):
    uuid.UUID(request_id)
    if action not in ROUTES or not isinstance(command,str) or not command:
        raise ValueError('Explicit supported Bancada request required')
    if (action=='estado' and payload is not None) or (action!='estado' and not isinstance(payload,dict)):
        raise ValueError('Exact HTTP body required; no scientific defaults supplied')
    envelope={'command':command,'action':action,'payload':payload,'scope':om.SCOPE}
    text=om.encode(envelope)
    om.core().guard.assert_clean_text(text,'bench.admission')
    init(runtime)
    reference=om.context_id('bench:'+request_id)
    with runtime.db() as db:
        db.execute('BEGIN IMMEDIATE')
        old=db.execute('SELECT * FROM queue_bench_activity WHERE request_id=?',(request_id,)).fetchone()
        if old and old['envelope_json']!=text: raise ValueError('Bancada request ID/payload conflict')
        if not old:db.execute('INSERT INTO queue_bench_activity(request_id,envelope_json,context_id) VALUES(?,?,?)',(request_id,text,reference))
    store=om.store(runtime)
    store.ensure_context(reference,objective=text,scope=om.SCOPE,actor=qa.ACTOR,
                         constraints={'consumer':'Bancada_Um_HTTP','no_repeat':True})
    ar=qa.runtime_for(runtime,reference)
    ticket=ar.begin(request_id,text,origin='authenticated_operator')['ticket']
    with runtime.db() as db:db.execute('UPDATE queue_bench_activity SET ticket_json=? WHERE request_id=?',(om.encode(ticket),request_id))
    return recover(runtime,request_id)

def load(runtime,request_id):
    uuid.UUID(request_id)
    with runtime.db() as db:row=db.execute('SELECT * FROM queue_bench_activity WHERE request_id=?',(request_id,)).fetchone()
    if row is None or not row['ticket_json']:raise ValueError('Bancada envelope not admitted')
    value=dict(row);env=json.loads(value['envelope_json']);ticket=json.loads(value['ticket_json'])
    if env['scope']!=om.SCOPE or ticket['scope']!=om.SCOPE or ticket['actor']!=qa.ACTOR or ticket['context_id']!=value['context_id']:
        raise ValueError('Bancada server envelope mismatch')
    ar=qa.runtime_for(runtime,value['context_id'])
    if om.store(runtime).get(value['context_id'],om.SCOPE)['objective']!=value['envelope_json']:
        raise ValueError('Bancada inscription changed')
    return value,env,ar,ticket

def http(path,body):
    # Same loopback route/body and X-Cliente contract as the existing proxy.
    data=None if body is None else json.dumps(body).encode('utf-8')
    request=urllib.request.Request('http://127.0.0.1:18777'+path,data=data,
        headers={'Content-Type':'application/json','X-Cliente':'mcp:iald-activity'})
    with urllib.request.urlopen(request,timeout=600) as response:
        return json.loads(response.read().decode('utf-8'))

def _persist_return(runtime,request_id,column,value):
    assert column in ('return_json','outcome_json')
    encoded=om.encode(value);om.core().guard.assert_clean_text(encoded,'bench.return')
    with runtime.db() as db:db.execute('UPDATE queue_bench_activity SET '+column+'=? WHERE request_id=?',(encoded,request_id))

def execute(runtime,request_id,*,transport=http):
    row,env,ar,ticket=load(runtime,request_id)
    if row['return_json'] is not None:raise ValueError('Bancada already returned; recover/reconcile, never resend')
    operation='bench:'+request_id
    prepared=ar.preflight(ticket,operation,refresh=True)
    ticket=prepared['ticket']
    with runtime.db() as db:db.execute('UPDATE queue_bench_activity SET ticket_json=? WHERE request_id=?',(om.encode(ticket),request_id))
    try:result=transport(ROUTES[env['action']],env['payload'])
    except BaseException:
        ar.mark_uncertain(ticket,operation,'Bancada HTTP interruption; remote effect unknown, no resend.')
        raise
    # Server HTTP success is not proof of calculation/mission satisfaction.
    _persist_return(runtime,request_id,'return_json',result)
    return reconcile(runtime,request_id)

def reconcile(runtime,request_id):
    row,env,ar,ticket=load(runtime,request_id)
    if row['return_json'] is None:raise ValueError('No durable Bancada return; recover uncertainty')
    result=json.loads(row['return_json'])
    # The same raw response is always reconciled, never replaced by a poll.
    try:
        synchronous=isinstance(result,dict) and not any(k in result for k in ('tarefa','erro','error'))
        outcome=ar.complete(ticket,'bench:'+request_id,result,terminal=synchronous,refresh=True)
    except Exception as exc:
        outcome={'integrated':False,'accepted':False,'return_preserved':True,
                 'error':getattr(exc,'code',type(exc).__name__)}
    remote=result.get('tarefa') if isinstance(result,dict) else None
    if remote is not None:
        if not isinstance(remote,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,160}',remote):
            raise ValueError('Remote task ID invalid; raw return preserved')
        store=om.store(runtime);s=store.get(row['context_id'],om.SCOPE)
        hid='bench_remote_'+om.digest(request_id)
        if not any(h['id']==hid for h in s['p']['handles']):
            store.transition(row['context_id'],om.SCOPE,s['revision'],hid,qa.ACTOR,
                {'flow':{'handles':[{'id':hid,'kind':'bench_remote','request_id':request_id,
                    'remote_id':remote,'status':'pending','no_repeat':True}]}})
    _persist_return(runtime,request_id,'outcome_json',outcome)
    return recover(runtime,request_id)

def poll(runtime,request_id,*,transport=http):
    """Explicit observation of the SAME admitted remote task; never POST again."""
    row,env,ar,ticket=load(runtime,request_id)
    response=json.loads(row['return_json']) if row['return_json'] else None
    remote=response.get('tarefa') if isinstance(response,dict) else None
    if not isinstance(remote,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,160}',remote):
        raise ValueError('No admitted remote task to observe')
    state=om.store(runtime).get(row['context_id'],om.SCOPE)
    hid='bench_remote_'+om.digest(request_id)
    handle=next((h for h in state['p']['handles'] if h['id']==hid),None)
    if not handle or handle['remote_id']!=remote:raise ValueError('Remote task binding differs')
    if handle['status'] in ('completed','failed'):return recover(runtime,request_id)
    with runtime.db() as db:
        db.execute('BEGIN IMMEDIATE')
        seq=db.execute('SELECT polls FROM queue_bench_activity WHERE request_id=?',(request_id,)).fetchone()[0]+1
        db.execute('UPDATE queue_bench_activity SET polls=? WHERE request_id=?',(seq,request_id))
    op='bench-poll:'+request_id+':'+str(seq)
    ticket=ar.preflight(ticket,op,refresh=True)['ticket']
    try:result=transport('/api/tarefas/'+remote,None)
    except BaseException:
        ar.mark_uncertain(ticket,op,'Remote observation uncertain; initial POST never repeated.')
        raise
    text=om.encode(result);om.core().guard.assert_clean_text(text,'bench.observation')
    with runtime.db() as db:
        db.execute('INSERT INTO queue_bench_observations VALUES(?,?,?)',(request_id,seq,text))
    terminal=isinstance(result,dict) and result.get('estado') in ('pronta','falhou')
    # Unknown/conflicting fields retain uncertainty rather than choosing success.
    if isinstance(result,dict) and any(k in result and result[k] != result.get('estado') for k in ('phase','status')):
        terminal=False
    if terminal:
        store=om.store(runtime);state=store.get(row['context_id'],om.SCOPE)
        store.transition(row['context_id'],om.SCOPE,state['revision'],'bench_terminal_'+om.digest(request_id),qa.ACTOR,
            {'flow':{'handles':[{'id':hid,'status':'completed' if result['estado']=='pronta' else 'failed'}]}})
    try:outcome=ar.complete(ticket,op,result,terminal=terminal,refresh=True)
    except Exception as exc:outcome={'integrated':False,'accepted':False,'return_preserved':True,'error':getattr(exc,'code',type(exc).__name__)}
    _persist_return(runtime,request_id,'outcome_json',outcome)
    return recover(runtime,request_id)

def recover(runtime,request_id):
    row,env,ar,ticket=load(runtime,request_id)
    with runtime.db() as db:observations=[dict(r) for r in db.execute('SELECT * FROM queue_bench_observations WHERE request_id=? ORDER BY sequence',(request_id,))]
    return {'request_id':request_id,'context_id':row['context_id'],'scope':om.SCOPE,
        'action':env['action'],'return':json.loads(row['return_json']) if row['return_json'] else None,
        'outcome':json.loads(row['outcome_json']) if row['outcome_json'] else None,
        'activity':ar.recover(request_id),'projection':ar.project(max_chars=125000),
        'observations':observations,
        'automatic_retry':False,'semantic_acceptance':False,
        'scope_note':'HTTP custody only; remote task/pending scientific review remains explicit.'}

def register_tools(server,runtime):
    @server.tool()
    def iald_bench_activity_execute(request_id:str)->dict:
        """Executa UMA chamada já admitida pelo servidor local; somente UUID, sem URL/cálculo novo."""
        return execute(runtime,request_id)
    @server.tool()
    def iald_bench_activity_get(request_id:str)->dict:
        """Recupera recibo local da Bancada, incluindo tarefa remota incerta; sem nova chamada."""
        return recover(runtime,request_id)
    @server.tool()
    def iald_bench_activity_reconcile(request_id:str)->dict:
        """Reconcilia apenas bytes já recebidos; nenhum HTTP nem aceite científico."""
        return reconcile(runtime,request_id)
    @server.tool()
    def iald_bench_activity_poll(request_id:str)->dict:
        """Observa só a tarefa remota já vinculada; GET, sem repetir o cálculo POST."""
        return poll(runtime,request_id)
