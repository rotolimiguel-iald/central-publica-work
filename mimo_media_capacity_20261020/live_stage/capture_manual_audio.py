"""Read-only local capture of two explicitly authorized jobs. Never sends/retries."""
import ast
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import sqlite3

W=Path(__file__).resolve().parent
R=Path('C:/IALD/projetos_pyhton/IALD')
M=Path('C:/IALD/MEMORIA_IALD/state')
JOBS={'MANUAL_AUDIO':('d7f3e284-cd11-46f3-aa8d-4a51e60c5d23','c_mvh8g01bjpvy')}

def digest(raw):return hashlib.sha256(raw).hexdigest()
def connect(path):
    db=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    db.row_factory=sqlite3.Row
    db.execute('PRAGMA query_only=ON')
    return db

# Extract only local DPAPI decryption class; never import the running app.
tree=ast.parse((R/'iald_chat_jobs.py').read_text(encoding='utf-8'))
node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='WindowsCipher')
ns=dict(ctypes=ctypes,wintypes=wintypes,os=os)
exec(compile(ast.Module(body=[node],type_ignores=[]),'<existing local DPAPI>','exec'),ns)
cipher=ns['WindowsCipher']()

def checked_artifact(source,context,scope):
    path=Path(source['ref']).resolve()
    assert path.is_relative_to((M/'activity_artifacts').resolve())
    raw=path.read_bytes();assert digest(raw)==source['sha256']
    data=json.loads(raw)
    assert data['context_id']==context and data['scope']==scope
    return data['payload']

