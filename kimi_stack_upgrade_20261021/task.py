"""Local mission client: explicit reference, fresh revision and real caller actor."""
from pathlib import Path
import hashlib,json,subprocess,uuid,sys
W=Path(__file__).resolve().parent; PY=r'C:\Python314\python.exe';REF=W/'SESSION_REFERENCE.json'
UNIT='F9.9.TURBINA_20261020';OWNER='codex-app-01a094df'
def call(payload,mission=True):
    p=subprocess.run([PY,'-B','-X','utf8',str(Path(r'C:\IALD\MEMORIA_IALD')/('mission_cli.py' if mission else 'session_memory.py'))],input=json.dumps(payload,ensure_ascii=False).encode(),capture_output=True)
    d=json.loads(p.stdout)
    if p.returncode or not d['ok']:raise RuntimeError(d)
    return d['result']
def project():return call({'operation':'project','reference':str(REF),'max_chars':100000})
def act(op,actor=OWNER,**kw):
    current=(call({'operation':'project','reference':str(REF),'max_chars':100000},False) if op=='configure' else project())
    req={'operation':op,'reference':str(REF),'actor':{'id':actor,'kind':'agent'},'expected_revision':current['receipt']['revision'],'projection_sha256':current['projection_sha256'],**kw}
    return call(req)
def check(task,actor=OWNER):
    p=project();t=next(x for x in p['projection']['active'] if x['id']==task)
    return call({'operation':'check','reference':str(REF),'actor':{'id':actor,'kind':'agent'},'task_id':task,'lease_id':t['lease']['id'],'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'max_chars':100000})
def new(name,value):
    raw=value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False,indent=2).encode()
    with (W/name).open('xb') as f:f.write(raw)
    assert (W/name).read_bytes()==raw
