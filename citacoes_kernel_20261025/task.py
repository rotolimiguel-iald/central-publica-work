from pathlib import Path
import json,hashlib,subprocess
W=Path(__file__).resolve().parent
PY=r'C:\Python314\python.exe'
REF=W/'SESSION_REFERENCE.json'
OWNER='codex-gerente-tgl'
UNIT='F1.CITACOES_20261025'
def pin(p): return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def new(name,data):
    with (W/name).open('xb') as f: f.write(json.dumps(data,ensure_ascii=False,indent=2).encode())
def call(d,mission=True):
    r=subprocess.run([PY,'-B','-X','utf8',str(Path(r'C:\IALD\MEMORIA_IALD') /('mission_cli.py' if mission else 'session_memory.py'))],input=json.dumps(d).encode(),capture_output=True)
    v=json.loads(r.stdout)
    if r.returncode or not v['ok']: raise RuntimeError(v)
    return v['result']
def project(): return call({'operation':'project','reference':str(REF),'max_chars':100000})
def act(op,**kw):
    p=call({'operation':'project','reference':str(REF),'max_chars':100000},False) if op=='configure' else project()
    return call({'operation':op,'reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],**kw})
def check(tid):
    t=next(t for t in project()['projection']['active'] if t['id']==tid)
    return act('check',task_id=tid,lease_id=t['lease']['id'])
