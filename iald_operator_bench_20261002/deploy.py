from contextlib import closing
from datetime import datetime,timezone
from pathlib import Path
import ast,hashlib,http.client,json,os,sqlite3,sys

W=Path(__file__).parent;S=W/'stage';R=Path(r'C:\IALD\projetos_pyhton\IALD')
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def atomic(path,raw):
    temp=path.with_name(path.name+'.tmp_bench_'+str(os.getpid()))
    with temp.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    assert raw and temp.read_bytes()==raw
    os.replace(temp,path);assert path.read_bytes()==raw

def backup(path,stamp):
    raw=path.read_bytes();dest=path.with_name(path.name+'.bak_'+stamp)
    with dest.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    assert dest.read_bytes()==raw
    return str(dest)

def quiet():
    for path,query in [(R/'.iald_runtime/chat_jobs/jobs.sqlite3',"SELECT COUNT(*) FROM jobs WHERE status IN ('queued','running')"),
         *[(p,"SELECT COUNT(*) FROM calls WHERE status='reserved'") for p in [*R.glob('*.reservas.sqlite3'),R/'.iald_runtime/app_evaluation/public_spend.sqlite3']]]:
        if path.is_file():
            with closing(sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)) as db:
                assert db.execute(query).fetchone()[0]==0,'Active work; postpone app restart'
    return {'active_jobs':0,'reserved_provider_calls':0}

def get(port,path):
    conn=http.client.HTTPConnection('127.0.0.1',port,timeout=20)
    try:
        conn.request('GET',path);resp=conn.getresponse();raw=resp.read(4*1024**2)
        assert resp.status==200
        return json.loads(raw)
    finally:conn.close()

def snapshot():
    gw=get(18765,'/api/universe/status');co=get(18766,'/api/cosmology/status')
    series=sorted((r['id'],r['strain_array_sha256']) for r in gw.get('series',[]))
    return {'gw':{k:gw.get(k) for k in ('status','domain','load_id','generation','loaded_files','total_files','resident_bytes','worker_pid','errors')},
            'strain_arrays_sha256':sha(json.dumps(series,sort_keys=True).encode()),
            'cosmos':{**{k:co.get(k) for k in ('status','engine_generation')},
                      **{k:co.get('memory',{}).get(k) for k in ('load_id','loaded_source_bytes','source_reads_total')}}}

def prepare():
    files=sorted(p.name for p in S.glob('iald_*.py'))
    base=json.loads((S/'integration_baseline.json').read_bytes())
    # Baseline schema is captured by the integration agent before any stage copy.
    base=base.get('files',base)
    records={}
    for name in files:
        raw=(S/name).read_bytes();ast.parse(raw)
        previous=(R/name).read_bytes() if (R/name).exists() else None
        if name in base:
            expected=base[name]
            if type(expected)is dict:expected=expected.get('sha256',expected.get('baseline_sha256'))
            assert sha(previous)==expected,('Production changed',name)
        elif previous is not None:
            raise AssertionError('New module unexpectedly exists: '+name)
        records[name]={'baseline':sha(previous) if previous is not None else None,'stage':sha(raw),'bytes':len(raw)}
    data={'files':records,'quiet':quiet(),'bench_before':snapshot(),'prepared_at':datetime.now(timezone.utc).isoformat()}
    if (W/'prepared.json').exists():backup(W/'prepared.json',datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    atomic(W/'prepared.json',json.dumps(data,indent=2).encode());print(json.dumps({'files':len(files),'quiet':data['quiet'],'bench_before':data['bench_before']}))

def install():
    assert not (W/'deployment.json').exists(),'Already installed; inspect receipt instead of repeating'
    prepared=json.loads((W/'prepared.json').read_bytes())
    checks=json.loads((W/'validation/final_checks.json').read_bytes());assert checks['passed']
    assert checks['stage_sha256']=={n:v['stage'] for n,v in prepared['files'].items()},'Checks do not cover this stage'
    assert (W/'validation/review_final.txt').is_file(),'Independent closure required'
    quiet();stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');old={};new={};backups={}
    for name,pin in prepared['files'].items():
        path=R/name;current=path.read_bytes() if path.exists() else None
        assert (sha(current) if current is not None else None)==pin['baseline'],('Concurrent file edit',name)
        raw=(S/name).read_bytes();assert sha(raw)==pin['stage'];ast.parse(raw)
        old[name]=current;new[name]=raw
        if current is not None:backups[name]=backup(path,stamp)
    userpath=R/'iald_users.json';oldusers=userpath.read_bytes();users=json.loads(oldusers)
    assert users['luiz'].get('admin') is True and not users['luiz'].get('bloqueado') and not users['luiz'].get('acesso_bloqueado')
    assert not any(k!='luiz' and v.get('classe_usuario')=='operador' for k,v in users.items())
    before=json.loads(oldusers);users['luiz']['classe_usuario']='operador'
    newusers=json.dumps(users,ensure_ascii=False,indent=2).encode()
    backups['iald_users.json']=backup(userpath,stamp)
    for name,raw in new.items():
        path=R/name
        assert (path.read_bytes() if path.exists() else None)==old[name]
        atomic(path,raw)
    assert userpath.read_bytes()==oldusers,'Concurrent account change; modules installed, role not modified'
    atomic(userpath,newusers)
    after=json.loads(userpath.read_bytes());original_luiz=dict(before['luiz']);original_luiz['classe_usuario']='operador'
    assert after['luiz']==original_luiz and {k:v for k,v in after.items() if k!='luiz'}=={k:v for k,v in before.items() if k!='luiz'}
    data={'installed_at':datetime.now(timezone.utc).isoformat(),'files':prepared['files'],'backups':backups,
          'operator_accounts':['luiz'],'other_accounts_unchanged':True,'billing_and_model_permissions_unchanged':True,
          'client_files_changed':False,'provider_calls':0,'bench_services_restarted':False,'web_restart_required':True}
    atomic(W/'deployment.json',json.dumps(data,indent=2).encode());print(json.dumps({'installed_files':len(new),'operator':'luiz','web_restart_required':True}))

if __name__=='__main__':
    {'prepare':prepare,'install':install,'quiet':lambda:print(json.dumps(quiet())),
     'snapshot':lambda:print(json.dumps(snapshot()))}[sys.argv[1]]()