def capture(which, verification=None):
    job_id,conversation=JOBS[which]
    out=W/(which+'_RESULT.json')
    if out.exists():
        old=json.loads(out.read_bytes());assert old['job']['id']==job_id and old['job']['conversation_id']==conversation
        return old
    with connect(R/'.iald_runtime/chat_jobs/jobs.sqlite3') as db:
        row=db.execute('SELECT id,conversation_id,status,created,updated,seq,error FROM jobs WHERE id=?',(job_id,)).fetchone()
        assert row is not None
        job=dict(row);assert job['conversation_id']==conversation
        owner=db.execute('SELECT owner FROM jobs WHERE id=?',(job_id,)).fetchone()['owner']
        assert owner==digest(b'iald-chat-job:luiz')
        assert job['status'] in ('completed','failed','cancelled','interrupted'), 'NOT_TERMINAL_NO_CAPTURE'
        events=list(db.execute('SELECT seq,data FROM events WHERE job=? ORDER BY seq',(job_id,)))
    text=[];warnings=[];done=False;tools=[];event_hash=hashlib.sha256()
    for event in events:
        raw=cipher.open(event['data']);event_hash.update(raw)
        value=raw.decode('utf-8')
        if value.strip()=='[DONE]':done=True;continue
        data=json.loads(value)
        if data.get('iald_aviso') or data.get('error'):warnings.append({'seq':event['seq'],'data':data})
        if data.get('iald_status',{}).get('fase')=='ferramenta':tools.append(data['iald_status'].get('tool'))
        for choice in data.get('choices',[]):
            part=(choice.get('delta') or {}).get('content')
            if isinstance(part,str):text.append(part)
    text=''.join(text)
    with connect(M/'memory.sqlite3') as db:
        links=list(db.execute('SELECT context_id,revision,changes_json FROM events WHERE changes_json LIKE ?',('%'+job_id+'%',)))
        contexts={row['context_id'] for row in links};assert len(contexts)==1
        context=next(iter(contexts))
        scoped=db.execute('SELECT scope_json FROM contexts WHERE context_id=?',(context,)).fetchone()
        scope=json.loads(scoped['scope_json']);assert scope['house']=='IALD_APP'
        with connect(R/'.iald_runtime/private_media/media.sqlite3') as media_db:
            bindings=media_db.execute('SELECT DISTINCT generation FROM media WHERE owner=? AND conversation=?',('luiz',conversation)).fetchall()
        assert len(bindings)==1 and bindings[0]['generation']==scope['principal']
        row=db.execute('SELECT revision,state_json,state_sha256,event_hash FROM context_state WHERE context_id=?',(context,)).fetchone()
        assert digest(row['state_json'].encode())==row['state_sha256']
        last=db.execute('SELECT revision,state_sha256,event_hash FROM events WHERE context_id=? ORDER BY revision DESC LIMIT 1',(context,)).fetchone()
        assert (row['revision'],row['state_sha256'],row['event_hash'])==(last['revision'],last['state_sha256'],last['event_hash'])
        snapshot=json.loads(row['state_json'])
    request='job_'+digest((scope['principal']+':'+job_id).encode())
    assert context=='app_'+digest((scope['principal']+':'+conversation).encode())
    handles=[h for h in snapshot['p']['handles'] if h.get('request_id')==request]
    ids={h.get('result_record_id') for h in handles if h.get('kind')=='activity_operation'}
    results=[r for r in snapshot['q']['records'] if r.get('id') in ids]
    wires=[];custody=[];response_match=False;native=[]
    for record in results:
        meta=record['meta']['iald_activity_v1']['data'];assert meta['request_id']==request
        for source in record['sources']:checked_artifact(source,context,scope)
        custody.append({'record_id':record['id'],'statute':record['statute'],'sources_verified':True})
        result=meta['result']
        if meta['operation_id']=='response':response_match=result.get('content')==text
        response=result.get('response')
        if not isinstance(response,dict) or response.get('protocol')!='iald-transport-reference/v1':continue
        payload=checked_artifact({'ref':response['ref']['path'],'sha256':response['ref']['sha256']},context,scope)
        wire=payload['wire_utf8'];assert digest(wire.encode())==payload['wire_sha256']==response['sha256']
        assert len(wire.encode())==response['bytes']
        wires.append({'reference':response['ref'],'wire_sha256':response['sha256'],'bytes':response['bytes'],'verified':True})
        for line in wire.splitlines():
            if line.startswith('data:') and line[5:].strip()!='[DONE]':
                try:chunk=json.loads(line[5:].strip())
                except ValueError:continue
                if chunk.get('model') and chunk.get('usage'):native.append({'model':chunk['model'],'usage':chunk['usage']})
    candidates=[]
    with connect(R/'.iald_runtime/app_evaluation/metrics.sqlite3') as db:
        rows=db.execute("SELECT data FROM turns WHERE (julianday(json_extract(data,'$.utc'))-2440587.5)*86400 BETWEEN ? AND ?",(job['created'],job['updated'])).fetchall()
    for rowmetric in rows:
        metric=json.loads(rowmetric['data'])
        if any(metric['model']==n['model'] and any(c.get('input_tokens')==n['usage'].get('prompt_tokens') and c.get('output_tokens')==n['usage'].get('completion_tokens') for c in metric.get('calls',[])) for n in native):candidates.append(metric)
    assert len(candidates)==1,'METRICS_AMBIGUOUS_OR_MISSING'
    metric=candidates[0]
    routed=[h for h in snapshot['p']['handles'] if h.get('kind')=='routing' and request in h.get('id','')]
    routing=[]
    for h in routed:
        rid=h['routing_id'];assert len(rid)==32 and all(c in '0123456789abcdef' for c in rid)
        path=R/'.iald_runtime/app_routing'/(rid+'.json');raw=path.read_bytes();record=json.loads(raw)
        assert record['id']==rid
        routing.append({'id':rid,'model':record.get('model'),'selected':record.get('selected'),'status':record['status'],'usage':record.get('usage'),'estimated_cost_usd':record.get('estimated_cost_usd'),'sha256':digest(raw)})
    cost=sum(c['cost_estimate_usd'] for c in metric['calls'])
    routing_cost=sum(r['estimated_cost_usd'] for r in routing) if routing and all(isinstance(r.get('estimated_cost_usd'),(int,float)) for r in routing) else None
    result={'status':'CAPTURED_TERMINAL','job':job,'done':done,'terminal_warnings':warnings,'text':text,'characters':len(text),'duration_seconds':job['updated']-job['created'],'tools':tools,
        'provider_real':metric['provider'],'model_real':metric['model'],'provider_verified_against_job_acom_wire':True,
        'usage':metric['calls'],'provider_cost_estimate_usd':cost,'routing':routing,'routing_cost_estimate_usd':routing_cost,
        'known_cost_estimate_usd':cost+routing_cost if routing_cost is not None else cost,
        'cost_scope':'Measured provider token usage priced with configured rates plus linked JEV estimate. Not invoice; moderation/other overhead not independently totalled. Metric matched by job-scoped ACOM wire model/usage and job time interval, not a direct metric job_id foreign key.',
        'metric_id':metric['id'],'metric_memory_sha256':metric.get('memory_sha256'),'metric_task':metric.get('task'),'metric_modality_counts':metric.get('modality_counts'),
        'acom':{'context_id':context,'request_id':request,'revision':row['revision'],'state_sha256':row['state_sha256'],'state_hash_verified':True,'latest_event_hash_matched':True,'response_matches_events':response_match,'custody':custody,'wire_artifacts':wires,'activity_handles':handles,'semantic_acceptance_inferred':False},
        'events':{'count':len(events),'max_seq':max(e['seq'] for e in events),'decrypted_values_concat_sha256':event_hash.hexdigest()},
        'read_only_runtime':True,'remote_calls':0,'retry':False,'adopted_context':False}
    if verification is not None:
        assert verification['runtime_science_sha256']==metric.get('memory_sha256')
        result['post_install_verification']=verification
    assert done and response_match
    temp=out.with_suffix('.json.tmp')
    with temp.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    assert json.loads(temp.read_bytes())['job']['id']==job_id
    temp.rename(out)
    return result

if __name__=='__main__':
    for which in JOBS:
        r=capture(which)
        print(json.dumps({'which':which,'job':r['job']['id'],'status':r['job']['status'],'warnings':len(r['terminal_warnings']),'provider':r['model_real'],'known_cost_estimate_usd':r['known_cost_estimate_usd'],'text':r['text']},ensure_ascii=False))
