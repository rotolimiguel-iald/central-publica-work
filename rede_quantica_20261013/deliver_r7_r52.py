"""Custody the reviewed R7 supplier and submit it without impersonating the reviewer."""
import copy
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, new, pin
from custody_fock_stress_r37 import verify

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live


def main():
    target = OUT / 'R7_DELIVERY_R52.json'
    if target.exists():
        raise RuntimeError('Immutable delivery exists; recover its submission, never overwrite')
    current, projection = live.project()
    task = next(t for t in current['projection']['active'] if t['id'] == 'R7')
    live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
        actor=live.ACTOR, task_id='R7', lease_id=task['lease']['id'],
        expected_revision=current['receipt']['revision'],
        projection_sha256=current['projection_sha256']), 'R52_R7_DELIVERY_CHECK')
    review_path = OUT / 'mission_review_20261016/R52_R7_FULL_REVIEW_R1.json'
    review = json.loads(review_path.read_bytes())
    assert review['verdict'] == 'PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE'
    assert review['requirement_satisfied'] is True
    assert not review['blocking_findings']
    builds = [verify('20261016T210351_533600Z', 3),
              verify('20261016T210640_174717Z', 11)]
    sources = [OUT / 'takesaki_fock' / name for name in [
        'CanonicalFockNormalizedSplitR5.lean',
        'CanonicalFockModularCoreInputR1.lean',
        'CanonicalFockCyclicTraceCompletionR3.lean',
        'CanonicalFockActualPositiveTracePackageR2.lean']]
    new(target, dict(unit='F1.FECHO_20261015', requirement='R7',
        author=live.ACTOR['id'], created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='REVIEWED_READY_FOR_INDEPENDENT_ACCEPTANCE', criterion=task['criterion'],
        reference=pin(live.REFERENCE), projection=pin(projection),
        sources=[pin(p) for p in sources], builds=builds, independent_review=pin(review_path),
        filled_fields=21, new_axiom_reports=14,
        claims=[
            'All 21 fields of RemainingModularCoreInput are supplied on the original represented regular Fock core.',
            'The existing positive normal semifinite faithful trace and dual exp(-s) scaling are retained; no final trace, corner, projection or equal-halves hypothesis is added.',
            'The normalized support has trace one and two orthogonal equal-trace faces.',
            'physicalModularCoreInput and physicalFockCertificate specialize to the already constructed physicalCanonicalNet.',
            'The total ENNReal reading is cyclic and agrees with the positive trace; complex linearity on the entire algebra is not claimed.'],
        remaining=['R8 final joint Maxwell supplier', 'R4/R5 physical clock and device identification',
                   'R3 complete candidate rite', 'R10 independent joint delivery'],
        original_criterion_unchanged=True, full_mission_complete=False,
        accept_performed=False, providers_called=False, production_modified=False, gate_moved=False,
        script=pin(Path(__file__))))
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R52_R7_REVIEW_GET')
    handles = copy.deepcopy(state['p']['handles'])
    h = next(x for x in handles if x['id'] == 'r52-core-final-review')
    h.update(status='returned', receipt=pin(review_path), requirement_recommended_for_acceptance=True)
    live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=state['revision'], event_id='r52-r7-final-review-returned',
        changes=dict(flow=dict(handles=handles))), 'R52_R7_REVIEW_RETURNED')
    current, _ = live.project()
    task = next(t for t in current['projection']['active'] if t['id'] == 'R7')
    result, receipt = live.call('mission_cli.py', dict(operation='submit', reference=str(live.REFERENCE),
        actor=live.ACTOR, task_id='R7', lease_id=task['lease']['id'],
        expected_revision=current['receipt']['revision'], projection_sha256=current['projection_sha256'],
        event_id='r52-r7-concrete-core-submit',
        evidence=[pin(target), *[pin(p) for p in sources], pin(review_path)],
        note='Complete original R7 criterion on the actual Fock representation; independent acceptance remains a separate reviewer action.'),
        'R52_R7_SUBMIT')
    print(json.dumps(dict(delivery=pin(target), submission_receipt=str(receipt), submitted=True), ensure_ascii=False))


if __name__ == '__main__':
    main()
