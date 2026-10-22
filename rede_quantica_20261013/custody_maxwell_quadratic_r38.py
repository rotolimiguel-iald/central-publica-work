"""Custody two completed Maxwell components; keep the full R8 criterion open."""
import datetime as dt
import json
from pathlib import Path
from diary_r1 import new, pin
from custody_fock_stress_r37 import verify, OUT, a


def main():
    target = OUT/'maxwell_global/REGULAR_MAXWELL_QUADRATIC_DELIVERY_R2.json'
    if target.exists():
        raise FileExistsError(target)
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%H%M%S_%f')
    v = a.call('mission_cli.py', dict(operation='project', reference=str(a.REF),
        max_chars=100000), 'R38_CUSTODY_'+stamp)
    task = next(t for t in v['projection']['active'] if t['id']=='R8')
    a.call('mission_cli.py', dict(operation='check', reference=str(a.REF), actor=a.ACTOR,
        task_id='R8', lease_id=task['lease']['id'], expected_revision=v['receipt']['revision'],
        projection_sha256=v['projection_sha256']), 'R38_CUSTODY_PREFLIGHT_'+stamp)
    builds = [verify('20261016T133828_570803Z', 9), verify('20261016T134547_843536Z', 9)]
    new(target, dict(unit='F1.FECHO_20261015', requirement='R8', author=a.ACTOR['id'],
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), statute='REAL',
        status='COMPONENT_COMPILED_FULL_R8_OPEN', builds=builds,
        content=[
            'Real coordinate stress on Fin 4 -> Real with Lebesgue weak conservation, symmetry, vacuum zero, nontrivial point witness and translation covariance.',
            'Boost covariance and assembly of the existing MaxwellQuadraticForm on the actual regular Fock domain, conditional on RemainingModularCoreInput A.'
        ],
        residuals=[
            'A retains the existing 21 trace/PF obligations; no inhabitant of A has been supplied by these components.',
            'Null-plane charge identity with the modular generator remains open.',
            'The pointwise nonzero stress witness does not replace the required nonzero modular-energy witness.',
            'No source coupling to the curved-space geometric record, universal H3 derivation, or complete MaxwellCertificate is claimed.'
        ], production_modified=False, gate_moved=False))
    print(json.dumps(dict(delivery=pin(target), builds=[dict(seconds=b['seconds'],
        declarations=len(b['axioms']), checked_files=len(b['checked_files'])) for b in builds])))


if __name__ == '__main__':
    main()
