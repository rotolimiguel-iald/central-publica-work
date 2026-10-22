"""Submit Q/R2 using its author and fresh CAS; never accept or install."""
import json,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W))
from mission_io import call,save,pin
A={'id':'codex-organism-queue-build','kind':'agent'}
ref=str(W/'SESSION_REFERENCE.json');delivery=W/'tests_queue/QUEUE_DELIVERY_R2.json'
d=json.loads(delivery.read_bytes());plan=json.loads(Path(d['installation_plan']['path']).read_bytes())
for item in [d['installation_plan'],d['api'],d['tests'],d['mcp_stdio']]:assert pin(item['path'])==item
for item in plan['files']:
    assert pin(item['source']['path'])=={k:item['source'][k] for k in ('path','sha256')}
for item in plan['required_core']:assert pin(item['path'])=={k:item[k] for k in ('path','sha256')}
p,pr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'q_r2_submit_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q')
assert t['status']=='working' and t['lease']['owner']==A['id']
c={'reference':ref,'actor':A,'task_id':'Q','lease_id':t['lease']['id'],'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
_,ck=call('mission_cli.py',dict(c,operation='check'),'q_r2_submit_check')
_,sr=call('mission_cli.py',dict(c,operation='submit',event_id='organism-Q-submit-r2',
    evidence=[pin(delivery),d['installation_plan'],d['api'],d['tests'],d['mcp_stdio']]+[pin(x['source']['path']) for x in plan['files']],
    note='Candidata Q R2: 29 testes privados e MCP real privado. Custodia precede freshness; R1 preservada. Sem autoaceite ou instalacao; V devera usar C2 final.'),'q_r2_submit')
state,gr=call('session_memory.py',{'operation':'get','reference':ref,'actor':A},'q_r2_handle_finish_get')
h=next(x for x in state['p']['handles'] if x['id']=='org-queue-build')
assert h['task_id']=='Q' and h['agent']=='/root/mission_memory_review'
h.update(status='completed',no_repeat=True,result_evidence=[pin(delivery)],completion_scope='construction_submitted_not_accepted')
_,hr=call('session_memory.py',{'operation':'transition','reference':ref,'actor':A,'expected_revision':state['revision'],
    'event_id':'organism-Q-build-completed-r2','changes':{'flow':{'handles':[h]}}},'q_r2_handle_completed')
p,fr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'q_r2_return_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q');assert t['status']=='review_pending'
out=W/'tests_queue/QUEUE_SUBMITTED_R2.json'
save(out,{'reference':ref,'actor':A,'requirement':'Q','status':t['status'],'revision':p['receipt']['revision'],
    'delivery':pin(delivery),'receipts':[pin(x) for x in [pr,ck,sr,gr,hr,fr]],'accepted':False,'installed':False})
print(json.dumps({'receipt':pin(out),'revision':p['receipt']['revision'],'status':t['status']},ensure_ascii=False))
