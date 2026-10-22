"""Record the coordinator's source review and verify the completed R51 build."""
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
    target = OUT / 'mission_review_20261016/R51_CYCLIC_REVIEW_R1.json'
    if target.exists():
        raise RuntimeError('Review exists; recover it, never overwrite')
    current, projected = live.project()
    task = next(t for t in current['projection']['active'] if t['id'] == 'R7')
    _, checked = live.call('mission_cli.py', dict(
        operation='check', reference=str(live.REFERENCE), actor=live.ACTOR,
        task_id='R7', lease_id=task['lease']['id'],
        expected_revision=current['receipt']['revision'],
        projection_sha256=current['projection_sha256']), 'R51_CYCLIC_REVIEW_CHECK')
    result = verify('20261016T203505_683079Z', 8)
    source = OUT / 'takesaki_fock/CanonicalFockCyclicTraceCompletionR3.lean'
    assert pin(source)['sha256'] == result['source']['sha256']
    review = dict(
        reviewer='codex-gerente-tgl', author='mission_memory_review',
        verdict='PASS_COMPONENT_WITH_SCOPE', review_complete=True,
        requirement_satisfied=False, reviewed_at=dt.datetime.now(dt.timezone.utc).isoformat(),
        reference=pin(live.REFERENCE), revision=current['receipt']['revision'],
        source=pin(source), project_receipt=pin(projected), preflight_receipt=pin(checked),
        verification=result,
        method='Source-level mathematical review by coordinator, distinct from candidate author; byte and axiom verification, no independent rebuild claimed.',
        findings=[
            'The codomain is ENNReal. The construction is the supremum of values of positive operators shift-related to the given represented-core element.',
            'The actual positive value, PositiveInput, represented Fock core and dualAction are imported unchanged; no SiteProfile model or new trace assumption is substituted.',
            'Cyclic invariance follows from ShiftRelated.cyclic and transitivity; star invariance uses positivity and star_transport.',
            'The two dual inequalities use the actual inverse dual action and value_dual; the generic double-supremum lemma changes elaboration, not hypotheses.',
            'Exact agreement on every positive element uses positiveShift_value_compatible. The imported supplier uses the existing polar and R49 quadratic trace law.',
            'Zero and positive faithfulness follow from the existing positive-value laws. No conclusion of linearity on the entire algebra is asserted.',
            'All eight public reports use only propext, Classical.choice and Quot.sound. Failed R2 remains preserved and is not part of this acceptance.'
        ],
        limits=[
            'This completes only the cyclic ENNReal interface component. It is not a complex-linear trace on all algebra elements.',
            'Finite projection, equal orthogonal split, full RemainingModularCoreInput and full R7 are not supplied by this file.',
            'The old p.next_action at revision 357 misidentified the second timeout: R2 line 107 was ENNReal.mul_iSup, not positive_dual_cancel. The R3 manifest records the correction.'
        ],
        production_modified=False, gate_moved=False)
    new(target, review)
    print(json.dumps(dict(review=pin(target), checked_files=len(result['checked_files']),
                         axiom_lists=len(result['axioms']), verdict=review['verdict']), ensure_ascii=False))


if __name__ == '__main__':
    main()
