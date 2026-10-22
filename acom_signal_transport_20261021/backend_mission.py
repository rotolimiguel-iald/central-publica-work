import json,subprocess,hashlib
from pathlib import Path
W=Path(__file__).resolve().parent
REF=str(W/'SESSION_REFERENCE.json');ACTOR={'id':'codex-transport-backend','kind':'agent'}
def call(req):
    req['reference']=REF
    out=json.loads(subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(req),capture_output=True,text=True).stdout)
    if not out.get('ok'):raise RuntimeError(out)
    return out['result']
def project():return call({'operation':'project','max_chars':30000})
def mutate(p,operation,event_id,**kw):return call(dict(operation=operation,actor=ACTOR,event_id=event_id,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],**kw))
if __name__=='__main__':
    p=project();task='backend_integration'
    tasks=p['projection']['active']+p['projection']['settled']
    if not any(t['id']==task for t in tasks):
        source=W/'CONTINUE_20261021.txt'
        mutate(p,'extend','backend-integration-extend-r1',reason='Continuação humana autoriza integração backend isolada para revisão, sem runtime.',sources=[dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest())],requirements=[dict(id=task,criterion='Backend staging interoperável com capabilities/decode/AV/page e testes Flask isolados, legado preservado, limites/concorrência/hash, zero provedores; revisão distinta antes de instalar.',depends_on=[])])
        p=project()
    t=next(t for t in p['projection']['active'] if t['id']==task)
    if t['status'] in ['open','needs_revalidation']:
        mutate(p,'claim','backend-integration-claim-r1',task_id=task,lease_seconds=7200);p=project();t=next(t for t in p['projection']['active'] if t['id']==task)
    assert t['lease']['owner']==ACTOR['id']
    check=call(dict(operation='check',task_id=task,actor=ACTOR,lease_id=t['lease']['id'],expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256']))
    d=W/'integration'/'backend';d.mkdir(parents=True,exist_ok=True)
    (d/'MISSION_PREFLIGHT.json').write_text(json.dumps(dict(actor=ACTOR,task_id=task,lease_id=t['lease']['id'],project=p,check=check),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(task_id=task,revision=p['receipt']['revision'],check=check)))
