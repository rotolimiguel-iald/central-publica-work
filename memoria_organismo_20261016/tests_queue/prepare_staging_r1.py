import hashlib,json,os,uuid
from pathlib import Path
W=Path(__file__).resolve().parents[1]
B=Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
S=W/'staging/queue'
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def publish(p,data):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
 with t.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==data;os.rename(t,p)
files=list((B/'iald_orchestrator').glob('*.py'))+[B/'transport_cli.py',B/'mcp_server.py']
baseline=[]
for src in files:
 assert src.name not in {'iald_stack_v7.py','iald_psion_state.json','.env'}
 dst=S/src.relative_to(B);publish(dst,src.read_bytes());baseline.append({'source':pin(src),'staged':str(dst)})
publish(W/'tests_queue/QUEUE_BASELINE_R1.json',(json.dumps({'base':str(B),'files':baseline,'core':[pin(W/'staging/core/lib/iald_memory'/n) for n in ('activity.py','mission.py','store.py')],'production_writes':False},ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'files':len(files),'baseline':pin(W/'tests_queue/QUEUE_BASELINE_R1.json')}))
