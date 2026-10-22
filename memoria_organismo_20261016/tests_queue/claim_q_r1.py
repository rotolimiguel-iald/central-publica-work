import importlib.util,json
from pathlib import Path
W=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('queue_io',W/'mission_io.py');io=importlib.util.module_from_spec(s);s.loader.exec_module(io)
A={'id':'codex-organism-queue-build','kind':'agent'}
ref=str(W/'SESSION_REFERENCE.json')
p,r=io.call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'queue_claim_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q')
assert t['status']=='open' and t['ready']
claim,cr=io.call('mission_cli.py',{'operation':'claim','reference':ref,'actor':A,'task_id':'Q','lease_seconds':43200,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'event_id':'organism-Q-claim-r1'},'queue_claim')
p,r=io.call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'queue_claimed_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q')
check,ck=io.call('mission_cli.py',{'operation':'check','reference':ref,'actor':A,'task_id':'Q','lease_id':t['lease']['id'],'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']},'queue_preflight')
state,gr=io.call('session_memory.py',{'operation':'get','reference':ref,'actor':A},'queue_handle_get')
assert not any(h['id']=='org-queue-build' for h in state['p']['handles'])
event={'operation':'transition','reference':ref,'actor':A,'expected_revision':state['revision'],'event_id':'organism-Q-handle-running-r1','changes':{'flow':{'handles':[{'id':'org-queue-build','kind':'agent','agent':'/root/mission_memory_review','actor':A['id'],'task_id':'Q','status':'running','no_repeat':True}]}}}
done,dr=io.call('session_memory.py',event,'queue_handle_running')
io.save(W/'tests_queue/Q_CLAIM_R1.json',{'actor':A,'lease':t['lease'],'claim':io.pin(cr),'check':io.pin(ck),'handle':io.pin(dr),'revision':done['revision']})
print(json.dumps({'claim':io.pin(W/'tests_queue/Q_CLAIM_R1.json'),'lease':t['lease'],'handle_receipt':str(dr)},ensure_ascii=False))
