"""Authorized submit N under its constructor; no acceptance or installation."""
from pathlib import Path
import json,sys
WORK=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(WORK))
from mission_io import call,save,pin,REFERENCE

actor={'id':'codex-organism-native-build','kind':'agent'}
delivery=WORK/'NATIVE_DELIVERY_R1.json'
d=json.loads(delivery.read_text(encoding='utf-8'))
for item in d['implementation']+[d['unchanged_supplier'],d['hooks'],d['tests']]:assert pin(item['path'])==item
receipts=[]
for attempt in range(4):
    p,pr=call('mission_cli.py',{'operation':'project','reference':str(REFERENCE),'max_chars':125000},'native_submit_project')
    task=next(t for t in p['projection']['active'] if t['id']=='N')
    assert task['status']=='working' and task['lease']['owner']==actor['id']
    common={'reference':str(REFERENCE),'actor':actor,'task_id':'N','lease_id':task['lease']['id'],
            'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256']}
    try:
        _,checked=call('mission_cli.py',dict(common,operation='check'),'native_submit_check')
        _,submitted=call('mission_cli.py',dict(common,operation='submit',event_id='organism-native-N-submit-r1',
            evidence=[pin(delivery),d['tests'],d['hooks'],d['unchanged_supplier']]+d['implementation'],
            note='Candidata N em staging; 20 testes privados incluindo hooks reais/Binding em snapshot de A. Sem aceite/instalação/provedor.'),'native_submit')
        receipts.extend([pr,checked,submitted]);break
    except RuntimeError as exc:
        if not any(s in str(exc) for s in ['stale_revision','RevisionConflict']):raise
else:raise RuntimeError('Concurrent submit changes require explicit reconciliation')
for attempt in range(4):
    snap,g=call('session_memory.py',{'operation':'get','reference':str(REFERENCE)},'native_finish_get')
    handles=snap['p']['handles']
    h=next(h for h in handles if h['id']=='org-native-build')
    assert h['task_id']=='N' and h['agent']=='/root/maxwell_covariance_review'
    h.update(status='completed',no_repeat=True,result_evidence=[pin(delivery)],completion_scope='construction_submitted_not_accepted')
    try:
        _,done=call('session_memory.py',{'operation':'transition','reference':str(REFERENCE),'actor':actor,
            'expected_revision':snap['revision'],'event_id':'organism-native-build-handle-completed-r1',
            'changes':{'flow':{'handles':handles}}},'native_handle_completed')
        receipts.extend([g,done]);break
    except RuntimeError as exc:
        if 'RevisionConflict' not in str(exc):raise
else:raise RuntimeError('Concurrent handle changes require explicit reconciliation')
final,r=call('mission_cli.py',{'operation':'project','reference':str(REFERENCE),'max_chars':125000},'native_return_project')
receipts.append(r)
task=next(t for t in final['projection']['active'] if t['id']=='N')
assert task['status']=='review_pending'
save(WORK/'NATIVE_SUBMITTED_R1.json',{'reference':str(REFERENCE),'actor':actor,'requirement':'N',
    'status':'review_pending','revision':final['receipt']['revision'],'delivery':pin(delivery),
    'receipts':[pin(r) for r in receipts],'accepted':False,'installed':False})
print(json.dumps({'revision':final['receipt']['revision'],'status':'review_pending',
                  'receipt':pin(WORK/'NATIVE_SUBMITTED_R1.json')}))
