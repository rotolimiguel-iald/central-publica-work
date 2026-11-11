import json, subprocess, sys, hashlib
from pathlib import Path
W=Path(__file__).resolve().parent
REF=str(W/'SESSION_REFERENCE.json')
ACTOR={'id':'codex-f03-v409-staging','kind':'agent'}
def call(op, mission=True, **kw):
    req=dict(operation=op,reference=REF,**kw)
    p=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8','C:/IALD/MEMORIA_IALD/'+('mission_cli.py' if mission else 'session_memory.py')],input=json.dumps(req).encode(),capture_output=True)
    r=json.loads(p.stdout)
    if not r.get('ok'): raise RuntimeError(r)
    return r['result']
def save(name,obj):
    p=W/name
    if p.exists(): raise ValueError('Already exists: '+name)
    raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(raw)
    assert t.read_bytes()==raw
    t.replace(p)
if __name__=='__main__':
    print(json.dumps(call('project',False),ensure_ascii=False))
    r=call('configure',actor=ACTOR,expected_revision=0,event_id='v409-staging-configure',requirements=[{'id':'staging','criterion':'Snapshot documental v409 isolado:13 fontes e todos os trechos/linhas/hashes conferidos, plano concreto de promoção protegida; revisão independente e autorização permanecem pendentes.','depends_on':[]}],sources=[{'path':str(W/'ORIGINAL.txt'),'sha256':hashlib.sha256((W/'ORIGINAL.txt').read_bytes()).hexdigest()}])
    p=call('project')
    r=call('claim',actor=ACTOR,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],event_id='v409-staging-claim',task_id='staging',lease_seconds=14400)
    p=call('project')
    print(json.dumps(p,ensure_ascii=False))
    save('CLAIM_MISSION.json',r)
