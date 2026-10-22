
import hashlib,json,uuid
from pathlib import Path
from . import operational_memory as opmem,request_controls as controls
from .policy import validate_prompt

def sha(raw):return hashlib.sha256(raw).hexdigest()

def pinned(path,pin):
    p=Path(path);low=str(p).lower()
    if not p.is_absolute() or any(x in low for x in ('escritorio','escritório','.env','iald_stack_v7','iald_psion_state','credential','senha')):
        raise ValueError('Unsafe supplement source')
    raw=p.read_bytes()
    if sha(raw)!=pin:raise ValueError('Supplement source changed')
    return raw

def init_db(db):
    db.execute('''CREATE TABLE IF NOT EXISTS scientific_contract_bindings(
      job_id TEXT PRIMARY KEY,supplement_sha256 TEXT NOT NULL,envelope_json TEXT NOT NULL,
      envelope_sha256 TEXT NOT NULL,event_id TEXT UNIQUE NOT NULL,original_version INTEGER NOT NULL)''')
    for action in ('UPDATE','DELETE'):
        db.execute(f'''CREATE TRIGGER IF NOT EXISTS scientific_binding_no_{action.lower()} BEFORE {action} ON scientific_contract_bindings
          BEGIN SELECT RAISE(ABORT,'Scientific binding append only'); END''')
    if 'scientific_binding_job_id' not in {r[1] for r in db.execute('PRAGMA table_info(tasks)')}:
        db.execute('ALTER TABLE tasks ADD COLUMN scientific_binding_job_id TEXT')

def read_binding(db,uid):
    row=db.execute('SELECT * FROM scientific_contract_bindings WHERE job_id=?',(uid,)).fetchone()
    if row is None:return None
    if sha(row['envelope_json'].encode())!=row['envelope_sha256']:raise ValueError('Binding envelope changed')
    v=json.loads(row['envelope_json'])
    if v['job_id']!=uid or v['supplement_sha256']!=row['supplement_sha256'] or v['event_id']!=row['event_id']:raise ValueError('Binding identity changed')
    if sha(v['contract_bytes'].encode('utf-8'))!=v['supplement_sha256'] or sha(v['authority_bytes'].encode('utf-8'))!=v['authority_sha256']:raise ValueError('Custody bytes changed')
    contract=json.loads(v['contract_bytes'])
    if controls.normalize(contract['execution_constraints'])!=v['effective_constraints']:raise ValueError('Effective constraints changed')
    return v

def effective(db,job):
    if job is None:raise ValueError('Missing coordination')
    original=json.loads(job['execution_constraints'] or 'null');v=read_binding(db,job['id'])
    if v and (original is not None or job['request_id']!=v['request_id'] or job['memory_context_id']!=v['context_id'] or opmem.digest(job['prompt'])!=v['prompt_sha256']):
        raise ValueError('Original job identity differs')
    return (v['effective_constraints'] if v else original),v

def task_effective(db,task):
    original=json.loads(task['execution_constraints'] or 'null');uid=task['scientific_binding_job_id']
    if not uid:return original,None
    job=db.execute('SELECT * FROM coordination_jobs WHERE id=?',(uid,)).fetchone();c,v=effective(db,job)
    if not v or original is not None or task['memory_context_id']!=v['context_id'] or opmem.digest(task['routing_prompt'])!=v['prompt_sha256'] or task['request_id']!=str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+uid)):
        raise ValueError('Task binding identity differs')
    return c,v

def ready(runtime,v):
    if not v:return
    pinned(v['contract_path'],v['supplement_sha256'])
    pinned(v['authority_path'],v['authority_sha256'])
    for source in v['pins']:
        if len(pinned(source['path'],source['sha256']))!=source['bytes']:raise ValueError('Dispatch source size changed')
    opmem.sync(runtime,v['context_id'])
    with runtime.db() as db:
        row=db.execute('SELECT receipt_json FROM memory_outbox WHERE event_id=?',(v['event_id'],)).fetchone()
        if not row or not row['receipt_json']:raise ValueError('Binding checkpoint pending')
    p=opmem.projection(runtime,v['context_id'],v['original_prompt'],None,max_chars=100000)
    if v['record_id'] not in p['included_record_ids'] or v['supplement_sha256'] not in p['text']:raise ValueError('Binding mandatory record missing')

