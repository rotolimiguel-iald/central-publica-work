"""Refresh R8 ownership and issue two bounded, synchronized followups."""
from pathlib import Path
import sys,json,hashlib
OUT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
sys.path.insert(0,str(OUT/'mission_resume_20261016'))
import live_mission_r39 as live
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
source=OUT/'maxwell_global/NULL_SCHWARTZ_CORE_CUSTODY_R43.json'
p,_=live.project();t=next(t for t in p['projection']['active'] if t['id']=='R8')
live.call('mission_cli.py',dict(operation='release',reference=str(live.REFERENCE),actor=live.ACTOR,
 task_id='R8',lease_id=t['lease']['id'],expected_revision=p['receipt']['revision'],
 projection_sha256=p['projection_sha256'],event_id='r43-r8-release-for-continuation',
 reason='Prior R8 builds terminal and candidates returned; renew ownership for measured S4 repair and independent component review.',sources=[pin(source)]),'R43_R8_RELEASE')
p,_=live.project()
live.call('mission_cli.py',dict(operation='claim',reference=str(live.REFERENCE),actor=live.ACTOR,
 task_id='R8',expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'],
 event_id='r43-r8-continuation-claim',lease_seconds=7200),'R43_R8_CLAIM')
s,_=live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)),'R43_FOLLOWUP_GET')
handles=s['p']['handles']
for hid in ['r43-r8-s4-repair','r43-r8-s1s3-review']:
 assert not any(h['id']==hid for h in handles)
 handles.append(dict(id=hid,kind='agent',task_id='R8',status='running',no_repeat=True))
live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),actor=live.ACTOR,
 expected_revision=s['revision'],event_id='r43-s4-repair-and-core-review',changes=dict(flow=dict(handles=handles))), 'R43_FOLLOWUPS')
p,_=live.project();t=next(t for t in p['projection']['active'] if t['id']=='R8')
_,r=live.call('mission_cli.py',dict(operation='handoff',reference=str(live.REFERENCE),actor=live.ACTOR,
 task_id='R8',lease_id=t['lease']['id'],expected_revision=p['receipt']['revision'],
 projection_sha256=p['projection_sha256'],max_chars=100000),'R43_R8_FOLLOWUP_HANDOFF')
print(json.dumps({'handoff':str(r),'revision':p['receipt']['revision']}))
