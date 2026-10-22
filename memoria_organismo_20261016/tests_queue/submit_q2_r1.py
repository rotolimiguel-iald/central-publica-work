"""Submit Q2/R1 using its author and fresh CAS; never accept or install."""
import json,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W))
from mission_io import call,save,pin
A={'id':'codex-organism-legacy-migration-build','kind':'agent'}
ref=str(W/'SESSION_REFERENCE.json');delivery=W/'tests_queue/Q2_DELIVERY_R1.json'
d=json.loads(delivery.read_bytes());plan=json.loads(Path(d['installation_plan']['path']).read_bytes())
for item in [d['installation_plan'],d['api'],d['tests']]:assert pin(item['path'])==item
for item in plan['files']:
    assert pin(item['source']['path'])=={k:item['source'][k] for k in ('path','sha256')}
for item in plan['core_pins']:assert pin(item['path'])=={k:item[k] for k in ('path','sha256')}
p,pr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'q2_r1_submit_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q2')
assert t['status']=='working' and t['lease']['owner']==A['id']
c={'reference':ref,'actor':A,'task_id':'Q2','lease_id':t['lease']['id'],'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
_,ck=call('mission_cli.py',dict(c,operation='check'),'q2_r1_submit_check')
_,sr=call('mission_cli.py',dict(c,operation='submit',event_id='organism-Q2-submit-r2',
    evidence=[pin(delivery),d['installation_plan'],d['api'],d['tests']]+[pin(x['source']['path']) for x in plan['files']],
    note='Candidata Q2: 44 testes privados, CLI novo, migracao local idempotente com CAS e intencoes. Zero migracoes reais, provedores ou autoaceite. V devera usar C2 final.'),'q2_r1_submit')
state,gr=call('session_memory.py',{'operation':'get','reference':ref,'actor':A},'q2_r1_handle_finish_get')
h=next(x for x in state['p']['handles'] if x['id']=='org-legacy-migration-build')
assert h['task_id']=='Q2' and h['agent']=='/root/mission_memory_review'
h.update(status='completed',no_repeat=True,result_evidence=[pin(delivery)],completion_scope='construction_submitted_not_accepted')
_,hr=call('session_memory.py',{'operation':'transition','reference':ref,'actor':A,'expected_revision':state['revision'],
    'event_id':'organism-Q2-build-completed-r2','changes':{'flow':{'handles':[h]}}},'q2_r1_handle_completed')
p,fr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'q2_r1_return_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q2');assert t['status']=='review_pending'
out=W/'tests_queue/Q2_SUBMITTED_R1.json'
save(out,{'reference':ref,'actor':A,'requirement':'Q2','status':t['status'],'revision':p['receipt']['revision'],
    'delivery':pin(delivery),'receipts':[pin(x) for x in [pr,ck,sr,gr,hr,fr]],'accepted':False,'installed':False})
print(json.dumps({'receipt':pin(out),'revision':p['receipt']['revision'],'status':t['status']},ensure_ascii=False))
