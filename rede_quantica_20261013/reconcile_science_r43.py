"""Reconcile returned R43 agents using complete state, retaining every old handle."""
from pathlib import Path
import sys, json, hashlib
BASE = Path(r'C:\IALD\Central de Patentes')
OUT = BASE / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT/'mission_resume_20261016'))
import live_mission_r39 as live
sys.path.insert(0, str(BASE/'work/rede_quantica_20261013'))
from custody_fock_stress_r37 import verify

def pin(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    p,_ = live.project()
    t = next(t for t in p['projection']['active'] if t['id']=='R8')
    live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
        actor=live.ACTOR, task_id='R8', lease_id=t['lease']['id'],
        expected_revision=p['receipt']['revision'], projection_sha256=p['projection_sha256']), 'R43_RECONCILE_CHECK')
    custody = OUT/'maxwell_global/NULL_SCHWARTZ_CORE_CUSTODY_R43.json'
    live.save_new(custody, verify('20261016T161839_194180Z',14))
    evidence = {
      'r43-r8-null-schwartz-fix': OUT/'maxwell_global/MAXWELL_NULL_SCHWARTZ_CORE_TRANSPORT_CANDIDATE_R3.json',
      'r43-r8-null-ae-transport': OUT/'maxwell_global/NullFrequencyAETransportR1.lean'}
    s,_ = live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)), 'R43_RECONCILE_GET')
    handles = s['p']['handles']
    for hid, path in evidence.items():
        h = next(h for h in handles if h['id']==hid)
        assert h['status']=='running', (hid,h['status'])
        h.update(status='completed', receipt=pin(path), scope='Candidate returned; no acceptance of full R8')
    live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),actor=live.ACTOR,
        expected_revision=s['revision'],event_id='r43-reconcile-returned-agents',changes=dict(
        records=[dict(id='r43-null-schwartz-core-green',kind='fact',statute='REAL',
            text='R8 S1-S3 compiled EXIT0, 14 printed declarations only trio; all pinned dependencies verified. S4 R1 failed in a separate attempt. Full R8 remains open.',
            sources=[dict(kind='artifact',ref=str(custody),sha256=pin(custody)['sha256'])])],
        flow=dict(handles=handles,next_action='Independent review of R8 S1-S3; repair measured S4 compiler errors before assembling dense domain. Preserve running R7 identity.'))), 'R43_RECONCILE_TRANSITION')
    print(json.dumps({'custody':str(custody),'agents_reconciled':list(evidence)},ensure_ascii=False))

if __name__=='__main__': main()
