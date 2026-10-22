import sys,json
from pathlib import Path
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W))
from mission_io import call,save,pin
A={'id':'codex-organism-legacy-migration-build','kind':'agent'};ref=str(W/'SESSION_REFERENCE.json')
p,pr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'q2_claim_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q2');assert t['status']=='open' and t['ready']
_,cr=call('mission_cli.py',{'operation':'claim','reference':ref,'actor':A,'task_id':'Q2','lease_seconds':43200,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'event_id':'organism-Q2-claim-r1'},'q2_claim')
p,pr=call('mission_cli.py',{'operation':'project','reference':ref,'actor':A,'max_chars':125000},'q2_claimed_project')
t=next(x for x in p['projection']['active'] if x['id']=='Q2')
_,ck=call('mission_cli.py',{'operation':'check','reference':ref,'actor':A,'task_id':'Q2','lease_id':t['lease']['id'],'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']},'q2_preflight')
state,gr=call('session_memory.py',{'operation':'get','reference':ref,'actor':A},'q2_handle_get')
assert not any(x['id']=='org-legacy-migration-build' for x in state['p']['handles'])
_,hr=call('session_memory.py',{'operation':'transition','reference':ref,'actor':A,'expected_revision':state['revision'],'event_id':'organism-Q2-handle-running-r1','changes':{'flow':{'handles':[{'id':'org-legacy-migration-build','kind':'agent','agent':'/root/mission_memory_review','actor':A['id'],'task_id':'Q2','status':'running','no_repeat':True}]}}},'q2_handle_running')
save(W/'tests_queue/Q2_CLAIM_R1.json',{'actor':A,'lease':t['lease'],'receipts':[pin(x) for x in [pr,cr,ck,gr,hr]]})
print(json.dumps({'receipt':pin(W/'tests_queue/Q2_CLAIM_R1.json'),'lease':t['lease']},ensure_ascii=False))
