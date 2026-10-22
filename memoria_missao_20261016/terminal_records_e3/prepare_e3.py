"""Anchor the measured E3 overflow before changing the memory implementation."""
from pathlib import Path
import sys, json
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/'terminal_projection_e2'))
import support_e2 as s
s.BASE=BASE
s.TASK='M3_TERMINAL_RECORDS'

def main():
    failure=s.OUT/'mission_resume_20261016/LIVE_PROJECT_20261016T170818_897908Z_1796d6d2_RECEIPT.json'
    assert json.loads(failure.read_bytes())['message']=='projection_overflow_required_100318'
    finding=s.new('FINDING.json',dict(statute='REAL',failure=s.pin(failure),
      required_chars=100318,previous_budget=100000,
      cause='Mechanical build tracking records duplicate terminal handles in current_records; E2 removes only handle details.',
      correction_scope='Exact mechanical records only, recoverable index, preserve every other record and full persistent history. New tracker emits flow deltas without duplicate fact prose.',
      original_order=s.pin(BASE.parent/'OPERADOR_VERBATIM.txt')))
    claim=s.command([r'C:\IALD\PROGRAMA_IALD\iald.py','ver',s.UNIT],'CLAIM_E3')
    assert claim['reivindicacao']['quem']==s.ACTOR['id']
    p=s.project('BEFORE_EXTEND')
    criterion=('Compact only strictly recognized mechanical records of terminal builds, cross-checked against the exact handle and receipt pins, with full-record digests and same-reference recovery. '
       'Unknown/conflicting/mismatched records stay visible. Preserve every instruction, decision, correction, scientific fact, criterion, persistent byte and unresolved execution. '
       'Future tracker uses flow deltas rather than duplicate fact records. Reuse existing ACOM/CLI/MCP; tests include adversarial mutations, recovery and preflight. '
       'Independent review, hash deployment with byte backups, updated protocol/instructions and live measurement; no infinite-context claim.')
    s.call('mission_cli.py',dict(s.args(p),operation='extend',event_id='memory-e3-extend',
       requirements=[dict(id=s.TASK,criterion=criterion,depends_on=['M2_TERMINAL_PROJECTION'])],
       reason='Measured overflow during authorized long mission; memory correction has priority.',sources=[s.pin(finding)]),'EXTEND_E3')
    p=s.project('BEFORE_CLAIM')
    s.call('mission_cli.py',dict(s.args(p),operation='claim',task_id=s.TASK,
       event_id='memory-e3-claim',lease_seconds=10800),'MISSION_CLAIM_E3')
    snap=s.call('session_memory.py',dict(operation='get',reference=str(s.REF)),'RECONCILE_GET')
    evidence={'r44-r8-normalization-review':s.OUT/'mission_review_20261016/R8_NORMALIZATION_AUDIT_R44.json',
      'r44-r8-strong-derivative':s.OUT/'maxwell_global/COMPACT_BOOST_STRONG_DERIVATIVE_REDUCTION_CANDIDATE_R1.json'}
    for hid,path in evidence.items():
        h=next(h for h in snap['p']['handles'] if h['id']==hid)
        assert h['status']=='running'
        h.update(status='completed',receipt=s.pin(path),scope='Returned component; full R8 remains open')
    snap['p']['handles'].append(dict(id='memory-e3-builder',kind='agent',task_id=s.TASK,status='running',no_repeat=True))
    s.call('session_memory.py',dict(operation='transition',reference=str(s.REF),actor=s.ACTOR,
       expected_revision=snap['revision'],event_id='memory-e3-priority-and-returns',changes=dict(
       flow=dict(handles=snap['p']['handles'],phase='memory_e3_priority',
       next_action='Correct measured projection overflow; no new scientific execution until memory E3 is verified.'))),'PRIORITY_E3')
    p=s.preflight('BUILDER_HANDOFF')
    t=next(t for t in p['projection']['active'] if t['id']==s.TASK)
    s.call('mission_cli.py',dict(s.args(p),operation='handoff',task_id=s.TASK,
        lease_id=t['lease']['id'],max_chars=200000),'HANDOFF_E3')
    print(json.dumps(dict(handoff=str(BASE/'HANDOFF_E3.json'),task=s.TASK,revision=p['receipt']['revision'])))

if __name__=='__main__':main()