def project(runtime,reference,objective,original,v):
    if not v:return opmem.projection(runtime,reference,objective,original)
    measured=opmem.projection(runtime,reference,objective,original,max_chars=100000)
    # Caller envelope budget only; preserve every mandatory record, no truncation.
    budget=max(6500,len(measured['text'])+512)
    return annotate(opmem.projection(runtime,reference,objective,original,max_chars=budget),v)

def annotate(projection,v):
    if v:
        if v['record_id'] not in projection['included_record_ids']:raise ValueError('Binding omitted from projection')
        projection['receipt']['scientific_binding']={k:v[k] for k in ('job_id','supplement_sha256','event_id','record_id','prompt_sha256','effective_constraints')}
        projection['receipt']['scientific_binding']['original_constraints']=None
    return projection

def validate_authority(contract,contract_sha,path,pin):
    # Trusted privileged caller seam. Pins alone NEVER authenticate a human.
    p=json.loads(pinned(path,pin));order=contract['authenticated_scope_order']
    expected={'job_id':contract['job_id'],'request_id':contract['request_id'],'unit':contract['unit'],
      'contract_sha256':contract_sha,'order_sha256':order['source']['sha256'],
      'source_thread_id':order['thread_id'],'verified_by':'codex-coordenadora'}
    if p.get('schema')!='scientific-binding-authority/v1' or any(p.get(k)!=v for k,v in expected.items()):raise ValueError('Authority scope differs')
    ids=p.get('human_message_ids')
    if not isinstance(ids,list) or not ids or any(not isinstance(x,str) or not x for x in ids):raise ValueError('Missing official human message evidence')
    board=json.loads(pinned(p['board_path'],p['board_sha256']))
    unit=next((u for u in board['unidades'] if u['id']==contract['unit']),None)
    if not unit or unit['status'] not in ('REIVINDICADA','EM_CURSO'):raise ValueError('Scientific unit not claimed')
    pinned(p['graph_path'],p['graph_sha256'])
    if p.get('graph_unit')!=contract['unit']:raise ValueError('Wrong graph unit')
    import sqlite3
    graph=Path(p['graph_path'])
    from contextlib import closing
    with closing(sqlite3.connect(graph.as_uri()+'?mode=ro',uri=True)) as db:
        node=db.execute('SELECT tipo FROM nos WHERE id=?',('unidade:'+contract['unit'],)).fetchone()
    if not node or node[0]!='unidade':raise ValueError('Scientific graph unit absent')

