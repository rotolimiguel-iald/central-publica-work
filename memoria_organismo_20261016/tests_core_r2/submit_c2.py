"""Submit the authored C2 candidate; genuine independent review stays separate."""
from pathlib import Path
import copy
import json
import sys
WORK=Path(__file__).resolve().parents[1];sys.path.insert(0,str(WORK))
from mission_io import call,save,pin,REFERENCE
actor={'kind':'agent','id':'codex-organism-core-projection-build'}
p,pr=call('mission_cli.py',{'operation':'project','reference':str(REFERENCE),'max_chars':125000},'C2_submit_sync')
task=next(t for t in p['projection']['active'] if t['id']=='C2')
assert task['status']=='working' and task['lease']['owner']==actor['id']
checked,cr=call('mission_cli.py',{'operation':'check','reference':str(REFERENCE),'actor':actor,
    'task_id':'C2','lease_id':task['lease']['id'],'expected_revision':p['receipt']['revision'],
    'projection_sha256':p['projection_sha256']},'C2_submit_preflight')
result,sr=call('mission_cli.py',{'operation':'submit','reference':str(REFERENCE),'actor':actor,
    'task_id':'C2','lease_id':task['lease']['id'],'expected_revision':p['receipt']['revision'],
    'projection_sha256':p['projection_sha256'],'event_id':'org-core-projection-submit-r1',
    'evidence':[pin(WORK/'CORE_C2_DELIVERY_R1.json')],
    'note':'Candidato C2:70 testes privados PASS,1/10/100 pending/reviewed medidos; apenas metadados mecânicos terminais indexados. JEV30k real ainda recusa10turnos; frente J separada. Sem instalação ou autoaceite.'},'C2_submit')
state,_=call('session_memory.py',{'operation':'get','reference':str(REFERENCE)},'C2_completed_handle_get')
handles=copy.deepcopy(state['p']['handles'])
handle=next(h for h in handles if h['id']=='org-core-projection-build')
assert handle['agent']==actor['id'] and handle['task_id']=='C2' and handle['status']=='running'
handle['status']='completed'
h,hr=call('session_memory.py',{'operation':'transition','reference':str(REFERENCE),'actor':actor,
    'expected_revision':state['revision'],'event_id':'org-core-projection-completed-r1',
    'changes':{'flow':{'handles':handles}}},'C2_handle_completed')
final,fr=call('mission_cli.py',{'operation':'project','reference':str(REFERENCE),'max_chars':125000},'C2_final_sync')
save(WORK/'CORE_C2_SUBMITTED_R1.json',{'reference':str(REFERENCE),'author':actor,
    'delivery':pin(WORK/'CORE_C2_DELIVERY_R1.json'),'preflight':pin(cr),'submit':pin(sr),
    'completed_handle':pin(hr),'final_projection':pin(fr),'revision':final['receipt']['revision'],
    'accepted':False,'installed':False})
print(json.dumps({'revision':final['receipt']['revision'],'submitted':result['task']['status'],
    'receipt':str(sr),'handle':'completed'}))
