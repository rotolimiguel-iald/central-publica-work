"""Recover exact mission, custody returned work and refresh the existing R8 lease."""
from pathlib import Path
import copy
import hashlib
import json
import sys

OUT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live

def pin(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    manifest = OUT / 'maxwell_global/PHYSICAL_MAXWELL_JOINT_CANDIDATES_R52_R2.json'
    terminal = OUT / 'orbital_rotation/attempts/20261016T211151_421554Z/RECEIPT.json'
    assert json.loads(terminal.read_bytes())['exit_code'] == 0
    # Required raw ACOM projection on resumption, kept as a receipt rather than printed.
    live.call('session_memory.py', dict(operation='project', reference=str(live.REFERENCE),
        max_chars=1000000), 'R52_SESSION_REANCHOR')
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R52_JOINT_GET')
    handles = copy.deepcopy(state['p']['handles'])
    h = next(x for x in handles if x['id'] == 'r52-maxwell-joint-consumer')
    assert h['status'] == 'running'
    h.update(status='returned', receipt=pin(manifest), verified_build=pin(terminal))
    live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=state['revision'], event_id='r52-joint-candidate-returned',
        changes=dict(flow=dict(handles=handles))), 'R52_JOINT_RETURNED')
    p, _ = live.project()
    task = next(t for t in p['projection']['active'] if t['id'] == 'R8')
    live.call('mission_cli.py', dict(operation='release', reference=str(live.REFERENCE), actor=live.ACTOR,
        task_id='R8', lease_id=task['lease']['id'], expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256'], event_id='r52-r8-refresh-release',
        reason='Circular transport compiled and author returned joint candidate. Refresh ownership for final consumer and independent review.',
        sources=[pin(manifest), pin(terminal)]), 'R52_R8_RELEASE')
    p, _ = live.project()
    live.call('mission_cli.py', dict(operation='claim', reference=str(live.REFERENCE), actor=live.ACTOR,
        task_id='R8', expected_revision=p['receipt']['revision'], projection_sha256=p['projection_sha256'],
        event_id='r52-r8-final-consumer-claim', lease_seconds=7200), 'R52_R8_CLAIM')
    p, _ = live.project()
    task = next(t for t in p['projection']['active'] if t['id'] == 'R8')
    _, receipt = live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE), actor=live.ACTOR,
        task_id='R8', lease_id=task['lease']['id'], expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256']), 'R52_R8_FINAL_PREFLIGHT')
    print(json.dumps({'revision': p['receipt']['revision'], 'preflight': str(receipt), 'reference': pin(live.REFERENCE)}))

if __name__ == '__main__':
    main()
