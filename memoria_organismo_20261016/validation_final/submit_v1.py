"""Submit delegated V under the actual builder identity; independent acceptance remains pending."""
from pathlib import Path
import json,sys
V=Path(__file__).resolve().parent;W=V.parent
sys.path.insert(0,str(W))
from mission_io import project,call,pin,save,REFERENCE
actor={'id':'codex-organism-integration-build','kind':'agent'}
lease='bc9cc5e9-fcb0-4376-a656-11169de7edeb'
x,start=project()
task=next(t for t in x['projection']['active'] if t['id']=='V')
assert task['lease']['owner']==actor['id'] and task['lease']['id']==lease
base={'reference':str(REFERENCE),'actor':actor,'task_id':'V','lease_id':lease,
      'expected_revision':x['receipt']['revision'],'projection_sha256':x['projection_sha256']}
_,checked=call('mission_cli.py',{**base,'operation':'check'},'V_final_check_r1')
paths=[V/n for n in ['V_DELIVERY_R1.json','ASSEMBLY_PROVENANCE_R1.json','COVERAGE_MATRIX_R1.json',
    'PRESERVATION_R1.json','PROCESS_CORE_PROVENANCE_R1.json','consolidate_v1.py','consolidate_v2.py']]
_,submitted=call('mission_cli.py',{**base,'operation':'submit','event_id':'organism-V-submit-r1',
    'evidence':[pin(p) for p in paths],
    'note':'DECLARADO: integração privada final, 70core+20native+44queue+23app+13J e 7 verificações MCP local. Fontes aceitas intactas; sem inferência, contas reais ou instalação. Revisão independente da raiz pendente.'},'V_submit_r1')
x,after=project()
_,handle=call('session_memory.py',{'operation':'transition','reference':str(REFERENCE),'actor':actor,
    'expected_revision':x['receipt']['revision'],'event_id':'organism-V-handle-returned-r1',
    'changes':{'flow':{'handles':[{'id':'org-integration-build','kind':'agent','task_id':'V',
        'agent':'/root/fock_r6_review','status':'returned','no_repeat':True,
        'evidence':pin(V/'V_DELIVERY_R1.json')}]}}},'V_handle_returned_r1')
x,last=project()
report={'status':'DECLARADO_REVIEW_PENDING','reference':str(REFERENCE),'actor':actor,
    'revision':x['receipt']['revision'],'start_project':pin(start),'check':pin(checked),
    'submit':pin(submitted),'handle':pin(handle),'project':pin(last),'delivery':pin(V/'V_DELIVERY_R1.json')}
save(V/'V_SUBMISSION_R1.json',report)
print(json.dumps(report,ensure_ascii=False))
