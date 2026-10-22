"""Custody the concrete joint Maxwell consumer and submit for independent review."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, new, pin
from custody_fock_stress_r37 import verify

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live

def evidence(path):
    p = pin(path)
    return {key: p[key] for key in ('path', 'sha256')}

def main():
    target = OUT / 'R8_DELIVERY_R52.json'
    if target.exists():
        raise RuntimeError('Recover immutable delivery; never overwrite it')
    current, projection = live.project()
    task = next(t for t in current['projection']['active'] if t['id'] == 'R8')
    r7 = next(t for t in current['projection']['settled'] if t['id'] == 'R7')
    assert r7['status'] == 'satisfied'
    live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE), actor=live.ACTOR,
        task_id='R8', lease_id=task['lease']['id'], expected_revision=current['receipt']['revision'],
        projection_sha256=current['projection_sha256']), 'R52_R8_DELIVERY_CHECK')
    sources = [OUT / 'maxwell_global' / n for n in
        ['CircularMaxwellCertificateR2.lean', 'PhysicalMaxwellJointRealizationR2.lean']]
    builds = [verify('20261016T211151_421554Z', 10), verify('20261016T211651_298033Z', 16)]
    new(target, dict(unit='F1.FECHO_20261015', requirement='R8', author=live.ACTOR['id'],
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), status='COMPILED_CANDIDATE_FOR_INDEPENDENT_REVIEW',
        criterion=task['criterion'], reference=pin(live.REFERENCE), projection=pin(projection),
        sources=[pin(p) for p in sources], builds=builds, new_axiom_reports=26,
        R7_acceptance=pin(OUT/'mission_review_20261016/R52_R7_ACCEPT_RECEIPT_R1.json'),
        claims=[
            'The unchanged MaxwellCertificate is inhabited on the concrete physicalFockCertificate and physicalCanonicalNet.',
            'Circular one-particle transport and its Fock lift connect the local smearing net to the Wick stress for the same transported state.',
            'A single normalized regular-domain witness has nonzero modular energy, actual null-plane charge identity and Wick tensor identification.',
            'Symmetry and distributional conservation are proved on the regular domain; the fixed-null geometric consumer uses that same tensor.'],
        limits=[
            'Killing normalization N and G > 0 remain explicit inputs.',
            'H3 is the existing fixed-null linearized geometric response, not a universal nonlinear Einstein construction.',
            'No bounded global point field or patented device realization is claimed.',
            'Compilation is not independent semantic acceptance; R4/R5/R3/R10 remain open.'],
        original_criterion_unchanged=True, accept_performed=False, full_mission_complete=False,
        providers_called=False, production_modified=False, gate_moved=False, script=pin(Path(__file__))))
    current, _ = live.project()
    task = next(t for t in current['projection']['active'] if t['id'] == 'R8')
    result, receipt = live.call('mission_cli.py', dict(operation='submit', reference=str(live.REFERENCE),
        actor=live.ACTOR, task_id='R8', lease_id=task['lease']['id'], expected_revision=current['receipt']['revision'],
        projection_sha256=current['projection_sha256'], event_id='r52-r8-concrete-joint-submit',
        evidence=[evidence(target), *[evidence(p) for p in sources]],
        note='Concrete joint Maxwell consumer, compiled with 26 axiom reports in the trio. Independent semantic review is separate.'), 'R52_R8_SUBMIT')
    print(json.dumps(dict(delivery=pin(target), receipt=str(receipt), submitted=True), ensure_ascii=False))

if __name__ == '__main__':
    main()