def bind(coord,uid,path,pin,*,expected_version,authority_path,authority_sha,prepared_supplement):
    # Exact historical acknowledgment must not revalidate independently changing board/source files.
    runtime=coord.runtime
    with runtime.db() as db:prior=read_binding(db,uid)
    if prior:
        prepared_supplement=validate_prompt(prepared_supplement,controls.prompt_limit(prior['effective_constraints']))
        if prior['contract_path']!=str(path) or prior['supplement_sha256']!=pin or prior['authority_path']!=str(authority_path) or prior['authority_sha256']!=authority_sha or prior['prepared_supplement']!=prepared_supplement:
            raise ValueError('Rebinding forbidden')
        return {'binding':prior,'replay':True}
    raw=pinned(path,pin);contract=json.loads(raw)
    if contract.get('schema')!='iald-scientific-contract-supplement/v1' or contract.get('preserve_original') is not True or contract.get('job_id')!=uid:raise ValueError('Invalid contract')
    validate_authority(contract,pin,authority_path,authority_sha)
    c=controls.normalize(contract['execution_constraints'])
    if not c or c['branch_id']!=contract['unit']:raise ValueError('Scientific unit differs')
    pins=[contract['authenticated_scope_order']['source'],*contract['primary_source_pins'],contract['working_v392']]
    for p in pins:
        if len(pinned(p['path'],p['sha256']))!=p['bytes']:raise ValueError('Source size differs')
    prepared_supplement=validate_prompt(prepared_supplement,controls.prompt_limit(c))
    runtime=coord.runtime
    with runtime.db() as db:
        prior=read_binding(db,uid);job=db.execute('SELECT * FROM coordination_jobs WHERE id=?',(uid,)).fetchone()
    if job is None:raise ValueError('Missing coordination')
    if prior:
        if prior['supplement_sha256']!=pin or prior['prepared_supplement']!=prepared_supplement or prior['authority_sha256']!=authority_sha:raise ValueError('Rebinding forbidden')
        return {'binding':prior,'replay':True}
    if job['request_id']!=contract['request_id'] or job['memory_context_id']!=contract['original_memory_context_id'] or opmem.digest(job['prompt'])!=contract['original_prompt_sha256']:raise ValueError('Original identities differ')
    original=opmem.sync(runtime,job['memory_context_id'])
    if original['objective']!=job['prompt'] or original['constraints']!={}:raise ValueError('Original ACOM anchor differs')
    event='scientific-contract:'+uid+':'+pin
    v={'job_id':uid,'request_id':job['request_id'],'context_id':job['memory_context_id'],'original_prompt':job['prompt'],
       'prompt_sha256':opmem.digest(job['prompt']),'supplement_sha256':pin,'contract_path':str(path),'effective_constraints':c,
       'pins':pins,'authority_path':str(authority_path),'authority_sha256':authority_sha,'contract_bytes':raw.decode('utf-8'),'authority_bytes':pinned(authority_path,authority_sha).decode('utf-8'),'event_id':event,
       'record_id':'binding_'+pin,'prepared_supplement':prepared_supplement}
    encoded=opmem.encode(v)
    with runtime.db() as db:
        db.execute('BEGIN IMMEDIATE');row=db.execute('SELECT * FROM coordination_jobs WHERE id=?',(uid,)).fetchone()
        prior=read_binding(db,uid)
        if prior:
            if prior!=v:raise ValueError('Concurrent rebinding')
            return {'binding':prior,'replay':True}
        if row['version']!=expected_version or row['stage']!='awaiting_dispatch' or json.loads(row['execution_constraints'] or 'null') is not None:raise ValueError('Binding stage/version differs')
        if any(row[k] for k in ('thread_id','prepared_prompt','execution_task_id','draft_source','synthesis_source')):raise ValueError('Prepared or dispatched job')
        if db.execute('SELECT 1 FROM coordination_events WHERE job_id=?',(uid,)).fetchone():raise ValueError('Prior coordination activity')
        derived=str(uuid.uuid5(uuid.NAMESPACE_URL,'iald-coordination:'+uid))
        if db.execute('SELECT 1 FROM tasks WHERE request_id=? OR memory_context_id=?',(derived,row['memory_context_id'])).fetchone():raise ValueError('Existing task/attempt context')
        if db.execute('SELECT 1 FROM memory_outbox WHERE context_id=? AND receipt_json IS NULL',(row['memory_context_id'],)).fetchone():raise ValueError('Unresolved original outbox')
        validate_authority(contract,pin,authority_path,authority_sha)
        db.execute('INSERT INTO scientific_contract_bindings VALUES(?,?,?,?,?,?)',(uid,pin,encoded,sha(encoded.encode()),event,expected_version))
        record={'id':v['record_id'],'kind':'decision','text':'Authorized scientific supplement '+pin+'; unit '+contract['unit']+'; original constraints null; effective constraints '+opmem.encode(c),
          'statute':'INPUT','sources':[{'kind':'artifact','ref':'scientific-contract:'+pin,'sha256':pin}],
          'meta':{'authority_sha256':authority_sha,'source_pins':[{'file':Path(p['path']).name,'sha256':p['sha256'],'bytes':p['bytes']} for p in pins]}}
        db.execute('INSERT INTO memory_outbox(event_id,context_id,objective,constraints_json,changes_json) VALUES(?,?,?,?,?)',
          (event,row['memory_context_id'],row['prompt'],'{}',opmem.encode({'records':[record]})))
        if db.execute('UPDATE coordination_jobs SET version=version+1 WHERE id=? AND version=?',(uid,expected_version)).rowcount!=1:raise ValueError('CAS lost')
        from .runtime import now
        db.execute('INSERT INTO coordination_events(job_id,at,action,from_stage,to_stage) VALUES(?,?,?,?,?)',(uid,now(),'bind_scientific_contract','awaiting_dispatch','awaiting_dispatch'))
    ready(runtime,v)
    return {'binding':v,'replay':False}
