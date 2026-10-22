"""Resume exact mission after accepted memory E2; preserve all handles."""
import sys, json, time
from pathlib import Path
sys.path.insert(0, str(Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\mission_resume_20261016')))
import live_mission_r39 as live

p,_=live.project()
source=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\terminal_projection_e2\FINAL_E2.json')
import hashlib
sources=[{'path':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]
for tid in ['R5']:
    t=next(t for t in p['projection']['active'] if t['id']==tid)
    if t['lease'] and t['lease']['expires_at'] < time.time():
        live.call('mission_cli.py',dict(operation='release',reference=str(live.REFERENCE),actor=live.ACTOR,
            task_id=tid,lease_id=t['lease']['id'],expected_revision=p['receipt']['revision'],
            projection_sha256=p['projection_sha256'],event_id='r43-release-expired-'+tid,
            reason='Prior build terminal and preserved in R42; lease expired during memory E2. No scientific criterion accepted.',sources=sources), 'R43_RELEASE_'+tid)
        p,_=live.project()
t=next(t for t in p['projection']['active'] if t['id']=='R4')
if t['lease'] is None:
    live.call('mission_cli.py',dict(operation='claim',reference=str(live.REFERENCE),actor=live.ACTOR,
        task_id='R4',expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],
        event_id='r43-claim-R4',lease_seconds=7200),'R43_CLAIM_R4')
s,_=live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)), 'R43_FULL_GET')
handles=s['p']['handles']
for hid,tid in [('r43-r7-conversion-fix','R7'),('r43-r8-null-schwartz-fix','R8')]:
    assert not any(h['id']==hid for h in handles)
    handles.append(dict(id=hid,kind='agent',task_id=tid,status='running',no_repeat=True))
live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),actor=live.ACTOR,
    expected_revision=s['revision'],event_id='r43-resume-science',changes=dict(flow=dict(handles=handles,
    phase='science_r43_after_memory_acceptance',next_action='Repair measured R7 Star inference and R8 ContDiff/PiLp failures; root investigates R4 physical clock using current inventory. Preserve full criteria and accepted M0/M1/M2.'))),'R43_RESUME')
for tid in ['R7','R8','R4']:
    p,_=live.project();t=next(t for t in p['projection']['active'] if t['id']==tid)
    _,receipt=live.call('mission_cli.py',dict(operation='handoff',reference=str(live.REFERENCE),actor=live.ACTOR,
        task_id=tid,lease_id=t['lease']['id'],expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256'],max_chars=100000),'R43_HANDOFF_'+tid)
    print(json.dumps({'task_id':tid,'handoff':str(receipt)}))
