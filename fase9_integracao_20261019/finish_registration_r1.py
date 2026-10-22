"""Recover only the read-only handoff; all successful registrations stay intact."""
from setup_mission import ROOT,REF,UNIT,ACTOR,pin,save,call
import json
for n in ['MEMORY_APPLIED_R1.json','MAP_REGISTER_R1.json','BOARD_PROGRESS_R1.json','TRANSITION_R1.json']:
    assert (ROOT/n).is_file(),n
projection=call('PROJECT_AFTER_REGISTER_R1.json',{'operation':'project','reference':REF,'max_chars':50000})
task=next(t for t in projection['projection']['active'] if t['id']=='R1')
h=call('HANDOFF_VALID_R1.json',{'operation':'handoff','reference':REF,'actor':ACTOR,
       'expected_revision':projection['receipt']['revision'],'projection_sha256':projection['projection_sha256'],
       'task_id':'R1','lease_id':task['lease']['id'],'max_chars':50000})
saved=json.loads((ROOT/'TRANSITION_R1.json').read_text(encoding='utf-8'))
transition=json.loads(saved['stdout'])['result']
save('REGISTRATION_R1.json',{'status':'PARTIAL_PROGRESS_REGISTERED','unit':UNIT,
     'progress':pin(ROOT/'PROGRESS_R1.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R1.json'),
     'map':pin(ROOT/'MAP_REGISTER_R1.json'),'board':pin(ROOT/'BOARD_PROGRESS_R1.json'),
     'acom':transition,'handoff':pin(ROOT/'HANDOFF_VALID_R1.json'),
     'administrative_correction':'Initial read-only handoff lacked revision/projection/lease and was refused. Successful memory/map/board/ACOM writes were not repeated. Corrected handoff supplied current R1 lease.',
     'failed_handoff':pin(ROOT/'HANDOFF_REGISTER_R1.json'),'scripts':[pin(ROOT/'register_progress_r1.py'),pin(__file__)]})
print(json.dumps({'status':'PARTIAL_PROGRESS_REGISTERED','revision':transition['revision'],
 'map_seq':1248,'board_event':1038,'receipt':pin(ROOT/'REGISTRATION_R1.json')},ensure_ascii=False))
